# PROMPT DEV A — Sprint 2 (Backend + Persistencia)
# Estado: COMPLETADO. Documento de referencia para el equipo.
# Todo el trabajo de Dev A está terminado y verificado.

Actúa como un Arquitecto de Software experto en Python (FastAPI),
patrones de diseño y Líneas de Productos de Software (SPLE).

---

## Contexto del proyecto

Somos un equipo de 3 personas en un proyecto universitario. Estamos
construyendo una **Línea de Productos de Software (SPL)** para el
dominio académico. Construimos **Core Assets** reutilizables que
permiten derivar múltiples productos (Colegio Básico, Universidad
Compleja, Instituto Técnico Nocturno) cambiando solo un archivo de
configuración YAML, sin tocar el código del Core.

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

## Estructura completa del proyecto (estado actual verificado)

```
academic-spl/
├── run_app.py
├── requirements.txt                         ← sqlalchemy==2.0.30, pydantic, fastapi, uvicorn
├── core_assets/backend/core_engine/
│   ├── config/
│   │   ├── feature_flags.py                 ← Motor de variabilidad (lee YAML)
│   │   ├── schema_loader.py                 ← Valida configs contra JSON Schema
│   │   └── config_schema.json               ← Contrato formal (database, seed_data, academic_settings completo)
│   ├── domain/
│   │   ├── entities.py                      ← Pydantic: Persona, Curso, Periodo, Evaluacion
│   │   ├── validators/
│   │   │   └── cedula_validator.py          ← CA-01: Módulo 10 Registro Civil Ecuador
│   │   └── calculators/
│   │       ├── grade_scale_converter.py     ← CA-02: literal/numeric según evaluation_scale del YAML
│   │       ├── attendance_calculator.py     ← CA-03: umbrales desde attendance_min_percentage del YAML
│   │       ├── grade_passing_checker.py     ← CA-04: aprobado/reprobado según passing_grade del YAML
│   │       └── enrollment_limit_checker.py  ← CA-05: límite de materias según max_enrollments_per_period del YAML
│   ├── features/
│   │   ├── personas/router.py               ← Core Service siempre activo (usa CA-01)
│   │   ├── cursos/router.py                 ← Core Service siempre activo
│   │   ├── periodos/router.py               ← Core Service siempre activo
│   │   ├── attendance/router.py             ← Optional Feature (usa CA-03)
│   │   ├── grading/router.py                ← Optional Feature (usa CA-02 + CA-04)
│   │   ├── enrollment/router.py             ← Optional Feature (usa CA-05)
│   │   ├── schedule/router.py               ← Optional Feature (implementado)
│   │   ├── reports/router.py                ← Optional Feature (implementado)
│   │   └── certificates/router.py           ← Optional Feature (implementado)
│   ├── persistence/
│   │   ├── connection_resolver.py           ← BD por producto desde database.path del YAML
│   │   ├── models.py                        ← ORM: PersonaDB, CursoDB, PeriodoDB, EvaluacionDB, AsistenciaDB, MatriculaDB, HorarioDB, CertificadoDB
│   │   ├── migrate.py                       ← CLI idempotente de migraciones
│   │   ├── seeder.py                        ← Siembra desde seed_data del YAML
│   │   ├── persona_repository.py            ← CRUD + CedulaValidator (CA-01)
│   │   ├── curso_repository.py              ← CRUD + filtro ?periodo_id=
│   │   ├── periodo_repository.py            ← CRUD
│   │   ├── grade_repository.py              ← CRUD calificaciones
│   │   ├── attendance_repository.py         ← CRUD asistencias
│   │   ├── enrollment_repository.py         ← CRUD matrículas + count_active_enrollments()
│   │   ├── schedule_repository.py           ← CRUD horarios
│   │   └── certificate_repository.py        ← CRUD certificados
│   └── main_factory.py                      ← Application Factory: Core Services siempre + Optional Features por YAML
├── products/
│   ├── colegio-basico/
│   │   ├── product_config.yaml
│   │   └── colegio_basico.db
│   ├── universidad-compleja/
│   │   ├── product_config.yaml
│   │   └── universidad_compleja.db
│   └── instituto-tecnico/
│       ├── product_config.yaml
│       └── instituto_tecnico.db (se crea al migrar)
└── docs/feature_model.md
```

---

## Los 5 Core Assets de lógica de negocio

### CA-01 — CedulaValidator
Algoritmo Módulo 10 del Registro Civil Ecuador. Usado en `PersonaRepository`.
```python
CedulaValidator.validate("1713175071")        # → True
CedulaValidator.validate("1234567890")        # → False
CedulaValidator.validate_or_raise("999...")   # → ValueError
```

