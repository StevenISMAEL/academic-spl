"""
Optional Feature — Certificates (Certificados de Aprobación)

Se monta solo si `features.certificates: true` en el product_config.yaml.

Genera certificados de aprobación para estudiantes que cumplieron los
requisitos académicos (nota >= passing_grade y asistencia >= mínimo).
Usa GradePassingChecker y AttendanceCalculator como Core Assets.

Relevante para: universidades e institutos técnicos con emisión formal.
No relevante para: colegios básicos donde las actas las emite el MINEDUC.

Sprint 2: estructura base.
Sprint 3: generación de PDF, firma digital, plantillas por producto.
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Request

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get("/", summary="Listar certificados generados")
def list_certificates(request: Request) -> Dict[str, Any]:
    """Lista los certificados emitidos en este producto."""
    flags = request.app.state.feature_flags
    product = flags.product_name()

    return {
        "feature": "certificates",
        "producto_emisor": product,
        "certificados": [],
        "message": "Implementacion completa en Sprint 3.",
    }


@router.post("/{persona_id}/generate", status_code=201, summary="Generar certificado de aprobacion")
def generate_certificate(persona_id: str, request: Request) -> Dict[str, Any]:
    """Genera un certificado si el estudiante cumple los requisitos.

    Verifica: nota >= passing_grade Y asistencia >= attendance_min_percentage.
    Usa CA-04 GradePassingChecker y CA-03 AttendanceCalculator.
    Implementación completa en Sprint 3.
    """
    flags = request.app.state.feature_flags
    passing = flags.get_setting("academic_settings", "passing_grade", default=7.0)
    attendance_min = flags.get_setting("academic_settings", "attendance_min_percentage", default=80.0)
    product = flags.product_name()

    return {
        "feature": "certificates",
        "persona_id": persona_id,
        "producto_emisor": product,
        "requisitos": {
            "nota_minima": passing,
            "asistencia_minima_pct": attendance_min,
        },
        "certificado": None,
        "message": "Implementacion completa en Sprint 3.",
    }
