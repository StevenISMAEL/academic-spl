import os
from dotenv import load_dotenv
from core_engine.main_factory import create_app
load_dotenv()
app = create_app()
