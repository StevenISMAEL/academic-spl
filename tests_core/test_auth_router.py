from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from core_assets.backend.core_engine.config.feature_flags import FeatureFlags
from core_assets.backend.core_engine.features.auth.router import (
    create_access_token,
    get_password_hash,
    router,
    verify_password,
)
from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.models import Base, PersonaDB


def _build_auth_client(db_path: str = ":memory:"):
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    session = Session(engine)
    session.add(
        PersonaDB(
            id="P-001",
            nombres="Ana",
            apellidos="García",
            documento_identidad="1001",
        )
    )
    session.commit()
    session.close()

    def override_get_db(request: Request):
        SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = FastAPI()
    app.state.feature_flags = FeatureFlags("tests_core/fixtures/colegio-basico/product_config.yaml")
    app.dependency_overrides[get_db] = override_get_db
    app.include_router(router)

    client = TestClient(app)
    return client, app, engine


class TestAuthRouter:
    def test_login_and_me_flow(self):
        client, _, _ = _build_auth_client()

        token_response = client.post(
            "/auth/token",
            data={"username": "1001", "password": "1001"},
        )

        assert token_response.status_code == 200
        token = token_response.json()["access_token"]
        assert token

        me_response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert me_response.status_code == 200
        body = me_response.json()
        assert body["id"] == "P-001"
        assert body["documento_identidad"] == "1001"

    def test_login_rejects_bad_credentials(self):
        client, _, _ = _build_auth_client()

        response = client.post(
            "/auth/token",
            data={"username": "1001", "password": "wrong"},
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Email o contraseña incorrectos"

    def test_invalid_token_is_rejected(self):
        client, _, _ = _build_auth_client()

        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid-token"},
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "No se pudieron validar las credenciales"

    def test_password_helpers_behave_as_expected(self):
        password = ("s3cret" * 20)[:72]
        assert len(password) <= 72

        hashed = get_password_hash(password)

        assert verify_password(password, hashed)
        assert create_access_token({"sub": "P-001"})
