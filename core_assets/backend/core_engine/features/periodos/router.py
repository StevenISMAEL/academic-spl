"""
Core Service: Periodos — Core Asset siempre activo (COR-19)

Los períodos académicos (semestres, años, trimestres) son la estructura
temporal de cualquier institución educativa. Son parte de la commonality
de la línea — no se pueden desactivar. Se registra en main_factory.py
fuera del FEATURE_REGISTRY condicional.

REGLA DE ORO respetada: ningún nombre de producto aparece aquí.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.periodo_repository import PeriodoRepository

router = APIRouter(prefix="/periodos", tags=["periodos (core service)"])


# ── Esquemas Pydantic ─────────────────────────────────────────────────────────

class PeriodoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre descriptivo del período. Ej: 'Semestre 2024-A'")
    fecha_inicio: str = Field(..., description="Fecha de inicio en formato YYYY-MM-DD")
    fecha_fin: str = Field(..., description="Fecha de fin en formato YYYY-MM-DD")


class PeriodoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1)
    fecha_inicio: Optional[str] = Field(None)
    fecha_fin: Optional[str] = Field(None)


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", summary="Listar todos los períodos académicos")
def list_periodos(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Devuelve todos los períodos académicos registrados en el producto activo."""
    repo = PeriodoRepository(db)
    periodos = repo.list_periodos()
    return {
        "service": "periodos",
        "total": len(periodos),
        "data": periodos,
    }


@router.get("/{periodo_id}", summary="Obtener un período por ID")
def get_periodo(periodo_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Busca un período académico por su ID único."""
    repo = PeriodoRepository(db)
    periodo = repo.get_periodo(periodo_id)
    if not periodo:
        raise HTTPException(status_code=404, detail=f"Periodo '{periodo_id}' no encontrado.")
    return periodo


@router.post("/", status_code=201, summary="Crear un nuevo período académico")
def create_periodo(
    payload: PeriodoCreate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Crea y persiste un nuevo período académico en la BD del producto activo."""
    repo = PeriodoRepository(db)
    return repo.create_periodo(payload.model_dump())


@router.put("/{periodo_id}", summary="Actualizar datos de un período")
def update_periodo(
    periodo_id: str,
    payload: PeriodoUpdate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Actualiza uno o más campos de un período existente."""
    repo = PeriodoRepository(db)
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=422, detail="Debes enviar al menos un campo para actualizar.")
    updated = repo.update_periodo(periodo_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Periodo '{periodo_id}' no encontrado.")
    return updated


@router.delete("/{periodo_id}", summary="Eliminar un período académico")
def delete_periodo(periodo_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Elimina un período existente de la BD del producto activo."""
    repo = PeriodoRepository(db)
    deleted = repo.delete_periodo(periodo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Periodo '{periodo_id}' no encontrado.")
    return {"message": f"Periodo '{periodo_id}' eliminado correctamente."}
