"""
Core Asset — UserSeeder genérico (COR-16)

Script que lee una lista de personas (y opcionalmente periodos y cursos)
del product_config.yaml de un producto y los inserta en su BD.

Uso:
    python core_assets/backend/core_engine/persistence/seeder.py <config_path>

Ejemplo:
    python core_assets/backend/core_engine/persistence/seeder.py products/colegio-basico/product_config.yaml

El product_config.yaml puede contener una sección `seed_data` opcional:

    seed_data:
      personas:
        - id: "P-001"
          nombres: "Ana"
          apellidos: "García"
          documento_identidad: "0001"
        - id: "P-002"
          nombres: "Luis"
          apellidos: "Martínez"
          documento_identidad: "0002"
      periodos:
        - id: "PER-001"
          nombre: "Periodo 2024-A"
          fecha_inicio: "2024-01-15"
          fecha_fin: "2024-06-30"
      cursos:
        - id: "C-001"
          nombre: "Matemáticas"
          periodo_id: "PER-001"

REGLA DE ORO: Este script NO hardcodea ningún producto. Lee la
configuración del producto indicado por argumento y siembra los
datos que ese YAML declara.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core_assets.backend.core_engine.persistence.models import (
    Base,
    CursoDB,
    MatriculaDB,
    PersonaDB,
    PeriodoDB,
)
from core_assets.backend.core_engine.persistence.path_utils import (
    ensure_parent_dir,
    safe_resolve_path,
)


def _load_config(config_path: str) -> Dict[str, Any]:
    # --- SEGURIDAD: validar ruta antes de abrir archivo ---
    # Protección contra Path Traversal (CWE-22 / OWASP A01).
    safe_path = safe_resolve_path(config_path)
    if not safe_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_path}")
    with open(safe_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _get_session(db_path: str):
    # --- SEGURIDAD: validar ruta de BD antes de crear engine ---
    # La ruta db_path puede venir del YAML (input externo); se valida igual.
    safe_db = safe_resolve_path(db_path)
    ensure_parent_dir(safe_db)
    engine = create_engine(f"sqlite:///{safe_db}", echo=False)
    Base.metadata.create_all(engine)  # Asegura que las tablas existan
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def _seed_personas(session, personas: List[Dict[str, Any]]) -> int:
    count = 0
    for p in personas:
        existing = session.query(PersonaDB).filter(PersonaDB.id == p["id"]).first()
        if not existing:
            session.add(PersonaDB(
                id=p["id"],
                nombres=p["nombres"],
                apellidos=p["apellidos"],
                documento_identidad=p["documento_identidad"],
            ))
            count += 1
    return count


def _seed_periodos(session, periodos: List[Dict[str, Any]]) -> int:
    count = 0
    for p in periodos:
        existing = session.query(PeriodoDB).filter(PeriodoDB.id == p["id"]).first()
        if not existing:
            session.add(PeriodoDB(
                id=p["id"],
                nombre=p["nombre"],
                fecha_inicio=p["fecha_inicio"],
                fecha_fin=p["fecha_fin"],
            ))
            count += 1
    return count


def _seed_cursos(session, cursos: List[Dict[str, Any]]) -> int:
    count = 0
    for c in cursos:
        existing = session.query(CursoDB).filter(CursoDB.id == c["id"]).first()
        if not existing:
            session.add(CursoDB(
                id=c["id"],
                nombre=c["nombre"],
                periodo_id=c["periodo_id"],
            ))
            count += 1
    return count


def run_seeder(config_path: str) -> None:
    """Ejecuta el seeder para el producto indicado por su config_path.

    Lee la sección `seed_data` del YAML del producto y siembra los datos
    en la BD correspondiente (indicada por `database.path` en el mismo YAML).

    Es idempotente: datos que ya existen (mismo ID) se omiten sin error.
    """
    config = _load_config(config_path)
    product_name = config.get("metadata", {}).get("product_name", "desconocido")

    db_path = config.get("database", {}).get("path")
    if not db_path:
        raise ValueError(
            f"El archivo '{config_path}' no tiene 'database.path' configurado. "
            "Agrega la sección 'database:' antes de usar el seeder."
        )

    seed_data = config.get("seed_data", {})
    if not seed_data:
        print(f"[Seeder] AVISO: '{config_path}' no tiene seccion 'seed_data'. Nada que sembrar.")
        return

    print(f"\n[Seeder] Iniciando siembra para: {product_name}")
    print(f"[Seeder] Base de datos: {db_path}")

    session = _get_session(db_path)
    try:
        totals: Dict[str, int] = {}

        if "personas" in seed_data:
            totals["personas"] = _seed_personas(session, seed_data["personas"])

        if "periodos" in seed_data:
            totals["periodos"] = _seed_periodos(session, seed_data["periodos"])

        if "cursos" in seed_data:
            totals["cursos"] = _seed_cursos(session, seed_data["cursos"])

        session.commit()

        print("[Seeder] OK - Siembra completada:")
        for entity, count in totals.items():
            print(f"         • {entity}: {count} registro(s) nuevo(s) insertado(s)")
        print()

    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "UserSeeder — Core Asset genérico. "
            "Siembra datos iniciales en la BD de cualquier producto derivado."
        )
    )
    parser.add_argument(
        "config_path",
        help="Ruta al product_config.yaml del producto a sembrar. "
             "Ejemplo: products/colegio-basico/product_config.yaml",
    )
    args = parser.parse_args()

    try:
        run_seeder(args.config_path)
    except ValueError as exc:
        # ValueError de safe_resolve_path → posible Path Traversal
        print(f"[Seeder] SEGURIDAD - Ruta rechazada: {exc}", file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        print(f"[Seeder] ERROR durante la siembra: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
