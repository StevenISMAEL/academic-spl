"""
Core Asset — Application Factory generico (COR-03, actualizado COR-20)

Esta es la pieza central de Application Engineering automatizado:
construye una instancia de FastAPI montando UNICAMENTE los modulos
(features) que la configuracion del producto declara como activos,
mas los Core Services que siempre se montan.

Este archivo NUNCA debe importar nada de products/. La unica forma en
que "sabe" que producto esta construyendo es a traves del path de
configuracion que recibe como parametro.

--- Estructura de montaje ---

  CORE SERVICES (siempre montados — son Commonality)
  ├── /periodos      → PeriodoRepository
  ├── /cursos        → CursoRepository
  └── /personas      → PersonaRepository (+ CedulaValidator CA-01)

  OPTIONAL FEATURES (montados segun product_config.yaml — son Variabilidad)
  ├── /attendance    → AttendanceRepository + AttendanceCalculator CA-03
  ├── /grading       → GradeRepository + GradeScaleConverter CA-02 + GradePassingChecker CA-04
  ├── /enrollment    → EnrollmentRepository + EnrollmentLimitChecker CA-05
  ├── /schedule      → Horarios (Sprint 3)
  ├── /reports       → Reportes academicos (Sprint 3)
  └── /certificates  → Certificados de aprobacion (Sprint 3)
"""
from __future__ import annotations

import os
from fastapi import FastAPI

from core_assets.backend.core_engine.config.feature_flags import FeatureFlags

# ── Core Services (Commonality) ───────────────────────────────────────────────
from core_assets.backend.core_engine.features.periodos.router import (
    router as periodos_router,
)
from core_assets.backend.core_engine.features.cursos.router import (
    router as cursos_router,
)
from core_assets.backend.core_engine.features.personas.router import (
    router as personas_router,
)

# ── Optional Features (Variabilidad) ─────────────────────────────────────────
from core_assets.backend.core_engine.features.attendance.router import (
    router as attendance_router,
)
from core_assets.backend.core_engine.features.grading.router import (
    router as grading_router,
)
from core_assets.backend.core_engine.features.enrollment.router import (
    router as enrollment_router,
)
from core_assets.backend.core_engine.features.schedule.router import (
    router as schedule_router,
)
from core_assets.backend.core_engine.features.reports.router import (
    router as reports_router,
)
from core_assets.backend.core_engine.features.certificates.router import (
    router as certificates_router,
)

# Catálogo de Core Assets opcionales (features).
# Agregar un nuevo optional feature consiste en: crear su router y
# registrarlo aquí UNA sola vez. Nunca se edita por producto.
FEATURE_REGISTRY = {
    "attendance":   attendance_router,
    "grading":      grading_router,
    "enrollment":   enrollment_router,
    "schedule":     schedule_router,
    "reports":      reports_router,
    "certificates": certificates_router,
}

# Core Services siempre presentes — son Commonality, no variabilidad.
# No se controlan con flags YAML porque todo producto académico los necesita.
CORE_SERVICES = [
    periodos_router,   # Base de la estructura temporal
    cursos_router,     # Cursos dentro de cada período
    personas_router,   # Estudiantes, docentes, etc.
]


def create_app(config_path: str | None = None) -> FastAPI:
    """Application Factory: ensambla un producto derivado de la línea.

    Args:
        config_path: ruta al product_config.yaml del producto a construir.
                      Si no se pasa, se toma de la variable de entorno
                      PRODUCT_CONFIG_PATH (necesario para Docker/CI-CD).
    """
    resolved_path = config_path or os.environ.get("PRODUCT_CONFIG_PATH")
    if not resolved_path:
        raise RuntimeError(
            "Debe indicarse 'config_path' o la variable de entorno "
            "PRODUCT_CONFIG_PATH para saber qué producto ensamblar."
        )

    flags = FeatureFlags(resolved_path)

    app = FastAPI(
        title=f"Academic Core Engine — {flags.product_name()}",
        description=(
            "Instancia derivada de la Línea de Productos de Software Académica. "
            "Los módulos activos en esta instancia dependen exclusivamente de "
            f"'{resolved_path}'."
        ),
        version="0.2.0-sprint2",
    )

    # Se guarda la referencia a los flags para que cualquier feature
    # pueda consultar parámetros de configuración en tiempo de request.
    app.state.feature_flags = flags

    # 1. Montar Core Services — siempre, en todo producto derivado
    for core_router in CORE_SERVICES:
        app.include_router(core_router)

    # 2. Montar Optional Features — solo los declarados activos en el YAML
    mounted_features = []
    for feature_name, router in FEATURE_REGISTRY.items():
        if flags.is_active(feature_name):
            app.include_router(router)
            mounted_features.append(feature_name)

    @app.get("/", tags=["core"])
    def product_info():
        """Endpoint de diagnóstico: muestra qué se ensambló y por qué."""
        return {
            "product": flags.product_name(),
            "config_file_used": resolved_path,
            "core_services": ["periodos", "cursos", "personas"],
            "active_optional_features": mounted_features,
            "available_optional_features": list(FEATURE_REGISTRY.keys()),
            "academic_settings": flags.get_setting("academic_settings", default={}),
        }

    return app
