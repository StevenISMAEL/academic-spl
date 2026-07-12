"""
Optional Feature — Reports (Reportes Académicos)

Se monta solo si `features.reports: true` en el product_config.yaml.

Genera reportes de rendimiento académico combinando datos de grading
y attendance. Usa GradePassingChecker y AttendanceCalculator para
calcular métricas de desempeño por estudiante y por curso.

Relevante para: universidades e institutos que requieren informes formales.
No relevante para: colegios básicos con evaluación integrada al sistema.

Sprint 2: estructura base y endpoint de reporte simple.
Sprint 3: reportes completos con PDF y exportación.
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Request

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/", summary="Resumen de reportes disponibles")
def list_reports(request: Request) -> Dict[str, Any]:
    """Lista los tipos de reportes disponibles para este producto."""
    flags = request.app.state.feature_flags
    scale = flags.get_setting("academic_settings", "evaluation_scale", default="numeric")
    passing = flags.get_setting("academic_settings", "passing_grade", default=7.0)

    return {
        "feature": "reports",
        "evaluation_scale": scale,
        "passing_grade_configured": passing,
        "reportes_disponibles": [
            "rendimiento_por_estudiante",
            "resumen_por_curso",
            "consolidado_periodo",
        ],
        "message": "Implementacion completa en Sprint 3.",
    }


@router.get("/rendimiento/{persona_id}", summary="Reporte de rendimiento por estudiante")
def student_performance_report(persona_id: str, request: Request) -> Dict[str, Any]:
    """Genera un reporte de rendimiento académico para un estudiante.

    Combina: notas (GradePassingChecker) + asistencia (AttendanceCalculator).
    Implementación completa en Sprint 3.
    """
    flags = request.app.state.feature_flags
    passing = flags.get_setting("academic_settings", "passing_grade", default=7.0)
    attendance_min = flags.get_setting("academic_settings", "attendance_min_percentage", default=80.0)

    return {
        "feature": "reports",
        "persona_id": persona_id,
        "configuracion_aplicada": {
            "nota_minima_aprobacion": passing,
            "asistencia_minima": attendance_min,
        },
        "resumen": {},
        "message": "Implementacion completa en Sprint 3.",
    }
