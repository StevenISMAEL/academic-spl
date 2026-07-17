# PROMPT — Academic SPL Workbench (Application Engineering CLI)
# Copia y pega esto completo como primer mensaje en un chat nuevo.
# Este prompt está autocontenido: no necesitas contexto previo.

Actúa como un Arquitecto de Software experto en Python, CLIs
interactivos, y Líneas de Productos de Software (SPLE). Voy a
explicarte el contexto completo de nuestro proyecto y la corrección
específica que nos hizo nuestro profesor para que me ayudes a
implementarla desde cero, archivo por archivo.

---

## 1. Contexto del proyecto

Somos un equipo de 3 personas construyendo una **Línea de Productos de
Software (SPL)** para el dominio académico. Tenemos ya construido y
funcionando un Core Engine en Python/FastAPI que:

- Lee un archivo `product_config.yaml` de configuración
- Activa o desactiva módulos (features) según esa configuración
- Soporta 3 productos derivados: Colegio Básico, Universidad Compleja,
  Instituto Técnico Nocturno
- Tiene 5 Core Assets de lógica de negocio (validador de cédula,
  conversor de escala de notas, calculador de asistencia, verificador
  de aprobación, verificador de límite de matrículas)

**La regla de oro que nunca se puede violar:**
`core_assets/` no puede contener el nombre de ningún producto ni
lógica condicional sobre productos. Toda diferencia de comportamiento
entre productos viene del `product_config.yaml`.

---

## 2. El problema que el profesor identificó

Lo que teníamos antes (incorrecto para SPLE):

```
Desarrollador edita el YAML manualmente
        ↓
App Factory lee el YAML
        ↓
Producto ensamblado
```

El problema: el desarrollador tenía que saber exactamente qué escribir
en el YAML, qué campos existen, qué features están disponibles, y
qué valores son válidos. Eso no es una Línea de Productos de Software
— es solo una app con configuración manual.

**Lo que el profesor exige (flujo correcto de Application Engineering):**

```
Paso 1: Seleccionar el tipo de institución (k12, universidad, técnico)
        ↓
Paso 2: Herramienta CREA la estructura de carpetas del nuevo producto
        ↓
Paso 3: Herramienta GENERA el .env con las variables del producto
        ↓
Paso 4: Recién ahora: seleccionar qué assets y features activar
        ↓
Paso 5: Herramienta genera el product_config.yaml automáticamente
        ↓
Paso 6: Herramienta ejecuta migraciones y siembra datos
        ↓
Paso 7: Producto corriendo
```

La diferencia clave: **existe una herramienta** (un CLI interactivo)
que hace todo ese trabajo. El desarrollador nunca toca el YAML a mano.
En SPLE esto se llama **Application Engineering Workbench**.

---

## 3. Estructura completa del proyecto actual

```
academic-spl/
├── run_app.py
├── requirements.txt
├── core_assets/
│   └── backend/core_engine/
│       ├── config/
│       │   ├── feature_flags.py          ← lee YAML y resuelve variabilidad
│       │   ├── schema_loader.py          ← valida YAML contra JSON Schema
│       │   └── config_schema.json        ← contrato formal de configuración
│       ├── domain/
│       │   ├── entities.py               ← Persona, Curso, Periodo, Evaluacion (Pydantic)
│       │   ├── validators/
│       │   │   └── cedula_validator.py   ← CA-01: Módulo 10 Ecuador
│       │   └── calculators/
│       │       ├── grade_scale_converter.py    ← CA-02
│       │       ├── attendance_calculator.py    ← CA-03
│       │       ├── grade_passing_checker.py    ← CA-04
│       │       └── enrollment_limit_checker.py ← CA-05
│       ├── features/
│       │   ├── personas/router.py        ← Core Service (siempre activo)
│       │   ├── cursos/router.py          ← Core Service (siempre activo)
│       │   ├── periodos/router.py        ← Core Service (siempre activo)
│       │   ├── attendance/router.py      ← Optional Feature
│       │   ├── grading/router.py         ← Optional Feature
│       │   ├── enrollment/router.py      ← Optional Feature
│       │   ├── schedule/router.py        ← Optional Feature (stub)
│       │   ├── reports/router.py         ← Optional Feature (stub)
│       │   └── certificates/router.py   ← Optional Feature (stub)
│       ├── persistence/
│       │   ├── connection_resolver.py
│       │   ├── models.py
│       │   ├── migrate.py
│       │   ├── seeder.py
│       │   ├── persona_repository.py
│       │   ├── curso_repository.py
│       │   ├── periodo_repository.py
│       │   ├── grade_repository.py
│       │   ├── attendance_repository.py
│       │   └── enrollment_repository.py
│       └── main_factory.py
├── products/
│   ├── colegio-basico/
│   │   ├── product_config.yaml
│   │   └── colegio_basico.db
│   ├── universidad-compleja/
│   │   ├── product_config.yaml
│   │   └── universidad_compleja.db
│   └── instituto-tecnico/
│       ├── product_config.yaml
│       └── instituto_tecnico.db
├── workbench/               ← CARPETA NUEVA — aquí va lo que debemos construir
└── docs/
    └── feature_model.md
```

