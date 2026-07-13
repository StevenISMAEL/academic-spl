"""
Core Asset — Modelos ORM de SQLAlchemy (COR-13)

Estos modelos son la representación de las entidades del dominio académico
en la base de datos relacional. Son diferentes de las entidades Pydantic
en `domain/entities.py` (que son el contrato de la API HTTP).

Separación de responsabilidades:
  - entities.py (Pydantic)  → validación HTTP, entrada/salida de la API
  - models.py (SQLAlchemy)  → persistencia, estructura de tablas en la BD

Los Repositories son los responsables de convertir entre ambas capas.

REGLA DE ORO: Este archivo NO menciona ningún producto. Las tablas son
genéricas para cualquier producto académico derivado de la línea.
"""
from __future__ import annotations

from sqlalchemy import Boolean, Column, Float, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Base declarativa compartida por todos los modelos del Core."""
    pass


class PersonaDB(Base):
    """Tabla de personas (estudiantes, docentes, etc.) — genérica."""
    __tablename__ = "personas"

    id = Column(String, primary_key=True, index=True)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    documento_identidad = Column(String, nullable=False, unique=True)

    # Relaciones inversas (opcionales para queries avanzadas)
    evaluaciones = relationship("EvaluacionDB", back_populates="persona")
    asistencias = relationship("AsistenciaDB", back_populates="persona")
    matriculas = relationship("MatriculaDB", back_populates="persona")


class PeriodoDB(Base):
    """Tabla de periodos académicos (semestres, años, trimestres, etc.)."""
    __tablename__ = "periodos"

    id = Column(String, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    fecha_inicio = Column(String, nullable=False)  # ISO 8601: "YYYY-MM-DD"
    fecha_fin = Column(String, nullable=False)

    cursos = relationship("CursoDB", back_populates="periodo")


class CursoDB(Base):
    """Tabla de cursos/materias — pertenece a un Periodo."""
    __tablename__ = "cursos"

    id = Column(String, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    periodo_id = Column(String, ForeignKey("periodos.id"), nullable=False)

    periodo = relationship("PeriodoDB", back_populates="cursos")
    evaluaciones = relationship("EvaluacionDB", back_populates="curso")
    asistencias = relationship("AsistenciaDB", back_populates="curso")
    matriculas = relationship("MatriculaDB", back_populates="curso")


class EvaluacionDB(Base):
    """Tabla de evaluaciones/calificaciones (feature: grading)."""
    __tablename__ = "evaluaciones"

    id = Column(String, primary_key=True, index=True)
    curso_id = Column(String, ForeignKey("cursos.id"), nullable=False)
    persona_id = Column(String, ForeignKey("personas.id"), nullable=False)
    valor = Column(Float, nullable=False)
    observacion = Column(Text, nullable=True)  # Campo extra para notas del docente

    curso = relationship("CursoDB", back_populates="evaluaciones")
    persona = relationship("PersonaDB", back_populates="evaluaciones")


class AsistenciaDB(Base):
    """Tabla de registros de asistencia (feature: attendance)."""
    __tablename__ = "asistencias"

    id = Column(String, primary_key=True, index=True)
    persona_id = Column(String, ForeignKey("personas.id"), nullable=False)
    curso_id = Column(String, ForeignKey("cursos.id"), nullable=False)
    fecha = Column(String, nullable=False)  # ISO 8601: "YYYY-MM-DD"
    presente = Column(Boolean, nullable=False, default=False)
    justificacion = Column(Text, nullable=True)

    persona = relationship("PersonaDB", back_populates="asistencias")
    curso = relationship("CursoDB", back_populates="asistencias")


class MatriculaDB(Base):
    """Tabla de matrículas/inscripciones (feature: enrollment)."""
    __tablename__ = "matriculas"

    id = Column(String, primary_key=True, index=True)
    persona_id = Column(String, ForeignKey("personas.id"), nullable=False)
    curso_id = Column(String, ForeignKey("cursos.id"), nullable=False)
    estado = Column(String, nullable=False, default="inscrito")
    # Posibles valores de estado: "inscrito", "retirado", "aprobado", "reprobado"

    persona = relationship("PersonaDB", back_populates="matriculas")
    curso = relationship("CursoDB", back_populates="matriculas")


class HorarioDB(Base):
    """Tabla de horarios de clases (feature: schedule)."""
    __tablename__ = "horarios"

    id         = Column(String, primary_key=True, index=True)
    curso_id   = Column(String, ForeignKey("cursos.id"), nullable=False)
    dia_semana = Column(String, nullable=False)   # Lunes, Martes, ... Viernes
    hora_inicio = Column(String, nullable=False)  # "HH:MM"
    hora_fin    = Column(String, nullable=False)  # "HH:MM"
    aula        = Column(String, nullable=True)

    curso = relationship("CursoDB")


class CertificadoDB(Base):
    """Tabla de certificados de aprobacion (feature: certificates).

    Cada registro representa un intento de certificacion:
    - estado 'emitido'   → el estudiante cumplió nota y asistencia
    - estado 'rechazado' → no cumplió algún requisito (motivo en motivo_rechazo)
    """
    __tablename__ = "certificados"

    id              = Column(String, primary_key=True, index=True)
    persona_id      = Column(String, ForeignKey("personas.id"), nullable=False)
    curso_id        = Column(String, ForeignKey("cursos.id"),   nullable=False)
    fecha_emision   = Column(String, nullable=False)   # ISO 8601
    nota_final      = Column(Float,  nullable=True)    # None si no hay nota registrada
    asistencia_pct  = Column(Float,  nullable=True)    # None si no hay asistencia registrada
    estado          = Column(String, nullable=False)   # "emitido" | "rechazado"
    motivo_rechazo  = Column(Text,   nullable=True)    # null si estado == "emitido"

    persona = relationship("PersonaDB")
    curso   = relationship("CursoDB")

