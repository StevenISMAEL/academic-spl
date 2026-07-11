"""
Feature: Enrollment (Matrícula/Inscripción) — Core Asset activable. (Sprint 2)

Se monta solo si `features.enrollment: true` en la configuración del
producto. Los datos ya NO son dummy — se leen/escriben en la BD del
producto activo via EnrollmentRepository.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.enrollment_repository import EnrollmentRepository

router = APIRouter(prefix="/enrollment", tags=["enrollment"])


# ── Esquemas Pydantic para validar entrada de la API ──────────────────────────

class EnrollmentCreate(BaseModel):
    persona_id: str = Field(..., description="ID de la persona a inscribir")
    curso_id: str = Field(..., description="ID del curso al que se inscribe")
    estado: Optional[str] = Field(
        default="inscrito",
        description="Estado inicial: inscrito | retirado | aprobado | reprobado",
    )


class EnrollmentStatusUpdate(BaseModel):
    estado: str = Field(
        ...,
        description="Nuevo estado: inscrito | retirado | aprobado | reprobado",
    )


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", summary="Listar todas las matrículas/inscripciones")
def list_enrollments(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Devuelve todas las matrículas registradas en la BD del producto activo."""
    repo = EnrollmentRepository(db)
    enrollments = repo.list_enrollments()
    return {
        "feature": "enrollment",
        "total": len(enrollments),
        "data": enrollments,
    }


@router.get("/{enrollment_id}", summary="Obtener una matrícula por ID")
def get_enrollment(enrollment_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Busca una matrícula por su ID único."""
    repo = EnrollmentRepository(db)
    enrollment = repo.get_enrollment(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail=f"Matrícula '{enrollment_id}' no encontrada.")
    return enrollment


@router.post("/", status_code=201, summary="Crear una nueva matrícula/inscripción")
def create_enrollment(
    payload: EnrollmentCreate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Inscribe a una persona en un curso y persiste la matrícula."""
    repo = EnrollmentRepository(db)
    try:
        return repo.create_enrollment(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.patch("/{enrollment_id}/status", summary="Actualizar estado de una matrícula")
def update_enrollment_status(
    enrollment_id: str,
    payload: EnrollmentStatusUpdate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Cambia el estado de una matrícula (ej. de 'inscrito' a 'aprobado')."""
    repo = EnrollmentRepository(db)
    try:
        updated = repo.update_enrollment_status(enrollment_id, payload.estado)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    if not updated:
        raise HTTPException(status_code=404, detail=f"Matrícula '{enrollment_id}' no encontrada.")
    return updated


@router.delete("/{enrollment_id}", summary="Eliminar una matrícula")
def delete_enrollment(enrollment_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Elimina una matrícula existente."""
    repo = EnrollmentRepository(db)
    deleted = repo.delete_enrollment(enrollment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Matrícula '{enrollment_id}' no encontrada.")
    return {"message": f"Matrícula '{enrollment_id}' eliminada correctamente."}
