import pytest
import os
import tempfile
import yaml
from pathlib import Path

from core_assets.backend.core_engine.config.schema_loader import validate_product_config, load_yaml, load_schema

def test_load_schema():
    schema = load_schema()
    assert isinstance(schema, dict)
    assert "$schema" in schema or "type" in schema

def test_validate_valid_config():
    # Arrange: Create a temporary valid yaml file
    valid_data = {
        "product_name": "Test Product",
        "passing_grade": 7.0,
        "attendance_min_percentage": 75,
        "evaluation_scale": "numerica"
    }
    
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as f:
        yaml.dump(valid_data, f)
        temp_path = f.name
        
    try:
        # Act
        config = validate_product_config(temp_path)
        # Assert
        assert config["product_name"] == "Test Product"
    finally:
        os.remove(temp_path)

def test_validate_invalid_config():
    # Arrange: Create a temporary invalid yaml file (missing required fields)
    invalid_data = {
        "product_name": "Test Product"
    }
    
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as f:
        yaml.dump(invalid_data, f)
        temp_path = f.name
        
    try:
        # Act & Assert
        with pytest.raises(ValueError) as excinfo:
            validate_product_config(temp_path)
        assert "Configuración inválida" in str(excinfo.value)
    finally:
        os.remove(temp_path)
