"""
Feature: Grading (Calificaciones) — Core Asset activable.

Se monta solo si `features.grading: true` en la configuración del producto.
Nota que también lee `academic_settings.evaluation_scale`, demostrando que
la variabilidad no es solo "encendido/apagado" sino también parametrizable.
"""
from fastapi import APIRouter, Request

router = APIRouter(prefix="/grading", tags=["grading"])


@router.get("/")
def list_grades(request: Request):
    flags = request.app.state.feature_flags
    scale = flags.get_setting("academic_settings", "evaluation_scale", default="numeric")
    return {
        "feature": "grading",
        "source": "core_assets/backend/core_engine/features/grading",
        "evaluation_scale_used": scale,
        "sample_data": [
            {"persona_id": "P-001", "curso_id": "C-001", "valor": 9.5 if scale == "numeric" else "Sobresaliente"},
        ],
    }
