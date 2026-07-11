"""
Core Asset — PeriodoRepository (COR-19)

Repositorio concreto para la entidad Periodo.

Periodo es un Core Service: toda instancia académica necesita gestionar
períodos (semestres, años escolares, trimestres). Se monta siempre.

Métodos públicos:
    list_periodos()             → List[dict]
    get_periodo(id)             → dict | None
    create_periodo(data)        → dict
    update_periodo(id, data)    → dict | None
    delete_periodo(id)          → bool
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.models import PeriodoDB


class PeriodoRepository:
    """Acceso a datos para la entidad Periodo."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def list_periodos(self) -> List[Dict[str, Any]]:
        """Devuelve todos los períodos académicos registrados."""
        rows = self._db.query(PeriodoDB).all()
        return [self._to_dict(row) for row in rows]

    def get_periodo(self, periodo_id: str) -> Optional[Dict[str, Any]]:
        """Busca un período por ID. Devuelve None si no existe."""
        row = self._db.query(PeriodoDB).filter(PeriodoDB.id == periodo_id).first()
        return self._to_dict(row) if row else None

    def create_periodo(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea y persiste un nuevo período académico.

        Args:
            data: Diccionario con campos:
                  - nombre (str, requerido) — Ej: "Semestre 2024-A"
                  - fecha_inicio (str, requerido) — formato ISO 8601: "YYYY-MM-DD"
                  - fecha_fin (str, requerido) — formato ISO 8601: "YYYY-MM-DD"

        Returns:
            Diccionario con el período creado incluyendo el id generado.
        """
        new_periodo = PeriodoDB(
            id=str(uuid.uuid4()),
            nombre=data["nombre"],
            fecha_inicio=data["fecha_inicio"],
            fecha_fin=data["fecha_fin"],
        )
        self._db.add(new_periodo)
        self._db.commit()
        self._db.refresh(new_periodo)
        return self._to_dict(new_periodo)

    def update_periodo(
        self, periodo_id: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Actualiza los datos de un período existente.

        Args:
            periodo_id: ID del período a actualizar.
            data: Campos a actualizar (nombre, fecha_inicio, fecha_fin).

        Returns:
            El período actualizado, o None si no existe.
        """
        row = self._db.query(PeriodoDB).filter(PeriodoDB.id == periodo_id).first()
        if not row:
            return None

        if "nombre" in data:
            row.nombre = data["nombre"]
        if "fecha_inicio" in data:
            row.fecha_inicio = data["fecha_inicio"]
        if "fecha_fin" in data:
            row.fecha_fin = data["fecha_fin"]

        self._db.commit()
        self._db.refresh(row)
        return self._to_dict(row)

    def delete_periodo(self, periodo_id: str) -> bool:
        """Elimina un período por ID. Devuelve True si existía."""
        row = self._db.query(PeriodoDB).filter(PeriodoDB.id == periodo_id).first()
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    @staticmethod
    def _to_dict(row: PeriodoDB) -> Dict[str, Any]:
        return {
            "id": row.id,
            "nombre": row.nombre,
            "fecha_inicio": row.fecha_inicio,
            "fecha_fin": row.fecha_fin,
        }
