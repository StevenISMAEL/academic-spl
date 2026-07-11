"""
Core Asset — MigrationRunner (COR-13)

Script de línea de comandos para crear las tablas del esquema académico
en cualquier base de datos SQLite indicada por argumento.

Uso:
    python core_assets/backend/core_engine/persistence/migrate.py <db_path>

Ejemplos:
    python core_assets/backend/core_engine/persistence/migrate.py products/colegio-basico/colegio_basico.db
    python core_assets/backend/core_engine/persistence/migrate.py products/universidad-compleja/universidad_compleja.db

REGLA DE ORO: Este script NO conoce el nombre del producto — solo
recibe una ruta de archivo. El mismo script sirve para cualquier
producto derivado de la línea, presente o futuro.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def run_migration(db_path: str) -> None:
    """Crea todas las tablas del esquema académico en la BD indicada.

    Si las tablas ya existen, SQLAlchemy las deja como están
    (CREATE TABLE IF NOT EXISTS). Es idempotente: se puede correr
    múltiples veces sin efecto negativo.

    Args:
        db_path: Ruta al archivo SQLite. Si el directorio no existe,
                 se crea automáticamente.
    """
    from sqlalchemy import create_engine

    # Importamos los modelos para que SQLAlchemy los conozca antes de
    # llamar a create_all. El import registra los modelos en Base.metadata.
    from core_assets.backend.core_engine.persistence.models import Base  # noqa: F401

    # Crear directorio padre si no existe (ej. products/colegio-basico/)
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    database_url = f"sqlite:///{db_path}"
    engine = create_engine(database_url, echo=True)

    print(f"\n[MigrationRunner] Creando tablas en: {db_path}")
    Base.metadata.create_all(bind=engine)
    print(f"[MigrationRunner] OK - Migracion completada: {db_path}\n")

    engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "MigrationRunner — Core Asset de persistencia. "
            "Crea el esquema de tablas del dominio académico en la BD indicada."
        )
    )
    parser.add_argument(
        "db_path",
        help="Ruta al archivo SQLite donde se crearán las tablas. "
             "Ejemplo: products/colegio-basico/colegio_basico.db",
    )
    args = parser.parse_args()

    try:
        run_migration(args.db_path)
    except Exception as exc:
        print(f"[MigrationRunner] ERROR durante la migracion: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