### CA-02 — GradeScaleConverter
Convierte notas a la escala del YAML (`evaluation_scale`). Mismo código, distinto resultado.
```python
# Colegio (literal):       → "Muy Bueno"
# Universidad (numeric):   → 8.5
GradeScaleConverter.to_display(8.5, scale)

# Tabla de conversión literal:
# 9.0 - 10.0 → "Sobresaliente"
# 7.0 -  8.9 → "Muy Bueno"
# 5.0 -  6.9 → "Bueno"
# 3.0 -  4.9 → "Regular"
# 0.0 -  2.9 → "Insuficiente"
```

### CA-03 — AttendanceCalculator
Calcula estadísticas de asistencia. Los umbrales vienen del YAML (`attendance_min_percentage`).
```python
# Colegio (umbral 80%):       77% → "EN_RIESGO"
# Universidad (umbral 75%):   77% → "APROBADO"
# Técnico (umbral 70%):       72% → "APROBADO"
AttendanceCalculator.status(77.0, threshold_approved=80.0)   # → "EN_RIESGO"
AttendanceCalculator.summarize(records, threshold_approved, threshold_at_risk)
AttendanceCalculator.summarize_by_persona(records, threshold_approved, threshold_at_risk)
```

### CA-04 — GradePassingChecker
Determina si una nota aprueba según `passing_grade` del YAML.
```python
# El mismo 6.5 tiene distinto significado:
GradePassingChecker.status(6.5, passing_grade=6.0)  # → "APROBADO"  (Universidad)
GradePassingChecker.status(6.5, passing_grade=7.0)  # → "REPROBADO" (Colegio)
GradePassingChecker.annotate_grades_list(grades, passing_grade)  # agrega aprueba + estado_aprobacion
```

### CA-05 — EnrollmentLimitChecker
Verifica límite de materias por estudiante según `max_enrollments_per_period` del YAML.
```python
EnrollmentLimitChecker.can_enroll(5, max_enrollments=6)  # → True  (Universidad)
EnrollmentLimitChecker.can_enroll(5, max_enrollments=5)  # → False (Técnico, ya llegó al límite)
EnrollmentLimitChecker.validate_or_raise(5, 5, "P-001")  # → ValueError
EnrollmentLimitChecker.slots_remaining(3, 8)             # → 5 (Colegio)
```

---

## academic_settings — Variabilidad paramétrica completa

| Parámetro | Colegio | Universidad | Técnico | Core Asset que lo usa |
|---|---|---|---|---|
| `evaluation_scale` | `literal` | `numeric` | `numeric` | CA-02 |
| `periods_per_year` | 1 | 2 | 2 | informativo |
| `passing_grade` | 7.0 | 6.0 | 7.0 | CA-04 |
| `attendance_min_percentage` | 80.0 | 75.0 | 70.0 | CA-03 |
| `max_enrollments_per_period` | 8 | 6 | 5 | CA-05 |
| `grading_max_value` | 10 | 10 | 10 | informativo |

---

## Optional Features — Variabilidad booleana completa

| Feature | Colegio | Universidad | Técnico | Descripción |
|---|---|---|---|---|
| `attendance` | ✅ | ❌ | ❌ | Asistencia diaria |
| `grading` | ✅ | ✅ | ✅ | Calificaciones |
| `enrollment` | ✅ | ✅ | ✅ | Matrículas/Inscripciones |
| `schedule` | ❌ | ✅ | ✅ | Horarios de clases |
| `reports` | ❌ | ✅ | ✅ | Reportes académicos |
| `certificates` | ❌ | ✅ | ❌ | Certificados de aprobación |

---

## Todos los endpoints disponibles

### Core Services (siempre disponibles en todos los productos)
```
GET    /                                   → diagnóstico: core_services + active_optional_features + academic_settings
GET    /periodos/                           → listar períodos
POST   /periodos/                           → crear período {"nombre", "fecha_inicio", "fecha_fin"}
GET    /periodos/{id}                       → obtener período
PUT    /periodos/{id}                       → actualizar período
DELETE /periodos/{id}                       → eliminar período

GET    /cursos/                             → listar cursos (acepta ?periodo_id= para filtrar)
POST   /cursos/                             → crear curso {"nombre", "periodo_id"}
GET    /cursos/{id}                         → obtener curso
PUT    /cursos/{id}                         → actualizar curso
DELETE /cursos/{id}                         → eliminar curso

GET    /personas/                           → listar personas
POST   /personas/                           → crear {"nombres", "apellidos", "documento_identidad"}
                                               ← CA-01 valida la cédula, retorna 409 si inválida
GET    /personas/{id}                       → obtener persona
GET    /personas/por-documento/{doc}        → buscar por cédula ecuatoriana
PUT    /personas/{id}                       → actualizar (CA-01 valida si cambia documento)
DELETE /personas/{id}                       → eliminar persona
```

