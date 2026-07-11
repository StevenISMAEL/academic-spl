# PROMPT DEV A — Sprint 2 (Backend + Persistencia) — ACTUALIZADO
# Estado: COMPLETADO. Este documento refleja lo que ya fue implementado.
# Úsalo como referencia o para continuar en un chat nuevo si necesitas ajustes.

Actúa como un Arquitecto de Software experto en Python (FastAPI),
patrones de diseño y Líneas de Productos de Software (SPLE).

---

## Contexto del proyecto

Somos un equipo de 3 personas en un proyecto universitario. Estamos
construyendo una **Línea de Productos de Software (SPL)** para el
dominio académico. Construimos **Core Assets** reutilizables que
permiten derivar múltiples productos (Colegio Básico, Universidad
Compleja) cambiando solo un archivo de configuración YAML, sin tocar
el código del Core.

**Regla de oro que nunca se puede violar:**
`core_assets/` no puede contener el nombre de ningún producto, ni
lógica condicional sobre productos (`if product == "colegio"`). Toda
diferencia de comportamiento entre productos viene del `product_config.yaml`.

---

## Stack tecnológico

- Backend: Python 3.12 + FastAPI + SQLAlchemy 2.0 + SQLite
- Frontend: PHP + Laravel (Dev B lo maneja)
- DevOps: Docker + GitHub Actions (Sprint 3)

---

## Lo que Dev A YA construyó y está verificado (Sprint 2 COMPLETADO)

### Estructura completa actual del proyecto

```
academic-spl/
├── run_app.py
├── requirements.txt                         ← sqlalchemy==2.0.30 agregado
├── core_assets/backend/core_engine/
│   ├── config/
│   │   ├── feature_flags.py                 ← COR-02: motor de variabilidad
│   │   ├── schema_loader.py                 ← COR-11: valida configs
│   │   └── config_schema.json               ← incluye secciones database y seed_data
│   ├── domain/
│   │   ├── entities.py                      ← Pydantic: Persona, Curso, Periodo, Evaluacion
│   │   ├── validators/
│   │   │   └── cedula_validator.py          ← CA-01: Algoritmo Módulo 10 Registro Civil Ecuador
│   │   └── calculators/
│   │       ├── grade_scale_converter.py     ← CA-02: convierte notas a escala literal/numeric
│   │       └── attendance_calculator.py     ← CA-03: estadísticas de asistencia (umbrales 80/70%)
│   ├── features/
│   │   ├── personas/router.py               ← Core Service SIEMPRE activo (COR-17)
│   │   ├── cursos/router.py                 ← Core Service SIEMPRE activo (COR-18)
│   │   ├── periodos/router.py               ← Core Service SIEMPRE activo (COR-19)
│   │   ├── attendance/router.py             ← Optional Feature, usa AttendanceCalculator
│   │   ├── grading/router.py                ← Optional Feature, usa GradeScaleConverter
│   │   └── enrollment/router.py             ← Optional Feature
│   ├── persistence/
│   │   ├── connection_resolver.py           ← COR-12: BD por producto vía YAML
│   │   ├── models.py                        ← COR-13: ORM SQLAlchemy (6 tablas)
│   │   ├── migrate.py                       ← COR-13: CLI idempotente de migraciones
│   │   ├── seeder.py                        ← COR-16: siembra desde seed_data del YAML
│   │   ├── persona_repository.py            ← COR-17: usa CedulaValidator
│   │   ├── curso_repository.py              ← COR-18
│   │   ├── periodo_repository.py            ← COR-19
│   │   ├── grade_repository.py              ← COR-14
│   │   ├── attendance_repository.py         ← COR-14
│   │   └── enrollment_repository.py        ← COR-14
│   └── main_factory.py                      ← COR-20: Core Services siempre + Features por YAML
├── products/
│   ├── colegio-basico/
│   │   ├── product_config.yaml              ← incluye database.path y seed_data
│   │   └── colegio_basico.db               ← BD SQLite generada (no versionar)
│   └── universidad-compleja/
│       ├── product_config.yaml              ← incluye database.path
│       └── universidad_compleja.db         ← BD SQLite generada (no versionar)
└── docs/feature_model.md
```

### Arquitectura: Core Services vs Optional Features

Esta es la distinción clave que faltaba en el Sprint 1:

**Core Services** — montados SIEMPRE en `main_factory.py`, sin flag:
```python
CORE_SERVICES = [periodos_router, cursos_router, personas_router]
for router in CORE_SERVICES:
    app.include_router(router)
```

**Optional Features** — montados solo si el YAML lo declara:
```python
FEATURE_REGISTRY = {"attendance": ..., "grading": ..., "enrollment": ...}
for name, router in FEATURE_REGISTRY.items():
    if flags.is_active(name):
        app.include_router(router)
```

### Core Assets de lógica de negocio (lo que faltaba en Sprint 1)

**CA-01 — CedulaValidator**
Algoritmo Módulo 10 del Registro Civil Ecuador. Se usa en
`PersonaRepository.create_persona()` — ningún producto puede crear
una persona con cédula inválida, independientemente de quién llame al repositorio.
```python
CedulaValidator.validate("1713175071")     # → True
CedulaValidator.validate("1234567890")     # → False
CedulaValidator.validate_or_raise("999")   # → ValueError con mensaje claro
```

