#!/usr/bin/env python3
"""
Cognee-Powered Template Renderer Integration

This module provides integration between the Cognee template engine and the existing
evaluation framework, enabling seamless rendering and testing of AI-enhanced templates.
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import yaml
import logging

# Add the project root to the Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from templates.cognee_powered.engine import CogneeTemplateEngine
from evaluations.scripts.evaluate_prompt import PromptEvaluator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CogneeTemplateRenderer:
    """
    Integration layer between Cognee template engine and evaluation framework
    
    This class provides a unified interface for rendering Cognee-powered templates
    and integrating them with the existing evaluation and testing infrastructure.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the template renderer with configuration"""
        self.config_path = config_path or "evaluations/config/cognee_config.yaml"
        self.engine = CogneeTemplateEngine(config_path)
        self.template_base_path = Path("templates/cognee-powered")
        self.render_cache = {}
        
    def list_available_templates(self) -> Dict[str, List[str]]:
        """
        List all available Cognee-powered templates by category
        
        Returns:
            Dictionary mapping categories to template filenames
        """
        templates = {}
        
        for category_dir in self.template_base_path.iterdir():
            if category_dir.is_dir() and category_dir.name != "__pycache__":
                category_templates = []
                
                # Main template
                main_template = category_dir / "template.md"
                if main_template.exists():
                    category_templates.append("template.md")
                
                # Variations
                variations_dir = category_dir / "variations"
                if variations_dir.exists():
                    for variation in variations_dir.glob("*.md"):
                        category_templates.append(f"variations/{variation.name}")
                
                if category_templates:
                    templates[category_dir.name] = category_templates
                    
        return templates
    
    def get_template_metadata(self, category: str) -> Optional[Dict[str, Any]]:
        """
        Load template metadata for a specific category
        
        Args:
            category: Template category name
            
        Returns:
            Template metadata dictionary or None if not found
        """
        metadata_path = self.template_base_path / category / "metadata.yaml"
        
        if not metadata_path.exists():
            logger.warning(f"No metadata found for template category: {category}")
            return None
            
        try:
            with open(metadata_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load metadata for {category}: {e}")
            return None
    
    async def render_template(self, 
                            category: str, 
                            template_name: str = "template.md",
                            context: Dict[str, Any] = None,
                            enable_graph_enhancement: bool = True) -> Dict[str, Any]:
        """
        Render a Cognee-powered template with knowledge graph enhancement
        
        Args:
            category: Template category (e.g., 'architecture-aware')
            template_name: Template filename (default: 'template.md')
            context: Template context variables
            enable_graph_enhancement: Whether to enhance with knowledge graph data
            
        Returns:
            Dictionary containing rendered template and metadata
        """
        start_time = time.time()
        context = context or {}
        
        # Construct template path
        template_path = f"{category}/{template_name}"
        full_path = self.template_base_path / template_path
        
        if not full_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        try:
            # Load template metadata
            metadata = self.get_template_metadata(category)
            
            # Render template using Cognee engine
            rendered_content = await self.engine.render_template(
                template_path=template_path,
                context=context,
                enable_graph_enhancement=enable_graph_enhancement
            )
            
            # Prepare result
            result = {
                'template_path': template_path,
                'category': category,
                'template_name': template_name,
                'rendered_content': rendered_content,
                'context': context,
                'metadata': metadata,
                'render_time': time.time() - start_time,
                'graph_enhanced': enable_graph_enhancement,
                'timestamp': time.time()
            }
            
            # Cache result for potential reuse
            cache_key = f"{template_path}:{hash(str(context))}"
            self.render_cache[cache_key] = result
            
            logger.info(f"Successfully rendered template {template_path} in {result['render_time']:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Failed to render template {template_path}: {e}")
            raise
    
    def prepare_evaluation_context(self, 
                                 category: str, 
                                 base_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare evaluation context based on template metadata and requirements
        
        Args:
            category: Template category
            base_context: Base context variables
            
        Returns:
            Enhanced context suitable for template evaluation
        """
        metadata = self.get_template_metadata(category)
        if not metadata:
            return base_context
        
        # Get template configuration
        template_config = metadata.get('template_configuration', {})
        input_variables = template_config.get('input_variables', [])
        
        # Ensure all required variables are present
        enhanced_context = base_context.copy()
        
        for var_config in input_variables:
            var_name = var_config.get('name')
            var_type = var_config.get('type', 'string')
            required = var_config.get('required', False)
            default = var_config.get('default')
            
            if var_name not in enhanced_context:
                if required and default is None:
                    logger.warning(f"Required variable {var_name} not provided for {category}")
                elif default is not None:
                    enhanced_context[var_name] = default
                    
        return enhanced_context
    
    async def evaluate_template(self,
                              category: str,
                              template_name: str = "template.md", 
                              test_cases: List[Dict[str, Any]] = None,
                              evaluation_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate a Cognee-powered template using the existing evaluation framework
        
        Args:
            category: Template category
            template_name: Template filename
            test_cases: List of test cases for evaluation
            evaluation_config: Evaluation configuration parameters
            
        Returns:
            Evaluation results dictionary
        """
        start_time = time.time()
        
        # Load template metadata for evaluation parameters
        metadata = self.get_template_metadata(category)
        if not metadata:
            raise ValueError(f"No metadata found for template category: {category}")
        
        # Prepare evaluation configuration
        eval_config = evaluation_config or {}
        
        # Use metadata quality metrics if available
        quality_metrics = metadata.get('quality_metrics', {})
        success_criteria = quality_metrics.get('success_criteria', [])
        
        if success_criteria:
            eval_config['success_thresholds'] = {
                criterion['metric']: criterion['threshold']
                for criterion in success_criteria
            }
        
        # Prepare test cases
        if not test_cases:
            test_cases = self._generate_default_test_cases(category, metadata)
        
        # Run evaluations for each test case
        evaluation_results = []
        
        for i, test_case in enumerate(test_cases):
            try:
                # Prepare context for this test case
                context = self.prepare_evaluation_context(category, test_case.get('context', {}))
                
                # Render template
                render_result = await self.render_template(
                    category=category,
                    template_name=template_name,
                    context=context,
                    enable_graph_enhancement=True
                )
                
                # Evaluate rendered result
                case_result = {
                    'test_case_id': i,
                    'test_case': test_case,
                    'render_result': render_result,
                    'evaluation_metrics': {},
                    'success': True,
                    'errors': []
                }
                
                # Add template-specific quality metrics
                case_result['evaluation_metrics'] = self._calculate_quality_metrics(
                    render_result, test_case, metadata
                )
                
                evaluation_results.append(case_result)
                
            except Exception as e:
                logger.error(f"Evaluation failed for test case {i}: {e}")
                evaluation_results.append({
                    'test_case_id': i,
                    'test_case': test_case,
                    'render_result': None,
                    'evaluation_metrics': {},
                    'success': False,
                    'errors': [str(e)]
                })
        
        # Aggregate results
        total_time = time.time() - start_time
        success_count = sum(1 for result in evaluation_results if result['success'])
        
        aggregated_results = {
            'template_category': category,
            'template_name': template_name,
            'total_test_cases': len(test_cases),
            'successful_cases': success_count,
            'success_rate': success_count / len(test_cases) if test_cases else 0,
            'total_evaluation_time': total_time,
            'average_render_time': sum(
                r['render_result']['render_time'] for r in evaluation_results 
                if r['render_result']
            ) / success_count if success_count > 0 else 0,
            'individual_results': evaluation_results,
            'metadata': metadata,
            'engine_performance': self.engine.get_performance_stats()
        }
        
        logger.info(
            f"Template evaluation completed: {success_count}/{len(test_cases)} "
            f"successful in {total_time:.2f}s"
        )
        
        return aggregated_results
    
    def _generate_default_test_cases(self, category: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate default test cases based on template metadata"""
        use_cases = metadata.get('use_cases', {})
        primary_use_cases = use_cases.get('primary_use_cases', [])
        
        test_cases = []
        
        # Generate basic test cases for primary use cases
        for i, use_case in enumerate(primary_use_cases[:3]):  # Limit to 3 for performance
            test_case = {
                'name': f"default_test_case_{i}",
                'description': use_case,
                'context': {
                    'CONTEXT': use_case,
                    'SCOPE': 'test_scope',
                }
            }
            
            # Add category-specific context
            if category == 'architecture-aware':
                test_case['context'].update({
                    'FOCUS': 'maintainability',
                    'AUDIENCE': 'development_team'
                })
            elif category == 'pattern-adaptive':
                test_case['context'].update({
                    'LANGUAGE': 'Python',
                    'PROJECT_PHASE': 'development'
                })
            elif category == 'dynamic-enhanced':
                test_case['context'].update({
                    'SUCCESS_METRICS': ['accuracy', 'efficiency'],
                    'OPTIMIZATION_GOALS': ['quality', 'speed']
                })
            
            test_cases.append(test_case)
        
        return test_cases
    
    def _calculate_quality_metrics(self, 
                                 render_result: Dict[str, Any],
                                 test_case: Dict[str, Any], 
                                 metadata: Dict[str, Any]) -> Dict[str, float]:
        """Calculate quality metrics for rendered template"""
        metrics = {}
        
        rendered_content = render_result.get('rendered_content', '')
        render_time = render_result.get('render_time', 0)
        
        # Basic metrics
        metrics['content_length'] = len(rendered_content)
        metrics['render_time'] = render_time
        metrics['graph_enhancement_success'] = 1.0 if render_result.get('graph_enhanced') else 0.0
        
        # Template-specific metrics based on metadata
        quality_criteria = metadata.get('quality_metrics', {}).get('success_criteria', [])
        
        for criterion in quality_criteria:
            metric_name = criterion.get('metric')
            threshold = criterion.get('threshold')
            
            if metric_name == 'response_time' and threshold:
                metrics['response_time_compliance'] = 1.0 if render_time <= threshold else 0.0
            elif metric_name == 'content_completeness':
                # Simple completeness check based on content length
                metrics['content_completeness'] = min(1.0, len(rendered_content) / 1000)
            elif metric_name == 'structure_compliance':
                # Check if content has expected structure
                has_headers = '##' in rendered_content
                has_sections = len(rendered_content.split('\n\n')) > 3
                metrics['structure_compliance'] = 1.0 if has_headers and has_sections else 0.5
        
        return metrics
    
    async def batch_render_templates(self, 
                                   render_configs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Render multiple templates in batch for efficiency
        
        Args:
            render_configs: List of rendering configurations
            
        Returns:
            List of render results
        """
        tasks = []
        
        for config in render_configs:
            task = self.render_template(
                category=config.get('category'),
                template_name=config.get('template_name', 'template.md'),
                context=config.get('context', {}),
                enable_graph_enhancement=config.get('enable_graph_enhancement', True)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Batch render failed for config {i}: {result}")
                processed_results.append({
                    'success': False,
                    'error': str(result),
                    'config': render_configs[i]
                })
            else:
                processed_results.append({
                    'success': True,
                    'result': result,
                    'config': render_configs[i]
                })
        
        return processed_results
    
    def save_evaluation_results(self, 
                              results: Dict[str, Any], 
                              output_path: Optional[str] = None) -> str:
        """
        Save evaluation results to file
        
        Args:
            results: Evaluation results dictionary
            output_path: Optional output file path
            
        Returns:
            Path to saved results file
        """
        if not output_path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            category = results.get('template_category', 'unknown')
            output_path = f"evaluations/results/cognee_{category}_evaluation_{timestamp}.json"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare results for JSON serialization
        serializable_results = self._make_json_serializable(results)
        
        with open(output_path, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        logger.info(f"Evaluation results saved to: {output_path}")
        return str(output_path)
    
    def _make_json_serializable(self, obj: Any) -> Any:
        """Convert objects to JSON-serializable format"""
        if isinstance(obj, dict):
            return {k: self._make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        else:
            return str(obj)

# Example usage and testing
async def main():
    """Example usage of the Cognee Template Renderer"""
    renderer = CogneeTemplateRenderer()
    
    try:
        # List available templates
        templates = renderer.list_available_templates()
        print("Available templates:")
        for category, template_list in templates.items():
            print(f"  {category}: {template_list}")
        
        # Example: Render architecture-aware template
        context = {
            'CONTEXT': 'E-commerce platform analysis',
            'SCOPE': 'full_codebase',
            'FOCUS': 'scalability',
            'AUDIENCE': 'development_team'
        }
        
        result = await renderer.render_template(
            category='architecture-aware',
            template_name='template.md',
            context=context
        )
        
        print(f"\nTemplate rendered successfully in {result['render_time']:.2f}s")
        print(f"Content length: {len(result['rendered_content'])} characters")
        
        # Example: Evaluate template
        evaluation_results = await renderer.evaluate_template(
            category='architecture-aware',
            template_name='template.md'
        )
        
        print(f"\nEvaluation completed:")
        print(f"Success rate: {evaluation_results['success_rate']:.2%}")
        print(f"Average render time: {evaluation_results['average_render_time']:.2f}s")
        
        # Save results
        results_path = renderer.save_evaluation_results(evaluation_results)
        print(f"Results saved to: {results_path}")
        
    except Exception as e:
        logger.error(f"Example execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())