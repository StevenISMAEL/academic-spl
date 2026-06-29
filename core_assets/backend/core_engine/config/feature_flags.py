"""
Core Asset — Motor de Resolución de Variabilidad (COR-02)

Este módulo es el corazón del mecanismo de variabilidad de la línea de
productos. Lee una configuración externa (YAML) y expone qué Features
y parámetros están activos para la instancia/producto que se está
ensamblando en este momento.

REGLA DE ORO: este archivo NO debe conocer el nombre de ningún producto
("colegio", "universidad", etc). Si en algún momento sientes la tentación
de escribir `if product == "colegio"` aquí, esa decisión pertenece a un
archivo de configuración en products/, no a este Core Asset.
"""
from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional

from core_assets.backend.core_engine.config.schema_loader import validate_product_config


class FeatureFlags:
    """Resuelve la configuración de variabilidad de un producto derivado."""

    def __init__(self, config_path: str | Path):
        self._config_path = Path(config_path)
        # COR-11: validación formal contra el esquema antes de aceptar la config.
        # Si esto falla, el producto ni siquiera intenta ensamblarse.
        self._config: Dict[str, Any] = validate_product_config(self._config_path)
        self._validate(self._config)

    @staticmethod
    def _load(path: Path) -> Dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo de configuración del producto: {path}"
            )
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data or {}

    @staticmethod
    def _validate(config: Dict[str, Any]) -> None:
        if "features" not in config:
            raise ValueError(
                "Configuración inválida: falta la sección obligatoria 'features'. "
                "Todo product_config.yaml debe declarar qué Core Assets activa."
            )
        if "metadata" not in config or "product_name" not in config.get("metadata", {}):
            raise ValueError(
                "Configuración inválida: falta 'metadata.product_name'."
            )

    def is_active(self, feature_name: str) -> bool:
        """Indica si un Feature (Core Asset activable) está encendido."""
        return bool(self._config.get("features", {}).get(feature_name, False))

    def get_active_features(self) -> List[str]:
        return [
            name for name, active in self._config.get("features", {}).items() if active
        ]

    def get_setting(self, *keys: str, default: Optional[Any] = None) -> Any:
        """Acceso genérico a cualquier parámetro de configuración anidado.

        Ejemplo: get_setting("academic_settings", "evaluation_scale")
        """
        node: Any = self._config
        for key in keys:
            if not isinstance(node, dict) or key not in node:
                return default
            node = node[key]
        return node

    def product_name(self) -> str:
        return self.get_setting("metadata", "product_name", default="unknown-product")

    def raw(self) -> Dict[str, Any]:
        """Devuelve la configuración completa (uso en debugging/inspección)."""
        return self._config
