"""
Template management and generation system.

This module handles template creation, rendering, and management including:
- Template hierarchy management
- Dynamic template generation using Cognee knowledge graphs
- Template validation and testing
- Template rendering with variable substitution
"""

from .engine import *
from .renderer import *

__all__ = [
    # Template engine
    'TemplateEngine',
    'generate_template',
    
    # Template renderer
    'TemplateRenderer', 
    'render_template',
]