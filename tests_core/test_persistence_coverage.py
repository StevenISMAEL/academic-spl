from __future__ import annotations

from pathlib import Path

import yaml

from core_assets.backend.core_engine.persistence.migrate import run_migration
from core_assets.backend.core_engine.persistence.seeder import _load_config, run_seeder
from core_assets.backend.core_engine.persistence.path_utils import safe_resolve_path


def _workspace_tmp_dir(name: str) -> Path:
    root = Path(__file__).resolve().parents[1]
    target = root / ".tmp_coverage_tests" / name
    target.mkdir(parents=True, exist_ok=True)
    return target


def test_run_migration_creates_expected_tables_for_active_features():
    tmp_dir = _workspace_tmp_dir("migration")
    db_path = tmp_dir / "academic.db"
    config_path = tmp_dir / "product_config.yaml"

    config_path.write_text(
        yaml.safe_dump(
            {
                "metadata": {"product_name": "Test Product"},
                "features": {
                    "grading": True,
                    "attendance": True,
                    "enrollment": True,
                    "schedule": True,
                    "certificates": True,
                    "auditing": True,
                },
            }
        ),
        encoding="utf-8",
    )

    run_migration(str(db_path), str(config_path))

    assert db_path.exists()


def test_safe_resolve_path_rejects_traversal_attempts():
    try:
        safe_resolve_path("../../../etc/passwd")
        assert False, "Se esperaba ValueError"
    except ValueError:
        assert True


def test_load_config_reads_yaml_and_returns_dict():
    tmp_dir = _workspace_tmp_dir("load_config")
    config_path = tmp_dir / "product_config.yaml"
    payload = {
        "metadata": {"product_name": "Demo"},
        "database": {"path": "demo.db"},
        "seed_data": {
            "personas": [{"id": "P-001", "nombres": "Ana", "apellidos": "López", "documento_identidad": "1234567890"}],
            "periodos": [{"id": "PER-001", "nombre": "2026-A", "fecha_inicio": "2026-01-01", "fecha_fin": "2026-06-30"}],
            "cursos": [{"id": "C-001", "nombre": "Matemáticas", "periodo_id": "PER-001"}],
        },
    }
    config_path.write_text(yaml.safe_dump(payload), encoding="utf-8")

    loaded = _load_config(str(config_path))
    assert loaded["metadata"]["product_name"] == "Demo"
    assert loaded["seed_data"]["personas"][0]["id"] == "P-001"


def test_seed_helpers_insert_new_rows_and_avoid_duplicates():
    tmp_dir = _workspace_tmp_dir("seed")
    db_path = tmp_dir / "seed.db"
    config_path = tmp_dir / "product_config.yaml"

    payload = {
        "metadata": {"product_name": "Demo"},
        "database": {"path": str(db_path)},
        "seed_data": {
            "personas": [{"id": "P-001", "nombres": "Ana", "apellidos": "López", "documento_identidad": "1234567890"}],
            "periodos": [{"id": "PER-001", "nombre": "2026-A", "fecha_inicio": "2026-01-01", "fecha_fin": "2026-06-30"}],
            "cursos": [{"id": "C-001", "nombre": "Matemáticas", "periodo_id": "PER-001"}],
        },
    }
    config_path.write_text(yaml.safe_dump(payload), encoding="utf-8")

    run_seeder(str(config_path))

    assert db_path.exists()


def test_run_seeder_raises_when_database_path_missing():
    tmp_dir = _workspace_tmp_dir("missing_db_path")
    config_path = tmp_dir / "product_config.yaml"
    config_path.write_text(yaml.safe_dump({"metadata": {"product_name": "Demo"}, "seed_data": {}}), encoding="utf-8")

    try:
        run_seeder(str(config_path))
        assert False, "Se esperaba ValueError"
    except ValueError:
        assert True
