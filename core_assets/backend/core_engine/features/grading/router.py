"""
Feature: Grading (Calificaciones) — Core Asset activable. (Sprint 2)

Se monta solo si `features.grading: true` en la configuración del producto.
Los datos ya NO son dummy — se leen/escriben en la BD del producto activo
via GradeRepository. El router no sabe nada de SQLAlchemy ni del path
de la BD: toda esa lógica vive en connection_resolver.py.

Usa el Core Asset GradeScaleConverter (CA-02) para convertir las notas
a la escala del producto activo (numeric o literal). Mismo código,
distinto resultado según el product_config.yaml — sin condicionales
sobre el nombre del producto.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.grade_repository import GradeRepository
from core_assets.backend.core_engine.domain.calculators.grade_scale_converter import GradeScaleConverter

router = APIRouter(prefix="/grading", tags=["grading"])


# ── Esquemas Pydantic para validar entrada de la API ──────────────────────────

class GradeCreate(BaseModel):
    curso_id: str = Field(..., description="ID del curso")
    persona_id: str = Field(..., description="ID de la persona (estudiante)")
    valor: float = Field(..., ge=0, le=10, description="Calificacion numerica (0-10)")
    observacion: Optional[str] = Field(None, description="Observacion del docente")


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", summary="Listar todas las calificaciones")
def list_grades(
    request: Request,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Devuelve todas las evaluaciones almacenadas en la BD del producto activo.

    El campo `valor_display` refleja la escala configurada en el producto:
    - Si evaluation_scale='numeric' → valor_display es el numero (ej: 8.5)
    - Si evaluation_scale='literal' → valor_display es la etiqueta (ej: 'Muy Bueno')

    Este comportamiento diferenciado lo produce el Core Asset GradeScaleConverter,
    no una condicion 'if producto == colegio'.
    """
    repo = GradeRepository(db)
    grades = repo.list_grades()

    flags = request.app.state.feature_flags
    scale = flags.get_setting("academic_settings", "evaluation_scale", default="numeric")

    # CA-02: GradeScaleConverter convierte las notas a la escala del producto activo
    grades_con_display = GradeScaleConverter.convert_grades_list(grades, scale)

    return {
        "feature": "grading",
        "evaluation_scale_used": scale,
        "total": len(grades_con_display),
        "data": grades_con_display,
    }


@router.get("/{grade_id}", summary="Obtener una calificacion por ID")
def get_grade(
    grade_id: str,
    request: Request,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Busca una evaluacion por su ID unico. Incluye valor_display en la escala del producto."""
    repo = GradeRepository(db)
    grade = repo.get_grade(grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail=f"Calificacion '{grade_id}' no encontrada.")

    flags = request.app.state.feature_flags
    scale = flags.get_setting("academic_settings", "evaluation_scale", default="numeric")
    grade["valor_display"] = GradeScaleConverter.to_display(grade["valor"], scale)
    return grade


@router.post("/", status_code=201, summary="Registrar una nueva calificacion")
def create_grade(
    payload: GradeCreate,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Crea y persiste una nueva evaluacion en la BD del producto activo."""
    repo = GradeRepository(db)
    return repo.create_grade(payload.model_dump())


@router.delete("/{grade_id}", summary="Eliminar una calificacion")
def delete_grade(grade_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Elimina una evaluacion existente. Devuelve 404 si no existe."""
    repo = GradeRepository(db)
    deleted = repo.delete_grade(grade_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Calificacion '{grade_id}' no encontrada.")
    return {"message": f"Calificacion '{grade_id}' eliminada correctamente."}
