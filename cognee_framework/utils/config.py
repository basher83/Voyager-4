"""
Configuration management utilities for the Cognee Framework.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from file or return default configuration.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        Configuration dictionary
    """
    default_config = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 2048,
        "temperature": 0.0,
        "evaluation_methods": ["exact_match", "consistency", "quality"],
        "metrics": {
            "accuracy_threshold": 0.85,
            "consistency_threshold": 0.8,
            "quality_threshold": 4.0
        },
        "retry_attempts": 3,
        "timeout": 30,
        "parallel_requests": False
    }
    
    if config_path and Path(config_path).exists():
        try:
            with open(config_path, 'r') as f:
                file_config = yaml.safe_load(f)
                # Merge with defaults
                default_config.update(file_config)
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
            print("Using default configuration.")
    
    return default_config


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def get_data_dir() -> Path:
    """Get the data directory."""
    return get_project_root() / "data"


def get_config_dir() -> Path:
    """Get the configuration directory.""" 
    return get_project_root() / "evaluations" / "config"


def get_results_dir() -> Path:
    """Get the results directory."""
    return get_project_root() / "evaluations" / "results"