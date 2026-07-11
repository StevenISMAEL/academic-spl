"""
Feature: Attendance (Asistencia) — Core Asset activable. (Sprint 2)

Este router se monta SOLO si el product_config.yaml del producto
derivado declara `features.attendance: true`. Los datos ya NO son dummy
— se leen/escriben en la BD del producto activo via AttendanceRepository.

Usa el Core Asset AttendanceCalculator (CA-03) para calcular estadisticas
de asistencia: porcentaje global y estado de riesgo por persona.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.attendance_repository import AttendanceRepository
from core_assets.backend.core_engine.domain.calculators.attendance_calculator import AttendanceCalculator

router = APIRouter(prefix="/attendance", tags=["attendance"])


# ── Esquemas Pydantic para validar entrada de la API ──────────────────────────

class AttendanceCreate(BaseModel):
    persona_id: str = Field(..., description="ID de la persona")
    curso_id: str = Field(..., description="ID del curso")
    fecha: str = Field(..., description="Fecha del registro (YYYY-MM-DD)")
    presente: bool = Field(..., description="True si asistio, False si falto")
    justificacion: Optional[str] = Field(None, description="Justificacion de inasistencia")


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", summary="Listar registros de asistencia con estadisticas")
def list_attendance_records(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Devuelve los registros de asistencia de la BD del producto activo.

    Incluye un resumen global calculado por el Core Asset AttendanceCalculator
    (CA-03): porcentaje de asistencia, estado (APROBADO/EN_RIESGO/REPROBADO_FALTA)
    y un desglose por persona ordenado de mayor a menor riesgo.
    """
    repo = AttendanceRepository(db)
    records = repo.list_records()

    # CA-03: AttendanceCalculator calcula estadisticas del dominio academico
    resumen_global = AttendanceCalculator.summarize(records)
    resumen_por_persona = AttendanceCalculator.summarize_by_persona(records)

    return {
        "feature": "attendance",
        "total": len(records),
        "estadisticas": resumen_global,
        "resumen_por_persona": resumen_por_persona,
        "data": records,
    }


@router.get("/{record_id}", summary="Obtener un registro de asistencia por ID")
def get_attendance_record(record_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Busca un registro de asistencia por su ID unico."""
    repo = AttendanceRepository(db)
    record = repo.get_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Registro '{record_id}' no encontrado.")
    return record


@router.post("/", status_code=201, summary="Registrar nueva asistencia")
def create_attendance_record(
    payload: AttendanceCreate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Crea y persiste un nuevo registro de asistencia."""
    repo = AttendanceRepository(db)
    return repo.create_record(payload.model_dump())


@router.delete("/{record_id}", summary="Eliminar un registro de asistencia")
def delete_attendance_record(record_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Elimina un registro de asistencia existente."""
    repo = AttendanceRepository(db)
    deleted = repo.delete_record(record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Registro '{record_id}' no encontrado.")
    return {"message": f"Registro '{record_id}' eliminado correctamente."}
