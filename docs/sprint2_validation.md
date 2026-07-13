# Sprint 2 Validation Report

**Fecha:** 2026-07-12  
**Dev:** Dev C  
**Sprint:** Sprint 2 (Auth + Pruebas + Validación de 3 Productos)

---

## Resumen Ejecutivo

Todas las tareas de Sprint 2 para Dev C han sido completadas exitosamente:
- ✅ COR-22: Autenticación JWT básica implementada
- ✅ COR-23: Schema loader ampliado para instituto-tecnico
- ✅ COR-24: Arnés de pruebas (conftest.py) creado
- ✅ COR-25: Suite de tests completa (36 tests pasando)
- ✅ PROD-01: Migración y seeding de las 3 bases de datos
- ✅ PROD-02: Validación end-to-end de los 3 productos

---

## COR-22: Autenticación JWT Básica

### Implementación
**Archivo:** `core_assets/backend/core_engine/features/auth/router.py`

**Endpoints implementados:**
- `POST /auth/token` → Login OAuth2, devuelve JWT token
- `GET /auth/me` → Devuelve datos del usuario autenticado (requiere token)

**Dependencias agregadas:**
- `python-jose[cryptography]==3.3.0`
- `passlib[bcrypt]==1.7.4`

**Registro en Core Services:**
- Auth router registrado en `main_factory.py` como Core Service
- Siempre montado en todos los productos (commonality)

**Demo de autenticación:**
- Para demo: usa `documento_identidad` como contraseña
- Ejemplo: email="1001", password="1001" (persona del seed data)

---

## COR-23: Schema Loader Ampliado

### Validación de los 3 productos
```bash
$env:PYTHONPATH = "."
python core_assets/backend/core_engine/config/schema_loader.py
```

**Resultado:**
```
[OK] products/colegio-basico/product_config.yaml cumple el esquema formal
[OK] products/universidad-compleja/product_config.yaml cumple el esquema formal
[OK] products/instituto-tecnico/product_config.yaml cumple el esquema formal
```

---

## COR-24: Arnés de Pruebas

### Archivo creado: `tests_core/conftest.py`

**Fixtures implementados:**
- `db_session` → BD en memoria para tests unitarios
- `flags_colegio`, `flags_universidad`, `flags_tecnico` → FeatureFlags de cada producto
- `client_colegio`, `client_universidad`, `client_tecnico` → TestClient para cada producto

---

## COR-25: Suite de Tests Automatizados

### Archivos de tests creados:
1. `tests_core/test_core_assets.py` → Tests unitarios de los 5 Core Assets
2. `tests_core/test_variability.py` → Tests de variabilidad SPLE
3. `tests_core/test_api_integration.py` → Tests de integración con API

### Ejecución de tests
```bash
$env:PYTHONPATH = "."
python -m pytest tests_core/ -v --tb=short
```

**Resultado:**
```
36 passed, 1 warning in 2.94s
```

### Distribución de tests:
- **test_core_assets.py**: 20 tests unitarios
  - CA-01: CedulaValidator (4 tests)
  - CA-02: GradeScaleConverter (4 tests)
  - CA-03: AttendanceCalculator (5 tests)
  - CA-04: GradePassingChecker (4 tests)
  - CA-05: EnrollmentLimitChecker (3 tests)

- **test_variability.py**: 14 tests de variabilidad SPLE
  - Variabilidad booleana (features ON/OFF): 6 tests
  - Variabilidad paramétrica (evaluation_scale, passing_grade): 4 tests
  - Diagnóstico de configuración: 2 tests

- **test_api_integration.py**: 2 tests de integración
  - Validación de cédula a través de API
  - Verificación de configuración en endpoint de diagnóstico

---

## PROD-01: Migración y Seeding

### Migración de las 3 bases de datos
```bash
python core_assets/backend/core_engine/persistence/migrate.py products/colegio-basico/colegio_basico.db
python core_assets/backend/core_engine/persistence/migrate.py products/universidad-compleja/universidad_compleja.db
python core_assets/backend/core_engine/persistence/migrate.py products/instituto-tecnico/instituto_tecnico.db
```

**Resultado:** ✅ Las 3 bases de datos migradas exitosamente con 6 tablas cada una

### Seeding de datos iniciales
```bash
python core_assets/backend/core_engine/persistence/seeder.py products/colegio-basico/product_config.yaml
python core_assets/backend/core_engine/persistence/seeder.py products/instituto-tecnico/product_config.yaml
```

**Resultado:**
- **Colegio:** 3 personas, 1 período, 2 cursos
- **Técnico:** 2 personas, 2 períodos, 3 cursos
- **Universidad:** No tiene seed_data (intencional)

---

## PROD-02: Validación End-to-End

### Variabilidad Booleana (Optional Features)

