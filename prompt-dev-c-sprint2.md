# PROMPT DEV C — Sprint 2 (Auth + Pruebas + Validación de 3 Productos)
# Copia y pega esto completo como primer mensaje en un chat nuevo

Actúa como un Arquitecto de Software experto en testing (pytest),
autenticación JWT, y Líneas de Productos de Software (SPLE). También
debes conocer Python (FastAPI) y cómo escribir tests que verifiquen
que el mismo Core Asset se comporta diferente según la configuración,
sin tocar el código del Core.

---

## Contexto del proyecto

Somos un equipo de 3 personas en un proyecto universitario. Estamos
construyendo una **Línea de Productos de Software (SPL)** para el
dominio académico. Construimos **Core Assets** reutilizables que
permiten derivar múltiples productos cambiando solo un YAML,
sin tocar el código del Core.

**Regla de oro que nunca se puede violar:**
`core_assets/` no puede contener el nombre de ningún producto. Toda
diferencia entre productos viene del `product_config.yaml`.

---

## Stack tecnológico

- Backend: Python 3.12 + FastAPI + SQLAlchemy 2.0 + SQLite + pytest
- Frontend: PHP + Laravel (Dev B lo maneja)
- DevOps: Docker + GitHub Actions (Sprint 3)

---

## Estructura real del proyecto (verificada y funcionando)

```
academic-spl/
├── run_app.py
├── requirements.txt
├── core_assets/backend/core_engine/
│   ├── config/
│   │   ├── feature_flags.py                 ← Motor de variabilidad
│   │   ├── schema_loader.py                 ← Valida configs contra JSON Schema
│   │   └── config_schema.json               ← Contrato formal del YAML
│   ├── domain/
│   │   ├── entities.py                      ← Pydantic: Persona, Curso, Periodo, Evaluacion
│   │   ├── validators/
│   │   │   └── cedula_validator.py          ← CA-01: Módulo 10 Registro Civil Ecuador
│   │   └── calculators/
│   │       ├── grade_scale_converter.py     ← CA-02: literal/numeric según YAML
│   │       ├── attendance_calculator.py     ← CA-03: umbrales desde attendance_min_percentage del YAML
│   │       ├── grade_passing_checker.py     ← CA-04: passing_grade del YAML
│   │       └── enrollment_limit_checker.py  ← CA-05: max_enrollments_per_period del YAML
│   ├── features/
│   │   ├── personas/router.py               ← Core Service (CA-01)
│   │   ├── cursos/router.py                 ← Core Service
│   │   ├── periodos/router.py               ← Core Service
│   │   ├── attendance/router.py             ← Optional Feature (CA-03)
│   │   ├── grading/router.py                ← Optional Feature (CA-02 + CA-04)
│   │   ├── enrollment/router.py             ← Optional Feature (CA-05)
│   │   ├── schedule/router.py               ← Optional Feature (stub)
│   │   ├── reports/router.py                ← Optional Feature (stub)
│   │   └── certificates/router.py           ← Optional Feature (stub)
│   ├── persistence/
│   │   ├── connection_resolver.py
│   │   ├── models.py                        ← 6 modelos ORM
│   │   ├── migrate.py                       ← CLI idempotente
│   │   ├── seeder.py                        ← siembra desde YAML
│   │   ├── persona_repository.py            ← usa CA-01
│   │   ├── curso_repository.py
│   │   ├── periodo_repository.py
│   │   ├── grade_repository.py
│   │   ├── attendance_repository.py
│   │   └── enrollment_repository.py        ← tiene count_active_enrollments()
│   └── main_factory.py                      ← FEATURE_REGISTRY con 6 features
├── products/
│   ├── colegio-basico/product_config.yaml
│   ├── universidad-compleja/product_config.yaml
│   └── instituto-tecnico/product_config.yaml
└── tests_core/   ← TU TRABAJO (crear esta carpeta)
```

---

## Los 5 Core Assets que debes testear

### CA-01 — CedulaValidator
```python
from core_assets.backend.core_engine.domain.validators.cedula_validator import CedulaValidator
CedulaValidator.validate("1713175071")      # True
CedulaValidator.validate("1234567890")      # False
CedulaValidator.validate_or_raise("9999")   # ValueError
```

