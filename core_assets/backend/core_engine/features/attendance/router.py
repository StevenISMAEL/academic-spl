"""
Feature: Attendance (Asistencia) — Core Asset activable.

Este router se monta SOLO si el product_config.yaml del producto
derivado declara `features.attendance: true`. No conoce ni le importa
qué producto lo está usando.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.get("/")
def list_attendance_records():
    return {
        "feature": "attendance",
        "source": "core_assets/backend/core_engine/features/attendance",
        "message": "Este endpoint solo existe porque el producto activó 'attendance' en su configuración.",
        "sample_data": [
            {"persona_id": "P-001", "curso_id": "C-001", "presente": True},
            {"persona_id": "P-002", "curso_id": "C-001", "presente": False},
        ],
    }
