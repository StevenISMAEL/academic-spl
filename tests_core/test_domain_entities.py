import pytest
from pydantic import ValidationError

from core_assets.backend.core_engine.domain.entities import (
    Curso,
    Evaluacion,
    Periodo,
    Persona,
)


class TestDomainEntities:
    def test_persona_model_constructs_and_serializes(self):
        persona = Persona(
            id="P-001",
            nombres="Ana",
            apellidos="García",
            documento_identidad="1001",
        )

        assert persona.id == "P-001"
        assert persona.model_dump()["documento_identidad"] == "1001"

    def test_periodo_curso_and_evaluacion_models_accept_expected_payloads(self):
        periodo = Periodo(
            id="PER-001",
            nombre="2026-A",
            fecha_inicio="2026-01-01",
            fecha_fin="2026-06-30",
        )
        curso = Curso(
            id="C-001",
            nombre="Matemáticas",
            periodo_id=periodo.id,
        )
        evaluacion = Evaluacion(
            id="E-001",
            curso_id=curso.id,
            persona_id="P-001",
            valor=8.5,
        )

        assert periodo.nombre == "2026-A"
        assert curso.periodo_id == "PER-001"
        assert evaluacion.valor == 8.5

    def test_domain_entities_reject_missing_required_fields(self):
        with pytest.raises(ValidationError):
            Persona(id="P-001", nombres="Ana", apellidos="García")

        with pytest.raises(ValidationError):
            Curso(id="C-001", nombre="Matemáticas")
