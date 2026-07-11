"""
Core Service: Cursos — Core Asset siempre activo (COR-18)

Los cursos/materias son una entidad fundamental en cualquier producto
académico. No pueden activarse/desactivarse por configuración — siempre
existen. Se registra en main_factory.py fuera del FEATURE_REGISTRY.

REGLA DE ORO respetada: ningún nombre de producto aparece aquí.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.curso_repository import CursoRepository

router = APIRouter(prefix="/cursos", tags=["cursos (core service)"])


# ── Esquemas Pydantic ─────────────────────────────────────────────────────────

class CursoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del curso o materia")
    periodo_id: str = Field(..., description="ID del período académico al que pertenece")


class CursoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1)
    periodo_id: Optional[str] = Field(None)


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", summary="Listar todos los cursos")
def list_cursos(
    periodo_id: Optional[str] = None,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Devuelve todos los cursos. Opcionalmente filtra por período con ?periodo_id=...

    Ejemplo: GET /cursos/?periodo_id=PER-2024-A
    """
    repo = CursoRepository(db)
    if periodo_id:
        cursos = repo.list_by_periodo(periodo_id)
    else:
        cursos = repo.list_cursos()
    return {
        "service": "cursos",
        "filtro_periodo_id": periodo_id,
        "total": len(cursos),
        "data": cursos,
    }


@router.get("/{curso_id}", summary="Obtener un curso por ID")
def get_curso(curso_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Busca un curso por su ID único."""
    repo = CursoRepository(db)
    curso = repo.get_curso(curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail=f"Curso '{curso_id}' no encontrado.")
    return curso


@router.post("/", status_code=201, summary="Crear un nuevo curso")
def create_curso(
    payload: CursoCreate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Crea y persiste un nuevo curso en la BD del producto activo."""
    repo = CursoRepository(db)
    return repo.create_curso(payload.model_dump())


@router.put("/{curso_id}", summary="Actualizar datos de un curso")
def update_curso(
    curso_id: str,
    payload: CursoUpdate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Actualiza uno o más campos de un curso existente."""
    repo = CursoRepository(db)
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=422, detail="Debes enviar al menos un campo para actualizar.")
    updated = repo.update_curso(curso_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Curso '{curso_id}' no encontrado.")
    return updated


@router.delete("/{curso_id}", summary="Eliminar un curso")
def delete_curso(curso_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Elimina un curso existente de la BD del producto activo."""
    repo = CursoRepository(db)
    deleted = repo.delete_curso(curso_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Curso '{curso_id}' no encontrado.")
    return {"message": f"Curso '{curso_id}' eliminado correctamente."}
