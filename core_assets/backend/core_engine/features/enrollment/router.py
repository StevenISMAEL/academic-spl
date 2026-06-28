"""
Feature: Enrollment (Matrícula/Inscripción) — Core Asset activable.

Se monta solo si `features.enrollment: true` en la configuración del
producto. Típicamente más relevante en productos de educación superior
(inscripción por créditos) que en colegios (matrícula anual simple),
pero esa decisión vive en la configuración del producto, no aquí.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/enrollment", tags=["enrollment"])


@router.get("/")
def list_enrollments():
    return {
        "feature": "enrollment",
        "source": "core_assets/backend/core_engine/features/enrollment",
        "sample_data": [
            {"persona_id": "P-010", "curso_id": "C-005", "estado": "inscrito"},
        ],
    }
