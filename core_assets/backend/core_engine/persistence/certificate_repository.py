"""
Core Asset — CertificateRepository (COR-26)

Repositorio para la feature de Certificados de Aprobacion (certificates).

Almacena cada intento de certificacion: si el estudiante cumplió los
requisitos (nota + asistencia) se guarda con estado 'emitido',
si no con 'rechazado' y el motivo.
"""
from __future__ import annotations

import uuid
import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.models import CertificadoDB


class CertificateRepository:
    """Acceso a datos para la entidad Certificado."""

    ESTADOS_VALIDOS = {"emitido", "rechazado"}

    def __init__(self, session: Session) -> None:
        self._db = session

    def list_certificates(self) -> List[Dict[str, Any]]:
        """Devuelve todos los certificados registrados."""
        rows = self._db.query(CertificadoDB).all()
        return [self._to_dict(row) for row in rows]

    def list_by_persona(self, persona_id: str) -> List[Dict[str, Any]]:
        """Devuelve todos los certificados de una persona específica."""
        rows = (
            self._db.query(CertificadoDB)
            .filter(CertificadoDB.persona_id == persona_id)
            .all()
        )
        return [self._to_dict(row) for row in rows]

    def get_certificate(self, certificate_id: str) -> Optional[Dict[str, Any]]:
        """Busca un certificado por ID."""
        row = (
            self._db.query(CertificadoDB)
            .filter(CertificadoDB.id == certificate_id)
            .first()
        )
        return self._to_dict(row) if row else None

    def create_certificate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Persiste un nuevo certificado (emitido o rechazado).

        Args:
            data: dict con persona_id, curso_id, nota_final, asistencia_pct,
                  estado ('emitido'/'rechazado') y motivo_rechazo (opcional).

        Returns:
            El certificado creado como dict.
        """
        estado = data.get("estado", "rechazado")
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado '{estado}' no válido. Use: {self.ESTADOS_VALIDOS}")

        row = CertificadoDB(
            id             = data.get("id", str(uuid.uuid4())),
            persona_id     = data["persona_id"],
            curso_id       = data["curso_id"],
            fecha_emision  = data.get("fecha_emision", datetime.date.today().isoformat()),
            nota_final     = data.get("nota_final"),
            asistencia_pct = data.get("asistencia_pct"),
            estado         = estado,
            motivo_rechazo = data.get("motivo_rechazo"),
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return self._to_dict(row)

    def _to_dict(self, row: CertificadoDB) -> Dict[str, Any]:
        return {
            "id":             row.id,
            "persona_id":     row.persona_id,
            "curso_id":       row.curso_id,
            "fecha_emision":  row.fecha_emision,
            "nota_final":     row.nota_final,
            "asistencia_pct": row.asistencia_pct,
            "estado":         row.estado,
            "motivo_rechazo": row.motivo_rechazo,
        }
