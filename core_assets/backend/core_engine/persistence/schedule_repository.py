"""
Core Asset — ScheduleRepository (COR-27)

Repositorio para la feature de Horarios (schedule).
Gestiona la tabla 'horarios' con los bloques de clase semanales.
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.models import HorarioDB, CursoDB

DIAS_VALIDOS = {"Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"}


class ScheduleRepository:
    """Acceso a datos para la entidad Horario."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def list_schedules(self) -> List[Dict[str, Any]]:
        """Devuelve todos los horarios registrados, enriquecidos con el nombre del curso."""
        rows = self._db.query(HorarioDB).all()
        return [self._to_dict(row) for row in rows]

    def list_by_curso(self, curso_id: str) -> List[Dict[str, Any]]:
        """Devuelve los horarios de un curso específico."""
        rows = (
            self._db.query(HorarioDB)
            .filter(HorarioDB.curso_id == curso_id)
            .all()
        )
        return [self._to_dict(row) for row in rows]

    def get_schedule(self, schedule_id: str) -> Optional[Dict[str, Any]]:
        """Busca un horario por ID."""
        row = (
            self._db.query(HorarioDB)
            .filter(HorarioDB.id == schedule_id)
            .first()
        )
        return self._to_dict(row) if row else None

    def create_schedule(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo bloque de horario.

        Args:
            data: dict con curso_id, dia_semana, hora_inicio, hora_fin, aula.

        Returns:
            El horario creado como dict.

        Raises:
            ValueError: si el dia_semana no es válido.
        """
        dia = data.get("dia_semana", "")
        if dia not in DIAS_VALIDOS:
            raise ValueError(f"Día '{dia}' no válido. Use: {sorted(DIAS_VALIDOS)}")

        row = HorarioDB(
            id          = data.get("id", str(uuid.uuid4())),
            curso_id    = data["curso_id"],
            dia_semana  = dia,
            hora_inicio = data["hora_inicio"],
            hora_fin    = data["hora_fin"],
            aula        = data.get("aula"),
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return self._to_dict(row)

    def delete_schedule(self, schedule_id: str) -> bool:
        """Elimina un horario por ID. Devuelve True si existía, False si no."""
        row = self._db.query(HorarioDB).filter(HorarioDB.id == schedule_id).first()
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    def _to_dict(self, row: HorarioDB) -> Dict[str, Any]:
        # Intentar obtener el nombre del curso si está cargado
        nombre_curso = None
        if row.curso:
            nombre_curso = row.curso.nombre

        return {
            "id":          row.id,
            "curso_id":    row.curso_id,
            "nombre_curso": nombre_curso,
            "dia_semana":  row.dia_semana,
            "hora_inicio": row.hora_inicio,
            "hora_fin":    row.hora_fin,
            "aula":        row.aula,
        }
