# PROMPT DEV B — Sprint 2 (Frontend Laravel)
# Copia y pega esto completo como primer mensaje en un chat nuevo

Actúa como un Arquitecto de Software experto en PHP (Laravel 11),
diseño de componentes Blade reutilizables y Líneas de Productos de
Software (SPLE). También debes conocer cómo consumir APIs REST desde
Laravel con el cliente HTTP de Laravel.

---

## Contexto del proyecto

Somos un equipo de 3 personas en un proyecto universitario. Estamos
construyendo una **Línea de Productos de Software (SPL)** para el
dominio académico. Construimos **Core Assets** reutilizables que
permiten derivar múltiples productos (Colegio Básico, Universidad
Compleja, Instituto Técnico Nocturno) cambiando solo un archivo de
configuración YAML en el backend, sin tocar el código del Core.

**Regla de oro que nunca se puede violar:**
`core_assets/` no puede contener el nombre de ningún producto ni
lógica condicional sobre productos. Toda diferencia de comportamiento
entre productos viene de la configuración.

---

## Stack tecnológico

- Backend: Python 3.12 + FastAPI (Dev A lo maneja — COMPLETADO)
- Frontend: PHP 8.3 + Laravel 11
- Comunicación: HTTP REST
- DevOps: Docker + GitHub Actions (Sprint 3)

---

## Lo que YA está construido — Backend Sprint 2 COMPLETADO

### Productos disponibles

| Puerto | Producto | academic_settings |
|---|---|---|
| 8001 | Colegio Básico | scale=literal, passing=7.0, attendance_min=80%, max_enroll=8 |
| 8002 | Universidad Compleja | scale=numeric, passing=6.0, attendance_min=75%, max_enroll=6 |
| 8003 | Instituto Técnico | scale=numeric, passing=7.0, attendance_min=70%, max_enroll=5 |

### Los 5 Core Assets de lógica de negocio

Estos assets ya están implementados en el backend y afectan las respuestas:

**CA-01 CedulaValidator** — `POST /personas/` valida la cédula antes de guardar.
- Cédula inválida → HTTP 409 con `{"detail": "El documento '...' no es válido..."}`

**CA-02 GradeScaleConverter** — `GET /grading/` tiene campo extra `valor_display`:
- Colegio (literal): `"valor_display": "Muy Bueno"` para nota 8.5
- Universidad (numeric): `"valor_display": 8.5` para nota 8.5

**CA-03 AttendanceCalculator** — `GET /attendance/` tiene campo `estadisticas`:
```json
{
  "estadisticas": {
    "total_registros": 10,
    "total_presentes": 8,
    "total_ausentes": 2,
    "porcentaje_asistencia": 80.0,
    "estado": "APROBADO",
    "umbral_aprobado": 80.0,
    "umbral_riesgo": 70.0
  },
  "resumen_por_persona": [...]
}
```

**CA-04 GradePassingChecker** — cada nota en `GET /grading/` tiene:
```json
{
  "valor": 6.5,
  "valor_display": "Bueno",
  "aprueba": false,
  "estado_aprobacion": "REPROBADO"
}
```
Ese mismo 6.5 en universidad: `"aprueba": true`, `"estado_aprobacion": "APROBADO"`.

**CA-05 EnrollmentLimitChecker** — `POST /enrollment/` puede devolver HTTP 409:
```json
{"detail": "El estudiante 'P-001' ya tiene 5 materia(s) inscrita(s). El limite configurado es 5."}
```

### Todos los endpoints disponibles

**Core Services (SIEMPRE activos, todos los productos):**
```
GET    /                                  → diagnóstico: core_services, active_optional_features, academic_settings
GET/POST/PUT/DELETE /periodos/{id}        → gestión de períodos
GET/POST/PUT/DELETE /cursos/{id}          → gestión de cursos (acepta ?periodo_id=)
GET/POST/PUT/DELETE /personas/{id}        → gestión de personas (CA-01 valida cédula)
GET                 /personas/por-documento/{doc} → buscar por cédula
```

