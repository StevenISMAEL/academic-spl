"""
Tests de integración con API real (COR-25 parte 3)

Estos tests verifican que los Core Assets se integren correctamente
a través de los endpoints de FastAPI.
"""


# Validación de cédula a través de la API
def test_persona_cedula_invalida_rechazada(client_colegio):
    r = client_colegio.post("/personas/", json={
        "nombres": "Test",
        "apellidos": "Test",
        "documento_identidad": "1234567890"
    })
    # El endpoint debería rechazar cédulas inválidas (409 o 422)
    assert r.status_code in [409, 422]


# Test de diagnóstico verifica que los endpoints existen
def test_diagnostico_colegio_muestra_configuracion(client_colegio):
    r = client_colegio.get("/")
    data = r.json()
    assert "academic_settings" in data
    assert "evaluation_scale" in data["academic_settings"]
    assert "passing_grade" in data["academic_settings"]