### CA-02 — GradeScaleConverter
```python
from core_assets.backend.core_engine.domain.calculators.grade_scale_converter import GradeScaleConverter
GradeScaleConverter.to_display(9.5, "literal")   # "Sobresaliente"
GradeScaleConverter.to_display(8.5, "literal")   # "Muy Bueno"
GradeScaleConverter.to_display(6.5, "literal")   # "Bueno"
GradeScaleConverter.to_display(4.0, "literal")   # "Regular"
GradeScaleConverter.to_display(2.0, "literal")   # "Insuficiente"
GradeScaleConverter.to_display(8.5, "numeric")   # 8.5
```

### CA-03 — AttendanceCalculator (umbrales del YAML, ya no hardcodeados)
```python
from core_assets.backend.core_engine.domain.calculators.attendance_calculator import AttendanceCalculator
# Estado varía según threshold_approved (del YAML del producto):
AttendanceCalculator.status(77.0, threshold_approved=80.0)  # "EN_RIESGO" (colegio)
AttendanceCalculator.status(77.0, threshold_approved=75.0)  # "APROBADO" (universidad)
AttendanceCalculator.status(72.0, threshold_approved=70.0)  # "APROBADO" (técnico)
# Porcentaje:
AttendanceCalculator.percentage(18, 20)  # 90.0
# Resumen incluye los umbrales aplicados:
result = AttendanceCalculator.summarize(records, threshold_approved=80.0)
# result["umbral_aprobado"] → 80.0
# result["umbral_riesgo"]   → 70.0
```

### CA-04 — GradePassingChecker (passing_grade del YAML)
```python
from core_assets.backend.core_engine.domain.calculators.grade_passing_checker import GradePassingChecker
GradePassingChecker.passes(6.5, passing_grade=6.0)     # True  (Universidad)
GradePassingChecker.passes(6.5, passing_grade=7.0)     # False (Colegio/Técnico)
GradePassingChecker.status(6.5, passing_grade=6.0)     # "APROBADO"
GradePassingChecker.status(6.5, passing_grade=7.0)     # "REPROBADO"
grades = [{"valor": 6.5}, {"valor": 8.0}]
GradePassingChecker.annotate_grades_list(grades, passing_grade=7.0)
# → [{"valor": 6.5, "aprueba": False, "estado_aprobacion": "REPROBADO"},
#    {"valor": 8.0, "aprueba": True,  "estado_aprobacion": "APROBADO"}]
```

### CA-05 — EnrollmentLimitChecker (max_enrollments_per_period del YAML)
```python
from core_assets.backend.core_engine.domain.calculators.enrollment_limit_checker import EnrollmentLimitChecker
EnrollmentLimitChecker.can_enroll(5, max_enrollments=6)  # True  (Universidad)
EnrollmentLimitChecker.can_enroll(5, max_enrollments=5)  # False (Técnico)
EnrollmentLimitChecker.can_enroll(5, max_enrollments=8)  # True  (Colegio)
EnrollmentLimitChecker.slots_remaining(3, max_enrollments=8)  # 5
# Lanza ValueError con mensaje descriptivo:
EnrollmentLimitChecker.validate_or_raise(5, 5, "P-001")  # ValueError
```

---

## Configuración de los 3 productos (lo que diferencia el comportamiento)

| Setting | Colegio (8001) | Universidad (8002) | Técnico (8003) |
|---|---|---|---|
| `evaluation_scale` | `literal` | `numeric` | `numeric` |
| `passing_grade` | 7.0 | 6.0 | 7.0 |
| `attendance_min_percentage` | 80.0 | 75.0 | 70.0 |
| `max_enrollments_per_period` | 8 | 6 | 5 |
| `attendance` feature | ✅ | ❌ | ❌ |
| `grading` feature | ✅ | ✅ | ✅ |
| `enrollment` feature | ✅ | ✅ | ✅ |
| `schedule` feature | ❌ | ✅ | ✅ |
| `reports` feature | ❌ | ✅ | ✅ |
| `certificates` feature | ❌ | ✅ | ❌ |

---

## Tu trabajo en Sprint 2 (COR-22 a COR-25 + PROD-01 + PROD-02)

Eres **Dev C**. Tienes tres responsabilidades:
1. Autenticación básica JWT
2. Arnés de pruebas y suite de tests completa (5 Core Assets)
3. Derivar y validar los 3 productos end-to-end

### COR-22 — Autenticación básica JWT (hacer primero)

Crea en el backend:

**Archivo:** `core_assets/backend/core_engine/features/auth/router.py`

