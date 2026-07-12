"""
Optional Feature — Schedule (Horarios de Clases)

Se monta solo si `features.schedule: true` en el product_config.yaml.

Relevante para: instituciones con horario fijo por aula (universidades,
institutos técnicos). No relevante para colegios con horario integrado.

Sprint 2: implementación base (estructura de endpoint).
Sprint 3: lógica completa con HorarioRepository.
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Request

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.get("/", summary="Listar horarios de clases")
def list_schedules(request: Request) -> Dict[str, Any]:
    """Lista los horarios disponibles para el período activo.

    Configuración que afecta este feature:
    - `periods_per_year`: determina cuántos horarios existen (uno por período)
    """
    flags = request.app.state.feature_flags
    periods = flags.get_setting("academic_settings", "periods_per_year", default=1)

    return {
        "feature": "schedule",
        "periods_per_year": periods,
        "message": "Horarios disponibles. Implementacion completa en Sprint 3.",
        "data": [],
    }


@router.get("/{curso_id}", summary="Ver horario de un curso")
def get_course_schedule(curso_id: str) -> Dict[str, Any]:
    """Devuelve el horario de un curso específico."""
    return {
        "feature": "schedule",
        "curso_id": curso_id,
        "horario": [],
        "message": "Implementacion completa en Sprint 3.",
    }
