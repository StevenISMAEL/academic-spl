#!/bin/bash
# =============================================================================
# Entrypoint del backend FastAPI (Academic SPL)
#
# Ejecuta las migraciones SQLite antes de arrancar uvicorn.
# PRODUCT_CONFIG_PATH y la ruta de la BD vienen del product_config.yaml.
# =============================================================================
set -e

echo ">>> [Backend] PRODUCT_CONFIG_PATH = ${PRODUCT_CONFIG_PATH}"

# Extraer el database.path del product_config.yaml para pasarlo al migrador
DB_PATH=$(python -c "
import yaml, sys
with open('${PRODUCT_CONFIG_PATH}', 'r') as f:
    cfg = yaml.safe_load(f)
db = cfg.get('database', {}).get('path')
if not db:
    print('ERROR: database.path no encontrado en product_config.yaml', file=sys.stderr)
    sys.exit(1)
print(db)
")

echo ">>> [Backend] Base de datos: ${DB_PATH}"
echo ">>> [Backend] Ejecutando migraciones..."
python -m core_assets.backend.core_engine.persistence.migrate \
    "${DB_PATH}" \
    "${PRODUCT_CONFIG_PATH}"

echo ">>> [Backend] Migraciones completadas. Arrancando uvicorn..."
exec uvicorn run_app:app --host 0.0.0.0 --port 8000
