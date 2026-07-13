"""
Optional Feature — Reports (Reportes Académicos) — IMPLEMENTACIÓN COMPLETA

Se monta solo si `features.reports: true` en el product_config.yaml.

Genera reportes de rendimiento académico combinando datos de:
  - EvaluacionDB (grading) → analizado con CA-04 GradePassingChecker
  - AsistenciaDB (attendance) → analizado con CA-03 AttendanceCalculator

No requiere nuevas tablas — agrega datos ya existentes.
"""
from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.persona_repository import PersonaRepository
from core_assets.backend.core_engine.persistence.grade_repository import GradeRepository
from core_assets.backend.core_engine.persistence.attendance_repository import AttendanceRepository
from core_assets.backend.core_engine.domain.calculators.grade_passing_checker import GradePassingChecker
from core_assets.backend.core_engine.domain.calculators.attendance_calculator import AttendanceCalculator
from core_assets.backend.core_engine.domain.calculators.grade_scale_converter import GradeScaleConverter

router = APIRouter(prefix="/reports", tags=["reports"])


def _build_student_report(
    persona: Dict[str, Any],
    grades: List[Dict[str, Any]],
    attendance_records: List[Dict[str, Any]],
    passing_grade: float,
    attendance_min: float,
    scale: str,
) -> Dict[str, Any]:
    """Construye el reporte de un estudiante combinando notas y asistencia.

    Usa CA-04 (GradePassingChecker) y CA-03 (AttendanceCalculator).
    No contiene lógica de negocio propia — delega en los Core Assets.
    """
    t_at_risk = max(attendance_min - 10, 0.0)

    # CA-04: analizar notas del estudiante
    notas_anotadas = GradePassingChecker.annotate_grades_list(grades, passing_grade)
    for nota in notas_anotadas:
        nota["valor_display"] = GradeScaleConverter.to_display(nota["valor"], scale)

    total_notas = len(notas_anotadas)
    notas_aprobadas = sum(1 for n in notas_anotadas if n.get("aprueba"))
    promedio = (
        round(sum(n["valor"] for n in notas_anotadas) / total_notas, 2)
        if total_notas > 0
        else None
    )

    # CA-03: analizar asistencia del estudiante
    resumen_asistencia = AttendanceCalculator.summarize(
        attendance_records, attendance_min, t_at_risk
    ) if attendance_records else {
        "total_registros": 0,
        "porcentaje_asistencia": None,
        "estado": "SIN_DATOS",
        "umbral_aprobado": attendance_min,
        "umbral_riesgo": t_at_risk,
    }

    # Determinación del estado final del estudiante
    if total_notas == 0:
        estado_final = "SIN_DATOS"
    elif notas_aprobadas == total_notas and resumen_asistencia["estado"] in ("APROBADO", "SIN_DATOS"):
        estado_final = "APROBADO"
    elif resumen_asistencia["estado"] == "REPROBADO_FALTA":
        estado_final = "REPROBADO_FALTA"
    elif notas_aprobadas < total_notas:
        estado_final = "REPROBADO_NOTA"
    else:
        estado_final = "EN_RIESGO"

    return {
        "persona_id": persona["id"],
        "nombre_completo": f"{persona['nombres']} {persona['apellidos']}",
        "documento_identidad": persona["documento_identidad"],
        "notas": notas_anotadas,
        "resumen_notas": {
            "total": total_notas,
            "aprobadas": notas_aprobadas,
            "reprobadas": total_notas - notas_aprobadas,
            "promedio": promedio,
        },
        "asistencia": resumen_asistencia,
        "estado_final": estado_final,
    }