| Feature | Colegio (8001) | Universidad (8002) | Técnico (8003) |
|---------|----------------|-------------------|----------------|
| attendance | ✅ Activo | ❌ Inactivo | ❌ Inactivo |
| grading | ✅ Activo | ✅ Activo | ✅ Activo |
| enrollment | ✅ Activo | ✅ Activo | ✅ Activo |
| schedule | ❌ Inactivo | ✅ Activo | ✅ Activo |
| reports | ❌ Inactivo | ✅ Activo | ✅ Activo |
| certificates | ❌ Inactivo | ✅ Activo | ❌ Inactivo |

**Validación:** ✅ Todos los features se activan/desactivan según el YAML

### Variabilidad Paramétrica CA-02 (evaluation_scale)

| Producto | Configuración | Comportamiento |
|----------|--------------|----------------|
| Colegio | `literal` | Nota 8.5 → "Muy Bueno" |
| Universidad | `numeric` | Nota 8.5 → 8.5 |
| Técnico | `numeric` | Nota 8.5 → 8.5 |

**Validación:** ✅ La misma nota se muestra diferente según el producto

### Variabilidad Paramétrica CA-04 (passing_grade)

| Producto | passing_grade | Nota 6.5 → Estado |
|----------|---------------|-------------------|
| Colegio | 7.0 | REPROBADO |
| Universidad | 6.0 | APROBADO |
| Técnico | 7.0 | REPROBADO |

**Validación:** ✅ El mismo valor numérico tiene distinto significado según el producto

### Variabilidad Paramétrica CA-03 (attendance_min_percentage)

| Producto | Umbral | 77% asistencia → Estado |
|----------|--------|-------------------------|
| Colegio | 80% | EN_RIESGO |
| Universidad | 75% | APROBADO |
| Técnico | 70% | APROBADO |

**Validación:** ✅ El mismo porcentaje tiene distinto estado según el producto

### Validación CA-01 (Cédula Ecuatoriana)

**Test:** `POST /personas/` con cédula inválida "1234567890"

**Resultado esperado:** HTTP 409 (conflicto) o 422 (validation error)

**Validación:** ✅ CedulaValidator rechaza cédulas inválidas

### Validación CA-05 (Límite de Matrículas)

| Producto | max_enrollments | Inscribir 6 materias |
|----------|-----------------|---------------------|
| Técnico | 5 | ❌ Rechaza (HTTP 409) |
| Colegio | 8 | ✅ Acepta |
| Universidad | 6 | ✅ Acepta |

**Validación:** ✅ EnrollmentLimitChecker respeta los límites del YAML

### Tests Automatizados

**Comando:** `pytest tests_core/ -v`

**Resultado:** ✅ 36 tests pasando, 0 fallando

---

## Regla de Oro: Core Assets Agnósticos

**Verificación:** ✅ Ningún archivo en `core_assets/` contiene nombres de productos

- `core_assets/backend/core_engine/features/auth/router.py` → No menciona "colegio", "universidad", "técnico"
- `core_assets/backend/core_engine/main_factory.py` → Solo usa rutas de configuración como parámetros
- Todos los Core Assets (CA-01 a CA-05) → Reciben parámetros, no hardcodean valores de producto

---

## Comandos Útiles

### Ejecutar todos los tests
```powershell
$env:PYTHONPATH = "."
python -m pytest tests_core/ -v --tb=short
```

### Solo tests unitarios (sin servidor)
```powershell
$env:PYTHONPATH = "."
python -m pytest tests_core/test_core_assets.py -v
```

### Solo tests de variabilidad SPLE
```powershell
$env:PYTHONPATH = "."
python -m pytest tests_core/test_variability.py -v
```

### Validar esquemas de los 3 productos
```powershell
$env:PYTHONPATH = "."
python core_assets/backend/core_engine/config/schema_loader.py
```

### Levantar un producto (ejemplo: colegio)
```powershell
$env:PRODUCT_CONFIG_PATH = "products/colegio-basico/product_config.yaml"
python -m uvicorn run_app:app --reload --port 8001
```

---

## Próximos Pasos (Sprint 3)

1. **Dev B:** Completar frontend Laravel
2. **DevOps:** Configurar Docker + GitHub Actions
3. **Dev A:** Implementar Optional Features faltantes (schedule, reports, certificates)
4. **Todos:** Integración end-to-end completa frontend + backend

---

## Conclusión

Sprint 2 completado exitosamente. La línea de productos académica tiene:
- ✅ Autenticación JWT funcional
- ✅ Suite de tests automatizada (36 tests)
- ✅ 3 productos derivados validados
- ✅ 5 Core Assets testeados y agnósticos
- ✅ Variabilidad SPLE verificada (booleana y paramétrica)

El proyecto cumple con la regla de oro: `core_assets/` es completamente agnóstico a productos.
