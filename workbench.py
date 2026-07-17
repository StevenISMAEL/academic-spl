import os
import sys
import shutil
import yaml
import subprocess
import string

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

console = Console()

PRODUCT_TEMPLATES = {
    "colegio": {
        "fixed": ["grading", "attendance", "enrollment", "reports"],
        "blocked": ["certificates"],
        "variables": ["schedule", "auditing"],
        "defaults": {
            "evaluation_scale": "numeric",
            "grading_max_value": 10,
            "passing_grade": 7.0,
            "attendance_min_percentage": 80.0,
            "max_enrollments_per_period": 12,
            "periods_per_year": 3
        }
    },
    "universidad": {
        "fixed": ["grading", "enrollment", "schedule", "certificates"],
        "blocked": [],
        "variables": ["attendance", "reports", "auditing"],
        "defaults": {
            "evaluation_scale": "numeric",
            "grading_max_value": 10,
            "passing_grade": 6.0,
            "attendance_min_percentage": 60.0,
            "max_enrollments_per_period": 6,
            "periods_per_year": 2
        }
    },
    "instituto": {
        "fixed": ["grading", "enrollment", "certificates"],
        "blocked": [],
        "variables": ["attendance", "schedule", "reports", "auditing"],
        "defaults": {
            "evaluation_scale": "numeric",
            "grading_max_value": 20,
            "passing_grade": 14.0,
            "attendance_min_percentage": 75.0,
            "max_enrollments_per_period": 8,
            "periods_per_year": 2
        }
    }
}

def generate_main_factory(selected_features: dict, product_name: str) -> str:
    """Genera dinámicamente el código fuente de main_factory.py para el producto derivado."""
    
    imports = []
    registry_entries = []
    
    # Optional features routing setup
    for feature, is_active in selected_features.items():
        if is_active:
            imports.append(f"from core_engine.features.{feature}.router import router as {feature}_router")
            registry_entries.append(f'    "{feature}": {feature}_router,')
            
    imports_str = "\n".join(imports)
    registry_str = "\n".join(registry_entries)

    # Template
    return f'''"""
Core Asset — Application Factory (Derivado)
Generado por el SPL Workbench.
"""
from __future__ import annotations

import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Cargar variables de entorno del producto (.env)
load_dotenv()

from core_engine.config.feature_flags import FeatureFlags

# ── Core Services (Commonality) ───────────────────────────────────────────────
from core_engine.features.periodos.router import router as periodos_router
from core_engine.features.cursos.router import router as cursos_router
from core_engine.features.personas.router import router as personas_router

# Autenticación temporalmente deshabilitada o importada
# from core_engine.features.auth.router import router as auth_router

# ── Optional Features Seleccionados (Variabilidad) ────────────────────────────
{imports_str}

FEATURE_REGISTRY = {{
{registry_str}
}}

CORE_SERVICES = [
    periodos_router,
    cursos_router,
    personas_router,
    # auth_router,
]

def create_app(config_path: str | None = None) -> FastAPI:
    resolved_path = config_path or os.environ.get("PRODUCT_CONFIG_PATH") or "product_config.yaml"
    flags = FeatureFlags(resolved_path)

    app = FastAPI(
        title="{product_name}",
        description="Producto derivado mediante Composición (Workbench).",
        version="1.0.0",
    )

    app.state.feature_flags = flags

    # Montar Core Services
    for core_router in CORE_SERVICES:
        app.include_router(core_router)

    # Montar Optional Features físicamente presentes
    for feature_name, router in FEATURE_REGISTRY.items():
        if flags.is_active(feature_name):
            app.include_router(router)

    @app.get("/", tags=["core"])
    def product_info():
        return {{
            "product": flags.product_name(),
            "core_services": ["periodos", "cursos", "personas"],
            "active_optional_features": list(FEATURE_REGISTRY.keys()),
            "academic_settings": flags.get_setting("academic_settings", default={{}}),
        }}

    return app
'''

