"""
Core Service: Auth — Autenticación JWT básica (COR-22)

Este router proporciona autenticación básica usando JWT tokens.
Es un Core Service (siempre montado) porque todo producto académico
necesita autenticación de usuarios.

Implementación:
- Usa python-jose[cryptography] para JWT
- Usa passlib[bcrypt] para hashing de contraseñas
- Verifica credenciales contra la tabla PersonaDB (documento_identidad como contraseña demo)
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core_assets.backend.core_engine.persistence.connection_resolver import get_db
from core_assets.backend.core_engine.persistence.persona_repository import PersonaRepository

# ── Configuración JWT ─────────────────────────────────────────────────────────────

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Demo: cambiar en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(prefix="/auth", tags=["auth (core service)"])


# ── Modelos Pydantic ─────────────────────────────────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    persona_id: str | None = None


class User(BaseModel):
    id: str
    nombres: str
    apellidos: str
    documento_identidad: str


# ── Funciones de utilidad ───────────────────────────────────────────────────────

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Genera un hash bcrypt de una contraseña."""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Crea un token JWT codificado."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """
    Autentica un usuario verificando credenciales.
    
    Para demo: usa documento_identidad como contraseña.
    En producción, esto debería usar una tabla de usuarios real con contraseñas hasheadas.
    """
    repo = PersonaRepository(db)
    # Buscar persona por documento_identidad (usando email como documento para demo)
    persona = repo.get_by_documento(email)
    
    if not persona:
        return None
    
    # Demo: verificar que la contraseña coincide con el documento_identidad
    if password != persona["documento_identidad"]:
        return None
    
    return User(
        id=persona["id"],
        nombres=persona["nombres"],
        apellidos=persona["apellidos"],
        documento_identidad=persona["documento_identidad"],
    )


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Obtiene el usuario actual a partir del token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        persona_id: str = payload.get("sub")
        if persona_id is None:
            raise credentials_exception
        token_data = TokenData(persona_id=persona_id)
    except JWTError:
        raise credentials_exception
    
    repo = PersonaRepository(db)
    persona = repo.get_persona(token_data.persona_id)
    
    if persona is None:
        raise credentials_exception
    
    return User(
        id=persona["id"],
        nombres=persona["nombres"],
        apellidos=persona["apellidos"],
        documento_identidad=persona["documento_identidad"],
    )


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/token", response_model=Token, summary="Obtener token de acceso")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """
    Endpoint de login OAuth2.
    
    Recibe email y password via form-data y devuelve un token JWT.
    
    Para demo: usa documento_identidad como contraseña.
    Ejemplo: email="1001", password="1001"
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User, summary="Obtener usuario actual")
async def read_users_me(current_user: User = Depends(get_current_user)) -> User:
    """
    Devuelve los datos del usuario autenticado.
    
    Requiere un token JWT válido en el header Authorization:
    Authorization: Bearer <token>
    """
    return current_user
