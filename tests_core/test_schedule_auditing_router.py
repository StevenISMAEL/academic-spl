from __future__ import annotations

import tempfile
from pathlib import Path

import yaml
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core_assets.backend.core_engine.main_factory import create_app
from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.models import (
    Base,
    CursoDB,
    HorarioDB,
    PeriodoDB,
)


FIXTURE_TEMPLATE = Path(__file__).resolve().parent / "fixtures" / "instituto-tecnico" / "product_config.yaml"


def _write_active_config(tmpdir: str) -> str:
    content = yaml.safe_load(FIXTURE_TEMPLATE.read_text(encoding="utf-8"))
    content["features"]["auditing"] = True
    content["features"]["schedule"] = True
    config_path = Path(tmpdir) / "product_config.yaml"
    config_path.write_text(yaml.safe_dump(content, sort_keys=False), encoding="utf-8")
    return str(config_path)


def _build_client(config_path: str) -> TestClient:
    app = create_app(config_path)
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
        db.add(
            PeriodoDB(
                id="PER-1",
                nombre="Semestre 2026-A",
                fecha_inicio="2026-01-01",
                fecha_fin="2026-06-30",
            )
        )
        db.add_all(
            [
                CursoDB(id="CUR-1", nombre="Matemática", periodo_id="PER-1"),
                CursoDB(id="CUR-2", nombre="Historia", periodo_id="PER-1"),
            ]
        )
        db.commit()

        db.add_all(
            [
                HorarioDB(
                    id="HOR-1",
                    curso_id="CUR-1",
                    dia_semana="Lunes",
                    hora_inicio="08:00",
                    hora_fin="10:00",
                    aula="A-101",
                ),
                HorarioDB(
                    id="HOR-2",
                    curso_id="CUR-2",
                    dia_semana="Martes",
                    hora_inicio="09:00",
                    hora_fin="11:00",
                    aula="B-202",
                ),
            ]
        )
        db.commit()

    return TestClient(app)


class TestScheduleAndAuditingRoutes:
    def test_schedule_routes_cover_crud_and_listing_branches(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as tmpdir:
            config_path = _write_active_config(tmpdir)
            client = _build_client(config_path)

            list_response = client.get("/schedule/")
            assert list_response.status_code == 200
            list_payload = list_response.json()
            assert list_payload["feature"] == "schedule"
            assert list_payload["total_horarios"] == 2
            assert "Lunes" in list_payload["horarios_por_dia"]

            invalid_create_response = client.post(
                "/schedule/",
                json={
                    "curso_id": "CUR-1",
                    "dia_semana": "Domingo",
                    "hora_inicio": "08:00",
                    "hora_fin": "10:00",
                    "aula": "A-101",
                },
            )
            assert invalid_create_response.status_code == 422
            assert "Día 'Domingo' no válido" in invalid_create_response.json()["detail"]

            create_response = client.post(
                "/schedule/",
                json={
                    "curso_id": "CUR-1",
                    "dia_semana": "Miércoles",
                    "hora_inicio": "11:00",
                    "hora_fin": "12:30",
                    "aula": "A-220",
                },
            )
            assert create_response.status_code == 201
            created_payload = create_response.json()
            assert created_payload["created"] is True
            assert created_payload["horario"]["dia_semana"] == "Miércoles"

            by_course_response = client.get("/schedule/curso/CUR-1")
            assert by_course_response.status_code == 200
            by_course_payload = by_course_response.json()
            assert by_course_payload["curso_id"] == "CUR-1"
            assert by_course_payload["total"] == 2

            schedule_id = created_payload["horario"]["id"]
            get_response = client.get(f"/schedule/{schedule_id}")
            assert get_response.status_code == 200
            assert get_response.json()["id"] == schedule_id

            delete_response = client.delete(f"/schedule/{schedule_id}")
            assert delete_response.status_code == 200
            assert delete_response.json()["deleted"] is True

            missing_delete_response = client.delete("/schedule/NO-EXISTE")
            assert missing_delete_response.status_code == 404

    def test_auditing_routes_create_and_list_logs(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as tmpdir:
            config_path = _write_active_config(tmpdir)
            client = _build_client(config_path)

            empty_get_response = client.get("/auditing/")
            assert empty_get_response.status_code == 200
            assert empty_get_response.json() == []

            create_response = client.post(
                "/auditing/",
                json={
                    "usuario_id": "U-001",
                    "accion": "CREATE",
                    "entidad": "personas",
                    "entidad_id": "P-001",
                    "detalles": {"mensaje": "registro creado"},
                },
            )
            assert create_response.status_code == 200
            created_payload = create_response.json()
            assert created_payload["usuario_id"] == "U-001"
            assert created_payload["accion"] == "CREATE"
            assert created_payload["detalles"] == {"mensaje": "registro creado"}

            list_response = client.get("/auditing/")
            assert list_response.status_code == 200
            list_payload = list_response.json()
            assert len(list_payload) == 1
            assert list_payload[0]["entidad"] == "personas"
            assert list_payload[0]["id"] == created_payload["id"]
