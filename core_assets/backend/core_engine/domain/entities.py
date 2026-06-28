"""
Core Asset — Entidades de Dominio Académico Genérico (COR-04)

Estas entidades representan la "commonality" (lo común) del dominio
académico: todo producto derivado (colegio, universidad, instituto)
comparte estos conceptos base. Los productos pueden EXTENDER estos
modelos en su propia carpeta (products/<producto>/overrides/), pero
nunca deben modificarse aquí.
"""
from pydantic import BaseModel, Field


class Persona(BaseModel):
    id: str
    nombres: str
    apellidos: str
    documento_identidad: str


class Periodo(BaseModel):
    id: str
    nombre: str
    fecha_inicio: str
    fecha_fin: str


class Curso(BaseModel):
    id: str
    nombre: str
    periodo_id: str


class Evaluacion(BaseModel):
    id: str
    curso_id: str
    persona_id: str
    valor: float = Field(..., description="Valor numérico de la evaluación")
