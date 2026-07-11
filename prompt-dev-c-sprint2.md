# PROMPT DEV C — Sprint 2 (Auth + Pruebas + Derivación de Producto)
# Copia y pega esto completo como primer mensaje en un chat nuevo

Actúa como un Arquitecto de Software experto en testing (pytest),
autenticación web, y Líneas de Productos de Software (SPLE). También
debes conocer tanto Python (FastAPI) como PHP (Laravel) a nivel básico
para poder coordinar entre los otros dos desarrolladores del equipo.

---

## Contexto del proyecto

Somos un equipo de 3 personas en un proyecto universitario. Estamos
construyendo una **Línea de Productos de Software (SPL)** para el
dominio académico. Construimos **Core Assets** reutilizables que
permiten derivar múltiples productos (Colegio Básico, Universidad
Compleja) cambiando solo un archivo de configuración YAML, sin tocar
el código del Core.

**Regla de oro que nunca se puede violar:**
`core_assets/` no puede contener el nombre de ningún producto. Toda
diferencia entre productos viene del `product_config.yaml`.

---

## Stack tecnológico

- Backend: Python 3.12 + FastAPI + SQLAlchemy 2.0 + SQLite + pytest
- Frontend: PHP 8.3 + Laravel 11
- DevOps: Docker + GitHub Actions (Sprint 3)

---

## Lo que YA está construido (Backend Sprint 2 — COMPLETADO por Dev A)

### Estructura real del proyecto

```
academic-spl/
├── run_app.py
├── requirements.txt                         ← sqlalchemy==2.0.30 ya está
├── core_assets/backend/core_engine/
│   ├── config/
│   │   ├── feature_flags.py                 ← motor de variabilidad
│   │   ├── schema_loader.py                 ← valida configs contra JSON Schema
│   │   └── config_schema.json               ← incluye database y seed_data
│   ├── domain/
│   │   ├── entities.py                      ← Pydantic: Persona, Curso, Periodo, Evaluacion
│   │   ├── validators/
│   │   │   └── cedula_validator.py          ← CA-01: Módulo 10 Registro Civil Ecuador
│   │   └── calculators/
│   │       ├── grade_scale_converter.py     ← CA-02: literal/numeric según YAML
│   │       └── attendance_calculator.py     ← CA-03: umbrales 80%/70% asistencia
│   ├── features/
│   │   ├── personas/router.py               ← Core Service (siempre activo)
│   │   ├── cursos/router.py                 ← Core Service (siempre activo)
│   │   ├── periodos/router.py               ← Core Service (siempre activo)
│   │   ├── attendance/router.py             ← Optional Feature (usa AttendanceCalculator)
│   │   ├── grading/router.py                ← Optional Feature (usa GradeScaleConverter)
│   │   └── enrollment/router.py             ← Optional Feature
│   ├── persistence/
│   │   ├── connection_resolver.py           ← BD por producto desde YAML
│   │   ├── models.py                        ← ORM: PersonaDB, CursoDB, PeriodoDB,
│   │   │                                       EvaluacionDB, AsistenciaDB, MatriculaDB
│   │   ├── migrate.py                       ← CLI idempotente de migraciones
│   │   ├── seeder.py                        ← siembra desde seed_data del YAML
│   │   ├── persona_repository.py            ← usa CedulaValidator internamente
│   │   ├── curso_repository.py
│   │   ├── periodo_repository.py
│   │   ├── grade_repository.py
│   │   ├── attendance_repository.py
│   │   └── enrollment_repository.py
│   └── main_factory.py                      ← Core Services siempre + Features por YAML
├── products/
│   ├── colegio-basico/
│   │   ├── product_config.yaml              ← attendance:true, grading:true, enrollment:true
│   │   └── colegio_basico.db               ← BD SQLite (ya migrada y sembrada)
│   └── universidad-compleja/
│       ├── product_config.yaml              ← attendance:false, grading:true, enrollment:true
│       └── universidad_compleja.db         ← BD SQLite (ya migrada)
└── docs/feature_model.md
```

