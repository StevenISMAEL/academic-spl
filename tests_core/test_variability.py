"""
Tests de variabilidad SPLE (COR-25 parte 2)

Estos tests verifican que el mismo Core Asset se comporta diferente según
la configuración del producto, sin tocar el código del Core.
"""
import pytest


# Tests de variabilidad booleana (Optional Features ON/OFF)
def test_attendance_activo_colegio(flags_colegio):
    assert flags_colegio.is_active("attendance") is True


def test_attendance_inactivo_universidad(flags_universidad):
    assert flags_universidad.is_active("attendance") is False


def test_attendance_inactivo_tecnico(flags_tecnico):
    assert flags_tecnico.is_active("attendance") is False


def test_schedule_inactivo_colegio(flags_colegio):
    assert flags_colegio.is_active("schedule") is False


def test_schedule_activo_universidad(flags_universidad):
    assert flags_universidad.is_active("schedule") is True


def test_reports_activo_universidad(flags_universidad):
    assert flags_universidad.is_active("reports") is True


def test_certificates_inactivo_colegio(flags_colegio):
    assert flags_colegio.is_active("certificates") is False


# Tests de variabilidad paramétrica (CA-02: evaluation_scale)
def test_grading_scale_literal_en_colegio(flags_colegio):
    assert flags_colegio.get_setting("academic_settings", "evaluation_scale") == "literal"


def test_grading_scale_numeric_en_universidad(flags_universidad):
    assert flags_universidad.get_setting("academic_settings", "evaluation_scale") == "numeric"


# Tests de variabilidad paramétrica (CA-04: passing_grade)
def test_passing_grade_colegio(flags_colegio):
    assert flags_colegio.get_setting("academic_settings", "passing_grade") == 7.0


def test_passing_grade_universidad(flags_universidad):
    assert flags_universidad.get_setting("academic_settings", "passing_grade") == 6.0


# Test de diagnóstico: core_services y active_optional_features correctos
def test_diagnostico_colegio(client_colegio):
    r = client_colegio.get("/")
    data = r.json()
    assert "attendance" in data["active_optional_features"]
    assert "personas" in data["core_services"]


def test_diagnostico_universidad_sin_attendance(client_universidad):
    r = client_universidad.get("/")
    data = r.json()
    assert "attendance" not in data["active_optional_features"]
    assert "schedule" in data["active_optional_features"]