---

## 4. Los product_config.yaml existentes (para entender la estructura)

### Colegio Básico
```yaml
metadata:
  product_name: "Colegio Básico Demo"
  product_type: "k12"

features:
  attendance: true
  grading: true
  enrollment: true
  schedule: false
  reports: false
  certificates: false

academic_settings:
  evaluation_scale: "literal"
  periods_per_year: 1
  passing_grade: 7.0
  attendance_min_percentage: 80.0
  max_enrollments_per_period: 8
  grading_max_value: 10

database:
  path: "products/colegio-basico/colegio_basico.db"

users:
  - email: "admin@colegio.local"
    password: "admin123"
    role: "admin"
  - email: "profesor@colegio.local"
    password: "prof123"
    role: "teacher"

seed_data:
  periodos:
    - id: "P-2024-1"
      nombre: "Año Lectivo 2024"
      fecha_inicio: "2024-09-01"
      fecha_fin: "2025-07-31"
  personas:
    - id: "EST-001"
      nombres: "María"
      apellidos: "González"
      documento_identidad: "1713175071"
```

### Universidad Compleja
```yaml
metadata:
  product_name: "Universidad Compleja Demo"
  product_type: "higher_education"

features:
  attendance: false
  grading: true
  enrollment: true
  schedule: true
  reports: true
  certificates: true

academic_settings:
  evaluation_scale: "numeric"
  periods_per_year: 2
  passing_grade: 6.0
  attendance_min_percentage: 75.0
  max_enrollments_per_period: 6
  grading_max_value: 10

database:
  path: "products/universidad-compleja/universidad_compleja.db"

users:
  - email: "admin@universidad.local"
    password: "admin123"
    role: "admin"
```

### Instituto Técnico Nocturno
```yaml
metadata:
  product_name: "Instituto Técnico Nocturno"
  product_type: "technical"

features:
  attendance: false
  grading: true
  enrollment: true
  schedule: true
  reports: true
  certificates: false

academic_settings:
  evaluation_scale: "numeric"
  periods_per_year: 2
  passing_grade: 7.0
  attendance_min_percentage: 70.0
  max_enrollments_per_period: 5
  grading_max_value: 10

database:
  path: "products/instituto-tecnico/instituto_tecnico.db"

users:
  - email: "admin@instituto.local"
    password: "admin123"
    role: "admin"
```

---

## 5. Los features disponibles y sus descripciones

### Core Services (siempre activos, no son seleccionables)
| Feature | Descripción |
|---|---|
| `personas` | Gestión de personas con validación de cédula ecuatoriana |
| `cursos` | Gestión de cursos académicos |
| `periodos` | Gestión de periodos académicos |

### Optional Features (seleccionables por producto)
| Feature | Descripción | Colegio | Universidad | Técnico |
|---|---|---|---|---|
| `attendance` | Control de asistencia diaria | ✅ | ❌ | ❌ |
| `grading` | Registro de calificaciones | ✅ | ✅ | ✅ |
| `enrollment` | Gestión de matrículas | ✅ | ✅ | ✅ |
| `schedule` | Horarios de clases | ❌ | ✅ | ✅ |
| `reports` | Reportes académicos | ❌ | ✅ | ✅ |
| `certificates` | Certificados de aprobación | ❌ | ✅ | ❌ |

---

## 6. Los parámetros académicos configurables

| Parámetro | Tipo | Colegio | Universidad | Técnico |
|---|---|---|---|---|
| `evaluation_scale` | `literal` o `numeric` | literal | numeric | numeric |
| `periods_per_year` | entero 1-4 | 1 | 2 | 2 |
| `passing_grade` | decimal 0-10 | 7.0 | 6.0 | 7.0 |
| `attendance_min_percentage` | decimal 0-100 | 80.0 | 75.0 | 70.0 |
| `max_enrollments_per_period` | entero 1-20 | 8 | 6 | 5 |

