from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core_assets.backend.core_engine.main_factory import create_app
from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.models import (
    Base,
    CursoDB,
    MatriculaDB,
    PeriodoDB,
    PersonaDB,
)


FIXTURE_CONFIG = "tests_core/fixtures/universidad-compleja/product_config.yaml"


def _build_client() -> TestClient:
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
                    nombre="Semestre 2026-A",
                    fecha_inicio="2026-01-01",
                    fecha_fin="2026-06-30",
                ),
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
                CursoDB(id="CUR-1", nombre="Álgebra", periodo_id="PER-1"),
                CursoDB(id="CUR-2", nombre="Historia", periodo_id="PER-1"),
            ]
        )
        db.commit()

        for index in range(8):
            db.add(
                MatriculaDB(
                    id=f"MAT-{index+1}",
                    persona_id="P-001",
                    curso_id=f"CUR-{(index % 2) + 1}",
                    estado="inscrito",
                )
            )
        db.commit()

    return TestClient(app)


class TestPeriodosAndEnrollmentRoutes:
    def test_periodos_crud_and_errors(self):
        client = _build_client()

        list_response = client.get("/periodos/")
        assert list_response.status_code == 200
        list_payload = list_response.json()
        assert list_payload["service"] == "periodos"
        assert list_payload["total"] == 1

        missing_response = client.get("/periodos/NO-EXISTE")
        assert missing_response.status_code == 404
        assert "NO-EXISTE" in missing_response.json()["detail"]

        create_response = client.post(
            "/periodos/",
            json={
                "nombre": "Semestre 2026-B",
                "fecha_inicio": "2026-07-01",
                "fecha_fin": "2026-12-31",
            },
        )
        assert create_response.status_code == 201
        created_payload = create_response.json()
        assert created_payload["nombre"] == "Semestre 2026-B"

        update_response = client.put(
            f"/periodos/{created_payload['id']}",
            json={"nombre": "Semestre 2026-B actualizado"},
        )
        assert update_response.status_code == 200
        assert update_response.json()["nombre"] == "Semestre 2026-B actualizado"

        empty_update_response = client.put(
            f"/periodos/{created_payload['id']}",
            json={"nombre": None, "fecha_inicio": None, "fecha_fin": None},
        )
        assert empty_update_response.status_code == 422

        delete_response = client.delete(f"/periodos/{created_payload['id']}")
        assert delete_response.status_code == 200
        assert "eliminado correctamente" in delete_response.json()["message"]

        deleted_get_response = client.get(f"/periodos/{created_payload['id']}")
        assert deleted_get_response.status_code == 404

    def test_enrollment_crud_and_limit_fail_closed_path(self):
        client = _build_client()

        list_response = client.get("/enrollment/")
        assert list_response.status_code == 200
        list_payload = list_response.json()
        assert list_payload["feature"] == "enrollment"
        assert list_payload["total"] == 8

        get_missing_response = client.get("/enrollment/NO-EXISTE")
        assert get_missing_response.status_code == 404

        create_response = client.post(
            "/enrollment/",
            json={
                "persona_id": "P-002",
                "curso_id": "CUR-2",
                "estado": "inscrito",
            },
        )
        assert create_response.status_code == 201
        created_payload = create_response.json()
        assert created_payload["persona_id"] == "P-002"
        assert created_payload["estado"] == "inscrito"

        patch_response = client.patch(
            f"/enrollment/{created_payload['id']}/status",
            json={"estado": "aprobado"},
        )
        assert patch_response.status_code == 200
        assert patch_response.json()["estado"] == "aprobado"

        invalid_patch_response = client.patch(
            f"/enrollment/{created_payload['id']}/status",
            json={"estado": "estado_invalido"},
        )
        assert invalid_patch_response.status_code == 422

        update_unknown_response = client.patch(
            "/enrollment/NO-EXISTE/status",
            json={"estado": "retirado"},
        )
        assert update_unknown_response.status_code == 404

        delete_response = client.delete(f"/enrollment/{created_payload['id']}")
        assert delete_response.status_code == 200
        assert "eliminada correctamente" in delete_response.json()["message"]

        limit_conflict_response = client.post(
            "/enrollment/",
            json={
                "persona_id": "P-001",
                "curso_id": "CUR-2",
                "estado": "inscrito",
            },
        )
        assert limit_conflict_response.status_code == 409
        assert "ya tiene 8" in limit_conflict_response.json()["detail"].lower()
