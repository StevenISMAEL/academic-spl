"""
Core Asset — ConnectionResolver (COR-12)

Resuelve la conexión a la base de datos del producto activo.

La regla de oro se cumple aquí: este módulo NUNCA hardcodea un nombre
de producto ni una ruta. Lee `database.path` del product_config.yaml
del producto activo, que está almacenado en `app.state.feature_flags`.

Uso en un router (FastAPI Depends):

    from core_assets.backend.core_engine.persistence.connection_resolver import get_db

    @router.get("/")
    def list_items(db: Session = Depends(get_db)):
        ...
"""
from __future__ import annotations

from functools import lru_cache
from typing import Generator

from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


@lru_cache(maxsize=None)
def _get_engine(db_path: str) -> Engine:
    """Crea (o reutiliza) el engine SQLAlchemy para una ruta de BD dada.

    Se cachea por `db_path`: si dos productos usan la misma ruta
    (raro pero posible en tests) compartirán engine. En producción cada
    producto tendrá su propio archivo .db y su propio engine.

    Args:
        db_path: Ruta relativa o absoluta al archivo SQLite (.db).
                 Proviene de `database.path` del product_config.yaml.
    """
    database_url = f"sqlite:///{db_path}"
    return create_engine(
        database_url,
        connect_args={"check_same_thread": False},  # Necesario para SQLite + FastAPI
        echo=False,  # Cambiar a True para ver SQL en consola durante debugging
    )


def get_db(request: Request) -> Generator[Session, None, None]:
    """Dependencia FastAPI: provee una sesión de BD por request.

    Lee el path de la BD desde la configuración del producto activo
    (almacenada en app.state.feature_flags). El router nunca sabe
    qué archivo .db se está usando — esa información vive solo en el
    product_config.yaml del producto derivado.

    Yields:
        Session: sesión SQLAlchemy lista para usar. Se cierra
                 automáticamente al terminar el request.

    Raises:
        RuntimeError: si el product_config.yaml no tiene la sección
                      `database.path` configurada.
    """
    flags = request.app.state.feature_flags
    db_path: str | None = flags.get_setting("database", "path")

    if not db_path:
        raise RuntimeError(
            "El product_config.yaml no tiene 'database.path' configurado. "
            "Agrega la sección 'database:' con el path al archivo .db del producto."
        )

    engine = _get_engine(db_path)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