---

## 7. Lo que hay que construir: el Workbench

Son exactamente 3 archivos nuevos dentro de la carpeta `workbench/`:

### Archivo 1 — `workbench/product_templates.py`

Define las plantillas por tipo de institución. Es un diccionario de
"puntos de partida" — qué features sugiere activar por defecto y qué
valores paramétricos recomienda para cada tipo. El usuario puede
aceptarlos o modificarlos.

No contiene lógica de negocio — solo datos de configuración
predeterminada.

### Archivo 2 — `workbench/scaffolder.py`

La pieza que hace el trabajo real:
1. Crea la estructura de carpetas del nuevo producto
2. Genera el archivo `.env` del producto
3. Genera el `product_config.yaml` completo y válido
4. Ejecuta las migraciones de BD (`migrate.py`)
5. Ejecuta el seeder si hay datos iniciales (`seeder.py`)

Recibe como parámetros: nombre del producto, tipo, features
seleccionados, parámetros académicos, usuarios. No interactúa con el
usuario — eso lo hace `assemble.py`.

### Archivo 3 — `workbench/assemble.py`

El punto de entrada. CLI interactivo que:
1. Muestra un menú de selección de tipo de institución
2. Pide el nombre del producto
3. Muestra los Core Services (informativos, siempre activos)
4. Muestra los Optional Features con los valores por defecto del
   template y permite modificarlos
5. Muestra los parámetros académicos con valores por defecto y permite
   modificarlos
6. Pide datos del usuario administrador
7. Llama a `scaffolder.py` con todo lo recopilado
8. Ofrece levantar el producto inmediatamente

---

## 8. El flujo exacto que debe tener el CLI

```
python workbench/assemble.py
```

```
╔══════════════════════════════════════════════╗
║   Academic SPL — Workbench v1.0              ║
║   Application Engineering CLI               ║
╚══════════════════════════════════════════════╝

[PASO 1] Tipo de institución
  [1] Colegio / Escuela Básica (k12)
  [2] Universidad / Instituto Superior (higher_education)
  [3] Instituto Técnico / Nocturno (technical)
  [4] Personalizado (selección manual de todo)
Selección [1-4]: 3

[PASO 2] Nombre del producto
  Nombre identificador (sin espacios, ej: mi-instituto): instituto-norte
  Nombre completo legible: Instituto Técnico del Norte

[PASO 3] Core Services (siempre activos en todos los productos)
  ✓ personas    — gestión de personas con validación de cédula
  ✓ cursos      — gestión de cursos académicos
  ✓ periodos    — gestión de periodos académicos
  → Estos no son configurables. Siempre se incluyen.

[PASO 4] Optional Features
  Plantilla "technical" sugiere estos valores por defecto.
  Presiona Enter para aceptar, o escribe s/n para cambiar.

  attendance   — Control de asistencia diaria    [defecto: n] →
  grading      — Registro de calificaciones      [defecto: s] →
  enrollment   — Gestión de matrículas           [defecto: s] →
  schedule     — Horarios de clases              [defecto: s] →
  reports      — Reportes académicos             [defecto: s] →
  certificates — Certificados de aprobación      [defecto: n] →

[PASO 5] Parámetros académicos
  Escala de evaluación (numeric/literal)  [defecto: numeric] →
  Periodos por año (1-4)                  [defecto: 2] →
  Nota mínima aprobatoria (0-10)          [defecto: 7.0] →
  Porcentaje mínimo asistencia (0-100)    [defecto: 70.0] →
  Máximo materias por periodo (1-20)      [defecto: 5] →

[PASO 6] Usuario administrador inicial
  Email: admin@instituto-norte.local
  Password: ••••••••

[PASO 7] Puerto para el backend
  Puerto [defecto: 8001]: 8004

══════════════════════════════════════════════
Generando estructura del producto...

  ✓ Carpeta creada:  products/instituto-norte/
  ✓ Carpeta creada:  products/instituto-norte/overrides/
  ✓ Carpeta creada:  products/instituto-norte/logs/
  ✓ .env generado:   products/instituto-norte/.env
  ✓ Config generada: products/instituto-norte/product_config.yaml
  ✓ Config válida:   schema_loader OK
  ✓ BD migrada:      products/instituto-norte/instituto-norte.db
  ✓ Datos sembrados: 1 usuario admin creado

══════════════════════════════════════════════
Producto listo: instituto-norte
  Tipo:     technical
  Features: grading, enrollment, schedule, reports
  BD:       products/instituto-norte/instituto-norte.db
  Puerto:   8004

¿Levantar el producto ahora? [s/n]: s

  Iniciando backend...
  Backend corriendo: http://localhost:8004
  Swagger UI:        http://localhost:8004/docs
  (Ctrl+C para detener)
```