def main():
    console.print(Panel.fit("[bold cyan]Academic SPL — Ensamblador v2.0[/bold cyan]", border_style="cyan"))
    
    product_id = questionary.text("Paso 1 — Identificador del producto (ej. mi-universidad):").ask()
    if not product_id:
        return
    product_id = product_id.replace(" ", "-").lower()

    # Detect if already exists
    base_dir = os.path.join("derived_products", product_id)
    config_path = os.path.join(base_dir, "backend", "product_config.yaml")
    
    existing_config = None
    if os.path.exists(config_path):
        console.print(f"\n[bold yellow]¡Producto '{product_id}' detectado![/bold yellow] Cargando configuración existente...")
        with open(config_path, "r", encoding="utf-8") as f:
            existing_config = yaml.safe_load(f)
            
        product_name = existing_config.get("metadata", {}).get("product_name", product_id)
        product_type = existing_config.get("metadata", {}).get("product_type", "instituto")
        console.print(f"[green]Nombre oficial:[/green] {product_name}")
        console.print(f"[green]Tipo de institución:[/green] {product_type}\n")
    else:
        product_type = questionary.select(
            "Paso 2 — ¿Qué línea de producto deseas crear?",
            choices=["colegio", "universidad", "instituto"]
        ).ask()
        if not product_type: return
        
        product_name = questionary.text("Paso 3 — Nombre oficial de la institución:").ask()
        if not product_name: return

    template = PRODUCT_TEMPLATES.get(product_type, PRODUCT_TEMPLATES["instituto"])
    features = {}
    
    # Procesar features fijos y bloqueados
    for f in template["fixed"]:
        features[f] = True
    for f in template["blocked"]:
        features[f] = False

    console.print("\n[bold]Paso 4 — Assets disponibles para este tipo de producto:[/bold]")
    console.print("  [dim]Core Services (siempre activos):[/dim]")
    console.print("    [green]✓[/green] personas    — gestión de personas")
    console.print("    [green]✓[/green] cursos      — gestión de cursos")
    console.print("    [green]✓[/green] periodos    — gestión de periodos\n")

    # Optional features via checkbox
    choices = []
    feature_labels = {
        'grading': "grading        — calificaciones",
        'attendance': "attendance     — control de asistencia",
        'enrollment': "enrollment     — matrículas/inscripciones",
        'schedule': "schedule       — horarios",
        'reports': "reports        — reportes académicos",
        'certificates': "certificates   — certificados",
        'auditing': "auditing       — auditoría de seguridad"
    }

    for f in template["variables"]:
        checked = False
        if existing_config and "features" in existing_config:
            checked = existing_config["features"].get(f, False)
            
        choices.append(questionary.Choice(title=feature_labels.get(f, f), value=f, checked=checked))

    selected_options = questionary.checkbox(
        "Optional Features (selecciona con Espacio y confirma con Enter):",
        choices=choices
    ).ask()
    
    if selected_options is None: return

    for f in template["variables"]:
        features[f] = (f in selected_options)

    # Parametros Academicos
    console.print("\n[bold]Paso 5 — Parámetros académicos:[/bold]")
    defs = template["defaults"]
    if existing_config and "academic_settings" in existing_config:
        defs = {**defs, **existing_config["academic_settings"]}

    academic_settings = {}
    
    academic_settings['evaluation_scale'] = questionary.select(
        "Escala de evaluación:",
        choices=["numeric", "literal"],
        default=defs.get("evaluation_scale", "numeric")
    ).ask()
    if not academic_settings['evaluation_scale']: return

    try:
        academic_settings['grading_max_value'] = int(questionary.text(
            "Nota máxima posible:",
            default=str(defs.get("grading_max_value", 10))
        ).ask())

        academic_settings['passing_grade'] = float(questionary.text(
            "Nota mínima aprobatoria:",
            default=str(defs.get("passing_grade", 7.0))
        ).ask())

        academic_settings['attendance_min_percentage'] = float(questionary.text(
            "Porcentaje mínimo asistencia:",
            default=str(defs.get("attendance_min_percentage", 80.0))
        ).ask())

        academic_settings['max_enrollments_per_period'] = int(questionary.text(
            "Máximo materias por periodo:",
            default=str(defs.get("max_enrollments_per_period", 12))
        ).ask())

        academic_settings['periods_per_year'] = int(questionary.text(
            "Períodos por año:",
            default=str(defs.get("periods_per_year", 2))
        ).ask())
    except (TypeError, ValueError):
        console.print("[red]✗ Datos inválidos o proceso cancelado.[/red]")
        return

    # Console output for derivation
    console.print(f"\n[bold green]Paso 6 — Creando estructura del producto '{product_id}'...[/bold green]")
    
    backend_dir = os.path.join(base_dir, "backend")
    db_name = f"{product_id.replace('-', '_')}.db"
    db_path_original = os.path.join(backend_dir, db_name)
    temp_db_path = None
    
    if os.path.exists(db_path_original):
        temp_db_path = os.path.join("derived_products", f"{db_name}.bak")
        shutil.copy2(db_path_original, temp_db_path)
        console.print("  [dim]✓[/dim] Respaldo de base de datos de producción.")

    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
        console.print("  [dim]✓[/dim] Limpieza de código antiguo.")

    os.makedirs(backend_dir)
    if temp_db_path:
        shutil.copy2(temp_db_path, db_path_original)
        os.remove(temp_db_path)
        console.print("  [dim]✓[/dim] Restauración de base de datos de producción.")
        
    core_engine_src = os.path.join("core_assets", "backend", "core_engine")
    core_engine_dest = os.path.join(backend_dir, "core_engine")
    shutil.copytree(core_engine_src, core_engine_dest, ignore=shutil.ignore_patterns('features', '__pycache__'))
    
    os.makedirs(os.path.join(core_engine_dest, "features"))
    core_services = ["periodos", "cursos", "personas", "auth", "__init__.py"]
    for cs in core_services:
        src = os.path.join(core_engine_src, "features", cs)
        dst = os.path.join(core_engine_dest, "features", cs)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        elif os.path.isfile(src):
            shutil.copy(src, dst)
            
    for feature, is_active in features.items():
        if is_active:
            src = os.path.join(core_engine_src, "features", feature)
            dst = os.path.join(core_engine_dest, "features", feature)
            if os.path.exists(src):
                shutil.copytree(src, dst)

    main_factory_code = generate_main_factory(features, product_name)
    with open(os.path.join(core_engine_dest, "main_factory.py"), "w", encoding="utf-8") as f:
        f.write(main_factory_code)

    shutil.copy("requirements.txt", base_dir)
    run_app_code = """import os
from dotenv import load_dotenv
from core_engine.main_factory import create_app
load_dotenv()
app = create_app()
"""
    with open(os.path.join(backend_dir, "run_app.py"), "w", encoding="utf-8") as f:
        f.write(run_app_code)

    env_content = f"""PRODUCT_NAME="{product_name}"
PRODUCT_TYPE="{product_type}"
PORT=8000
DATABASE_URL="sqlite:///./{db_name}"
"""
    with open(os.path.join(backend_dir, ".env"), "w", encoding="utf-8") as f:
        f.write(env_content)

    config_data = {
        "metadata": {"product_name": product_name, "product_type": product_type},
        "features": features,
        "academic_settings": academic_settings,
        "database": {"path": f"{db_name}"}
    }
    
    yaml_path = os.path.join(backend_dir, "product_config.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(config_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    console.print("  [green]✓[/green] Código backend aislado y YAML generado.")
    
    for root, dirs, files in os.walk(backend_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                content = content.replace("core_assets.backend.core_engine", "core_engine")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(backend_dir)
    python_exe = sys.executable
    migrate_script = os.path.join("core_engine", "persistence", "migrate.py")
    
    try:
        subprocess.run([python_exe, migrate_script, db_name, "product_config.yaml"], cwd=backend_dir, env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        console.print("  [green]✓[/green] Migraciones ejecutadas exitosamente.")
    except subprocess.CalledProcessError as e:
        console.print(f"  [red]✗ Error al migrar:[/red] {e}")

    import base64
    import re
    env_example_path = os.path.join("core_assets", "frontend", "laravel-shell", ".env.example")
    frontend_env_content = ""
    if os.path.exists(env_example_path):
        with open(env_example_path, "r", encoding="utf-8") as f:
            frontend_env_content = f.read()
    else:
        frontend_env_content = "APP_ENV=local\nAPP_DEBUG=true\nAPP_KEY=\n"

    new_app_key = "base64:" + base64.b64encode(os.urandom(32)).decode('utf-8')
    frontend_env_content = re.sub(r"^APP_NAME=.*", f'APP_NAME="{product_name}"', frontend_env_content, flags=re.MULTILINE)
    frontend_env_content = re.sub(r"^APP_URL=.*", f"APP_URL=http://localhost:8000", frontend_env_content, flags=re.MULTILINE)
    if re.search(r"^APP_KEY=", frontend_env_content, flags=re.MULTILINE):
        frontend_env_content = re.sub(r"^APP_KEY=.*", f"APP_KEY={new_app_key}", frontend_env_content, flags=re.MULTILINE)
    else:
        frontend_env_content += f"\nAPP_KEY={new_app_key}"
        
    frontend_env_content += f"\n\n# SPL Configuration\nCORE_ENGINE_BACKEND_URL=http://localhost:8001\n"
    env_frontend_path = os.path.join(base_dir, ".env.frontend")
    with open(env_frontend_path, "w", encoding="utf-8") as f:
        f.write(frontend_env_content)
    console.print("  [green]✓[/green] Entorno Frontend (.env.frontend) generado.")
    
    # Final Summary Panel
    summary_text = (
        f"[bold]Producto derivado exitosamente en:[/bold]\n"
        f"derived_products/{product_id}\n\n"
        f"[bold cyan]1) BACKEND:[/bold cyan]\n"
        f"cd derived_products/{product_id}/backend\n"
        f"..\\..\\..\\.venv\\Scripts\\python.exe -m uvicorn run_app:app --port 8001 --reload\n\n"
        f"[bold cyan]2) FRONTEND:[/bold cyan]\n"
        f"copy derived_products\\{product_id}\\.env.frontend core_assets\\frontend\\laravel-shell\\.env\n"
        f"cd core_assets\\frontend\\laravel-shell\n"
        f"php artisan serve --port=8000"
    )
    console.print()
    console.print(Panel(summary_text, title="¡Proceso Completado!", border_style="green"))
    
    console.print()
    start_now = questionary.confirm("¿Levantar el producto ahora?").ask()
    if start_now:
        backend_proc = None
        frontend_proc = None
        try:
            # Preparar Frontend
            env_front_src = os.path.join(base_dir, ".env.frontend")
            env_front_dest = os.path.join("core_assets", "frontend", "laravel-shell", ".env")
            shutil.copy2(env_front_src, env_front_dest)
            laravel_dir = os.path.join("core_assets", "frontend", "laravel-shell")
            
            has_php = shutil.which("php") is not None
            
            if has_php:
                console.print("  [green]Backend corriendo en http://localhost:8001  (Swagger: /docs)[/green]")
                console.print("  [green]Frontend corriendo en http://localhost:8000[/green]")
                console.print("  [dim]Presiona Ctrl+C para detener ambos servidores.[/dim]\n")
                
                subprocess.run("php artisan config:clear", cwd=laravel_dir, stdout=subprocess.DEVNULL, shell=True)
                
                # Lanzar procesos simultáneos
                backend_proc = subprocess.Popen([python_exe, "-m", "uvicorn", "run_app:app", "--port", "8001", "--reload"], cwd=backend_dir)
                frontend_proc = subprocess.Popen("php artisan serve --port=8000", cwd=laravel_dir, shell=True)
                
                backend_proc.wait()
                frontend_proc.wait()
            else:
                console.print("\n[yellow]⚠️ Advertencia: 'php' no está instalado o no está disponible en ESTA terminal.[/yellow]")
                console.print("  [green]Backend corriendo en http://localhost:8001  (Swagger: /docs)[/green]")
                console.print("  [dim]Presiona Ctrl+C para detener el backend.[/dim]\n")
                
                console.print("  [cyan]Para levantar el frontend, abre tu consola de PHP/Laragon y corre:[/cyan]")
                console.print(f"  [cyan]cd {laravel_dir}[/cyan]")
                console.print("  [cyan]php artisan serve --port=8000[/cyan]\n")
                
                backend_proc = subprocess.Popen([python_exe, "-m", "uvicorn", "run_app:app", "--port", "8001", "--reload"], cwd=backend_dir)
                backend_proc.wait()
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Deteniendo servidores...[/yellow]")
            if backend_proc: backend_proc.terminate()
            if frontend_proc: frontend_proc.terminate()
            console.print("[yellow]Servidores detenidos.[/yellow]")

if __name__ == "__main__":
    main()