Endpoints:
```
POST /auth/token   → {"email": "...", "password": "..."} → {"access_token": "...", "token_type": "bearer"}
GET  /auth/me      → devuelve datos del usuario autenticado (requiere token)
```

Implementación:
- Usa `python-jose[cryptography]` + `passlib[bcrypt]` para JWT
- Verifica credenciales contra la tabla `PersonaDB` (usar `documento_identidad` como contraseña demo)
- Registrar en `main_factory.py` como **Core Service** (siempre montado, como personas/cursos)

Agregar a `requirements.txt`:
```
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

Modelo Pydantic para el token:
```python
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    persona_id: str | None = None
```

---

### COR-23 — Ampliar `schema_loader.py` para validar `instituto-tecnico`

El `schema_loader.py` actual solo valida colegio y universidad. Ampliar
para que valide los 3 productos:

```powershell
$env:PYTHONPATH = "."
.venv\Scripts\python.exe core_assets/backend/core_engine/config/schema_loader.py
# Resultado esperado:
# [OK] products/colegio-basico/product_config.yaml
# [OK] products/universidad-compleja/product_config.yaml
# [OK] products/instituto-tecnico/product_config.yaml
```

---

### COR-24 — Arnés de pruebas reutilizable

**Archivo:** `tests_core/conftest.py`

Instalar:
```powershell
$env:PYTHONPATH = "."
.venv\Scripts\pip.exe install pytest pytest-asyncio httpx
```

Fixtures a crear:

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from core_assets.backend.core_engine.persistence.models import Base
from core_assets.backend.core_engine.config.feature_flags import FeatureFlags
from core_assets.backend.core_engine.main_factory import create_app

# BD en memoria — se destruye al terminar cada test
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# FeatureFlags cargados desde los YAMLs reales
@pytest.fixture
def flags_colegio():
    return FeatureFlags("products/colegio-basico/product_config.yaml")

@pytest.fixture
def flags_universidad():
    return FeatureFlags("products/universidad-compleja/product_config.yaml")

@pytest.fixture
def flags_tecnico():
    return FeatureFlags("products/instituto-tecnico/product_config.yaml")

# Clientes HTTP para tests de integración
@pytest.fixture
def client_colegio():
    app = create_app("products/colegio-basico/product_config.yaml")
    return TestClient(app)

@pytest.fixture
def client_universidad():
    app = create_app("products/universidad-compleja/product_config.yaml")
    return TestClient(app)

@pytest.fixture
def client_tecnico():
    app = create_app("products/instituto-tecnico/product_config.yaml")
    return TestClient(app)
```

---

### COR-25 — Suite de tests automatizados (después de COR-24)

Mínimo 20 tests distribuidos en 3 archivos:

#### **`tests_core/test_core_assets.py`** — Tests unitarios (sin BD, sin servidor)

```python
# CA-01: CedulaValidator
def test_cedula_valida(): assert CedulaValidator.validate("1713175071") is True
def test_cedula_invalida(): assert CedulaValidator.validate("1234567890") is False
def test_cedula_longitud_incorrecta(): assert CedulaValidator.validate("123") is False
def test_cedula_validate_or_raise_invalida():
    with pytest.raises(ValueError): CedulaValidator.validate_or_raise("1234567890")

# CA-02: GradeScaleConverter
def test_grade_literal_sobresaliente(): assert GradeScaleConverter.to_display(9.5, "literal") == "Sobresaliente"
def test_grade_literal_muy_bueno(): assert GradeScaleConverter.to_display(8.5, "literal") == "Muy Bueno"
def test_grade_literal_regular(): assert GradeScaleConverter.to_display(4.0, "literal") == "Regular"
def test_grade_numeric(): assert GradeScaleConverter.to_display(8.5, "numeric") == 8.5

# CA-03: AttendanceCalculator (ahora con umbrales configurables)
def test_attendance_percentage(): assert AttendanceCalculator.percentage(18, 20) == 90.0
def test_attendance_approved_colegio(): assert AttendanceCalculator.status(85.0, threshold_approved=80.0) == "APROBADO"
def test_attendance_en_riesgo_colegio(): assert AttendanceCalculator.status(77.0, threshold_approved=80.0) == "EN_RIESGO"
def test_attendance_approved_universidad(): assert AttendanceCalculator.status(77.0, threshold_approved=75.0) == "APROBADO"
def test_attendance_umbral_en_resumen():
    records = [{"presente": True}] * 8 + [{"presente": False}] * 2
    result = AttendanceCalculator.summarize(records, threshold_approved=80.0)
    assert result["umbral_aprobado"] == 80.0
    assert result["estado"] == "APROBADO"

# CA-04: GradePassingChecker
def test_grade_passing_universidad(): assert GradePassingChecker.passes(6.5, passing_grade=6.0) is True
def test_grade_failing_colegio(): assert GradePassingChecker.passes(6.5, passing_grade=7.0) is False
def test_grade_status(): assert GradePassingChecker.status(9.0, passing_grade=7.0) == "APROBADO"
def test_grade_annotate_list():
    result = GradePassingChecker.annotate_grades_list([{"valor": 6.5}], passing_grade=7.0)
    assert result[0]["aprueba"] is False
    assert result[0]["estado_aprobacion"] == "REPROBADO"

# CA-05: EnrollmentLimitChecker
def test_enrollment_can_enroll(): assert EnrollmentLimitChecker.can_enroll(5, max_enrollments=6) is True
def test_enrollment_at_limit(): assert EnrollmentLimitChecker.can_enroll(5, max_enrollments=5) is False
def test_enrollment_slots_remaining(): assert EnrollmentLimitChecker.slots_remaining(3, max_enrollments=8) == 5
def test_enrollment_validate_or_raise():
    with pytest.raises(ValueError): EnrollmentLimitChecker.validate_or_raise(5, 5, "P-001")
```

