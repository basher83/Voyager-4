"""
MCP (Model Context Protocol) server integration for enhanced capabilities.

This module provides integration with MCP servers, particularly Cognee,
to enable advanced knowledge graph features and AI-powered evaluations.
"""

from .utils import *

__all__ = [
    # MCP integration utilities
    'MCPCogneeClient',
    'connect_to_cognee',
    'search_knowledge_graph',
    'create_knowledge_graph',
]