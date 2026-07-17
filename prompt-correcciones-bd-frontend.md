# CORRECCIONES ARQUITECTÓNICAS — BD Selectiva y Ensamblaje Frontend

Tengo dos problemas arquitectónicos en mi proyecto SPLE que necesito
corregir. Te explico cada uno con lo que tengo actualmente y lo que
debe quedar.

---

## Contexto mínimo necesario

Es una Línea de Productos de Software académica. El Core Engine es
FastAPI + SQLAlchemy. El frontend es un único proyecto Laravel
compartido por todos los productos. El ensamblaje lo hace un script
`workbench.py`.

**Regla de oro:** `core_assets/` no puede leer configuración de
ningún producto específico. `models.py` es un Core Asset.

---

## PROBLEMA 1 — Base de datos selectiva

### Qué tengo actualmente (incorrecto)

`models.py` lee el `product_config.yaml` antes de declarar las
clases y usa bloques `if flags.is_active(...)` para declarar o no
declarar modelos opcionales:

```python
# INCORRECTO — models.py leyendo configuración
flags = FeatureFlags(os.environ["PRODUCT_CONFIG_PATH"])

class PersonaDB(Base):  # siempre
    ...

if flags.is_active("certificates"):
    class CertificadoDB(Base):  # solo si está activo
        ...
```

**Por qué es incorrecto:** `models.py` es un Core Asset y no puede
importar ni leer configuración de productos. Acopla el ORM al sistema
de variabilidad, rompe si el YAML tiene un error, y hace el código
impredecible.

### Qué debe quedar (correcto)

La solución correcta es mover la responsabilidad a `migrate.py`:
- `models.py` sigue siendo estático — declara TODOS los modelos
  posibles sin leer ningún config
- `migrate.py` recibe la ruta del `product_config.yaml`, lo lee,
  y llama a `create_all()` solo con las tablas que corresponden
  a los features activos del producto

```python
# CORRECTO — models.py estático
class PersonaDB(Base): ...      # siempre existe
class CertificadoDB(Base): ...  # siempre declarada, migrate decide si crearla

# CORRECTO — migrate.py selectivo
def run_migrations(db_path, config_path):
    flags = FeatureFlags(config_path)
    tablas = TABLAS_CORE.copy()  # siempre: personas, cursos, periodos
    if flags.is_active("certificates"):
        tablas.append(CertificadoDB.__table__)
    ...
    Base.metadata.create_all(engine, tables=tablas)
```

### Lo que necesito para el Problema 1

1. Reescribir `models.py` como archivo completamente estático,
   sin ningún import de configuración, declarando todos los modelos.
2. Reescribir `migrate.py` para que reciba tanto `db_path` como
   `config_path`, lea los features activos, y use
   `Base.metadata.create_all(engine, tables=[...])` pasando
   únicamente las tablas que corresponden.
3. Un mapeo explícito dentro de `migrate.py` que diga qué tablas
   pertenecen a qué feature:
   ```python
   FEATURE_TABLES = {
       "attendance": [AsistenciaDB.__table__],
       "grading":    [EvaluacionDB.__table__],
       "enrollment": [MatriculaDB.__table__],
       "schedule":   [HorarioDB.__table__],
       "reports":    [],   # usa tablas existentes, no tiene tabla propia
       "certificates": [CertificadoDB.__table__],
   }
   ```
4. Las tablas Core (personas, cursos, periodos, users) siempre
   se crean sin importar qué features estén activos.

---

## PROBLEMA 2 — Ensamblaje del frontend

### Qué tengo actualmente (incorrecto)

`workbench.py` copia físicamente la carpeta del Laravel Shell y
elimina los módulos no seleccionados:

```python
# INCORRECTO — clone-and-own
shutil.copytree("core_assets/frontend/laravel-shell", f"products/{nombre}/frontend")
for modulo in modulos_no_activos:
    shutil.rmtree(f"products/{nombre}/frontend/app/Modules/{modulo}")
```

**Por qué es incorrecto:** si hay un bug en `AttendanceController.php`
hay que corregirlo en cada copia. Una mejora en un componente Blade
hay que aplicarla en N carpetas. Eso es clone-and-own, el anti-patrón
que SPLE existe para eliminar.

### Qué debe quedar (correcto)

Un solo Laravel Shell en `core_assets/frontend/laravel-shell/`.
Todos los productos usan ese mismo código. Lo que varía por producto
es únicamente su archivo `.env`.

El Workbench genera dos cosas para el frontend:
1. Un `.env` de Laravel dentro de `products/<nombre>/` con la URL
   del backend correcto
2. Nada más — el código PHP no se toca ni se copia

```
products/
└── mi-instituto/
    ├── product_config.yaml    ← config del backend
    ├── .env.backend           ← variables del backend Python
    ├── .env.frontend          ← variables de Laravel (NUEVO)
    └── mi-instituto.db
```

### Cómo funciona el `.env.frontend`

```env
# Generado por workbench.py — NO editar manualmente
APP_NAME="Instituto del Norte"
APP_URL=http://localhost:8080
CORE_ENGINE_BACKEND_URL=http://localhost:8004
```

### Cómo se levanta Laravel apuntando al producto correcto

```powershell
# Copiar el .env del producto al Laravel Shell y levantar
copy products\mi-instituto\.env.frontend core_assets\frontend\laravel-shell\.env
cd core_assets\frontend\laravel-shell
php artisan config:clear
php artisan serve --port=8080
```

O el propio `workbench.py` puede hacer ese copy y levantar el proceso.

### Por qué esto funciona sin copiar código

El `FeatureGate.php` ya existente consulta al backend qué features
están activos y el menú de Laravel se muestra u oculta con
`@feature('nombre')`. El mismo Laravel Shell reacciona de forma
distinta según a qué backend apunta su `.env`. No necesita copias.

### Lo que necesito para el Problema 2

1. Modificar `workbench.py` para que **elimine** el bloque que
   copia `laravel-shell` y elimina módulos.
2. En su lugar, generar `products/<nombre>/.env.frontend` con:
   - `APP_NAME` = nombre legible del producto
   - `APP_URL` = `http://localhost:<puerto_frontend>`
   - `CORE_ENGINE_BACKEND_URL` = `http://localhost:<puerto_backend>`
3. Agregar al final del ensamblaje un bloque que ofrezca levantar
   el frontend copiando ese `.env.frontend` al Laravel Shell y
   corriendo `php artisan serve`.
4. Documentar en el output del CLI que el frontend es compartido:
   ```
   ✓ .env.frontend generado: products/mi-instituto/.env.frontend
   → El frontend Laravel es compartido (core_assets/frontend/laravel-shell)
   → Para levantar: copy products\mi-instituto\.env.frontend
                         core_assets\frontend\laravel-shell\.env
                    php artisan serve --port=8080
   ```

---

## Lo que necesito de ti

Corrígeme ambos problemas en orden. Primero el Problema 1
(`models.py` + `migrate.py`), luego el Problema 2 (`workbench.py`).
Código completo, listo para copiar y pegar, un archivo a la vez.
Después de cada archivo dime qué comando correr para verificar.
Entorno: Windows + PowerShell.