#### **`tests_core/test_variability.py`** — Tests de variabilidad SPLE

```python
# Tests de variabilidad booleana (Optional Features ON/OFF)
def test_attendance_activo_colegio(client_colegio):
    r = client_colegio.get("/attendance/")
    assert r.status_code == 200

def test_attendance_inactivo_universidad(client_universidad):
    r = client_universidad.get("/attendance/")
    assert r.status_code == 404

def test_attendance_inactivo_tecnico(client_tecnico):
    r = client_tecnico.get("/attendance/")
    assert r.status_code == 404

def test_schedule_inactivo_colegio(client_colegio):
    r = client_colegio.get("/schedule/")
    assert r.status_code == 404

def test_schedule_activo_universidad(client_universidad):
    r = client_universidad.get("/schedule/")
    assert r.status_code == 200

def test_reports_activo_universidad(client_universidad):
    r = client_universidad.get("/reports/")
    assert r.status_code == 200

def test_certificates_inactivo_colegio(client_colegio):
    r = client_colegio.get("/certificates/")
    assert r.status_code == 404

# Tests de variabilidad paramétrica (CA-02: evaluation_scale)
def test_grading_scale_literal_en_colegio(client_colegio):
    r = client_colegio.get("/grading/")
    assert r.json()["evaluation_scale_used"] == "literal"

def test_grading_scale_numeric_en_universidad(client_universidad):
    r = client_universidad.get("/grading/")
    assert r.json()["evaluation_scale_used"] == "numeric"

# Tests de variabilidad paramétrica (CA-04: passing_grade)
def test_passing_grade_colegio(client_colegio):
    r = client_colegio.get("/grading/")
    assert r.json()["passing_grade_used"] == 7.0

def test_passing_grade_universidad(client_universidad):
    r = client_universidad.get("/grading/")
    assert r.json()["passing_grade_used"] == 6.0

# Test que core services existen en los 3 productos
def test_personas_core_service_colegio(client_colegio):
    assert client_colegio.get("/personas/").status_code == 200

def test_personas_core_service_universidad(client_universidad):
    assert client_universidad.get("/personas/").status_code == 200

def test_personas_core_service_tecnico(client_tecnico):
    assert client_tecnico.get("/personas/").status_code == 200

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
```

#### **`tests_core/test_api_integration.py`** — Tests de integración con API real

```python
# Validación de cédula a través de la API
def test_persona_cedula_invalida_rechazada(client_colegio):
    r = client_colegio.post("/personas/", json={
        "nombres": "Test", "apellidos": "Test", "documento_identidad": "1234567890"
    })
    assert r.status_code == 409

# Notas devuelven campos de CA-02 y CA-04
def test_grading_response_tiene_campos_ca02_ca04(client_colegio):
    r = client_colegio.get("/grading/")
    assert "evaluation_scale_used" in r.json()
    assert "passing_grade_used" in r.json()

# Attendance devuelve estadísticas de CA-03 con umbral
def test_attendance_estadisticas_tienen_umbral(client_colegio):
    r = client_colegio.get("/attendance/")
    stats = r.json()["estadisticas"]
    assert "umbral_aprobado" in stats
    assert stats["umbral_aprobado"] == 80.0  # YAML colegio

# Enrollment incluye campo total
def test_enrollment_response_tiene_total(client_colegio):
    r = client_colegio.get("/enrollment/")
    assert "total" in r.json()
```

