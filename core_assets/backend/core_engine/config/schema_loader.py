"""
Core Asset — Validador formal de configuración (COR-11)

Antes de que feature_flags.py pueda usar un product_config.yaml, este
módulo verifica que el archivo cumple el contrato formal definido en
config_schema.json. Esto evita que un producto derivado tenga una
configuración inválida que solo se descubra en producción.

Este es el "contrato" entre Domain Engineering (quien define qué se
puede configurar) y Application Engineering (quien escribe cada
product_config.yaml).
"""
from __future__ import annotations

import json
import yaml
from pathlib import Path
from typing import Any, Dict

from jsonschema import validate, ValidationError, exceptions as js_exceptions

_SCHEMA_PATH = Path(__file__).parent / "config_schema.json"


def load_schema() -> Dict[str, Any]:
    with open(_SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


from core_assets.backend.core_engine.persistence.path_utils import safe_resolve_path


def load_yaml(path: str | Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_product_config(path: str | Path) -> Dict[str, Any]:
    """Valida un product_config.yaml contra el esquema formal.

    Devuelve la configuración ya cargada si es válida.
    Lanza ValueError con un mensaje claro si no lo es o si la ruta es inválida.
    """
    # --- SEGURIDAD: Validar ruta para prevenir Path Traversal (CWE-22) ---
    safe_path = safe_resolve_path(str(path))
    
    config = load_yaml(safe_path)
    schema = load_schema()
    try:
        validate(instance=config, schema=schema)
    except ValidationError as e:
        raise ValueError(
            f"Configuración inválida en '{path}': {e.message} "
            f"(ruta del error: {'/'.join(str(p) for p in e.path) or 'raíz'})"
        ) from e
    return config


if __name__ == "__main__":
    import sys

    targets = sys.argv[1:] or [
        "products/colegio-basico/product_config.yaml",
        "products/universidad-compleja/product_config.yaml",
        "products/instituto-tecnico/product_config.yaml",
    ]
    for target in targets:
        try:
            validate_product_config(target)
            print(f"[OK]    {target} cumple el esquema formal")
        except ValueError as e:
            print(f"[ERROR] {e}")