### Comportamiento verificado en vivo

```bash
# GET / devuelve Core Services separados de Optional Features:
# Colegio: core_services=[periodos,cursos,personas] + active_optional_features=[attendance,grading,enrollment]
# Universidad: core_services=[periodos,cursos,personas] + active_optional_features=[grading,enrollment]

# attendance da 200 en colegio y 404 en universidad (variabilidad verificada)
# grading devuelve valor_display="Muy Bueno" en colegio y valor_display=8.5 en universidad
# PersonaRepository valida cédula ecuatoriana antes de insertar
```

### Datos en los YAMLs actuales de los productos

```yaml
# products/colegio-basico/product_config.yaml
metadata:
  product_name: "Instituto Basico Demo"
  product_type: "colegio"
features:
  attendance: true
  grading: true
  enrollment: true
academic_settings:
  evaluation_scale: "literal"
  periods_per_year: 1
database:
  path: "products/colegio-basico/colegio_basico.db"
seed_data:
  personas:
    - {id: "P-001", nombres: "Ana", apellidos: "Garcia Lopez", documento_identidad: "1001"}
    - {id: "P-002", nombres: "Luis", apellidos: "Martinez Torres", documento_identidad: "1002"}
    - {id: "P-003", nombres: "Maria", apellidos: "Rodriguez Silva", documento_identidad: "1003"}
  periodos:
    - {id: "PER-2024-A", nombre: "Ano Escolar 2024", fecha_inicio: "2024-01-15", fecha_fin: "2024-11-30"}
  cursos:
    - {id: "C-MAT", nombre: "Matematicas", periodo_id: "PER-2024-A"}
    - {id: "C-ESP", nombre: "Espanol", periodo_id: "PER-2024-A"}
```

---

## Lo que están construyendo los otros devs en este sprint

- **Dev A** (COMPLETADO): persistencia SQLAlchemy, 3 Core Services
  (personas/cursos/periodos), 3 Optional Features con datos reales,
  y 3 Core Assets de lógica de negocio (CedulaValidator, GradeScaleConverter,
  AttendanceCalculator). El backend está listo.

- **Dev B** (EN PROGRESO): `CoreEngineClient.php`, componentes Blade
  (`<x-data-table>`, `<x-entity-form>`), vistas reales de 5 módulos
  y layout con navegación condicional.

Tu trabajo (Dev C) no bloquea a nadie — puedes empezar ya con los tests
unitarios de los Core Assets sin esperar a Dev B.

---

## Tu trabajo en Sprint 2 (COR-22 a COR-25 + PROD-01 + PROD-02)

Eres **Dev C**. Tienes tres responsabilidades:
1. Construir el sistema de autenticación básico
2. Construir el arnés de pruebas reutilizable y la suite de tests
3. Derivar y validar el primer producto real: Colegio Básico

### Las tareas en orden de dependencia

**COR-22 — Autenticación básica** (hacer primero)

Auth es un **Core Service** (siempre activo, no un Optional Feature opcional).
Crea en el backend:
- `core_assets/backend/core_engine/features/auth/router.py`
  - `POST /auth/token` → recibe `{email, password}`, devuelve `{access_token, token_type}`
  - Usa `python-jose` + `passlib[bcrypt]` para JWT — agregar a `requirements.txt`
  - Verifica credenciales contra la tabla `personas` (campo `documento_identidad`
    puede usarse como contraseña simple en demo, o agrega campo `password_hash`
    al modelo `PersonaDB`)
  - Registrar en `main_factory.py` como Core Service (siempre montado)

- Middleware de FastAPI (`Depends`) para proteger endpoints:
  ```python
  # Opcional en demo — verificar token en el header Authorization: Bearer <token>
  async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict: ...
  ```

