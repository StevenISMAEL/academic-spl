"""
Optional Feature — Certificates (Certificados de Aprobacion) — IMPLEMENTACIÓN COMPLETA

Se monta solo si `features.certificates: true` en el product_config.yaml.
En el proyecto: Universidad Compleja = ON, Colegio = OFF, Técnico = OFF.

Lógica de negocio:
  - Usa CA-04 (GradePassingChecker) para verificar nota >= passing_grade
  - Usa CA-03 (AttendanceCalculator) para verificar asistencia >= attendance_min_percentage
  - Si ambos se cumplen → estado: "emitido"
  - Si alguno falla    → estado: "rechazado" con motivo descriptivo
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.persona_repository import PersonaRepository
from core_assets.backend.core_engine.persistence.grade_repository import GradeRepository
from core_assets.backend.core_engine.persistence.attendance_repository import AttendanceRepository
from core_assets.backend.core_engine.persistence.certificate_repository import CertificateRepository
from core_assets.backend.core_engine.domain.calculators.grade_passing_checker import GradePassingChecker
from core_assets.backend.core_engine.domain.calculators.attendance_calculator import AttendanceCalculator

router = APIRouter(prefix="/certificates", tags=["certificates"])


# ── GET /certificates/ ────────────────────────────────────────────────────────

@router.get("/", summary="Listar todos los certificados emitidos y rechazados")
def list_certificates(
    request: Request,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    flags = request.app.state.feature_flags
    repo  = CertificateRepository(db)
    certs = repo.list_certificates()

    emitidos  = [c for c in certs if c["estado"] == "emitido"]
    rechazados = [c for c in certs if c["estado"] == "rechazado"]

    return {
        "feature":           "certificates",
        "product_name":      flags.product_name(),
        "total_certificados": len(certs),
        "emitidos":          len(emitidos),
        "rechazados":        len(rechazados),
        "requisitos": {
            "nota_minima":        flags.get_setting("academic_settings", "passing_grade", 7.0),
            "asistencia_minima_pct": flags.get_setting("academic_settings", "attendance_min_percentage", 80.0),
        },
        "certificados": certs,
    }


# ── GET /certificates/{id} ────────────────────────────────────────────────────

@router.get("/{certificate_id}", summary="Obtener un certificado por ID")
def get_certificate(
    certificate_id: str,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    cert = CertificateRepository(db).get_certificate(certificate_id)
    if not cert:
        raise HTTPException(status_code=404, detail=f"Certificado '{certificate_id}' no encontrado.")
    return cert


# ── GET /certificates/persona/{persona_id} ────────────────────────────────────

@router.get("/persona/{persona_id}", summary="Historial de certificados de un estudiante")
def get_certificates_by_persona(
    persona_id: str,
    request: Request,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    flags = request.app.state.feature_flags

    persona = PersonaRepository(db).get_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' no encontrada.")

    certs = CertificateRepository(db).list_by_persona(persona_id)

    return {
        "persona_id":     persona_id,
        "nombre":         f"{persona['nombres']} {persona['apellidos']}",
        "product_name":   flags.product_name(),
        "certificados":   certs,
    }


# ── POST /certificates/{persona_id}/generate ─────────────────────────────────

@router.post("/{persona_id}/generate", summary="Generar certificado de aprobacion para un estudiante", status_code=201)
def generate_certificate(
    persona_id: str,
    request: Request,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Verifica si un estudiante cumple los requisitos académicos y emite (o rechaza)
    su certificado de aprobación.

    Proceso:
    1. Busca todas las notas del estudiante (GradeRepository).
    2. Busca todos sus registros de asistencia (AttendanceRepository).
    3. Aplica CA-04 (GradePassingChecker) con passing_grade del YAML.
    4. Aplica CA-03 (AttendanceCalculator) con attendance_min del YAML.
    5. Si cumple ambos → persiste CertificadoDB con estado='emitido'.
    6. Si falla alguno → persiste con estado='rechazado' + motivo.

    Retorna el certificado creado con su estado y motivo.
    """
    flags = request.app.state.feature_flags
    passing_grade = flags.get_setting("academic_settings", "passing_grade", default=7.0)
    att_min       = flags.get_setting("academic_settings", "attendance_min_percentage", default=80.0)
    att_at_risk   = max(att_min - 10, 0.0)

    # Verificar que la persona existe
    persona = PersonaRepository(db).get_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' no encontrada.")

    # Obtener datos académicos del estudiante
    todas_notas = GradeRepository(db).list_grades()
    notas_persona = [n for n in todas_notas if n.get("persona_id") == persona_id]

    todos_att = AttendanceRepository(db).list_records()
    att_persona = [r for r in todos_att if r.get("persona_id") == persona_id]

    # CA-04: ¿Aprueba por nota?
    promedio: float | None = None
    aprueba_nota = False
    razon_nota = ""

    if notas_persona:
        promedio = round(sum(n["valor"] for n in notas_persona) / len(notas_persona), 2)
        aprueba_nota = GradePassingChecker.passes(promedio, passing_grade)
        if aprueba_nota:
            razon_nota = f"Promedio {promedio} ≥ {passing_grade} (passing_grade)"
        else:
            razon_nota = f"Promedio {promedio} < {passing_grade} (passing_grade requerido)"
    else:
        razon_nota = "Sin notas registradas"

    # CA-03: ¿Aprueba por asistencia?
    pct_asistencia: float | None = None
    aprueba_asistencia = False
    razon_asistencia = ""

    if att_persona:
        presentes = sum(1 for r in att_persona if r.get("presente"))
        total_att = len(att_persona)
        pct_asistencia = AttendanceCalculator.percentage(presentes, total_att)
        estado_att = AttendanceCalculator.status(pct_asistencia, att_min, att_at_risk)
        aprueba_asistencia = (estado_att == "APROBADO")
        if aprueba_asistencia:
            razon_asistencia = f"Asistencia {pct_asistencia}% ≥ {att_min}% (mínimo requerido)"
        else:
            razon_asistencia = f"Asistencia {pct_asistencia}% < {att_min}% (mínimo requerido)"

    else:
        # Sin datos de asistencia → se permite emitir si hay nota (política permisiva)
        aprueba_asistencia = True
        razon_asistencia = "Sin registros de asistencia — se omite verificación"

    # Determinación del estado final
    motivos_rechazo: List[str] = []
    if not aprueba_nota:
        motivos_rechazo.append(razon_nota)
    if not aprueba_asistencia:
        motivos_rechazo.append(razon_asistencia)

    estado = "emitido" if not motivos_rechazo else "rechazado"
    motivo_texto = " | ".join(motivos_rechazo) if motivos_rechazo else None

    # Usar el primer curso con nota registrada, o "N/A" si no hay
    curso_id = notas_persona[0]["curso_id"] if notas_persona else "sin_curso"

    # Persistir el certificado
    cert_data = {
        "persona_id":     persona_id,
        "curso_id":       curso_id,
        "fecha_emision":  datetime.date.today().isoformat(),
        "nota_final":     promedio,
        "asistencia_pct": pct_asistencia,
        "estado":         estado,
        "motivo_rechazo": motivo_texto,
    }
    certificado = CertificateRepository(db).create_certificate(cert_data)

    return {
        "feature":          "certificates",
        "product_name":     flags.product_name(),
        "persona_id":       persona_id,
        "nombre":           f"{persona['nombres']} {persona['apellidos']}",
        "certificado":      certificado,
        "verificaciones": {
            "nota": {
                "cumple":  aprueba_nota,
                "detalle": razon_nota,
                "passing_grade_usado": passing_grade,
            },
            "asistencia": {
                "cumple":  aprueba_asistencia,
                "detalle": razon_asistencia,
                "attendance_min_usado": att_min,
            },
        },
    }
