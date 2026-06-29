# Academic SPL — Core Assets (Sprint 1 — COMPLETO)

Este paquete contiene **todos** los Core Assets planeados para el
Sprint 1 de la Línea de Productos de Software del dominio académico.
Los archivos dentro de `products/` siguen siendo únicamente
configuraciones de ejemplo, usadas para *probar* el Core Engine — los
productos completos corresponden a Sprint 2 y 3.

## Mapeo con el backlog de Linear (Sprint 1) — estado final

| Tarea | Estado | Archivo | Evidencia |
|---|---|---|---|
| COR-01 — Feature Model formal | ✅ Done | `docs/feature_model.md` | Documento con notación FODA, tabla de binding time |
| COR-02 — Motor de Feature Flags | ✅ Done | `config/feature_flags.py` | Probado con curl (200/404 según flag) |
| COR-03 — App Factory FastAPI | ✅ Done | `main_factory.py` | Probado con dos configs simultáneas |
| COR-04 — Entidades de dominio | ✅ Done | `domain/entities.py` | Usadas por ambos productos de prueba |
| COR-05 — Contrato gRPC base | ✅ Done | `grpc_contracts/academic_core.proto` | Compilado sin errores |
| COR-06 — Extensión gRPC | ✅ Done | `grpc_contracts/extensions/*.proto` | Compilado, importa el base sin modificarlo |
| COR-07 — Plantilla Docker | ✅ Done | `docker/templates/backend.Dockerfile.tpl` | Plantilla parametrizada con ARGs |
| COR-08 — Laravel Shell + Auth | 🟡 Done (código) / Pendiente ejecución real | `frontend/laravel-shell/app/Http/Controllers/Auth/LoginController.php` | Sintaxis validada con `php -l`; falta correr dentro de Laravel real (requiere Composer) |
| COR-09 — FeatureGate | 🟡 Done (código) / Validado vía POC | `frontend/laravel-shell/app/Core/Services/FeatureGate.php` | Patrón probado end-to-end con `feature_gate_poc.php` contra el backend real |
| COR-10 — Módulo Laravel de ejemplo | 🟡 Done (código) / Pendiente ejecución real | `frontend/laravel-shell/app/Modules/AttendanceModule/` | Sintaxis validada con `php -l` |
| COR-11 — Esquema formal de configuración | ✅ Done | `config/config_schema.json` + `config/schema_loader.py` | Validado contra configs correctas e incorrectas |

**Por qué COR-08/09/10 están en amarillo y no en verde:** el código
está completo y sintácticamente verificado, pero no pudo ejecutarse
dentro de un proyecto Laravel real en este entorno (Composer requiere
acceso a Packagist, no disponible aquí). Ver
`frontend/laravel-shell/INTEGRACION.md` para los pasos exactos de
cómo terminarlo de validar en una máquina con Laravel instalado. Sé
honesto con tu tutor sobre esta distinción — es exactamente el tipo de
rigor que un proceso real de ingeniería de software exige.

## Instalación

```bash
pip install -r requirements.txt
```

## La Demo de Oro (para presentar)

Abre dos terminales. En cada una, el **mismo código** (`run_app.py` →
`main_factory.py`) se ejecuta con una configuración distinta:

**Terminal 1 — Colegio Básico**
```bash
PRODUCT_CONFIG_PATH=products/colegio-basico/product_config.yaml \
  uvicorn run_app:app --port 8001
```

**Terminal 2 — Universidad Compleja**
```bash
PRODUCT_CONFIG_PATH=products/universidad-compleja/product_config.yaml \
  uvicorn run_app:app --port 8002
```

**Lo que debes mostrar en vivo:**

```bash
curl http://127.0.0.1:8001/ | python3 -m json.tool
curl http://127.0.0.1:8002/ | python3 -m json.tool

curl -i http://127.0.0.1:8001/attendance/   # -> 200 OK
curl -i http://127.0.0.1:8002/attendance/   # -> 404 Not Found

curl -i http://127.0.0.1:8001/enrollment/   # -> 404 Not Found
curl -i http://127.0.0.1:8002/enrollment/   # -> 200 OK
```

## Validar el esquema de configuración (COR-11)

```bash
python3 core_assets/backend/core_engine/config/schema_loader.py
```

Debe imprimir `[OK]` para ambos productos. Si quieres ver que también
detecta errores, créate un YAML con un valor inválido y pásaselo como
argumento.

## Validar el contrato gRPC

```bash
cd core_assets/backend/core_engine/grpc_contracts
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. academic_core.proto
python3 -m grpc_tools.protoc -I. --python_out=. extensions/higher_education_extension.proto
```

## Validar el patrón FeatureGate (sin instalar Laravel todavía)

Con los dos backends corriendo (puertos 8001 y 8002 como arriba):

```bash
php core_assets/frontend/laravel-shell/feature_gate_poc.php http://127.0.0.1:8001/ http://127.0.0.1:8002/
```

## Qué falta (a propósito) para Sprint 2 y 3

- Persistencia real / multi-tenancy (`core_assets/backend/core_engine/persistence/`)
- Ejecutar el Laravel Shell dentro de un proyecto Laravel real instalado vía Composer
- Pipeline CI/CD que automatice el build mostrado arriba
- Segundo producto real, no solo su configuración de prueba

