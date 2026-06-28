# Academic SPL — Core Assets (Sprint 1)

Este paquete contiene los **Core Assets** construidos en el Sprint 1 de
la Línea de Productos de Software del dominio académico. **No contiene
ningún producto terminado** (eso corresponde a Sprint 2 y 3) — los
archivos dentro de `products/` son únicamente configuraciones de
ejemplo usadas para *probar* que el Core Engine resuelve variabilidad
correctamente.

## Mapeo con el backlog de Linear (Sprint 1)

| Tarea | Archivo |
|---|---|
| COR-02 — Motor de Feature Flags | `core_assets/backend/core_engine/config/feature_flags.py` |
| COR-03 — App Factory FastAPI | `core_assets/backend/core_engine/main_factory.py` |
| COR-04 — Entidades de dominio | `core_assets/backend/core_engine/domain/entities.py` |
| COR-05 — Contrato gRPC base | `core_assets/backend/core_engine/grpc_contracts/academic_core.proto` |
| COR-06 — POC extensión gRPC | `core_assets/backend/core_engine/grpc_contracts/extensions/higher_education_extension.proto` |
| COR-07 — Plantilla Docker | `docker/templates/backend.Dockerfile.tpl` |

## Instalación

```bash
pip install -r requirements.txt
```

## La Demo de Oro (para presentar mañana)

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
# Vista general: features activos en cada producto
curl http://127.0.0.1:8001/ | python3 -m json.tool
curl http://127.0.0.1:8002/ | python3 -m json.tool

# La prueba contundente: el mismo endpoint existe en uno y NO en el otro
curl -i http://127.0.0.1:8001/attendance/   # -> 200 OK (colegio sí controla asistencia)
curl -i http://127.0.0.1:8002/attendance/   # -> 404 Not Found (universidad no la activó)

curl -i http://127.0.0.1:8001/enrollment/   # -> 404 Not Found
curl -i http://127.0.0.1:8002/enrollment/   # -> 200 OK

# La calificación también varía en formato, no solo en encendido/apagado
curl http://127.0.0.1:8001/grading/   # escala "literal"
curl http://127.0.0.1:8002/grading/   # escala "numeric"
```

También puedes abrir `http://127.0.0.1:8001/docs` y `http://127.0.0.1:8002/docs`
(Swagger UI autogenerado por FastAPI) y mostrar visualmente que cada
instancia tiene un conjunto distinto de endpoints documentados.

## Validar el contrato gRPC

```bash
cd core_assets/backend/core_engine/grpc_contracts
pip install grpcio-tools
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. academic_core.proto
python3 -m grpc_tools.protoc -I. --python_out=. extensions/higher_education_extension.proto
```

Si ambos comandos terminan sin error, el contrato base y su extensión
(sin modificar el base) son válidos.

## Por qué esto demuestra SPLE y no una app tradicional

1. **`core_assets/` no menciona "colegio" ni "universidad" en ningún
   archivo.** Solo conoce conceptos genéricos: Persona, Curso,
   Periodo, Evaluación.
2. **La diferencia de comportamiento entre productos viene 100% de un
   archivo YAML**, no de un `if` en el código.
3. **El contrato gRPC se extiende, no se modifica**, validando que
   agregar un producto nuevo no rompe a los productos existentes.
4. **La plantilla Docker es parametrizada**: la misma plantilla
   construye la imagen de cualquier producto según los `--build-arg`.

## Qué falta (a propósito) para Sprint 2 y 3

- Persistencia real / multi-tenancy (`core_assets/backend/core_engine/persistence/`)
- Laravel Shell con FeatureGate conectado al backend
- Pipeline CI/CD que automatice el build mostrado arriba
- Segundo producto real, no solo su configuración de prueba
