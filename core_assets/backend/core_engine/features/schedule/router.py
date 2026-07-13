"""
Optional Feature — Schedule (Horarios de Clases) — IMPLEMENTACIÓN COMPLETA

Se monta solo si `features.schedule: true` en el product_config.yaml.
En el proyecto: Universidad = ON, Técnico = ON, Colegio = OFF.

Gestiona bloques de horario semanales (dia, hora_inicio, hora_fin, aula)
asociados a un curso. La configuración `periods_per_year` del YAML indica
cuántos semestres/períodos tiene el producto activo.
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.schedule_repository import ScheduleRepository, DIAS_VALIDOS

router = APIRouter(prefix="/schedule", tags=["schedule"])


# ── Schemas Pydantic ──────────────────────────────────────────────────────────

class HorarioCreate(BaseModel):
    curso_id:    str = Field(..., description="ID del curso al que pertenece el horario")
    dia_semana:  str = Field(..., description="Día de la semana: Lunes, Martes, Miércoles, Jueves, Viernes, Sábado")
    hora_inicio: str = Field(..., description="Hora de inicio en formato HH:MM, ej: 08:00")
    hora_fin:    str = Field(..., description="Hora de fin en formato HH:MM, ej: 10:00")
    aula:        str | None = Field(None, description="Número o nombre del aula (opcional)")


# ── GET /schedule/ ────────────────────────────────────────────────────────────

@router.get("/", summary="Listar todos los horarios del producto activo")
def list_schedules(
    request: Request,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Devuelve todos los horarios registrados agrupados por día de la semana.

    El campo `periods_per_year` refleja la configuracion del YAML del producto,
    mostrando cuántos periodos académicos tiene la institución en el año.
    """
    flags = request.app.state.feature_flags
    periods_per_year = flags.get_setting("academic_settings", "periods_per_year", default=2)

    repo     = ScheduleRepository(db)
    horarios = repo.list_schedules()

    # Agrupar por día de semana
    por_dia: Dict[str, list] = {d: [] for d in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]}
    for h in horarios:
        dia = h.get("dia_semana", "")
        if dia in por_dia:
            por_dia[dia].append(h)

    return {
        "feature":           "schedule",
        "product_name":      flags.product_name(),
        "periods_per_year":  periods_per_year,
        "total_horarios":    len(horarios),
        "dias_validos":      sorted(DIAS_VALIDOS),
        "horarios_por_dia":  {d: v for d, v in por_dia.items() if v},
        "horarios":          horarios,
    }


# ── POST /schedule/ ───────────────────────────────────────────────────────────

@router.post("/", summary="Crear un bloque de horario", status_code=201)
def create_schedule(
    payload: HorarioCreate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Crea un nuevo bloque de horario para un curso.

    El `dia_semana` debe ser uno de los días válidos (Lunes…Sábado).
    El formato de hora es HH:MM (24h), ej: "08:00", "14:30".
    """
    repo = ScheduleRepository(db)
    try:
        horario = repo.create_schedule(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return {"created": True, "horario": horario}


# ── GET /schedule/curso/{curso_id} ────────────────────────────────────────────

@router.get("/curso/{curso_id}", summary="Horarios de un curso específico")
def get_schedules_by_curso(
    curso_id: str,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Devuelve todos los bloques de horario asociados a un curso."""
    repo     = ScheduleRepository(db)
    horarios = repo.list_by_curso(curso_id)

    return {
        "curso_id": curso_id,
        "total":    len(horarios),
        "horarios": horarios,
    }


# ── GET /schedule/{id} ────────────────────────────────────────────────────────

@router.get("/{schedule_id}", summary="Obtener un horario por ID")
def get_schedule(
    schedule_id: str,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    horario = ScheduleRepository(db).get_schedule(schedule_id)
    if not horario:
        raise HTTPException(status_code=404, detail=f"Horario '{schedule_id}' no encontrado.")
    return horario


# ── DELETE /schedule/{id} ─────────────────────────────────────────────────────

@router.delete("/{schedule_id}", summary="Eliminar un horario")
def delete_schedule(
    schedule_id: str,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    deleted = ScheduleRepository(db).delete_schedule(schedule_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Horario '{schedule_id}' no encontrado.")
    return {"deleted": True, "id": schedule_id}