**Optional Features (dependen del YAML del producto):**
```
GET    /grading/            → lista notas con valor_display (CA-02) + aprueba/estado_aprobacion (CA-04)
POST   /grading/            → {"curso_id", "persona_id", "valor" (0-10), "observacion"}
GET    /grading/{id}        → nota individual
DELETE /grading/{id}        → eliminar nota

GET    /attendance/         → registros + estadisticas completas (CA-03) + resumen_por_persona
POST   /attendance/         → {"persona_id", "curso_id", "fecha", "presente", "justificacion"}
DELETE /attendance/{id}     → eliminar registro

GET    /enrollment/         → listar matrículas
POST   /enrollment/         → {"persona_id", "curso_id"} ← puede dar 409 si límite superado (CA-05)
PATCH  /enrollment/{id}/status → {"estado": "inscrito|retirado|aprobado|reprobado"}
DELETE /enrollment/{id}     → eliminar matrícula

GET    /schedule/           → listar horarios agrupados por día
POST   /schedule/           → crear horario
GET    /schedule/{curso_id} → horario de un curso
DELETE /schedule/{id}       → eliminar horario

GET    /reports/            → config del producto y lista de estudiantes
GET    /reports/rendimiento/{persona_id} → reporte detallado (notas + asistencia)
GET    /reports/consolidado/ → tabla de estados de todos los estudiantes

GET    /certificates/       → listar certificados emitidos/rechazados
POST   /certificates/{persona_id}/generate → verifica CA-03/CA-04 y emite/rechaza
GET    /certificates/persona/{persona_id} → historial de un estudiante
```

### Datos sembrados en Colegio (puerto 8001)

- Personas: P-001 (Ana García), P-002 (Luis Martínez), P-003 (María Rodríguez)
- Período: PER-2024-A (Año Escolar 2024)
- Cursos: C-MAT (Matemáticas), C-ESP (Español)

### Datos sembrados en Técnico (puerto 8003)

- Personas: T-001 (Roberto Vega), T-002 (Carmen Flores)
- Períodos: SEM-2024-A, SEM-2024-B
- Cursos: T-PROG (Programación), T-REDES (Redes), T-BD (Bases de Datos)

---

## Lo que YA existe en el frontend Laravel (Sprint 1)

```
core_assets/frontend/laravel-shell/
├── app/
│   ├── Core/Services/
│   │   └── FeatureGate.php        ← consulta al backend qué features están activos
│   ├── Providers/
│   │   └── FeatureGateServiceProvider.php  ← registra directiva @feature en Blade
│   ├── Http/Controllers/Auth/
│   │   └── LoginController.php    ← auth básica
│   └── Modules/
│       └── AttendanceModule/
│           ├── Http/Controllers/AttendanceController.php  ← datos HARDCODEADOS (a reemplazar)
│           ├── resources/views/index.blade.php
│           └── routes.php
├── config/
│   └── core_engine.php            ← URL del backend (desde .env)
├── resources/views/
│   └── dashboard.blade.php        ← vista genérica con @feature()
└── routes/web.php
```

### FeatureGate.php — cómo funciona

```php
class FeatureGate {
    public static function isActive(string $featureName): bool {
        return in_array($featureName, self::activeFeatures(), true);
    }
    public static function activeFeatures(): array {
        return self::productInfo()['active_optional_features'] ?? [];
    }
    public static function productInfo(): array {
        return Cache::remember('core_engine_info', 30, function () {
            $response = Http::timeout(2)->get(config('core_engine.backend_url'));
            return $response->json();
        });
    }
    public static function academicSetting(string $key, $default = null) {
        return self::productInfo()['academic_settings'][$key] ?? $default;
    }
}
```

### Directiva @feature en Blade

```blade
@feature('attendance')
    <div>Este bloque SOLO aparece si attendance está activo</div>
@endfeature
```

---

## Tu trabajo en Sprint 2 (COR-17 a COR-21)

Eres **Dev B**. Tu responsabilidad es construir los Core Assets de
frontend de Laravel: cliente HTTP reutilizable, componentes Blade
genéricos, vistas reales conectadas al backend, y layout con
navegación condicional.

### COR-17 — `CoreEngineClient.php` (hacer PRIMERO — todo lo demás depende de esto)

**Archivo:** `app/Core/Services/CoreEngineClient.php`

Clase reutilizable con métodos:
```php
class CoreEngineClient {
    private string $baseUrl;

    public function __construct() {
        $this->baseUrl = rtrim(config('core_engine.backend_url'), '/');
    }

    public function get(string $endpoint): array { ... }
    public function post(string $endpoint, array $data): array { ... }
    public function put(string $endpoint, array $data): array { ... }
    public function patch(string $endpoint, array $data): array { ... }
    public function delete(string $endpoint): array { ... }
}
```

Requisitos:
- URL base desde `config('core_engine.backend_url')`
- Timeout de 3 segundos en todos los métodos
- Manejo de errores: si el backend devuelve 4xx/5xx, relanzar con mensaje claro
- `FeatureGate.php` debe refactorizarse para usar esta clase internamente

