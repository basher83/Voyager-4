#!/usr/bin/env python3
"""
Cognee-Powered Template Rendering Engine

This module provides the core rendering engine for AI-enhanced templates that leverage
knowledge graph intelligence through Cognee integration.
"""

import asyncio
import json
import time
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import yaml
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader, Template
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GraphContext:
    """Container for knowledge graph context data"""
    architectural_patterns: List[Dict] = None
    component_relationships: List[Dict] = None
    technology_stack: Dict = None
    business_context: Dict = None
    code_patterns: List[Dict] = None
    historical_decisions: List[Dict] = None
    performance_insights: Dict = None

@dataclass
class TemplateMetadata:
    """Template metadata for configuration and tracking"""
    template_id: str
    category: str
    version: str
    description: str
    dependencies: List[str]
    performance_metrics: Dict
    last_updated: str
    success_rate: float

class CogneeTemplateEngine:
    """
    AI-Enhanced Template Rendering Engine with Cognee Integration
    
    This engine provides intelligent template rendering that leverages knowledge
    graph insights for context enhancement, relationship awareness, and adaptive
    prompt generation.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the template engine with configuration"""
        self.config_path = config_path or "evaluations/config/cognee_config.yaml"
        self.config = self._load_config()
        self.jinja_env = Environment(
            loader=FileSystemLoader('templates/cognee-powered'),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.cache = {}
        self.performance_metrics = {}
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}. Using defaults.")
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Provide default configuration"""
        return {
            'cognee': {
                'llm_provider': 'anthropic',
                'default_model': 'claude-3-haiku-20240307'
            },
            'search': {
                'default_search_type': 'GRAPH_COMPLETION',
                'max_results': 20,
                'similarity_threshold': 0.7
            },
            'performance': {
                'cache_duration': 86400,
                'use_async_processing': True
            }
        }

    async def query_knowledge_graph(self, 
                                   query: str, 
                                   search_type: str = "GRAPH_COMPLETION",
                                   context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Query the Cognee knowledge graph for relevant information
        
        Args:
            query: Natural language query for the knowledge graph
            search_type: Type of search (GRAPH_COMPLETION, CODE, INSIGHTS, etc.)
            context: Additional context to refine the search
            
        Returns:
            Dictionary containing graph query results
        """
        cache_key = f"{query}:{search_type}:{hash(str(context))}"
        
        # Check cache first
        if cache_key in self.cache:
            cache_time, result = self.cache[cache_key]
            if time.time() - cache_time < self.config['performance']['cache_duration']:
                logger.debug(f"Cache hit for query: {query[:50]}...")
                return result
        
        start_time = time.time()
        
        try:
            # Import cognee here to avoid dependency issues if not installed
            try:
                import cognee
            except ImportError:
                logger.warning("Cognee not available. Using mock data.")
                return self._mock_graph_response(query, search_type)
            
            # Execute graph query
            result = await self._execute_graph_query(cognee, query, search_type, context)
            
            # Cache the result
            self.cache[cache_key] = (time.time(), result)
            
            # Track performance
            query_time = time.time() - start_time
            self._record_performance('graph_query', query_time)
            
            logger.info(f"Graph query completed in {query_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Graph query failed: {str(e)}")
            return self._mock_graph_response(query, search_type)
    
    async def _execute_graph_query(self, cognee, query: str, search_type: str, context: Optional[Dict]) -> Dict[str, Any]:
        """Execute the actual graph query using Cognee"""
        try:
            # Search the knowledge graph
            search_result = cognee.search(
                search_query=query,
                search_type=search_type.upper()
            )
            
            # Process and structure the result
            if isinstance(search_result, list) and len(search_result) > 0:
                # Extract content from MCP response format
                content = search_result[0].text if hasattr(search_result[0], 'text') else str(search_result[0])
                
                return {
                    'query': query,
                    'search_type': search_type,
                    'content': content,
                    'metadata': {
                        'timestamp': time.time(),
                        'result_count': len(search_result),
                        'confidence': 0.8  # Default confidence
                    }
                }
            else:
                return self._empty_graph_response(query, search_type)
                
        except Exception as e:
            logger.error(f"Cognee query execution failed: {str(e)}")
            return self._mock_graph_response(query, search_type)
    
    def _mock_graph_response(self, query: str, search_type: str) -> Dict[str, Any]:
        """Generate mock response when Cognee is not available"""
        mock_responses = {
            'GRAPH_COMPLETION': f"Mock architectural analysis for query: {query}",
            'CODE': {"components": ["MockComponent1", "MockComponent2"], "relationships": []},
            'INSIGHTS': f"Mock insights: This appears to be a {query.lower()} related query."
        }
        
        return {
            'query': query,
            'search_type': search_type,
            'content': mock_responses.get(search_type, f"Mock response for {query}"),
            'metadata': {
                'timestamp': time.time(),
                'is_mock': True,
                'confidence': 0.5
            }
        }
    
    def _empty_graph_response(self, query: str, search_type: str) -> Dict[str, Any]:
        """Generate empty response when no results found"""
        return {
            'query': query,
            'search_type': search_type,
            'content': "No relevant information found in knowledge graph.",
            'metadata': {
                'timestamp': time.time(),
                'result_count': 0,
                'confidence': 0.0
            }
        }

    async def enhance_context(self, base_context: Dict[str, Any], template_category: str) -> GraphContext:
        """
        Enhance template context with knowledge graph insights
        
        Args:
            base_context: Base template variables
            template_category: Category of template (architecture-aware, context-enriched, etc.)
            
        Returns:
            GraphContext with enhanced information
        """
        start_time = time.time()
        
        # Define category-specific queries
        category_queries = {
            'architecture-aware': [
                ("architectural patterns and design structures", "INSIGHTS"),
                ("component dependencies and interactions", "CODE"),
                ("technology stack and frameworks", "GRAPH_COMPLETION")
            ],
            'context-enriched': [
                ("business logic and domain context", "GRAPH_COMPLETION"),
                ("feature relationships and workflows", "INSIGHTS"),
                ("user requirements and use cases", "GRAPH_COMPLETION")
            ],
            'relationship-informed': [
                ("component relationships and dependencies", "CODE"),
                ("api usage patterns and integrations", "INSIGHTS"),
                ("data flow and communication patterns", "INSIGHTS")
            ],
            'pattern-adaptive': [
                ("coding patterns and conventions", "CODE"),
                ("best practices and standards", "GRAPH_COMPLETION"),
                ("team preferences and styles", "INSIGHTS")
            ],
            'dynamic-enhanced': [
                ("performance metrics and optimization", "INSIGHTS"),
                ("usage patterns and feedback", "GRAPH_COMPLETION"),
                ("success metrics and improvements", "INSIGHTS")
            ]
        }
        
        # Get queries for this category
        queries = category_queries.get(template_category, [])
        
        # Execute queries concurrently
        tasks = [
            self.query_knowledge_graph(query, search_type, base_context)
            for query, search_type in queries
        ]
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
        else:
            results = []
        
        # Process results into GraphContext
        graph_context = GraphContext()
        
        for i, (query, search_type) in enumerate(queries):
            if i < len(results) and not isinstance(results[i], Exception):
                result = results[i]
                content = result.get('content', '')
                
                # Assign to appropriate context field based on query type
                if 'architectural' in query or 'design' in query:
                    graph_context.architectural_patterns = self._parse_patterns(content)
                elif 'component' in query or 'dependencies' in query:
                    graph_context.component_relationships = self._parse_relationships(content)
                elif 'technology' in query or 'stack' in query:
                    graph_context.technology_stack = self._parse_technology(content)
                elif 'business' in query or 'domain' in query:
                    graph_context.business_context = self._parse_business_context(content)
                elif 'coding patterns' in query or 'conventions' in query:
                    graph_context.code_patterns = self._parse_code_patterns(content)
                elif 'performance' in query or 'optimization' in query:
                    graph_context.performance_insights = self._parse_performance(content)
        
        # Track performance
        enhancement_time = time.time() - start_time
        self._record_performance('context_enhancement', enhancement_time)
        
        logger.info(f"Context enhancement completed in {enhancement_time:.2f}s")
        return graph_context

    def _parse_patterns(self, content: str) -> List[Dict]:
        """Parse architectural patterns from content"""
        # Simple parsing - in production, this would be more sophisticated
        patterns = []
        lines = content.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['pattern', 'architecture', 'design']):
                patterns.append({
                    'name': line.strip(),
                    'confidence': 0.8,
                    'source': 'knowledge_graph'
                })
        
        return patterns[:5]  # Limit to top 5 patterns
    
    def _parse_relationships(self, content: str) -> List[Dict]:
        """Parse component relationships from content"""
        relationships = []
        
        # Look for dependency-like patterns
        if isinstance(content, dict) and 'components' in content:
            components = content.get('components', [])
            for i, comp in enumerate(components):
                if i < len(components) - 1:
                    relationships.append({
                        'source': comp,
                        'target': components[i + 1],
                        'type': 'depends_on',
                        'confidence': 0.7
                    })
        
        return relationships
    
    def _parse_technology(self, content: str) -> Dict:
        """Parse technology stack information from content"""
        technologies = {
            'backend': [],
            'frontend': [],
            'database': [],
            'tools': []
        }
        
        # Simple keyword-based parsing
        tech_keywords = {
            'backend': ['python', 'node', 'java', 'django', 'flask', 'express'],
            'frontend': ['react', 'vue', 'angular', 'javascript', 'typescript'],
            'database': ['postgresql', 'mysql', 'mongodb', 'redis'],
            'tools': ['docker', 'kubernetes', 'git', 'jenkins']
        }
        
        content_lower = content.lower()
        for category, keywords in tech_keywords.items():
            for keyword in keywords:
                if keyword in content_lower:
                    technologies[category].append(keyword)
        
        return technologies
    
    def _parse_business_context(self, content: str) -> Dict:
        """Parse business context from content"""
        return {
            'domain': 'general',
            'context': content[:500],  # First 500 chars as summary
            'key_concepts': [],
            'stakeholders': []
        }
    
    def _parse_code_patterns(self, content: str) -> List[Dict]:
        """Parse coding patterns from content"""
        patterns = []
        
        # Look for pattern indicators
        pattern_indicators = ['class', 'function', 'import', 'def', 'const', 'var']
        lines = content.split('\n')
        
        for line in lines:
            for indicator in pattern_indicators:
                if indicator in line.lower():
                    patterns.append({
                        'pattern': line.strip(),
                        'type': indicator,
                        'frequency': 1
                    })
                    break
        
        return patterns[:10]  # Limit to top 10 patterns
    
    def _parse_performance(self, content: str) -> Dict:
        """Parse performance insights from content"""
        return {
            'metrics': {},
            'bottlenecks': [],
            'recommendations': [],
            'trends': {}
        }

    async def render_template(self, 
                            template_path: str, 
                            context: Dict[str, Any], 
                            enable_graph_enhancement: bool = True) -> str:
        """
        Render a template with optional knowledge graph enhancement
        
        Args:
            template_path: Path to the template file
            context: Template context variables
            enable_graph_enhancement: Whether to enhance with graph data
            
        Returns:
            Rendered template string
        """
        start_time = time.time()
        
        try:
            # Load template
            template = self.jinja_env.get_template(template_path)
            
            # Enhance context if requested
            if enable_graph_enhancement:
                # Determine template category from path
                category = Path(template_path).parent.name
                
                # Get enhanced context
                graph_context = await self.enhance_context(context, category)
                
                # Merge graph context into template variables
                enhanced_context = self._merge_graph_context(context, graph_context)
            else:
                enhanced_context = context
            
            # Render template
            rendered = template.render(**enhanced_context)
            
            # Track performance
            render_time = time.time() - start_time
            self._record_performance('template_render', render_time)
            
            logger.info(f"Template rendered in {render_time:.2f}s")
            return rendered
            
        except Exception as e:
            logger.error(f"Template rendering failed: {str(e)}")
            raise

    def _merge_graph_context(self, base_context: Dict[str, Any], graph_context: GraphContext) -> Dict[str, Any]:
        """Merge graph context into base template context"""
        enhanced = base_context.copy()
        
        # Add graph-specific variables
        enhanced.update({
            'ARCHITECTURAL_PATTERNS': self._format_patterns(graph_context.architectural_patterns),
            'COMPONENT_RELATIONSHIPS': self._format_relationships(graph_context.component_relationships),
            'TECHNOLOGY_STACK': self._format_technology(graph_context.technology_stack),
            'BUSINESS_CONTEXT': self._format_business_context(graph_context.business_context),
            'CODE_PATTERNS': self._format_code_patterns(graph_context.code_patterns),
            'PERFORMANCE_INSIGHTS': self._format_performance(graph_context.performance_insights)
        })
        
        return enhanced

    def _format_patterns(self, patterns: Optional[List[Dict]]) -> str:
        """Format architectural patterns for template"""
        if not patterns:
            return "No specific architectural patterns detected in the knowledge graph."
        
        formatted = "**Discovered Architectural Patterns:**\n"
        for pattern in patterns:
            name = pattern.get('name', 'Unknown Pattern')
            confidence = pattern.get('confidence', 0.0)
            formatted += f"- **{name}** (confidence: {confidence:.1f})\n"
        
        return formatted
    
    def _format_relationships(self, relationships: Optional[List[Dict]]) -> str:
        """Format component relationships for template"""
        if not relationships:
            return "No component relationships identified in the knowledge graph."
        
        formatted = "**Component Dependencies:**\n"
        for rel in relationships:
            source = rel.get('source', 'Unknown')
            target = rel.get('target', 'Unknown')
            rel_type = rel.get('type', 'relates_to')
            formatted += f"- {source} → {target} ({rel_type})\n"
        
        return formatted
    
    def _format_technology(self, tech_stack: Optional[Dict]) -> str:
        """Format technology stack for template"""
        if not tech_stack:
            return "No technology stack information available from knowledge graph."
        
        formatted = "**Technology Stack Analysis:**\n"
        for category, technologies in tech_stack.items():
            if technologies:
                tech_list = ", ".join(technologies)
                formatted += f"- **{category.title()}**: {tech_list}\n"
        
        return formatted
    
    def _format_business_context(self, business_context: Optional[Dict]) -> str:
        """Format business context for template"""
        if not business_context:
            return "No business context available from knowledge graph."
        
        context_text = business_context.get('context', 'No context available')
        return f"**Business Context:**\n{context_text}"
    
    def _format_code_patterns(self, code_patterns: Optional[List[Dict]]) -> str:
        """Format code patterns for template"""
        if not code_patterns:
            return "No code patterns identified in the knowledge graph."
        
        formatted = "**Code Patterns:**\n"
        for pattern in code_patterns:
            pattern_text = pattern.get('pattern', 'Unknown')
            pattern_type = pattern.get('type', 'general')
            formatted += f"- {pattern_text} (type: {pattern_type})\n"
        
        return formatted
    
    def _format_performance(self, performance_insights: Optional[Dict]) -> str:
        """Format performance insights for template"""
        if not performance_insights:
            return "No performance insights available from knowledge graph."
        
        return "**Performance Insights:**\nPerformance data analysis not yet implemented."

    def _record_performance(self, operation: str, duration: float):
        """Record performance metrics for monitoring"""
        if operation not in self.performance_metrics:
            self.performance_metrics[operation] = []
        
        self.performance_metrics[operation].append({
            'duration': duration,
            'timestamp': time.time()
        })
        
        # Keep only last 100 measurements
        if len(self.performance_metrics[operation]) > 100:
            self.performance_metrics[operation] = self.performance_metrics[operation][-100:]

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for monitoring"""
        stats = {}
        
        for operation, measurements in self.performance_metrics.items():
            if measurements:
                durations = [m['duration'] for m in measurements]
                stats[operation] = {
                    'count': len(measurements),
                    'avg_duration': sum(durations) / len(durations),
                    'min_duration': min(durations),
                    'max_duration': max(durations),
                    'total_duration': sum(durations)
                }
        
        return stats

# Example usage and testing
async def main():
    """Example usage of the Cognee Template Engine"""
    engine = CogneeTemplateEngine()
    
    # Example context
    context = {
        'CONTEXT': 'E-commerce platform architecture analysis',
        'SCOPE': 'full_codebase',
        'FOCUS': 'microservices_migration',
        'AUDIENCE': 'development_team'
    }
    
    try:
        # Test knowledge graph query
        result = await engine.query_knowledge_graph(
            "architectural patterns in e-commerce systems",
            "INSIGHTS"
        )
        print("Graph query result:", result)
        
        # Test context enhancement
        graph_context = await engine.enhance_context(context, 'architecture-aware')
        print("Enhanced context created")
        
        # Print performance stats
        stats = engine.get_performance_stats()
        print("Performance stats:", stats)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())