"""
Entrypoint de ejecución. Usado tanto en local (demo) como dentro del
contenedor Docker. Lee PRODUCT_CONFIG_PATH y delega todo el trabajo de
ensamblaje al Core Engine.
"""
from core_assets.backend.core_engine.main_factory import create_app

app = create_app()
