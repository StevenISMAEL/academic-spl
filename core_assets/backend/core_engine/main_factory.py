"""
Core Asset — Application Factory genérico (COR-03)

Esta es la pieza central de Application Engineering automatizado:
construye una instancia de FastAPI montando ÚNICAMENTE los módulos
(features) que la configuración del producto declara como activos.

Este archivo NUNCA debe importar nada de products/. La única forma en
que "sabe" qué producto está construyendo es a través del path de
configuración que recibe como parámetro.
"""
from __future__ import annotations

import os
from fastapi import FastAPI

from core_assets.backend.core_engine.config.feature_flags import FeatureFlags
from core_assets.backend.core_engine.features.attendance.router import (
    router as attendance_router,
)
from core_assets.backend.core_engine.features.grading.router import (
    router as grading_router,
)
from core_assets.backend.core_engine.features.enrollment.router import (
    router as enrollment_router,
)

# Catálogo de Core Assets (features) disponibles para ensamblar.
# Agregar un nuevo feature al Core consiste en: crear su router y
# registrarlo aquí UNA sola vez. Nunca se edita por producto.
FEATURE_REGISTRY = {
    "attendance": attendance_router,
    "grading": grading_router,
    "enrollment": enrollment_router,
}


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
        version="0.1.0-sprint1",
    )

    # Se guarda la referencia a los flags para que cualquier feature
    # pueda consultar parámetros de configuración en tiempo de request
    # (ver features/grading/router.py para un ejemplo).
    app.state.feature_flags = flags

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
            "active_features": mounted_features,
            "available_features_in_core": list(FEATURE_REGISTRY.keys()),
            "academic_settings": flags.get_setting("academic_settings", default={}),
        }

    return app
