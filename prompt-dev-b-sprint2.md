# PROMPT DEV B — Sprint 2 (Frontend Laravel)
# Copia y pega esto completo como primer mensaje en un chat nuevo

Actúa como un Arquitecto de Software experto en PHP (Laravel), diseño
de componentes Blade reutilizables, y Líneas de Productos de Software
(SPLE). También debes conocer cómo consumir APIs REST desde Laravel.

---

## Contexto del proyecto

Somos un equipo de 3 personas en un proyecto universitario. Estamos
construyendo una **Línea de Productos de Software (SPL)** para el
dominio académico. Esto significa que NO construimos una app fija —
construimos **Core Assets** reutilizables que permiten derivar múltiples
productos (Colegio Básico, Universidad Compleja) cambiando solo un
archivo de configuración YAML en el backend, sin tocar el código del Core.

**Regla de oro que nunca se puede violar:**
`core_assets/` no puede contener el nombre de ningún producto, ni
lógica condicional sobre productos. Toda diferencia de comportamiento
entre productos viene de la configuración.

---

## Stack tecnológico

- Backend: Python 3.12 + FastAPI (Dev A lo maneja — ya completado)
- Frontend: PHP 8.3 + Laravel 11
- La comunicación entre Laravel y FastAPI es HTTP REST
- DevOps: Docker + GitHub Actions (Sprint 3)

---

## Lo que YA está construido (Backend Sprint 2 — Dev A COMPLETADO)

El backend está 100% funcional. Dev B puede trabajar sin bloqueos.

### Endpoints disponibles

El backend corre en `http://127.0.0.1:8001/` (Colegio) y `8002/` (Universidad).

**Core Services — siempre disponibles en ambos productos:**
```
GET    /                              → info del producto, core_services y active_optional_features
GET    /periodos/                     → listar períodos académicos
POST   /periodos/                     → crear período {"nombre", "fecha_inicio", "fecha_fin"}
GET    /periodos/{id}                 → obtener período
PUT    /periodos/{id}                 → actualizar período
DELETE /periodos/{id}                 → eliminar período

GET    /cursos/                       → listar cursos (acepta ?periodo_id= para filtrar)
POST   /cursos/                       → crear curso {"nombre", "periodo_id"}
GET    /cursos/{id}                   → obtener curso
PUT    /cursos/{id}                   → actualizar curso
DELETE /cursos/{id}                   → eliminar curso

GET    /personas/                     → listar personas
POST   /personas/                     → crear persona {"nombres", "apellidos", "documento_identidad"}
GET    /personas/{id}                 → obtener persona
GET    /personas/por-documento/{doc}  → buscar por cédula
PUT    /personas/{id}                 → actualizar persona
DELETE /personas/{id}                 → eliminar persona
```

**Optional Features — dependen del product_config.yaml:**
```
GET    /grading/                      → lista de notas con "valor_display" (escala del producto)
POST   /grading/                      → crear nota {"curso_id", "persona_id", "valor", "observacion"}
GET    /grading/{id}                  → obtener nota por ID
DELETE /grading/{id}                  → eliminar nota

GET    /attendance/                   → registros + estadísticas (porcentaje, estado APROBADO/EN_RIESGO)
POST   /attendance/                   → registrar {"persona_id", "curso_id", "fecha", "presente", "justificacion"}
GET    /attendance/{id}               → obtener registro
DELETE /attendance/{id}               → eliminar registro

GET    /enrollment/                   → listar matrículas
POST   /enrollment/                   → crear matrícula {"persona_id", "curso_id"}
GET    /enrollment/{id}               → obtener matrícula
PATCH  /enrollment/{id}/status        → cambiar estado {"estado": "inscrito|aprobado|reprobado"}
DELETE /enrollment/{id}               → eliminar matrícula
```

### Comportamiento diferenciado por producto (la demo SPLE)

El endpoint `/` responde así:

**Colegio Básico (puerto 8001):**
```json
{
  "core_services": ["periodos", "cursos", "personas"],
  "active_optional_features": ["attendance", "grading", "enrollment"],
  "academic_settings": {"evaluation_scale": "literal"}
}
```

