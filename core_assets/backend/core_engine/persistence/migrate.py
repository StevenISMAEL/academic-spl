"""
Core Asset — MigrationRunner (COR-13)

Script de línea de comandos para crear las tablas del esquema académico
en cualquier base de datos SQLite indicada por argumento.

Uso:
    python core_assets/backend/core_engine/persistence/migrate.py <db_path> <config_path>

Ejemplos:
    python core_assets/backend/core_engine/persistence/migrate.py products/colegio/colegio.db products/colegio/product_config.yaml

REGLA DE ORO: Este script NO conoce el nombre del producto, pero 
SÍ es responsable de la Variabilidad de Persistencia. Lee los features
activos y crea UNICAMENTE las tablas necesarias en la base de datos.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def run_migration(db_path: str, config_path: str) -> None:
    """Crea las tablas del esquema académico requeridas por el producto.

    Args:
        db_path: Ruta al archivo SQLite.
        config_path: Ruta al archivo product_config.yaml
    """
    from sqlalchemy import create_engine
    
    # Importar FeatureFlags para conocer qué features están activos
    from core_assets.backend.core_engine.config.feature_flags import FeatureFlags
    # Importar todos los modelos (estáticos)
    from core_assets.backend.core_engine.persistence.models import (
        Base, PersonaDB, PeriodoDB, CursoDB, 
        EvaluacionDB, AsistenciaDB, MatriculaDB, 
        HorarioDB, CertificadoDB, AuditoriaDB
    )

    flags = FeatureFlags(config_path)

    # Las tablas Core siempre se crean
    tablas_activas = [
        PersonaDB.__table__,
        PeriodoDB.__table__,
        CursoDB.__table__,
    ]

    # Mapeo explícito de Feature -> Tablas
    FEATURE_TABLES = {
        "grading": [EvaluacionDB.__table__],
        "attendance": [AsistenciaDB.__table__],
        "enrollment": [MatriculaDB.__table__],
        "schedule": [HorarioDB.__table__],
        "reports": [],  # no tiene tablas propias
        "certificates": [CertificadoDB.__table__],
        "auditing": [AuditoriaDB.__table__],
    }

    # Agregar tablas de los features opcionales activos
    for feature_name, tables in FEATURE_TABLES.items():
        if flags.is_active(feature_name):
            tablas_activas.extend(tables)

    # Crear directorio padre si no existe
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    database_url = f"sqlite:///{db_path}"
    engine = create_engine(database_url, echo=True)

    print(f"\n[MigrationRunner] Creando tablas en: {db_path}")
    print(f"[MigrationRunner] Tablas a crear: {[t.name for t in tablas_activas]}")
    
    # Crear ÚNICAMENTE las tablas activas
    Base.metadata.create_all(bind=engine, tables=tablas_activas)
    
    print(f"[MigrationRunner] OK - Migracion completada: {db_path}\n")
    engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "MigrationRunner — Core Asset de persistencia. "
            "Crea el esquema selectivo del dominio académico en la BD indicada."
        )
    )
    parser.add_argument(
        "db_path",
        help="Ruta al archivo SQLite donde se crearán las tablas."
    )
    parser.add_argument(
        "config_path",
        help="Ruta al archivo product_config.yaml del producto."
    )
    args = parser.parse_args()

    try:
        run_migration(args.db_path, args.config_path)
    except Exception as exc:
        print(f"[MigrationRunner] ERROR durante la migracion: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
