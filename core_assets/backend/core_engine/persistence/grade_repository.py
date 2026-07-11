"""
Core Asset — GradeRepository (COR-14)

Repositorio concreto para la feature de Calificaciones (grading).

Recibe una sesión de BD en su constructor y NO sabe de dónde viene
esa sesión (la provee el ConnectionResolver via FastAPI Depends).
Tampoco importa SQLAlchemy directamente en los routers — esa es
la garantía de separación de capas del patrón Repository.

Métodos públicos:
    list_grades()        → List[dict]
    get_grade(id)        → dict | None
    create_grade(data)   → dict
    delete_grade(id)     → bool
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.models import EvaluacionDB


class GradeRepository:
    """Acceso a datos para la entidad Evaluacion (calificaciones)."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def list_grades(self) -> List[Dict[str, Any]]:
        """Devuelve todas las evaluaciones registradas en la BD."""
        rows = self._db.query(EvaluacionDB).all()
        return [self._to_dict(row) for row in rows]

    def get_grade(self, grade_id: str) -> Optional[Dict[str, Any]]:
        """Busca una evaluación por su ID. Devuelve None si no existe."""
        row = self._db.query(EvaluacionDB).filter(EvaluacionDB.id == grade_id).first()
        return self._to_dict(row) if row else None

    def create_grade(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nueva evaluación y la persiste en la BD.

        Args:
            data: Diccionario con campos:
                  - curso_id (str, requerido)
                  - persona_id (str, requerido)
                  - valor (float, requerido)
                  - observacion (str, opcional)

        Returns:
            Diccionario con la evaluación creada, incluyendo el id generado.
        """
        new_grade = EvaluacionDB(
            id=str(uuid.uuid4()),
            curso_id=data["curso_id"],
            persona_id=data["persona_id"],
            valor=float(data["valor"]),
            observacion=data.get("observacion"),
        )
        self._db.add(new_grade)
        self._db.commit()
        self._db.refresh(new_grade)
        return self._to_dict(new_grade)

    def delete_grade(self, grade_id: str) -> bool:
        """Elimina una evaluación por ID. Devuelve True si existía."""
        row = self._db.query(EvaluacionDB).filter(EvaluacionDB.id == grade_id).first()
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    @staticmethod
    def _to_dict(row: EvaluacionDB) -> Dict[str, Any]:
        return {
            "id": row.id,
            "curso_id": row.curso_id,
            "persona_id": row.persona_id,
            "valor": row.valor,
            "observacion": row.observacion,
        }