### Optional Features (según product_config.yaml)
```
GET    /grading/           → lista notas con valor_display (CA-02), aprueba y estado_aprobacion (CA-04)
POST   /grading/           → {"curso_id", "persona_id", "valor" (0-10), "observacion"}
GET    /grading/{id}       → nota individual con valor_display + aprueba + estado_aprobacion
DELETE /grading/{id}       → eliminar nota

GET    /attendance/        → lista + estadisticas (CA-03): porcentaje, estado, umbral_aprobado
POST   /attendance/        → {"persona_id", "curso_id", "fecha", "presente", "justificacion"}
GET    /attendance/{id}    → registro individual
DELETE /attendance/{id}    → eliminar registro

GET    /enrollment/        → listar matrículas
POST   /enrollment/        → {"persona_id", "curso_id"} ← CA-05 verifica límite antes de insertar
GET    /enrollment/{id}    → matrícula individual
PATCH  /enrollment/{id}/status → {"estado": "inscrito|retirado|aprobado|reprobado"}
DELETE /enrollment/{id}    → eliminar matrícula

GET    /schedule/          → listar horarios por día
POST   /schedule/          → crear horario {"curso_id", "dia_semana", "hora_inicio", "hora_fin", "aula"}
GET    /schedule/{curso_id}→ horario de un curso
DELETE /schedule/{id}      → eliminar horario
GET    /reports/           → config producto y lista de estudiantes
GET    /reports/rendimiento/{persona_id} → reporte detallado notas+asistencia
GET    /reports/consolidado/ → tabla de estados de todos los estudiantes
GET    /certificates/      → listar certificados emitidos/rechazados
POST   /certificates/{persona_id}/generate → verifica CA-03/CA-04 y emite/rechaza
GET    /certificates/persona/{persona_id} → historial de certificados
```

---

## Comandos de referencia (todos verificados)

```powershell
# Setup (en cada terminal nueva)
$env:PYTHONPATH = "."

# Migrar BDs
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/migrate.py products/colegio-basico/colegio_basico.db
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/migrate.py products/universidad-compleja/universidad_compleja.db
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/migrate.py products/instituto-tecnico/instituto_tecnico.db

# Sembrar datos
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/seeder.py products/colegio-basico/product_config.yaml
.venv\Scripts\python.exe core_assets/backend/core_engine/persistence/seeder.py products/instituto-tecnico/product_config.yaml

# Levantar productos (3 terminales)
$env:PRODUCT_CONFIG_PATH = "products/colegio-basico/product_config.yaml"
.venv\Scripts\python.exe -m uvicorn run_app:app --port 8001 --reload

$env:PRODUCT_CONFIG_PATH = "products/universidad-compleja/product_config.yaml"
.venv\Scripts\python.exe -m uvicorn run_app:app --port 8002 --reload

$env:PRODUCT_CONFIG_PATH = "products/instituto-tecnico/product_config.yaml"
.venv\Scripts\python.exe -m uvicorn run_app:app --port 8003 --reload

# Swagger UI
# Colegio     → http://localhost:8001/docs  (10 rutas)
# Universidad → http://localhost:8002/docs  (18 rutas, incluye schedule/reports/certificates)
# Técnico     → http://localhost:8003/docs  (14 rutas, incluye schedule/reports pero no certificates)
```

---

## Demo SPLE verificada (las pruebas más importantes)

```
1. VARIABILIDAD BOOLEANA: attendance da 200 en colegio, 404 en universidad
2. VARIABILIDAD PARAMÉTRICA CA-02: nota 8.5 → "Muy Bueno" en colegio, 8.5 en universidad
3. VARIABILIDAD PARAMÉTRICA CA-04: nota 6.5 → APROBADO en universidad (6.0), REPROBADO en colegio (7.0)
4. VARIABILIDAD PARAMÉTRICA CA-03: 77% asistencia → EN_RIESGO en colegio (80%), APROBADO en universidad (75%)
5. VARIABILIDAD PARAMÉTRICA CA-05: inscripción 6 rechazada en técnico (max=5), aceptada en colegio (max=8)
6. BDs separadas: nota en 8001 NO aparece en 8002
7. FEATURES NUEVOS: schedule/reports/certificates existen en Swagger de universidad, NO en colegio
```

---

## Qué hace Dev A para Sprint 3

Dev A no tiene trabajo pendiente de backend. Para Sprint 3:
- `Dockerfile` para el backend (lee `PRODUCT_CONFIG_PATH` desde variable de entorno)
- `docker-compose.yml` para los 3 productos en paralelo
- Colaborar con Dev C en los tests de los nuevos Core Assets (CA-04 y CA-05)
