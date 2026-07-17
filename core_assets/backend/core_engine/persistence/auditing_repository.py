"""
Repositorio para el Módulo de Auditoría (Optional Feature)
"""
import uuid
import datetime
import json
from typing import List, Dict, Any, Optional

from sqlalchemy.orm import Session
from core_assets.backend.core_engine.persistence.models import AuditoriaDB

class AuditingRepository:
    """Acceso a datos para los registros de auditoría."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def create_log(
        self, 
        usuario_id: str, 
        accion: str, 
        entidad: str, 
        entidad_id: str, 
        detalles: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Registra una nueva entrada de auditoría."""
        nuevo_log = AuditoriaDB(
            id=f"AUD-{uuid.uuid4().hex[:8].upper()}",
            usuario_id=usuario_id,
            accion=accion.upper(),
            entidad=entidad,
            entidad_id=entidad_id,
            fecha_hora=datetime.datetime.utcnow().isoformat() + "Z",
            detalles=json.dumps(detalles) if detalles else None
        )
        self._db.add(nuevo_log)
        self._db.commit()
        self._db.refresh(nuevo_log)
        return self._to_dict(nuevo_log)

    def get_logs(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Devuelve los registros de auditoría ordenados por fecha descendente."""
        rows = (
            self._db.query(AuditoriaDB)
            .order_by(AuditoriaDB.fecha_hora.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._to_dict(row) for row in rows]

    def _to_dict(self, db_obj: AuditoriaDB) -> Dict[str, Any]:
        detalles_dict = None
        if db_obj.detalles:
            try:
                detalles_dict = json.loads(db_obj.detalles)
            except:
                detalles_dict = db_obj.detalles

        return {
            "id": db_obj.id,
            "usuario_id": db_obj.usuario_id,
            "accion": db_obj.accion,
            "entidad": db_obj.entidad,
            "entidad_id": db_obj.entidad_id,
            "fecha_hora": db_obj.fecha_hora,
            "detalles": detalles_dict,
        }