**Universidad Compleja (puerto 8002):**
```json
{
  "core_services": ["periodos", "cursos", "personas"],
  "active_optional_features": ["grading", "enrollment"],
  "academic_settings": {"evaluation_scale": "numeric"}
}
```

`GET /attendance/` devuelve 200 en colegio y **404** en universidad.
`GET /grading/` devuelve `"valor_display": "Muy Bueno"` en colegio y `"valor_display": 8.5` en universidad.

### Datos de prueba sembrados en el Colegio

El backend ya tiene datos de ejemplo en `colegio_basico.db`:
- Personas: P-001 (Ana García), P-002 (Luis Martínez), P-003 (María Rodríguez)
- Periodo: PER-2024-A (Año Escolar 2024)
- Cursos: C-MAT (Matemáticas), C-ESP (Español)

---

## Lo que YA existe en el frontend Laravel (Sprint 1)

```
core_assets/frontend/laravel-shell/
├── app/
│   ├── Core/Services/
│   │   └── FeatureGate.php      ← consulta al backend qué features están activos
│   ├── Providers/
│   │   └── FeatureGateServiceProvider.php  ← registra directiva @feature en Blade
│   ├── Http/Controllers/Auth/
│   │   └── LoginController.php  ← auth básica
│   └── Modules/
│       └── AttendanceModule/    ← módulo de ejemplo (patrón a replicar)
│           ├── Http/Controllers/AttendanceController.php  ← datos HARDCODEADOS aún
│           ├── resources/views/index.blade.php
│           └── routes.php
├── config/
│   └── core_engine.php          ← URL del backend (desde .env)
├── resources/views/
│   └── dashboard.blade.php      ← vista genérica con @feature()
└── routes/web.php
```

### FeatureGate.php — cómo funciona

```php
class FeatureGate {
    public static function isActive(string $featureName): bool {
        return in_array($featureName, self::activeFeatures(), true);
    }
    public static function productInfo(): array {
        return Cache::remember('core_engine_info', 30, function () {
            $response = Http::timeout(2)->get(config('core_engine.backend_url'));
            return $response->json();
        });
    }
    // NUEVO: también expone los Core Services (siempre activos)
    public static function coreServices(): array {
        return self::productInfo()['core_services'] ?? [];
    }
    public static function activeFeatures(): array {
        return self::productInfo()['active_optional_features'] ?? [];
    }
}
```

### La directiva @feature en Blade — ya registrada

```blade
@feature('attendance')
    <div>Este bloque SOLO aparece si attendance está activo</div>
@endfeature
```

---

## El problema actual del frontend

El `AttendanceController` existente devuelve datos hardcodeados:
```php
$sampleData = [
    ['persona' => 'P-001', 'curso' => 'C-001', 'presente' => true],
];
```

No hay llamada real al backend, no hay CRUD, no hay componentes
reutilizables — solo datos inventados.

---

## Tu trabajo en Sprint 2 (COR-17 a COR-21)

Eres **Dev B**. Tu responsabilidad es construir los **Core Assets de
frontend** de Laravel: el cliente HTTP reutilizable, los componentes
Blade genéricos, las vistas reales conectadas al backend, y el layout
con navegación condicional.

### Las tareas en orden de dependencia

**COR-17 — `CoreEngineClient.php`** (hacer primero — todo lo demás depende de esto)
- Archivo: `app/Core/Services/CoreEngineClient.php`
- Clase reutilizable con métodos:
  - `get(string $endpoint): array`
  - `post(string $endpoint, array $data): array`
  - `put(string $endpoint, array $data): array`
  - `patch(string $endpoint, array $data): array`
  - `delete(string $endpoint): array`
- Centraliza: URL base desde `config('core_engine.backend_url')`,
  timeout de 3 segundos, manejo de errores claro
- `FeatureGate.php` se refactoriza para usar esta clase
- Probar: `CoreEngineClient::get('/')` debe devolver el JSON real del backend

**COR-18 — Componente Blade `<x-data-table>`** (después de COR-17)
- Archivo: `resources/views/components/data-table.blade.php`
- Props: `$columns` (array de etiquetas), `$rows` (array de arrays de datos)
- Renderiza tabla HTML genérica y reutilizable
- **Nuevo requerimiento:** debe mostrar `valor_display` en la columna de nota
  (no `valor` directamente) — el backend ya diferencia entre numérico y literal