Prueba de verificación:
```php
$client = new CoreEngineClient();
$info = $client->get('/');
dd($info['active_optional_features']); // ['attendance', 'grading', 'enrollment'] en colegio
```

---

### COR-18 — Componente Blade `<x-data-table>` (después de COR-17)

**Archivo:** `resources/views/components/data-table.blade.php`

Props:
- `$columns` — array de etiquetas de columnas
- `$rows` — array de arrays con los datos
- `$emptyMessage` — mensaje cuando no hay datos (opcional)

Debe mostrar un badge de color para campos especiales:
- `estado_aprobacion`: verde para "APROBADO", rojo para "REPROBADO"
- `estado` en attendance: verde APROBADO, amarillo EN_RIESGO, rojo REPROBADO_FALTA
- `aprueba`: ✅ / ❌

Uso de ejemplo:
```blade
<x-data-table
    :columns="['Persona', 'Curso', 'Nota', 'Escala', 'Aprueba', 'Estado']"
    :rows="$notas"
    emptyMessage="No hay calificaciones registradas"
/>
```

---

### COR-19 — Componente Blade `<x-entity-form>` (después de COR-17)

**Archivo:** `resources/views/components/entity-form.blade.php`

Props:
- `$fields` — array de definición de campos
- `$action` — URL de destino del formulario
- `$method` — GET/POST (default POST)
- `$submitLabel` — texto del botón

Tipos de campo soportados: `text`, `number`, `date`, `select`, `checkbox`

Uso para crear persona:
```blade
<x-entity-form
    :fields="[
        ['name' => 'nombres', 'type' => 'text', 'label' => 'Nombres', 'required' => true],
        ['name' => 'apellidos', 'type' => 'text', 'label' => 'Apellidos', 'required' => true],
        ['name' => 'documento_identidad', 'type' => 'text', 'label' => 'Cédula (10 dígitos)', 'required' => true]
    ]"
    action="/personas"
    submitLabel="Registrar Persona"
/>
```

Uso para registrar nota:
```blade
<x-entity-form
    :fields="[
        ['name' => 'persona_id', 'type' => 'select', 'label' => 'Estudiante', 'options' => $personas],
        ['name' => 'curso_id', 'type' => 'select', 'label' => 'Curso', 'options' => $cursos],
        ['name' => 'valor', 'type' => 'number', 'label' => 'Nota (0-10)', 'min' => 0, 'max' => 10, 'step' => '0.1'],
        ['name' => 'observacion', 'type' => 'text', 'label' => 'Observación']
    ]"
    action="/grading"
    submitLabel="Registrar Nota"
/>
```

---

### COR-20 — Vistas reales de los 6 módulos (después de COR-17, COR-18, COR-19)

#### PersonasModule (Core Service — siempre visible)

**Archivo:** `app/Modules/PersonasModule/Http/Controllers/PersonasController.php`

```php
class PersonasController extends Controller {
    public function index() {
        $personas = CoreEngineClient::get('/personas/');
        return view('personas.index', compact('personas'));
    }

    public function store(Request $request) {
        try {
            CoreEngineClient::post('/personas/', $request->all());
            return redirect('/personas')->with('success', 'Persona registrada');
        } catch (\Exception $e) {
            // El backend devuelve 409 si la cédula es inválida o duplicada
            return back()->withErrors(['documento' => $e->getMessage()]);
        }
    }
}
```

Vista: tabla con `<x-data-table>` + formulario `<x-entity-form>`.
**Importante:** mostrar el error 409 del backend si la cédula es inválida.

#### GradingModule (Optional Feature)

```php
class GradingController extends Controller {
    public function index() {
        abort_unless(FeatureGate::isActive('grading'), 404);
        $response = CoreEngineClient::get('/grading/');
        $notas = $response['data'];
        $scale = $response['evaluation_scale_used'];
        $passing = $response['passing_grade_used'];
        return view('grading.index', compact('notas', 'scale', 'passing'));
    }
}
```

Vista debe mostrar:
- `valor_display` en la columna de nota (CA-02 — puede ser "Muy Bueno" o 8.5)
- Badge `estado_aprobacion` (CA-04 — APROBADO/REPROBADO, color según valor)
- El `passing_grade_used` en el encabezado: "Nota mínima para aprobar: 7.0"

#### AttendanceModule (Optional Feature — REFACTORIZAR el existente)

