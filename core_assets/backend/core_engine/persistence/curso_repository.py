"""
Core Asset — CursoRepository (COR-18)

Repositorio concreto para la entidad Curso.

Curso es un Core Service: toda instancia académica necesita gestionar
cursos/materias. Se monta siempre, independientemente del producto.

Métodos públicos:
    list_cursos()             → List[dict]
    list_by_periodo(id)       → List[dict]
    get_curso(id)             → dict | None
    create_curso(data)        → dict
    update_curso(id, data)    → dict | None
    delete_curso(id)          → bool
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.models import CursoDB


class CursoRepository:
    """Acceso a datos para la entidad Curso."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def list_cursos(self) -> List[Dict[str, Any]]:
        """Devuelve todos los cursos registrados."""
        rows = self._db.query(CursoDB).all()
        return [self._to_dict(row) for row in rows]

    def list_by_periodo(self, periodo_id: str) -> List[Dict[str, Any]]:
        """Devuelve todos los cursos de un período académico específico."""
        rows = (
            self._db.query(CursoDB)
            .filter(CursoDB.periodo_id == periodo_id)
            .all()
        )
        return [self._to_dict(row) for row in rows]

    def get_curso(self, curso_id: str) -> Optional[Dict[str, Any]]:
        """Busca un curso por ID. Devuelve None si no existe."""
        row = self._db.query(CursoDB).filter(CursoDB.id == curso_id).first()
        return self._to_dict(row) if row else None

    def create_curso(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea y persiste un nuevo curso.

        Args:
            data: Diccionario con campos:
                  - nombre (str, requerido)
                  - periodo_id (str, requerido) — debe existir en la tabla periodos

        Returns:
            Diccionario con el curso creado incluyendo el id generado.
        """
        new_curso = CursoDB(
            id=str(uuid.uuid4()),
            nombre=data["nombre"],
            periodo_id=data["periodo_id"],
        )
        self._db.add(new_curso)
        self._db.commit()
        self._db.refresh(new_curso)
        return self._to_dict(new_curso)

    def update_curso(
        self, curso_id: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Actualiza los datos de un curso existente.

        Args:
            curso_id: ID del curso a actualizar.
            data: Campos a actualizar (nombre, periodo_id).

        Returns:
            El curso actualizado, o None si no existe.
        """
        row = self._db.query(CursoDB).filter(CursoDB.id == curso_id).first()
        if not row:
            return None

        if "nombre" in data:
            row.nombre = data["nombre"]
        if "periodo_id" in data:
            row.periodo_id = data["periodo_id"]

        self._db.commit()
        self._db.refresh(row)
        return self._to_dict(row)

    def delete_curso(self, curso_id: str) -> bool:
        """Elimina un curso por ID. Devuelve True si existía."""
        row = self._db.query(CursoDB).filter(CursoDB.id == curso_id).first()
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    @staticmethod
    def _to_dict(row: CursoDB) -> Dict[str, Any]:
        return {
            "id": row.id,
            "nombre": row.nombre,
            "periodo_id": row.periodo_id,
        }
