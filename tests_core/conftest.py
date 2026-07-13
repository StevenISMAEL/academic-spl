"""
Arnés de pruebas reutilizable para la línea de productos académica (COR-24)

Este archivo configura fixtures pytest que permiten testear los Core Assets
y la variabilidad SPLE sin levantar servidores manualmente.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi.testclient import TestClient

from core_assets.backend.core_engine.persistence.models import Base
from core_assets.backend.core_engine.config.feature_flags import FeatureFlags
from core_assets.backend.core_engine.main_factory import create_app


@pytest.fixture
def db_session():
    """Base de datos en memoria — se destruye al terminar cada test."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def flags_colegio():
    """FeatureFlags cargados desde el YAML del colegio."""
    return FeatureFlags("products/colegio-basico/product_config.yaml")


@pytest.fixture
def flags_universidad():
    """FeatureFlags cargados desde el YAML de la universidad."""
    return FeatureFlags("products/universidad-compleja/product_config.yaml")


@pytest.fixture
def flags_tecnico():
    """FeatureFlags cargados desde el YAML del instituto técnico."""
    return FeatureFlags("products/instituto-tecnico/product_config.yaml")


@pytest.fixture
def client_colegio():
    """Cliente HTTP para tests de integración del colegio."""
    app = create_app("products/colegio-basico/product_config.yaml")
    return TestClient(app)


@pytest.fixture
def client_universidad():
    """Cliente HTTP para tests de integración de la universidad."""
    app = create_app("products/universidad-compleja/product_config.yaml")
    return TestClient(app)


@pytest.fixture
def client_tecnico():
    """Cliente HTTP para tests de integración del instituto técnico."""
    app = create_app("products/instituto-tecnico/product_config.yaml")
    return TestClient(app)