- Ejemplo de uso:
```blade
<x-data-table
    :columns="['Persona', 'Curso', 'Nota', 'Escala']"
    :rows="$registros"
/>
```

**COR-19 — Componente Blade `<x-entity-form>`** (después de COR-17)
- Archivo: `resources/views/components/entity-form.blade.php`
- Props: `$fields`, `$action`, `$submitLabel`
- Reutilizable para: crear Persona, crear Nota, registrar Asistencia
- Ejemplo de uso para crear persona:
```blade
<x-entity-form
    :fields="[
        ['name' => 'nombres', 'type' => 'text', 'label' => 'Nombres'],
        ['name' => 'apellidos', 'type' => 'text', 'label' => 'Apellidos'],
        ['name' => 'documento_identidad', 'type' => 'text', 'label' => 'Cedula (10 digitos)']
    ]"
    action="/personas"
    submitLabel="Registrar Persona"
/>
```

**COR-20 — Vistas reales de los 5 módulos** (después de COR-17, COR-18, COR-19)

Ahora hay más módulos que antes porque el backend tiene Core Services:

- **PersonasModule** (Core Service — siempre visible):
  - `PersonasController`: index() lista personas, store() crea persona
  - Vista: tabla con `<x-data-table>` + formulario de registro con `<x-entity-form>`
  - **Nota:** el backend valida cédula ecuatoriana — mostrar error 409 al usuario si es inválida

- **GradingModule** (Optional Feature):
  - `GradingController`: index() + store()
  - Vista: tabla que muestra `valor_display` (puede ser "Muy Bueno" o 8.5 según producto)
  - La primera línea del controlador SIEMPRE:
    ```php
    abort_unless(FeatureGate::isActive('grading'), 404);
    ```

- **AttendanceModule** (ya existe, refactorizar):
  - Reemplazar el array hardcodeado por llamada real a `CoreEngineClient::get('/attendance/')`
  - **Nuevo:** mostrar las estadísticas que devuelve el backend:
    `estadisticas.porcentaje_asistencia` y `estadisticas.estado`

- **EnrollmentModule** (Optional Feature):
  - `EnrollmentController`: index() + store() + updateStatus()
  - Vista: tabla + formulario + botón para cambiar estado de matrícula

- **CursosModule** (Core Service — puede ser solo lectura en el frontend):
  - `CursosController`: index() — lista cursos (útil para los dropdowns de los formularios)

**COR-21 — Layout base con navegación condicional** (hacer último)
- Archivo: `resources/views/layouts/app.blade.php`
- Siempre visible (Core Services):
```blade
<a href="/personas">Personas</a>
<a href="/cursos">Cursos</a>
```
- Condicional por producto (Optional Features):
```blade
@feature('grading')
    <a href="/grading">Calificaciones</a>
@endfeature
@feature('attendance')
    <a href="/attendance">Asistencia</a>
@endfeature
@feature('enrollment')
    <a href="/enrollment">Matriculas</a>
@endfeature
```
- Muestra el nombre del producto activo desde `FeatureGate::productInfo()['product']`

---

## Configuración del proyecto Laravel

```env
# .env
CORE_ENGINE_BACKEND_URL=http://127.0.0.1:8001/
```

```php
// bootstrap/providers.php
App\Providers\FeatureGateServiceProvider::class,
```

Para probar contra Universidad (puerto 8002):
```env
CORE_ENGINE_BACKEND_URL=http://127.0.0.1:8002/
```
La navegación condicional ocultará automáticamente "Asistencia" sin tocar código.

---

## Lo que necesito de ti en este chat

1. Guíame paso a paso comenzando por COR-17 (`CoreEngineClient.php`),
   con el código completo listo para pegar — no pseudocódigo.
2. Para cada componente Blade, dame también un ejemplo de vista completa
   que lo use, para poder probarlo en el navegador.
3. Después de cada tarea, dime qué URL abrir en el navegador para verificar.
4. Recuérdame siempre que ningún controlador puede tener datos hardcodeados.
5. Al implementar PersonasModule: el backend puede devolver error 409 si la
   cédula es inválida — el formulario debe mostrar ese error al usuario.
6. El código debe funcionar con Laravel 11 (la versión actual).
