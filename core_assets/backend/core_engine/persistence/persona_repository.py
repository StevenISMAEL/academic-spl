"""
Core Asset — PersonaRepository (COR-17)

Repositorio concreto para la entidad Persona.

Persona es un Core Service (no un Optional Feature): toda instancia
derivada de la línea académica necesita gestionar personas (estudiantes,
docentes, etc.). Por eso este router se monta SIEMPRE, no bajo un flag.

Métodos públicos:
    list_personas()          → List[dict]
    get_persona(id)          → dict | None
    get_by_documento(doc)    → dict | None
    create_persona(data)     → dict
    update_persona(id, data) → dict | None
    delete_persona(id)       → bool
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.models import PersonaDB
from core_assets.backend.core_engine.domain.validators.cedula_validator import CedulaValidator


class PersonaRepository:
    """Acceso a datos para la entidad Persona."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def list_personas(self) -> List[Dict[str, Any]]:
        """Devuelve todas las personas registradas."""
        rows = self._db.query(PersonaDB).all()
        return [self._to_dict(row) for row in rows]

    def get_persona(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """Busca una persona por ID. Devuelve None si no existe."""
        row = self._db.query(PersonaDB).filter(PersonaDB.id == persona_id).first()
        return self._to_dict(row) if row else None

    def get_by_documento(self, documento: str) -> Optional[Dict[str, Any]]:
        """Busca una persona por documento de identidad."""
        row = (
            self._db.query(PersonaDB)
            .filter(PersonaDB.documento_identidad == documento)
            .first()
        )
        return self._to_dict(row) if row else None

    def create_persona(self, data: dict) -> dict:
        """Crea y persiste una nueva persona.

        Args:
            data: Diccionario con campos:
                  - nombres (str, requerido)
                  - apellidos (str, requerido)
                  - documento_identidad (str, requerido, unico)

        Returns:
            Diccionario con la persona creada incluyendo el id generado.

        Raises:
            ValueError: si ya existe una persona con el mismo documento.
            ValueError: si el documento no es una cedula ecuatoriana valida (CA-01).
        """
        # CA-01: CedulaValidator — valida el algoritmo del Registro Civil Ecuador
        documento_validado = CedulaValidator.validate_or_raise(
            data["documento_identidad"]
        )

        existing = self.get_by_documento(documento_validado)
        if existing:
            raise ValueError(
                f"Ya existe una persona con documento '{documento_validado}'."
            )

        new_persona = PersonaDB(
            id=str(uuid.uuid4()),
            nombres=data["nombres"],
            apellidos=data["apellidos"],
            documento_identidad=documento_validado,
        )
        self._db.add(new_persona)
        self._db.commit()
        self._db.refresh(new_persona)
        return self._to_dict(new_persona)

    def update_persona(
        self, persona_id: str, data: dict
    ) -> dict | None:
        """Actualiza los datos de una persona existente.

        Si se incluye documento_identidad en los datos a actualizar,
        el Core Asset CedulaValidator (CA-01) lo valida antes de guardar.
        """
        row = self._db.query(PersonaDB).filter(PersonaDB.id == persona_id).first()
        if not row:
            return None

        if "nombres" in data:
            row.nombres = data["nombres"]
        if "apellidos" in data:
            row.apellidos = data["apellidos"]
        if "documento_identidad" in data:
            # CA-01: validar cédula antes de actualizar
            row.documento_identidad = CedulaValidator.validate_or_raise(
                data["documento_identidad"]
            )

        self._db.commit()
        self._db.refresh(row)
        return self._to_dict(row)

    def delete_persona(self, persona_id: str) -> bool:
        """Elimina una persona por ID. Devuelve True si existía."""
        row = self._db.query(PersonaDB).filter(PersonaDB.id == persona_id).first()
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    @staticmethod
    def _to_dict(row: PersonaDB) -> Dict[str, Any]:
        return {
            "id": row.id,
            "nombres": row.nombres,
            "apellidos": row.apellidos,
            "documento_identidad": row.documento_identidad,
        }
