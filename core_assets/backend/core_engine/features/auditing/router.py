"""
Optional Feature: Auditing
"""
from __future__ import annotations

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.auditing_repository import AuditingRepository

router = APIRouter(prefix="/auditing", tags=["auditing (optional feature)"])

class AuditLogCreate(BaseModel):
    usuario_id: str
    accion: str
    entidad: str
    entidad_id: str
    detalles: Optional[Dict[str, Any]] = None

@router.get("/")
def get_audit_logs(
    limit: int = 100,
    offset: int = 0,
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Obtiene los logs de auditoria."""
    flags = request.app.state.feature_flags
    if not flags.is_active("auditing"):
        return {"error": "Auditing feature is disabled"}

    repo = AuditingRepository(db)
    return repo.get_logs(limit, offset)

@router.post("/")
def create_audit_log(
    log_data: AuditLogCreate,
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Crea un nuevo log de auditoria manualmente."""
    flags = request.app.state.feature_flags
    if not flags.is_active("auditing"):
        return {"error": "Auditing feature is disabled"}

    repo = AuditingRepository(db)
    return repo.create_log(
        usuario_id=log_data.usuario_id,
        accion=log_data.accion,
        entidad=log_data.entidad,
        entidad_id=log_data.entidad_id,
        detalles=log_data.detalles
    )