@router.get("/", summary="Configuracion del producto y lista de estudiantes para reportes")
def list_reports(request: Request, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Devuelve la configuracion del producto activo y la lista de personas disponibles.

    El frontend usa esto para llenar el selector de estudiante antes de
    solicitar el reporte individual.
    """
    flags = request.app.state.feature_flags
    scale = flags.get_setting("academic_settings", "evaluation_scale", default="numeric")
    passing = flags.get_setting("academic_settings", "passing_grade", default=7.0)
    att_min = flags.get_setting("academic_settings", "attendance_min_percentage", default=80.0)

    repo_personas = PersonaRepository(db)
    personas = repo_personas.list_personas()

    return {
        "feature": "reports",
        "configuracion_producto": {
            "product_name": flags.product_name(),
            "evaluation_scale": scale,
            "passing_grade": passing,
            "attendance_min_percentage": att_min,
        },
        "personas_disponibles": [
            {"id": p["id"], "nombre": f"{p['nombres']} {p['apellidos']}"}
            for p in personas
        ],
        "reportes_disponibles": [
            {"endpoint": "/reports/rendimiento/{persona_id}", "descripcion": "Reporte individual de rendimiento"},
            {"endpoint": "/reports/consolidado/", "descripcion": "Resumen general de todos los estudiantes"},
        ],
    }


@router.get("/rendimiento/{persona_id}", summary="Reporte de rendimiento por estudiante")
def student_performance_report(
    persona_id: str,
    request: Request,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Genera un reporte de rendimiento completo para un estudiante.

    Combina:
    - Notas del estudiante → CA-04 GradePassingChecker (aprueba/reprueba)
    - Asistencia del estudiante → CA-03 AttendanceCalculator (porcentaje + estado)

    Los umbrales vienen del product_config.yaml del producto activo.
    """
    flags = request.app.state.feature_flags
    scale   = flags.get_setting("academic_settings", "evaluation_scale", default="numeric")
    passing = flags.get_setting("academic_settings", "passing_grade", default=7.0)
    att_min = flags.get_setting("academic_settings", "attendance_min_percentage", default=80.0)

    repo_personas  = PersonaRepository(db)
    repo_grades    = GradeRepository(db)
    repo_att       = AttendanceRepository(db)

    persona = repo_personas.get_persona(persona_id)
    if not persona:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' no encontrada.")

    # Notas y asistencia del estudiante
    todas_las_notas = repo_grades.list_grades()
    notas_persona = [n for n in todas_las_notas if n.get("persona_id") == persona_id]

    todos_registros = repo_att.list_records()
    att_persona = [r for r in todos_registros if r.get("persona_id") == persona_id]

    reporte = _build_student_report(
        persona, notas_persona, att_persona, passing, att_min, scale
    )
    reporte["configuracion_aplicada"] = {
        "evaluation_scale": scale,
        "passing_grade": passing,
        "attendance_min_percentage": att_min,
        "product_name": flags.product_name(),
    }

    return {"feature": "reports", "reporte": reporte}


@router.get("/consolidado/", summary="Resumen consolidado de todos los estudiantes")
def consolidated_report(
    request: Request,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Genera el reporte consolidado de TODOS los estudiantes.

    Muestra un resumen por persona: promedio de notas, asistencia y estado final.
    Útil para la vista general del docente o director académico.
    """
    flags = request.app.state.feature_flags
    scale   = flags.get_setting("academic_settings", "evaluation_scale", default="numeric")
    passing = flags.get_setting("academic_settings", "passing_grade", default=7.0)
    att_min = flags.get_setting("academic_settings", "attendance_min_percentage", default=80.0)

    repo_personas = PersonaRepository(db)
    repo_grades   = GradeRepository(db)
    repo_att      = AttendanceRepository(db)

    personas     = repo_personas.list_personas()
    todas_notas  = repo_grades.list_grades()
    todos_att    = repo_att.list_records()

    consolidado = []
    resumen_estados: Dict[str, int] = {
        "APROBADO": 0, "REPROBADO_NOTA": 0, "REPROBADO_FALTA": 0,
        "EN_RIESGO": 0, "SIN_DATOS": 0,
    }

    for p in personas:
        pid = p["id"]
        notas_p = [n for n in todas_notas if n.get("persona_id") == pid]
        att_p   = [r for r in todos_att   if r.get("persona_id") == pid]

        rep = _build_student_report(p, notas_p, att_p, passing, att_min, scale)
        consolidado.append({
            "persona_id":      rep["persona_id"],
            "nombre_completo": rep["nombre_completo"],
            "promedio":        rep["resumen_notas"]["promedio"],
            "asistencia_pct":  rep["asistencia"].get("porcentaje_asistencia"),
            "estado_final":    rep["estado_final"],
        })
        resumen_estados[rep["estado_final"]] = resumen_estados.get(rep["estado_final"], 0) + 1

    return {
        "feature":        "reports",
        "product_name":   flags.product_name(),
        "total_estudiantes": len(personas),
        "resumen_estados": resumen_estados,
        "configuracion_aplicada": {
            "passing_grade":            passing,
            "attendance_min_percentage": att_min,
            "evaluation_scale":          scale,
        },
        "consolidado": consolidado,
    }
