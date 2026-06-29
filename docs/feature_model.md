# Feature Model — Academic SPL

> COR-01. Este documento formaliza qué es **común** (Commonality) y qué
> **varía** (Variability) en la línea de productos académica. Es la
> referencia que cualquier desarrollo posterior debe respetar.

## 1. Commonality — lo que todos los productos comparten

Todo producto derivado de esta línea (colegio, instituto, universidad)
comparte, sin excepción:

- **Entidades de dominio:** Persona, Curso, Periodo, Evaluación
  (`core_assets/backend/core_engine/domain/entities.py`).
- **Contrato de comunicación base:** `academic_core.proto`.
- **Mecanismo de ensamblaje:** un Application Factory que monta
  módulos según configuración (`main_factory.py`).
- **Mecanismo de resolución de variabilidad:** lectura y validación de
  un `product_config.yaml` (`feature_flags.py` + `schema_loader.py`).

Estas piezas constituyen el **Core** de la línea de productos: viven en
`core_assets/` y ningún producto puede modificarlas para "encajar".

## 2. Variability — los puntos de variación

Usamos la notación estándar de Feature-Oriented Domain Analysis
(FODA): cada punto de variación se clasifica por **tipo** y por
**binding time** (momento en que se decide su valor).

| ID | Punto de variación | Tipo | Binding time | Realizado por |
|---|---|---|---|---|
| VP-01 | Asistencia (`attendance`) | Optional Feature | Configuración (antes de desplegar) | `features/attendance/router.py` + flag en YAML |
| VP-02 | Calificaciones (`grading`) | Optional Feature | Configuración | `features/grading/router.py` + flag en YAML |
| VP-03 | Matrícula (`enrollment`) | Optional Feature | Configuración | `features/enrollment/router.py` + flag en YAML |
| VP-04 | Escala de evaluación | Alternative Feature (XOR: numeric \| literal) | Configuración | `academic_settings.evaluation_scale` |
| VP-05 | Periodos académicos por año | Parametric (rango 1-4) | Configuración | `academic_settings.periods_per_year` |
| VP-06 | Extensión de contrato gRPC | Extension Point (composición, no modificación) | Diseño / Build | `grpc_contracts/extensions/*.proto` |
| VP-07 | Tipo de producto (`product_type`) | Parametric abierto (sin enum) | Configuración | `metadata.product_type` |

**Por qué "Optional Feature" y no "if hardcodeado":** un Optional
Feature en SPLE significa que el feature puede estar presente o
ausente en un producto derivado SIN que el código del Core necesite
saber por qué. La decisión vive 100% en la configuración, nunca en una
condición sobre el nombre del producto.

**Por qué VP-06 es un "Extension Point" y no un Optional Feature:**
porque no se resuelve con un simple `true/false`, sino agregando un
archivo `.proto` nuevo que *compone* (no modifica) el contrato base.
Es variabilidad a nivel estructural, no solo de activación.

## 3. Matriz de productos (Application Engineering)

Esta tabla es la prueba de que los mismos puntos de variación producen
productos distintos:

| Punto de variación | Colegio Básico | Universidad Compleja |
|---|---|---|
| VP-01 Asistencia | ✅ Activo | ❌ Inactivo |
| VP-02 Calificaciones | ✅ Activo | ✅ Activo |
| VP-03 Matrícula | ❌ Inactivo | ✅ Activo |
| VP-04 Escala de evaluación | `literal` | `numeric` |
| VP-05 Periodos por año | 1 | 2 |

## 4. Binding time — cuándo se decide cada cosa

```
Diseño del Core (Domain Engineering)
        │
        ▼
Definición del product_config.yaml (Application Engineering)
        │
        ▼
Validación contra el esquema formal (schema_loader.py)         ← falla rápido si está mal
        │
        ▼
Arranque de la app (main_factory.py lee la config)              ← AQUÍ se resuelve la variabilidad
        │
        ▼
Build de la imagen Docker (futuro Sprint 3, mismo config inyectado)
```

Todos nuestros puntos de variación actuales se resuelven en **tiempo
de configuración / arranque**, no en tiempo de compilación. Esto es
una decisión de diseño deliberada: permite cambiar un producto sin
recompilar nada, solo reiniciando con otro YAML.

## 5. Qué NO es variabilidad en este proyecto (para evitar confusión)

- Las entidades de dominio (`entities.py`) **no varían** — son
  commonality pura. Si un producto necesita un campo adicional, no se
  agrega aquí; se extiende en su propia capa (ver VP-06 como
  precedente del patrón a seguir también en el dominio).
- El mecanismo de ensamblaje (`main_factory.py`) **no varía** — su
  comportamiento es siempre el mismo algoritmo ("por cada feature en
  el catálogo, preguntar si está activo, montar o no"). Lo que varía
  es el resultado de esa pregunta, no el algoritmo.
