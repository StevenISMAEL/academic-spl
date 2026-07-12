"""
Core Asset — EnrollmentRepository (COR-14)

Repositorio concreto para la feature de Matrículas/Inscripciones (enrollment).

Recibe una sesión de BD en su constructor y NO sabe de dónde viene
esa sesión (la provee el ConnectionResolver via FastAPI Depends).

Métodos públicos:
    list_enrollments()          → List[dict]
    get_enrollment(id)          → dict | None
    create_enrollment(data)     → dict
    delete_enrollment(id)       → bool
    update_enrollment_status    → dict | None
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.models import MatriculaDB


class EnrollmentRepository:
    """Acceso a datos para la entidad Matricula (inscripciones/matrículas)."""

    # Estados válidos de matrícula — genéricos para cualquier producto académico
    ESTADOS_VALIDOS = {"inscrito", "retirado", "aprobado", "reprobado"}

    def __init__(self, session: Session) -> None:
        self._db = session

    def list_enrollments(self) -> List[Dict[str, Any]]:
        """Devuelve todas las matrículas/inscripciones registradas."""
        rows = self._db.query(MatriculaDB).all()
        return [self._to_dict(row) for row in rows]

    def count_active_enrollments(self, persona_id: str) -> int:
        """Cuenta las matrículas activas (estado 'inscrito') de una persona.

        Usado por CA-05 EnrollmentLimitChecker para verificar si el estudiante
        puede inscribirse en más cursos según el límite del YAML del producto.

        Args:
            persona_id: ID de la persona a consultar.

        Returns:
            Número de matrículas con estado 'inscrito' para esa persona.
        """
        return (
            self._db.query(MatriculaDB)
            .filter(
                MatriculaDB.persona_id == persona_id,
                MatriculaDB.estado == "inscrito",
            )
            .count()
        )

    def get_enrollment(self, enrollment_id: str) -> Optional[Dict[str, Any]]:
        """Busca una matrícula por ID. Devuelve None si no existe."""
        row = (
            self._db.query(MatriculaDB)
            .filter(MatriculaDB.id == enrollment_id)
            .first()
        )
        return self._to_dict(row) if row else None

    def create_enrollment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nueva matrícula y la persiste en la BD.

        Args:
            data: Diccionario con campos:
                  - persona_id (str, requerido)
                  - curso_id (str, requerido)
                  - estado (str, opcional, default: "inscrito")

        Returns:
            Diccionario con la matrícula creada, incluyendo el id generado.
        """
        estado = data.get("estado", "inscrito")
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado '{estado}' no válido. "
                f"Opciones: {sorted(self.ESTADOS_VALIDOS)}"
            )

        new_enrollment = MatriculaDB(
            id=str(uuid.uuid4()),
            persona_id=data["persona_id"],
            curso_id=data["curso_id"],
            estado=estado,
        )
        self._db.add(new_enrollment)
        self._db.commit()
        self._db.refresh(new_enrollment)
        return self._to_dict(new_enrollment)

    def update_enrollment_status(
        self, enrollment_id: str, new_status: str
    ) -> Optional[Dict[str, Any]]:
        """Actualiza el estado de una matrícula existente.

        Args:
            enrollment_id: ID de la matrícula a actualizar.
            new_status: Nuevo estado (debe estar en ESTADOS_VALIDOS).

        Returns:
            La matrícula actualizada, o None si no existe.
        """
        if new_status not in self.ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado '{new_status}' no válido. "
                f"Opciones: {sorted(self.ESTADOS_VALIDOS)}"
            )

        row = (
            self._db.query(MatriculaDB)
            .filter(MatriculaDB.id == enrollment_id)
            .first()
        )
        if not row:
            return None

        row.estado = new_status
        self._db.commit()
        self._db.refresh(row)
        return self._to_dict(row)

    def delete_enrollment(self, enrollment_id: str) -> bool:
        """Elimina una matrícula por ID. Devuelve True si existía."""
        row = (
            self._db.query(MatriculaDB)
            .filter(MatriculaDB.id == enrollment_id)
            .first()
        )
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    @staticmethod
    def _to_dict(row: MatriculaDB) -> Dict[str, Any]:
        return {
            "id": row.id,
            "persona_id": row.persona_id,
            "curso_id": row.curso_id,
            "estado": row.estado,
        }
