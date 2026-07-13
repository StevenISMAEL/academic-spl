import os
import yaml
import subprocess
import sys

def prompt_bool(question: str) -> bool:
    while True:
        resp = input(f"{question} [s/n]: ").strip().lower()
        if resp in ['s', 'si', 'sí', 'y', 'yes']:
            return True
        if resp in ['n', 'no']:
            return False

def prompt_string(question: str, required: bool = True) -> str:
    while True:
        resp = input(f"{question}: ").strip()
        if not resp and required:
            print("Este campo es requerido.")
            continue
        return resp

def prompt_int(question: str) -> int:
    while True:
        resp = input(f"{question}: ").strip()
        try:
            return int(resp)
        except ValueError:
            print("Por favor, ingresa un número entero válido.")

def prompt_float(question: str) -> float:
    while True:
        resp = input(f"{question}: ").strip()
        try:
            return float(resp)
        except ValueError:
            print("Por favor, ingresa un número decimal válido.")

def prompt_choice(question: str, choices: list) -> str:
    print(question)
    for i, choice in enumerate(choices, 1):
        print(f"  {i}. {choice}")
    while True:
        resp = input("Selecciona una opción: ").strip()
        try:
            idx = int(resp) - 1
            if 0 <= idx < len(choices):
                return choices[idx]
        except ValueError:
            pass
        print("Opción inválida.")

def main():
    print("="*60)
    print(" SPL ACADEMICO - ASISTENTE DE DERIVACION DE PRODUCTOS ")
    print("="*60)
    print("Este asistente creará un nuevo producto configurando su YAML")
    print("y ejecutando sus migraciones automáticamente.\\n")

    product_id = prompt_string("1. Identificador corto del producto (ej. conservatorio-musica)").replace(" ", "-").lower()
    product_name = prompt_string("2. Nombre oficial legible (ej. Conservatorio Nacional de Música)")
    product_type = prompt_choice("3. Tipo de institución", ["colegio", "universidad", "instituto"])

    print("\n--- SELECCION DE FEATURES (Variabilidad Booleana) ---")
    features = {}
    features['grading'] = prompt_bool("¿Habilitar sistema de calificaciones? (grading)")
    features['attendance'] = prompt_bool("¿Habilitar sistema de asistencia diaria? (attendance)")
    features['enrollment'] = prompt_bool("¿Habilitar gestión de matrículas? (enrollment)")
    features['schedule'] = prompt_bool("¿Habilitar gestión de horarios? (schedule)")
    features['reports'] = prompt_bool("¿Habilitar generación de reportes? (reports)")
    features['certificates'] = prompt_bool("¿Habilitar emisión de certificados? (certificates)")

    print("\n--- PARAMETROS ACADEMICOS (Variabilidad Paramétrica) ---")
    academic_settings = {}
    academic_settings['evaluation_scale'] = prompt_choice("Escala de evaluación", ["literal", "numeric"])
    academic_settings['grading_max_value'] = prompt_int("Nota máxima posible (ej. 10)")
    academic_settings['passing_grade'] = prompt_float("Nota mínima para aprobar (ej. 7.0)")
    academic_settings['attendance_min_percentage'] = prompt_float("Porcentaje mínimo de asistencia (ej. 80.0)")
    academic_settings['max_enrollments_per_period'] = prompt_int("Límite de materias por estudiante (ej. 6)")
    academic_settings['periods_per_year'] = prompt_int("Períodos o semestres por año (ej. 2)")

    # Data structure
    config_data = {
        "metadata": {
            "product_name": product_name,
            "product_type": product_type
        },
        "features": features,
        "academic_settings": academic_settings,
        "database": {
            "path": f"products/{product_id}/{product_id.replace('-', '_')}.db"
        }
    }

    # Creación de carpeta y YAML
    product_dir = os.path.join("products", product_id)
    os.makedirs(product_dir, exist_ok=True)
    
    yaml_path = os.path.join(product_dir, "product_config.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(config_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\n[OK] Carpeta '{product_dir}' creada.")
    print(f"[OK] Archivo '{yaml_path}' generado.")

    # Ejecutar Migraciones
    print("\nEjecutando migraciones de base de datos (creando el Super Esquema)...")
    db_path = config_data["database"]["path"]
    
    python_exe = sys.executable
    migrate_script = os.path.join("core_assets", "backend", "core_engine", "persistence", "migrate.py")
    
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    
    try:
        subprocess.run([python_exe, migrate_script, db_path], env=env, check=True)
        print(f"\n[OK] Base de datos SQLite creada y migrada en '{db_path}'.")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Falló la migración de base de datos: {e}")
        return

    print("="*60)
    print(" ¡PRODUCTO DERIVADO CON EXITO! ")
    print("="*60)
    print("Para levantar el servidor backend de tu nuevo producto:")
    if os.name == 'nt':
        print(f'   $env:PRODUCT_CONFIG_PATH="{yaml_path}"')
        print('   .venv\\Scripts\\python.exe -m uvicorn run_app:app --port 8004 --reload')
    else:
        print(f'   export PRODUCT_CONFIG_PATH="{yaml_path}"')
        print('   .venv/bin/python -m uvicorn run_app:app --port 8004 --reload')
    print("="*60)

if __name__ == "__main__":
    main()
