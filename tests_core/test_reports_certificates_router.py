from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from core_assets.backend.core_engine.main_factory import create_app
from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.models import (
    AsistenciaDB,
    Base,
    CertificadoDB,
    CursoDB,
    EvaluacionDB,
    PeriodoDB,
    PersonaDB,
)


FIXTURE_CONFIG = "tests_core/fixtures/universidad-compleja/product_config.yaml"


def _build_client_with_seed_data() -> TestClient:
    app = create_app(FIXTURE_CONFIG)
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with SessionLocal() as db:
        db.add_all(
            [
                PeriodoDB(
                    id="PER-1",
                    nombre="2026-A",
                    fecha_inicio="2026-01-01",
                    fecha_fin="2026-06-30",
                ),
                CursoDB(id="CUR-1", nombre="Álgebra", periodo_id="PER-1"),
                PersonaDB(
                    id="P-001",
                    nombres="Ana",
                    apellidos="García",
                    documento_identidad="1001",
                ),
                PersonaDB(
                    id="P-002",
                    nombres="Luis",
                    apellidos="Pérez",
                    documento_identidad="1002",
                ),
            ]
        )
        db.commit()

        db.add_all(
            [
                EvaluacionDB(
                    id="EV-1",
                    curso_id="CUR-1",
                    persona_id="P-001",
                    valor=8.0,
                    observacion="Excelente",
                ),
                EvaluacionDB(
                    id="EV-2",
                    curso_id="CUR-1",
                    persona_id="P-001",
                    valor=6.0,
                    observacion="Suficiente",
                ),
                EvaluacionDB(
                    id="EV-3",
                    curso_id="CUR-1",
                    persona_id="P-002",
                    valor=4.5,
                    observacion="Reprobado",
                ),
                AsistenciaDB(
                    id="AS-1",
                    persona_id="P-001",
                    curso_id="CUR-1",
                    fecha="2026-01-02",
                    presente=True,
                    justificacion=None,
                ),
                AsistenciaDB(
                    id="AS-2",
                    persona_id="P-001",
                    curso_id="CUR-1",
                    fecha="2026-01-03",
                    presente=True,
                    justificacion=None,
                ),
                AsistenciaDB(
                    id="AS-3",
                    persona_id="P-002",
                    curso_id="CUR-1",
                    fecha="2026-01-02",
                    presente=False,
                    justificacion="Sin justificación",
                ),
            ]
        )
        db.commit()

    return TestClient(app)


class TestReportsAndCertificatesRoutes:
    def test_reports_routes_return_config_and_student_consolidated_summary(self):
        client = _build_client_with_seed_data()

        list_response = client.get("/reports/")
        assert list_response.status_code == 200
        payload = list_response.json()
        assert payload["feature"] == "reports"
        assert payload["configuracion_producto"]["product_name"] == "Universidad Compleja (Test Fixture)"
        assert payload["configuracion_producto"]["passing_grade"] == 6.0
        assert payload["configuracion_producto"]["attendance_min_percentage"] == 60.0
        assert len(payload["personas_disponibles"]) == 2

        student_response = client.get("/reports/rendimiento/P-001")
        assert student_response.status_code == 200
        student_payload = student_response.json()
        assert student_payload["feature"] == "reports"
        assert student_payload["reporte"]["persona_id"] == "P-001"
        assert student_payload["reporte"]["estado_final"] == "APROBADO"
        assert student_payload["reporte"]["resumen_notas"]["promedio"] == 7.0
        assert student_payload["reporte"]["asistencia"]["estado"] == "APROBADO"

        consolidated_response = client.get("/reports/consolidado/")
        assert consolidated_response.status_code == 200
        consolidated_payload = consolidated_response.json()
        assert consolidated_payload["feature"] == "reports"
        assert consolidated_payload["total_estudiantes"] == 2
        assert consolidated_payload["resumen_estados"]["APROBADO"] == 1
        assert consolidated_payload["resumen_estados"]["REPROBADO_FALTA"] == 1

    def test_certificates_routes_generate_and_read_certificate_history(self):
        client = _build_client_with_seed_data()

        list_response = client.get("/certificates/")
        assert list_response.status_code == 200
        list_payload = list_response.json()
        assert list_payload["feature"] == "certificates"
        assert list_payload["product_name"] == "Universidad Compleja (Test Fixture)"
        assert list_payload["total_certificados"] == 0

        missing_response = client.post("/certificates/NO-EXISTE/generate")
        assert missing_response.status_code == 404
        assert "NO-EXISTE" in missing_response.json()["detail"]

        generate_response = client.post("/certificates/P-001/generate")
        assert generate_response.status_code == 201
        generated_payload = generate_response.json()
        assert generated_payload["feature"] == "certificates"
        assert generated_payload["persona_id"] == "P-001"
        assert generated_payload["certificado"]["estado"] == "emitido"
        assert generated_payload["verificaciones"]["nota"]["cumple"] is True
        assert generated_payload["verificaciones"]["asistencia"]["cumple"] is True

        certificate_id = generated_payload["certificado"]["id"]

        certificate_response = client.get(f"/certificates/{certificate_id}")
        assert certificate_response.status_code == 200
        certificate_payload = certificate_response.json()
        assert certificate_payload["id"] == certificate_id
        assert certificate_payload["estado"] == "emitido"

        by_persona_response = client.get("/certificates/persona/P-001")
        assert by_persona_response.status_code == 200
        by_persona_payload = by_persona_response.json()
        assert by_persona_payload["persona_id"] == "P-001"
        assert len(by_persona_payload["certificados"]) == 1
        assert by_persona_payload["certificados"][0]["estado"] == "emitido"

        list_after_response = client.get("/certificates/")
        assert list_after_response.status_code == 200
        list_after_payload = list_after_response.json()
        assert list_after_payload["total_certificados"] == 1
        assert list_after_payload["emitidos"] == 1
        assert list_after_payload["rechazados"] == 0