Reemplazar los datos hardcodeados por llamada real. Vista debe mostrar:
- Las estadísticas de CA-03: `porcentaje_asistencia`, `estado`, `umbral_aprobado`
- El resumen por persona con su estado individual
- Sección de estadísticas globales visible antes de la tabla

```php
abort_unless(FeatureGate::isActive('attendance'), 404);
$response = CoreEngineClient::get('/attendance/');
$estadisticas = $response['estadisticas'];
$resumen = $response['resumen_por_persona'];
$registros = $response['data'];
```

#### EnrollmentModule (Optional Feature)

```php
abort_unless(FeatureGate::isActive('enrollment'), 404);

// En store():
try {
    CoreEngineClient::post('/enrollment/', $request->all());
} catch (\Exception $e) {
    // HTTP 409 = límite de materias superado (CA-05)
    return back()->withErrors(['limite' => $e->getMessage()]);
}
```

Vista incluye botones para cambiar estado: `PATCH /enrollment/{id}/status`.

#### CursosModule (Core Service — útil para dropdowns)

```php
// Devuelve lista de cursos para llenar <select> en otros formularios
$cursos = CoreEngineClient::get('/cursos/');
// Con filtro por período:
$cursos = CoreEngineClient::get('/cursos/?periodo_id=PER-2024-A');
```

#### ScheduleModule (Optional Feature — si está activo)

```php
abort_unless(FeatureGate::isActive('schedule'), 404);
$horarios = CoreEngineClient::get('/schedule/');
```

Vista funcional: Muestra los horarios agrupados por día de la semana e incluye formulario para asignar aula.

#### ReportsModule (Optional Feature)

```php
abort_unless(FeatureGate::isActive('reports'), 404);
$data = CoreEngineClient::get('/reports/consolidado/');
// Contiene la tabla con todos los estudiantes y su estado_final
```

#### CertificatesModule (Optional Feature)

```php
abort_unless(FeatureGate::isActive('certificates'), 404);
$response = CoreEngineClient::post('/certificates/' . $id . '/generate');
// Muestra si fue emitido o rechazado y el motivo_rechazo.
```

---

### COR-21 — Layout base con navegación condicional (hacer ÚLTIMO)

**Archivo:** `resources/views/layouts/app.blade.php`

```blade
<nav>
    {{-- Core Services: siempre visibles --}}
    <a href="/personas">Personas</a>
    <a href="/cursos">Cursos</a>
    <a href="/periodos">Períodos</a>

    {{-- Optional Features: condicionales según el producto activo --}}
    @feature('grading')
        <a href="/grading">Calificaciones</a>
    @endfeature

    @feature('attendance')
        <a href="/attendance">Asistencia</a>
    @endfeature

    @feature('enrollment')
        <a href="/enrollment">Matrículas</a>
    @endfeature

    @feature('schedule')
        <a href="/schedule">Horarios</a>
    @endfeature

    @feature('reports')
        <a href="/reports">Reportes</a>
    @endfeature

    @feature('certificates')
        <a href="/certificates">Certificados</a>
    @endfeature

    {{-- Nombre del producto activo --}}
    <span class="product-name">
        {{ \App\Core\Services\FeatureGate::productInfo()['product'] ?? 'Producto' }}
    </span>
</nav>
```

---

## Configuración del proyecto Laravel

```env
# .env — apuntar a cualquier producto cambiando solo el puerto
CORE_ENGINE_BACKEND_URL=http://127.0.0.1:8001/
```

**Prueba de variabilidad completa:**
1. `.env` apunta al colegio (8001) → navega a `/grading` → notas como "Muy Bueno", "Bueno"
2. Cambia a universidad (8002) → navega a `/grading` → notas como 8.5, 6.0
3. Navega a `/attendance` en colegio → funciona
4. Navega a `/attendance` en universidad → 404 (el menú tampoco lo muestra)

---

## Lo que necesito de ti en este chat

1. Empieza por **COR-17** (`CoreEngineClient.php`) — código completo listo para pegar.
2. Para cada componente Blade, dame también la vista completa de ejemplo.
3. En GradingModule: mostrar `passing_grade_used` del backend, y `estado_aprobacion` con badge de color.
4. En AttendanceModule: mostrar las `estadisticas` del CA-03 en una card resumen antes de la tabla.
5. En EnrollmentModule: mostrar el error 409 (límite CA-05) de forma amigable.
6. El layout debe usar `@feature` con los 6 features disponibles.
7. Verificar que el código funciona con **Laravel 11**.
8. Recuérdame siempre: ningún controlador puede tener datos hardcodeados.