**CA-02 — GradeScaleConverter**
Convierte notas numéricas a escala de presentación según el YAML del producto.
El MISMO router de grading devuelve `"Muy Bueno"` para el Colegio y `8.5`
para la Universidad — sin `if producto == "colegio"`.
```python
GradeScaleConverter.to_display(8.5, "literal")   # → "Muy Bueno"
GradeScaleConverter.to_display(8.5, "numeric")   # → 8.5
GradeScaleConverter.to_display(9.5, "literal")   # → "Sobresaliente"
GradeScaleConverter.to_display(4.0, "literal")   # → "Regular"
```

**CA-03 — AttendanceCalculator**
Reglas de negocio del dominio académico ecuatoriano. Se usa en
`attendance/router.py` — el `GET /attendance/` devuelve estadísticas reales.
```python
AttendanceCalculator.percentage(18, 20)    # → 90.0
AttendanceCalculator.status(90.0)          # → "APROBADO"
AttendanceCalculator.status(75.0)          # → "EN_RIESGO"
AttendanceCalculator.status(65.0)          # → "REPROBADO_FALTA"
AttendanceCalculator.summarize(records)    # → {total, presentes, %, estado}
AttendanceCalculator.summarize_by_persona(records) # → lista ordenada por riesgo
```

### Endpoints disponibles para Dev B y Dev C

| Método | Endpoint | Disponible | Novedades |
|---|---|---|---|
| GET | `/` | Siempre | Muestra `core_services` + `active_optional_features` separados |
| GET/POST | `/periodos/` | Siempre | Core Service |
| GET/PUT/DELETE | `/periodos/{id}` | Siempre | |
| GET/POST | `/cursos/` | Siempre | Filtro ?periodo_id= en GET |
| GET/PUT/DELETE | `/cursos/{id}` | Siempre | |
| GET/POST | `/personas/` | Siempre | Valida cédula ecuatoriana |
| GET/PUT/DELETE | `/personas/{id}` | Siempre | |
| GET | `/personas/por-documento/{doc}` | Siempre | |
| GET/POST/DELETE | `/grading/` | Si grading:true | Devuelve `valor_display` con escala del producto |
| GET/POST/DELETE | `/attendance/` | Si attendance:true | Devuelve estadísticas + resumen por persona |
| GET/POST/DELETE/PATCH | `/enrollment/` | Si enrollment:true | PATCH /enrollment/{id}/status |

### Comandos de referencia

```powershell
# Setup (una vez por terminal)
$env:PYTHONPATH = "."

# Migrar BD (idempotente)
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/migrate.py products/colegio-basico/colegio_basico.db
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/migrate.py products/universidad-compleja/universidad_compleja.db

# Sembrar datos
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/seeder.py products/colegio-basico/product_config.yaml

# Levantar Colegio Básico (puerto 8001)
$env:PRODUCT_CONFIG_PATH = "products/colegio-basico/product_config.yaml"
.venv\Scripts\python.exe -m uvicorn run_app:app --port 8001 --reload

# Levantar Universidad Compleja (puerto 8002)
$env:PRODUCT_CONFIG_PATH = "products/universidad-compleja/product_config.yaml"
.venv\Scripts\python.exe -m uvicorn run_app:app --port 8002 --reload

# Swagger UI
# Colegio   → http://localhost:8001/docs
# Universidad → http://localhost:8002/docs
```

### Demo SPLE verificada en vivo

```powershell
# 1. Misma ruta, comportamiento diferente según producto:
# Colegio:       GET /attendance/ → 200 OK
# Universidad:   GET /attendance/ → 404 Not Found

# 2. El evaluation_scale del YAML afecta el comportamiento real:
# Colegio (literal):      GET /grading/ → {"valor": 8.5, "valor_display": "Muy Bueno"}
# Universidad (numeric):  GET /grading/ → {"valor": 8.5, "valor_display": 8.5}
# MISMO código. DISTINTO resultado. SIN if-else sobre el nombre del producto.

# 3. BDs completamente separadas:
# Una nota creada en el puerto 8001 NO aparece en el 8002.
```

---

## Qué falta para Sprint 3 (DevOps)

Dev A no tiene trabajo pendiente para el backend. Las tareas de Sprint 3 son:
- `Dockerfile` para el backend (Lee `PRODUCT_CONFIG_PATH` desde variable de entorno)
- `docker-compose.yml` para levantar ambos productos en paralelo
- GitHub Actions: lint + tests automatizados (ver trabajo de Dev C)

---

## Coordinación con Dev C (Tests)

Dev C necesita los siguientes fixtures de tu código:
- `GradeRepository`, `AttendanceRepository`, `EnrollmentRepository` (para tests de persistencia)
- `PersonaRepository` con `CedulaValidator` integrado (test de validación)
- `GradeScaleConverter` (test de conversión literal/numeric)
- `AttendanceCalculator` (test de umbrales de riesgo)

Todos están en `core_assets/backend/core_engine/`. Ninguno requiere levantar el servidor para ser testeado unitariamente.
