"""
Cognee Framework - AI-Powered Prompt Development and Evaluation System

This package provides a comprehensive framework for developing, testing, and optimizing
Claude Code prompts using AI knowledge graphs and advanced evaluation techniques.

Main Components:
- core: Core framework functionality and base classes
- evaluation: Evaluation engines and metrics
- templates: Template management and generation
- utils: Utility functions and helpers
- mcp_integration: MCP server integration for enhanced capabilities
"""

__version__ = "1.0.0"
__author__ = "Claude Code Prompt Development Framework"

from .core import *
from .evaluation import *
from .templates import *
from .utils import *

# Optional MCP integration (graceful fallback if not available)
try:
    from .mcp_integration import *
except ImportError:
    pass