**Comando para correr todos:**
```powershell
$env:PYTHONPATH = "."
.venv\Scripts\python.exe -m pytest tests_core/ -v --tb=short

# Solo unitarios (sin servidor):
.venv\Scripts\python.exe -m pytest tests_core/test_core_assets.py -v

# Solo variabilidad:
.venv\Scripts\python.exe -m pytest tests_core/test_variability.py -v
```

**Output esperado cuando todo pasa:**
```
tests_core/test_core_assets.py::test_cedula_valida PASSED
tests_core/test_core_assets.py::test_cedula_invalida PASSED
... (20+ tests)
20 passed in X.XXs
```

---

### PROD-01 — Migrar y sembrar los 3 productos

```powershell
$env:PYTHONPATH = "."

# Migrar los 3 productos
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/migrate.py products/colegio-basico/colegio_basico.db
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/migrate.py products/universidad-compleja/universidad_compleja.db
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/migrate.py products/instituto-tecnico/instituto_tecnico.db

# Sembrar datos iniciales
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/seeder.py products/colegio-basico/product_config.yaml
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/seeder.py products/instituto-tecnico/product_config.yaml
# Universidad no tiene seed_data en el YAML — es intencional
```

---

### PROD-02 — Validar los 3 productos end-to-end

Levanta los 3 servidores y crea `docs/sprint2_validation.md` con resultados de:

**Variabilidad booleana (ver en Swagger UI):**
- [ ] Colegio (8001): `/attendance` existe, `/schedule` NO existe
- [ ] Universidad (8002): `/attendance` NO existe, `/schedule` SÍ existe, `/reports` SÍ existe
- [ ] Técnico (8003): `/attendance` NO existe, `/schedule` SÍ existe, `/certificates` NO existe

**Variabilidad paramétrica CA-02 (mismo valor, distinto display):**
- [ ] Colegio: `GET /grading/` → `"valor_display": "Muy Bueno"` para nota 8.5
- [ ] Universidad: `GET /grading/` → `"valor_display": 8.5` para nota 8.5

**Variabilidad paramétrica CA-04 (mismo valor, distinto estado):**
- [ ] Colegio: nota 6.5 → `"aprueba": false` (passing_grade=7.0)
- [ ] Universidad: nota 6.5 → `"aprueba": true` (passing_grade=6.0)

**Variabilidad paramétrica CA-03 (mismo porcentaje, distinto estado):**
- [ ] Colegio: 77% asistencia → `"estado": "EN_RIESGO"` (umbral 80%)
- [ ] Universidad: 77% asistencia → `"estado": "APROBADO"` (umbral 75%)

**Validación CA-01 (cédula ecuatoriana):**
- [ ] `POST /personas/` con cédula inválida → HTTP 409

**Validación CA-05 (límite de matrículas):**
- [ ] Técnico: inscribir 6 materias → la 6ta da HTTP 409 (max=5)
- [ ] Colegio: inscribir 6 materias → funciona (max=8)

**Tests automatizados:**
- [ ] `pytest tests_core/ -v` → todos los tests pasan

---

## Coordinación con los otros devs

- **Dev A COMPLETADO**: backend 100% funcional con 5 Core Assets, 6 Optional Features y 3 productos.
- **Dev B EN PROGRESO**: frontend Laravel. Puedes empezar con `test_core_assets.py` sin esperar a Dev B.
- Para `test_variability.py` y `test_api_integration.py` solo necesitas el backend (ya está listo).
- `PROD-02` requiere los 3 servidores corriendo simultáneamente.

---

## Lo que necesito de ti en este chat

1. Empieza por **COR-24** (conftest.py) + **`test_core_assets.py`** — son completamente independientes.
2. Luego **COR-25** completo — dame el comando exacto para correr todos los tests.
3. **COR-22** (auth JWT) — código completo con JWT, no pseudocódigo.
4. **PROD-01** antes de **PROD-02** — migrar y sembrar primero.
5. Si ves código que viola la regla de oro (Core Asset con nombre de producto), corrígeme — eres el guardián de la calidad arquitectónica.
6. Todos los archivos en `core_assets/` deben ser agnósticos al producto.
