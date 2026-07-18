"""
Tests unitarios para PathUtils — validación segura de rutas (COR-SEC-01)

Verifica que:
  1. Rutas válidas dentro del proyecto se aceptan correctamente.
  2. Rutas con componentes '..' son rechazadas (Path Traversal bloqueado).
  3. La función ensure_parent_dir crea directorios correctamente.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

# Importar el módulo bajo prueba
from core_assets.backend.core_engine.persistence.path_utils import (
    ensure_parent_dir,
    safe_resolve_path,
)


# ─── Tests de safe_resolve_path ────────────────────────────────────────────────

class TestSafeResolvePath:
    """Tests para la función de validación segura de rutas."""

    def test_ruta_relativa_valida_aceptada(self, tmp_path, monkeypatch):
        """Una ruta relativa dentro del CWD debe ser aceptada."""
        monkeypatch.chdir(tmp_path)
        # Crear un subdir para que la ruta sea resoluble
        subdir = tmp_path / "products" / "colegio"
        subdir.mkdir(parents=True)
        ruta = "products/colegio/colegio.db"
        resultado = safe_resolve_path(ruta)
        assert resultado == (tmp_path / "products" / "colegio" / "colegio.db").resolve()

    def test_ruta_absoluta_dentro_proyecto_aceptada(self, tmp_path, monkeypatch):
        """Una ruta absoluta dentro del CWD debe ser aceptada."""
        monkeypatch.chdir(tmp_path)
        ruta_abs = str(tmp_path / "data" / "test.db")
        resultado = safe_resolve_path(ruta_abs)
        assert resultado == Path(ruta_abs).resolve()

    def test_path_traversal_con_doble_punto_bloqueado(self, tmp_path, monkeypatch):
        """Una ruta con '..' que escape del CWD debe ser rechazada."""
        monkeypatch.chdir(tmp_path)
        with pytest.raises(ValueError, match="Path Traversal|\\.\\."):
            safe_resolve_path("../../../etc/passwd")

    def test_path_traversal_con_doble_punto_en_medio_bloqueado(self, tmp_path, monkeypatch):
        """'products/../../../etc/passwd' debe ser rechazada."""
        monkeypatch.chdir(tmp_path)
        with pytest.raises(ValueError, match="Path Traversal|\\.\\."):
            safe_resolve_path("products/../../../etc/passwd")

    def test_path_traversal_con_solo_doble_punto_bloqueado(self, tmp_path, monkeypatch):
        """'..' puro debe ser rechazado."""
        monkeypatch.chdir(tmp_path)
        with pytest.raises(ValueError):
            safe_resolve_path("..")

    def test_ruta_con_doble_punto_al_inicio_bloqueada(self, tmp_path, monkeypatch):
        """'../config.yaml' debe ser rechazada aunque la ruta resuelta parezca válida."""
        monkeypatch.chdir(tmp_path / "subdir" if (tmp_path / "subdir").exists() else tmp_path)
        with pytest.raises(ValueError):
            safe_resolve_path("../config.yaml")

    def test_allow_outside_project_omite_check_de_prefix(self, tmp_path, monkeypatch):
        """Con allow_outside_project=True, rutas fuera del CWD son aceptadas (pero '..' sigue bloqueado)."""
        monkeypatch.chdir(tmp_path)
        # /tmp es fuera del proyecto — debe aceptarse con la flag
        external = "/tmp/test.db"
        resultado = safe_resolve_path(external, allow_outside_project=True)
        assert resultado == Path(external).resolve()

    def test_allow_outside_project_sigue_bloqueando_doble_punto(self, tmp_path, monkeypatch):
        """Incluso con allow_outside_project=True, '..' sigue siendo rechazado."""
        monkeypatch.chdir(tmp_path)
        with pytest.raises(ValueError):
            safe_resolve_path("../escape.db", allow_outside_project=True)

    def test_ruta_simple_nombre_archivo_aceptada(self, tmp_path, monkeypatch):
        """Un nombre de archivo simple (sin separadores) debe ser aceptado."""
        monkeypatch.chdir(tmp_path)
        resultado = safe_resolve_path("my_database.db")
        assert resultado == (tmp_path / "my_database.db").resolve()

    def test_ruta_yaml_config_valida(self, tmp_path, monkeypatch):
        """Una ruta típica de product_config.yaml debe ser aceptada."""
        monkeypatch.chdir(tmp_path)
        ruta = "derived_products/colegio-norte/product_config.yaml"
        resultado = safe_resolve_path(ruta)
        assert str(resultado).endswith("product_config.yaml")

    def test_retorna_objeto_path(self, tmp_path, monkeypatch):
        """El resultado debe ser un objeto Path, no str."""
        monkeypatch.chdir(tmp_path)
        resultado = safe_resolve_path("data.db")
        assert isinstance(resultado, Path)

    def test_ruta_actual_punto_aceptada(self, tmp_path, monkeypatch):
        """'.' (directorio actual) debe ser aceptado."""
        monkeypatch.chdir(tmp_path)
        resultado = safe_resolve_path(".")
        assert resultado == tmp_path.resolve()


# ─── Tests de ensure_parent_dir ────────────────────────────────────────────────

class TestEnsureParentDir:
    """Tests para la función de creación de directorios padre."""

    def test_crea_directorio_padre_inexistente(self, tmp_path):
        """Debe crear el directorio padre si no existe."""
        target = tmp_path / "nuevo" / "profundo" / "archivo.db"
        assert not target.parent.exists()
        ensure_parent_dir(target)
        assert target.parent.exists()

    def test_no_falla_si_directorio_ya_existe(self, tmp_path):
        """Debe ser idempotente: no lanza error si el directorio ya existe."""
        target = tmp_path / "archivo.db"
        # El directorio padre (tmp_path) ya existe
        ensure_parent_dir(target)  # No debe lanzar excepción
        assert tmp_path.exists()

    def test_crea_multiples_niveles(self, tmp_path):
        """Debe crear todos los niveles necesarios (parents=True)."""
        target = tmp_path / "a" / "b" / "c" / "d.db"
        ensure_parent_dir(target)
        assert (tmp_path / "a" / "b" / "c").is_dir()

    def test_archivo_en_si_no_se_crea(self, tmp_path):
        """Solo crea el directorio padre, NO el archivo mismo."""
        target = tmp_path / "subdir" / "database.db"
        ensure_parent_dir(target)
        assert target.parent.exists()
        assert not target.exists()  # El archivo no debe existir