---

## 9. La estructura de carpetas que crea el Scaffolder

Para un producto llamado `instituto-norte`:

```
products/
└── instituto-norte/
    ├── product_config.yaml      ← generado, nunca editado a mano
    ├── .env                     ← generado por el Workbench
    ├── instituto-norte.db       ← creado por migrate.py
    ├── overrides/               ← vacío, para customizaciones futuras
    └── logs/                    ← carpeta de logs
```

### El .env generado debe verse así:
```env
# Generado automáticamente por Academic SPL Workbench
# NO editar manualmente — usar: python workbench/assemble.py
# Producto: instituto-norte
# Tipo: technical
# Generado: 2025-07-17 10:30:00

PRODUCT_CONFIG_PATH=products/instituto-norte/product_config.yaml
PRODUCT_NAME=instituto-norte
PRODUCT_TYPE=technical
DB_PATH=products/instituto-norte/instituto-norte.db
BACKEND_PORT=8004
LOG_LEVEL=info
ENVIRONMENT=development
```

---

## 10. Integración con el sistema existente

### Cómo se levanta un producto después de ensamblarlo

El `.env` generado se usa directamente con uvicorn:

```powershell
# En Windows, cargar el .env y levantar:
Get-Content products/instituto-norte/.env |
  Where-Object { $_ -notmatch '^#' -and $_ -match '=' } |
  ForEach-Object {
    $key, $value = $_ -split '=', 2
    [System.Environment]::SetEnvironmentVariable($key.Trim(), $value.Trim())
  }
.venv\Scripts\python.exe -m uvicorn run_app:app --port 8004 --reload
```

O más simple, el propio `assemble.py` puede leer el `.env` y levantar
el proceso directamente desde Python.

### Cómo se integra con los comandos existentes

El Scaffolder llama internamente a los scripts ya existentes:
- `core_assets/backend/core_engine/persistence/migrate.py` → migraciones
- `core_assets/backend/core_engine/persistence/seeder.py` → datos iniciales
- `core_assets/backend/core_engine/config/schema_loader.py` → validación

No duplica lógica — la reutiliza. Eso es exactamente el principio SPLE.

---

## 11. Reglas que el Workbench debe respetar

1. **No crea ni modifica nada dentro de `core_assets/`** — solo crea
   dentro de `products/<nombre-producto>/`.
2. **Siempre valida el YAML generado** con `schema_loader.py` antes de
   continuar. Si falla, muestra el error y detiene el proceso.
3. **Es idempotente con advertencia**: si el producto ya existe,
   pregunta antes de sobreescribir.
4. **Nunca hardcodea nombres de producto** dentro de su propio código
   — recibe todo como parámetros.
5. **El product_config.yaml generado debe ser 100% válido** y
   funcionalmente equivalente a los que ya existen para los 3 productos.

---

## 12. Tareas en Linear asociadas (referencia)

| ID | Título |
|---|---|
| WB-01 | Construir `product_templates.py`: plantillas por tipo de institución |
| WB-02 | Construir `scaffolder.py`: generador de estructura, .env y product_config.yaml |
| WB-03 | Construir `assemble.py`: CLI interactivo de ensamblaje paso a paso |

---

## 13. Lo que necesito de ti en este chat

1. Construye los 3 archivos en orden: primero `product_templates.py`,
   luego `scaffolder.py`, luego `assemble.py`.
2. Dámelos **archivo por archivo**, con el contenido completo listo
   para copiar y pegar. No pseudocódigo.
3. Después de cada archivo, dime exactamente qué comando correr para
   verificar que funciona antes de pasar al siguiente.
4. El CLI debe funcionar en **Windows con PowerShell** (el equipo
   trabaja en Windows). Ten en cuenta las rutas con `\` vs `/` y
   que el comando para limpiar pantalla es `cls`, no `clear`.
5. Para la selección de features en el Paso 4, usa una interfaz
   simple de texto (no librerías externas como `inquirer` o `rich`
   — solo `input()` estándar de Python), para evitar problemas de
   instalación.
6. El producto generado debe poder levantarse inmediatamente después
   del ensamblaje y mostrar el Swagger UI con los endpoints correctos.
7. Si ves alguna inconsistencia entre lo que describo y los principios
   SPLE, corrígeme antes de implementar.
