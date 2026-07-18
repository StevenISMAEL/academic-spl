"""
Arnés de pruebas reutilizable para la línea de productos académica (COR-24)

Este archivo configura fixtures pytest que permiten testear los Core Assets
y la variabilidad SPLE sin levantar servidores manualmente.

NOTA: Los product_config.yaml usados aquí son FIXTURES de test, ubicados en
tests_core/fixtures/. Son independientes de los productos derivados reales
(derived_products/) para que el pipeline CI/CD sea autosuficiente.
"""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from core_assets.backend.core_engine.persistence.models import Base
from core_assets.backend.core_engine.config.feature_flags import FeatureFlags
from core_assets.backend.core_engine.main_factory import create_app

# Ruta base de los fixtures de test — relativa a este archivo
_FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.fixture
def db_session():
    """Base de datos en memoria — se destruye al terminar cada test."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def flags_colegio():
    """FeatureFlags cargados desde el fixture de test del colegio."""
    path = os.path.join(_FIXTURES_DIR, "colegio-basico", "product_config.yaml")
    return FeatureFlags(path)


@pytest.fixture
def flags_universidad():
    """FeatureFlags cargados desde el fixture de test de la universidad."""
    path = os.path.join(_FIXTURES_DIR, "universidad-compleja", "product_config.yaml")
    return FeatureFlags(path)


@pytest.fixture
def flags_tecnico():
    """FeatureFlags cargados desde el fixture de test del instituto técnico."""
    path = os.path.join(_FIXTURES_DIR, "instituto-tecnico", "product_config.yaml")
    return FeatureFlags(path)


@pytest.fixture
def client_colegio():
    """Cliente HTTP para tests de integración del colegio."""
    path = os.path.join(_FIXTURES_DIR, "colegio-basico", "product_config.yaml")
    app = create_app(path)
    return TestClient(app)


@pytest.fixture
def client_universidad():
    """Cliente HTTP para tests de integración de la universidad."""
    path = os.path.join(_FIXTURES_DIR, "universidad-compleja", "product_config.yaml")
    app = create_app(path)
    return TestClient(app)


@pytest.fixture
def client_tecnico():
    """Cliente HTTP para tests de integración del instituto técnico."""
    path = os.path.join(_FIXTURES_DIR, "instituto-tecnico", "product_config.yaml")
    app = create_app(path)
    return TestClient(app)