Agregar a `requirements.txt`:
```
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

**COR-23 — `UserSeeder` genérico** (después de COR-22)

El seeder genérico para personas/cursos/periodos ya existe en
`core_assets/backend/core_engine/persistence/seeder.py`. Necesitas:
- Extenderlo O crear `user_seeder.py` separado para manejar la sección `users`
  del YAML con contraseñas hasheadas:
  ```yaml
  # Agregar a product_config.yaml:
  users:
    - email: "admin@demo.local"
      password: "admin123"
      role: "admin"
  ```
- Hashear las contraseñas con `passlib` antes de insertar en BD
- Reutilizable: `python user_seeder.py products/colegio-basico/product_config.yaml`

**COR-24 — Arnés de pruebas reutilizable** (puede hacerse en paralelo con COR-22)

- Archivo: `tests_core/conftest.py`
- Instalar: `pip install pytest pytest-asyncio httpx` y agregar a `requirements.txt`

Fixtures a crear:

```python
# BD en memoria — se destruye al terminar cada test, sin archivos en disco
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", ...)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# FeatureFlags cargado desde los YAMLs reales (no mocks)
@pytest.fixture
def flags_colegio():
    return FeatureFlags("products/colegio-basico/product_config.yaml")

@pytest.fixture
def flags_universidad():
    return FeatureFlags("products/universidad-compleja/product_config.yaml")

# App completa de colegio montada para tests de integración
@pytest.fixture
def client_colegio():
    app = create_app("products/colegio-basico/product_config.yaml")
    return TestClient(app)

@pytest.fixture
def client_universidad():
    app = create_app("products/universidad-compleja/product_config.yaml")
    return TestClient(app)
```

**COR-25 — Suite de pruebas automatizadas** (después de COR-24)

Mínimo 12 tests distribuidos en 3 archivos:

**`tests_core/test_core_assets.py`** — tests unitarios de los Core Assets
(estos NO requieren BD ni servidor):
1. `test_cedula_validator_valida()` — `CedulaValidator.validate("1713175071")` → True
2. `test_cedula_validator_invalida()` — `CedulaValidator.validate("1234567890")` → False
3. `test_grade_scale_literal()` — `GradeScaleConverter.to_display(8.5, "literal")` → "Muy Bueno"
4. `test_grade_scale_numeric()` — `GradeScaleConverter.to_display(8.5, "numeric")` → 8.5
5. `test_attendance_status_aprobado()` — `AttendanceCalculator.status(90.0)` → "APROBADO"
6. `test_attendance_status_riesgo()` — `AttendanceCalculator.status(75.0)` → "EN_RIESGO"
7. `test_attendance_status_reprobado()` — `AttendanceCalculator.status(65.0)` → "REPROBADO_FALTA"

**`tests_core/test_repository.py`** — tests de persistencia:
8. `test_create_grade_persists()` — crear nota y verificar en `list_grades()`
9. `test_grade_scale_applied_in_list()` — verificar que `valor_display` aparece en GET /grading/
10. `test_attendance_estadisticas_en_response()` — GET /attendance/ incluye campo `estadisticas`
11. `test_persona_cedula_invalida_rechazada()` — POST /personas/ con cédula inválida → 422 o 409

**`tests_core/test_variability.py`** — tests de variabilidad SPLE:
12. `test_attendance_activo_en_colegio()` — `GET /attendance/` → 200 con client_colegio
13. `test_attendance_inactivo_en_universidad()` — `GET /attendance/` → 404 con client_universidad
14. `test_grading_literal_en_colegio()` — `valor_display` es string en colegio
15. `test_grading_numeric_en_universidad()` — `valor_display` es float en universidad

Comando para correr todos:
```powershell
$env:PYTHONPATH = "."
.venv\Scripts\python.exe -m pytest tests_core/ -v
```

Output esperado cuando todo pasa:
```
tests_core/test_core_assets.py::test_cedula_validator_valida PASSED
tests_core/test_core_assets.py::test_grade_scale_literal PASSED
...
15 passed in X.XXs
```

**PROD-01 — Ampliar config_schema.json para la sección `users`** (puede hacerse antes)

La sección `database` y `seed_data` ya están en el schema. Falta:
```json
"users": {
  "type": "array",
  "items": {
    "type": "object",
    "required": ["email", "password", "role"],
    "properties": {
      "email": { "type": "string" },
      "password": { "type": "string" },
      "role": { "type": "string", "enum": ["admin", "teacher", "student"] }
    }
  }
}
```

Actualizar ambos `product_config.yaml` con usuarios de prueba y verificar:
```powershell
$env:PYTHONPATH = "."
.venv\Scripts\python.exe core_assets/backend/core_engine/config/schema_loader.py
# [OK] products/colegio-basico/product_config.yaml cumple el esquema formal
# [OK] products/universidad-compleja/product_config.yaml cumple el esquema formal
```

**PROD-02 — Derivar y validar Colegio Básico end-to-end** (hacer último)

Crea `products/colegio-basico/RUN.md` con los pasos exactos:

```powershell
# 1. Instalar dependencias
.venv\Scripts\pip.exe install -r requirements.txt

