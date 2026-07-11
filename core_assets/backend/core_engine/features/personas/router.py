"""
Core Service: Personas — Core Asset siempre activo (COR-17)

A diferencia de los Optional Features (grading, attendance, enrollment),
este router se monta en TODAS las instancias de la línea de productos.
La razón: no tiene sentido tener un sistema académico que no pueda
gestionar las personas que lo usan.

No está bajo el FEATURE_REGISTRY condicional — se registra directamente
en main_factory.py como parte de la commonality del Core.

REGLA DE ORO respetada: este archivo no menciona ningún producto.
La BD que se usa la determina el product_config.yaml via ConnectionResolver.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.persona_repository import PersonaRepository

router = APIRouter(prefix="/personas", tags=["personas (core service)"])


# ── Esquemas Pydantic ─────────────────────────────────────────────────────────

class PersonaCreate(BaseModel):
    nombres: str = Field(..., min_length=1, description="Nombre(s) de la persona")
    apellidos: str = Field(..., min_length=1, description="Apellido(s) de la persona")
    documento_identidad: str = Field(..., min_length=1, description="Documento único de identidad")


class PersonaUpdate(BaseModel):
    nombres: Optional[str] = Field(None, min_length=1)
    apellidos: Optional[str] = Field(None, min_length=1)
    documento_identidad: Optional[str] = Field(None, min_length=1)


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", summary="Listar todas las personas")
def list_personas(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Devuelve todas las personas (estudiantes, docentes) registradas en el producto activo."""
    repo = PersonaRepository(db)
    personas = repo.list_personas()
    return {
        "service": "personas",
        "total": len(personas),
        "data": personas,
    }


@router.get("/{persona_id}", summary="Obtener una persona por ID")
def get_persona(persona_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Busca una persona por su ID único."""
    repo = PersonaRepository(db)
    persona = repo.get_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' no encontrada.")
    return persona


@router.get("/por-documento/{documento}", summary="Buscar persona por documento de identidad")
def get_by_documento(documento: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Busca una persona por número de documento de identidad."""
    repo = PersonaRepository(db)
    persona = repo.get_by_documento(documento)
    if not persona:
        raise HTTPException(status_code=404, detail=f"Documento '{documento}' no encontrado.")
    return persona


@router.post("/", status_code=201, summary="Registrar una nueva persona")
def create_persona(
    payload: PersonaCreate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Crea y persiste una nueva persona. El documento de identidad debe ser único."""
    repo = PersonaRepository(db)
    try:
        return repo.create_persona(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put("/{persona_id}", summary="Actualizar datos de una persona")
def update_persona(
    persona_id: str,
    payload: PersonaUpdate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Actualiza uno o más campos de una persona existente."""
    repo = PersonaRepository(db)
    # Excluir campos no enviados (None) para hacer update parcial
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=422, detail="Debes enviar al menos un campo para actualizar.")
    updated = repo.update_persona(persona_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' no encontrada.")
    return updated


@router.delete("/{persona_id}", summary="Eliminar una persona")
def delete_persona(persona_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Elimina una persona existente de la BD del producto activo."""
    repo = PersonaRepository(db)
    deleted = repo.delete_persona(persona_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' no encontrada.")
    return {"message": f"Persona '{persona_id}' eliminada correctamente."}
