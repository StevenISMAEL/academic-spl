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

from core_assets.backend.core_engine.persistence.path_utils import (
    ensure_parent_dir,
    safe_resolve_path,
)


def run_migration(db_path: str, config_path: str) -> None:
    """Crea las tablas del esquema académico requeridas por el producto.

    Args:
        db_path: Ruta al archivo SQLite. Se valida contra Path Traversal.
        config_path: Ruta al archivo product_config.yaml. Se valida contra Path Traversal.

    Raises:
        ValueError: Si alguna ruta contiene componentes `..` que escapen del
                    directorio del proyecto (protección contra CWE-22).
    """
    # --- SEGURIDAD: Validar rutas recibidas desde CLI antes de cualquier acceso ---
    # Protección contra Path Traversal (CWE-22 / OWASP A01).
    safe_db_path: Path = safe_resolve_path(db_path)
    safe_config_path: Path = safe_resolve_path(config_path)
    from sqlalchemy import create_engine
    
    # Importar FeatureFlags para conocer qué features están activos
    from core_assets.backend.core_engine.config.feature_flags import FeatureFlags
    # Importar todos los modelos (estáticos)
    from core_assets.backend.core_engine.persistence.models import (
        Base, PersonaDB, PeriodoDB, CursoDB, 
        EvaluacionDB, AsistenciaDB, MatriculaDB, 
        HorarioDB, CertificadoDB, AuditoriaDB
    )

    flags = FeatureFlags(str(safe_config_path))

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

    # Crear directorio padre si no existe (usa helper centralizado)
    ensure_parent_dir(safe_db_path)

    database_url = f"sqlite:///{safe_db_path}"
    engine = create_engine(database_url, echo=True)

    print(f"\n[MigrationRunner] Creando tablas en: {safe_db_path}")
    print(f"[MigrationRunner] Tablas a crear: {[t.name for t in tablas_activas]}")
    
    # Crear ÚNICAMENTE las tablas activas
    Base.metadata.create_all(bind=engine, tables=tablas_activas)
    
    print(f"[MigrationRunner] OK - Migracion completada: {safe_db_path}\n")
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
    except ValueError as exc:
        # ValueError de safe_resolve_path → posible Path Traversal
        print(f"[MigrationRunner] SEGURIDAD - Ruta rechazada: {exc}", file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        print(f"[MigrationRunner] ERROR durante la migracion: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