# 2. Migrar BD (idempotente — safe correr múltiples veces)
$env:PYTHONPATH = "."
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/migrate.py products/colegio-basico/colegio_basico.db

# 3. Sembrar datos académicos de ejemplo
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/seeder.py products/colegio-basico/product_config.yaml

# 4. Sembrar usuarios (después de COR-23)
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/user_seeder.py products/colegio-basico/product_config.yaml

# 5. Levantar backend
$env:PRODUCT_CONFIG_PATH = "products/colegio-basico/product_config.yaml"
.venv\Scripts\python.exe -m uvicorn run_app:app --port 8001

# 6. Verificar (en otra terminal)
Invoke-RestMethod http://localhost:8001/ | ConvertTo-Json -Depth 3
Invoke-RestMethod http://localhost:8001/personas/ | ConvertTo-Json -Depth 3
```

Validaciones end-to-end a documentar en `docs/sprint2_validation.md`:
- [ ] `GET /` muestra `core_services` y `active_optional_features` separados
- [ ] `GET /personas/` devuelve las 3 personas sembradas
- [ ] `GET /grading/` devuelve `valor_display: "Sobresaliente"` para nota 9.5 (escala literal)
- [ ] `GET /attendance/` devuelve campo `estadisticas` con `porcentaje_asistencia`
- [ ] `GET /attendance/` en UNIVERSIDAD devuelve 404 (no existe el feature)
- [ ] POST `/personas/` con cédula `"9999999999"` devuelve error (cédula inválida)
- [ ] Todos los tests pasan: `.venv\Scripts\python.exe -m pytest tests_core/ -v`

---

## Coordinación con los otros devs

- Los Core Assets de Dev A son testeable unitariamente ya — empieza
  por `test_core_assets.py` (COR-25 parcial) sin esperar nada.
- Para `test_variability.py` necesitas los `TestClient` fixtures —
  Dev A ya terminó, el backend corre correctamente.
- Para `PROD-02` (validación end-to-end con frontend) necesitas que
  Dev B termine el layout. Si no está listo, valida primero solo la API.

---

## Lo que necesito de ti en este chat

1. Empieza por COR-24 (arnés de pruebas) + `test_core_assets.py` — son
   completamente independientes y demuestran los Core Assets de inmediato.
2. Luego COR-25 completo — dame el comando exacto para correr todos los tests.
3. COR-22 (auth) — dame el código completo con JWT, no pseudocódigo.
4. PROD-01 antes de PROD-02 — actualizar el schema primero.
5. Si ves inconsistencias con los principios SPLE, corrígeme — eres el
   guardián de la calidad arquitectónica del proyecto.
6. Todo el código debe respetar la regla de oro: ningún archivo en
   `core_assets/` puede mencionar "colegio" ni "universidad".
