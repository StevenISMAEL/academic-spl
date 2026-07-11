"""
Core Asset — AttendanceRepository (COR-14)

Repositorio concreto para la feature de Asistencia (attendance).

Recibe una sesión de BD en su constructor y NO sabe de dónde viene
esa sesión (la provee el ConnectionResolver via FastAPI Depends).

Métodos públicos:
    list_records()          → List[dict]
    get_record(id)          → dict | None
    create_record(data)     → dict
    delete_record(id)       → bool
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.models import AsistenciaDB


class AttendanceRepository:
    """Acceso a datos para la entidad Asistencia."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def list_records(self) -> List[Dict[str, Any]]:
        """Devuelve todos los registros de asistencia."""
        rows = self._db.query(AsistenciaDB).all()
        return [self._to_dict(row) for row in rows]

    def get_record(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Busca un registro de asistencia por ID. Devuelve None si no existe."""
        row = self._db.query(AsistenciaDB).filter(AsistenciaDB.id == record_id).first()
        return self._to_dict(row) if row else None

    def create_record(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo registro de asistencia y lo persiste en la BD.

        Args:
            data: Diccionario con campos:
                  - persona_id (str, requerido)
                  - curso_id (str, requerido)
                  - fecha (str, requerido, formato ISO 8601: "YYYY-MM-DD")
                  - presente (bool, requerido)
                  - justificacion (str, opcional)

        Returns:
            Diccionario con el registro creado, incluyendo el id generado.
        """
        new_record = AsistenciaDB(
            id=str(uuid.uuid4()),
            persona_id=data["persona_id"],
            curso_id=data["curso_id"],
            fecha=data["fecha"],
            presente=bool(data["presente"]),
            justificacion=data.get("justificacion"),
        )
        self._db.add(new_record)
        self._db.commit()
        self._db.refresh(new_record)
        return self._to_dict(new_record)

    def delete_record(self, record_id: str) -> bool:
        """Elimina un registro por ID. Devuelve True si existía."""
        row = self._db.query(AsistenciaDB).filter(AsistenciaDB.id == record_id).first()
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    @staticmethod
    def _to_dict(row: AsistenciaDB) -> Dict[str, Any]:
        return {
            "id": row.id,
            "persona_id": row.persona_id,
            "curso_id": row.curso_id,
            "fecha": row.fecha,
            "presente": row.presente,
            "justificacion": row.justificacion,
        }
