"""
Core Asset — PathUtils (Utilidad de seguridad de rutas)

Módulo compartido por migrate.py y seeder.py para validar que las rutas
recibidas desde la línea de comandos no contengan escapes de directorio
del tipo `../` (Path Traversal — CWE-22).

REGLA DE SEGURIDAD:
  - Toda ruta recibida desde input externo (CLI, env vars) DEBE pasar
    por `safe_resolve_path` antes de usarse en operaciones de filesystem.
  - Si la ruta contiene componentes `..` que escapen del CWD, se rechaza.

Referencia OWASP: https://owasp.org/www-community/attacks/Path_Traversal
"""
from __future__ import annotations

import os
from pathlib import Path


def get_project_root() -> Path:
    """Retorna el directorio base permitido (CWD en tiempo de ejecución)."""
    return Path(os.getcwd()).resolve()


def safe_resolve_path(raw: str, allow_outside_project: bool = False) -> Path:
    """Resuelve y valida que una ruta no escape del directorio del proyecto.

    Normaliza la ruta con `Path.resolve()` (elimina `..`, symlinks, etc.)
    y comprueba que el resultado esté dentro de `_PROJECT_ROOT` o de un
    directorio padre permitido.

    Args:
        raw: Ruta en bruto recibida desde CLI o configuración externa.
        allow_outside_project: Si True, solo normaliza sin verificar el
            prefix del proyecto. Útil para rutas de BD en directorios
            del sistema operativo (no recomendado en producción).

    Returns:
        Path resuelto y validado.

    Raises:
        ValueError: Si la ruta resuelta escapa del directorio del proyecto
                    (posible ataque Path Traversal).

    Examples:
        >>> safe_resolve_path("products/colegio/colegio.db")   # OK
        PosixPath('/workspace/products/colegio/colegio.db')
        >>> safe_resolve_path("../../../etc/passwd")           # Bloqueado
        ValueError: Ruta no permitida: ...
    """
    resolved: Path = Path(raw).resolve()

    if not allow_outside_project:
        # La ruta resuelta debe comenzar dentro de _PROJECT_ROOT
        project_root = get_project_root()
        try:
            resolved.relative_to(project_root)
        except ValueError:
            raise ValueError(
                f"Ruta no permitida (posible Path Traversal): '{raw}' "
                f"se resuelve fuera del directorio del proyecto ({project_root}). "
                "Solo se permiten rutas dentro del directorio raíz del proyecto."
            )

    # Comprobación adicional: rechazar explícitamente componentes '..'
    # en la ruta cruda (antes de resolver), como medida de defensa en profundidad.
    raw_path = Path(raw)
    if any(part == ".." for part in raw_path.parts):
        raise ValueError(
            f"Ruta rechazada: '{raw}' contiene componentes '..' que podrían "
            "escapar del directorio esperado (Path Traversal)."
        )

    return resolved


def ensure_parent_dir(path: Path) -> None:
    """Crea el directorio padre de `path` si no existe.

    Función auxiliar que centraliza la creación de directorios para evitar
    duplicación entre migrate.py y seeder.py.

    Args:
        path: Ruta al archivo cuyo directorio padre se debe garantizar.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
