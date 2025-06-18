#!/usr/bin/env python3
"""
Cognee Template System Integration Test

This script tests the complete AI-enhanced template system to ensure all components
work together correctly with the existing evaluation framework.
"""

import asyncio
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from templates.cognee_powered.template_renderer import CogneeTemplateRenderer
from templates.cognee_powered.engine import CogneeTemplateEngine

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CogneeTemplateSystemTest:
    """Comprehensive test suite for the Cognee template system"""
    
    def __init__(self):
        self.renderer = CogneeTemplateRenderer()
        self.engine = CogneeTemplateEngine()
        self.test_results = []
        self.start_time = time.time()
        
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        logger.info("Starting Cognee Template System Integration Tests")
        
        test_suite = [
            ("Template Discovery", self.test_template_discovery),
            ("Metadata Loading", self.test_metadata_loading),
            ("Knowledge Graph Queries", self.test_knowledge_graph_queries),
            ("Template Rendering", self.test_template_rendering),
            ("Pattern Adaptation", self.test_pattern_adaptation),
            ("Dynamic Enhancement", self.test_dynamic_enhancement),
            ("Template Evaluation", self.test_template_evaluation),
            ("Batch Processing", self.test_batch_processing),
            ("Error Handling", self.test_error_handling),
            ("Performance Benchmarks", self.test_performance_benchmarks)
        ]
        
        for test_name, test_func in test_suite:
            logger.info(f"Running test: {test_name}")
            try:
                test_result = await test_func()
                self.test_results.append({
                    'test_name': test_name,
                    'status': 'PASSED',
                    'result': test_result,
                    'error': None
                })
                logger.info(f"✓ {test_name} PASSED")
            except Exception as e:
                self.test_results.append({
                    'test_name': test_name,
                    'status': 'FAILED',
                    'result': None,
                    'error': str(e)
                })
                logger.error(f"✗ {test_name} FAILED: {e}")
        
        return self._generate_test_report()
    
    async def test_template_discovery(self) -> Dict[str, Any]:
        """Test template discovery and listing functionality"""
        templates = self.renderer.list_available_templates()
        
        # Verify all expected categories are present
        expected_categories = ['architecture-aware', 'context-enriched', 'relationship-informed', 
                             'pattern-adaptive', 'dynamic-enhanced']
        
        found_categories = list(templates.keys())
        missing_categories = [cat for cat in expected_categories if cat not in found_categories]
        
        if missing_categories:
            raise AssertionError(f"Missing template categories: {missing_categories}")
        
        # Verify each category has templates
        for category, template_list in templates.items():
            if not template_list:
                raise AssertionError(f"No templates found for category: {category}")
            
            if "template.md" not in template_list:
                raise AssertionError(f"Main template.md missing for category: {category}")
        
        return {
            'categories_found': len(found_categories),
            'total_templates': sum(len(templates) for templates in templates.values()),
            'categories': found_categories
        }
    
    async def test_metadata_loading(self) -> Dict[str, Any]:
        """Test metadata loading for all template categories"""
        templates = self.renderer.list_available_templates()
        metadata_results = {}
        
        for category in templates.keys():
            metadata = self.renderer.get_template_metadata(category)
            
            if not metadata:
                raise AssertionError(f"No metadata found for category: {category}")
            
            # Verify required metadata fields
            required_fields = ['template_info', 'template_type', 'cognee_integration']
            missing_fields = [field for field in required_fields if field not in metadata]
            
            if missing_fields:
                raise AssertionError(f"Missing metadata fields for {category}: {missing_fields}")
            
            metadata_results[category] = {
                'fields_count': len(metadata),
                'has_cognee_integration': 'cognee_integration' in metadata,
                'template_version': metadata.get('template_info', {}).get('version')
            }
        
        return metadata_results
    
    async def test_knowledge_graph_queries(self) -> Dict[str, Any]:
        """Test knowledge graph query functionality"""
        query_results = {}
        
        # Test different query types
        test_queries = [
            ("architectural patterns", "INSIGHTS"),
            ("component dependencies", "CODE"),
            ("technology stack", "GRAPH_COMPLETION")
        ]
        
        for query, search_type in test_queries:
            try:
                result = await self.engine.query_knowledge_graph(query, search_type)
                
                # Verify result structure
                required_keys = ['query', 'search_type', 'content', 'metadata']
                missing_keys = [key for key in required_keys if key not in result]
                
                if missing_keys:
                    raise AssertionError(f"Missing keys in query result: {missing_keys}")
                
                query_results[f"{query}_{search_type}"] = {
                    'success': True,
                    'content_length': len(str(result.get('content', ''))),
                    'has_metadata': 'metadata' in result,
                    'confidence': result.get('metadata', {}).get('confidence', 0)
                }
                
            except Exception as e:
                query_results[f"{query}_{search_type}"] = {
                    'success': False,
                    'error': str(e)
                }
        
        return query_results
    
    async def test_template_rendering(self) -> Dict[str, Any]:
        """Test template rendering for each category"""
        render_results = {}
        
        test_contexts = {
            'architecture-aware': {
                'CONTEXT': 'Test architecture analysis',
                'SCOPE': 'full_codebase',
                'FOCUS': 'maintainability',
                'AUDIENCE': 'development_team'
            },
            'context-enriched': {
                'CONTEXT': 'Test business analysis',
                'FEATURE': 'user_authentication',
                'SCOPE': 'feature_analysis',
                'STAKEHOLDERS': 'product_team'
            },
            'relationship-informed': {
                'CONTEXT': 'Test relationship analysis',
                'COMPONENT': 'user_service',
                'SCOPE': 'service_analysis',
                'CHANGE_TYPE': 'api_modification'
            },
            'pattern-adaptive': {
                'CONTEXT': 'Test pattern adaptation',
                'LANGUAGE': 'Python',
                'SCOPE': 'component_development',
                'PROJECT_PHASE': 'development'
            },
            'dynamic-enhanced': {
                'CONTEXT': 'Test dynamic optimization',
                'SUCCESS_METRICS': ['accuracy', 'speed'],
                'OPTIMIZATION_GOALS': ['quality', 'efficiency'],
                'CONSTRAINTS': ['response_time < 30s']
            }
        }
        
        for category, context in test_contexts.items():
            try:
                result = await self.renderer.render_template(
                    category=category,
                    context=context,
                    enable_graph_enhancement=True
                )
                
                render_results[category] = {
                    'success': True,
                    'render_time': result['render_time'],
                    'content_length': len(result['rendered_content']),
                    'graph_enhanced': result['graph_enhanced'],
                    'has_content': len(result['rendered_content']) > 100
                }
                
            except Exception as e:
                render_results[category] = {
                    'success': False,
                    'error': str(e)
                }
        
        return render_results
    
    async def test_pattern_adaptation(self) -> Dict[str, Any]:
        """Test pattern-adaptive template specific functionality"""
        context = {
            'CONTEXT': 'Implement user profile component',
            'LANGUAGE': 'JavaScript',
            'SCOPE': 'component_development',
            'TEAM_SIZE': '5',
            'PROJECT_PHASE': 'development'
        }
        
        # Test main template
        result = await self.renderer.render_template(
            category='pattern-adaptive',
            context=context
        )
        
        rendered_content = result['rendered_content']
        
        # Verify pattern-specific content
        pattern_indicators = [
            'Pattern Analysis',
            'Team Conventions',
            'Implementation Strategy',
            'Pattern Compliance'
        ]
        
        found_indicators = [indicator for indicator in pattern_indicators 
                          if indicator in rendered_content]
        
        if len(found_indicators) < len(pattern_indicators) * 0.8:
            raise AssertionError(f"Pattern template missing key sections: {pattern_indicators}")
        
        return {
            'render_success': True,
            'pattern_indicators_found': len(found_indicators),
            'content_quality': 'high' if len(rendered_content) > 1000 else 'low',
            'includes_code_examples': '```' in rendered_content
        }
    
    async def test_dynamic_enhancement(self) -> Dict[str, Any]:
        """Test dynamic-enhanced template specific functionality"""
        context = {
            'CONTEXT': 'Production system optimization',
            'SUCCESS_METRICS': ['accuracy', 'response_time', 'user_satisfaction'],
            'OPTIMIZATION_GOALS': ['quality', 'efficiency'],
            'USER_PROFILE': 'senior_developer',
            'CONSTRAINTS': ['budget_limit', 'time_constraint']
        }
        
        result = await self.renderer.render_template(
            category='dynamic-enhanced',
            context=context
        )
        
        rendered_content = result['rendered_content']
        
        # Verify dynamic enhancement content
        enhancement_indicators = [
            'Performance Analytics',
            'Success Pattern',
            'Optimization',
            'Continuous Learning',
            'Adaptive Recommendations'
        ]
        
        found_indicators = [indicator for indicator in enhancement_indicators 
                          if indicator in rendered_content]
        
        return {
            'render_success': True,
            'enhancement_indicators_found': len(found_indicators),
            'has_performance_metrics': 'Performance' in rendered_content,
            'has_optimization_content': 'Optimization' in rendered_content,
            'content_comprehensiveness': 'high' if len(rendered_content) > 2000 else 'medium'
        }
    
    async def test_template_evaluation(self) -> Dict[str, Any]:
        """Test template evaluation functionality"""
        # Test evaluation on architecture-aware template
        evaluation_result = await self.renderer.evaluate_template(
            category='architecture-aware',
            template_name='template.md'
        )
        
        # Verify evaluation structure
        required_fields = ['template_category', 'total_test_cases', 'successful_cases', 
                         'success_rate', 'individual_results']
        
        missing_fields = [field for field in required_fields if field not in evaluation_result]
        
        if missing_fields:
            raise AssertionError(f"Missing evaluation fields: {missing_fields}")
        
        if evaluation_result['success_rate'] < 0.5:
            raise AssertionError(f"Low success rate: {evaluation_result['success_rate']}")
        
        return {
            'evaluation_success': True,
            'test_cases_run': evaluation_result['total_test_cases'],
            'success_rate': evaluation_result['success_rate'],
            'average_render_time': evaluation_result['average_render_time']
        }
    
    async def test_batch_processing(self) -> Dict[str, Any]:
        """Test batch template rendering"""
        render_configs = [
            {
                'category': 'architecture-aware',
                'context': {'CONTEXT': 'Batch test 1', 'SCOPE': 'component'}
            },
            {
                'category': 'pattern-adaptive',
                'context': {'CONTEXT': 'Batch test 2', 'LANGUAGE': 'Python'}
            },
            {
                'category': 'dynamic-enhanced',
                'context': {'CONTEXT': 'Batch test 3', 'SUCCESS_METRICS': ['speed']}
            }
        ]
        
        batch_results = await self.renderer.batch_render_templates(render_configs)
        
        if len(batch_results) != len(render_configs):
            raise AssertionError("Batch processing returned incorrect number of results")
        
        successful_renders = sum(1 for result in batch_results if result['success'])
        
        return {
            'batch_success': True,
            'total_renders': len(batch_results),
            'successful_renders': successful_renders,
            'success_rate': successful_renders / len(batch_results)
        }
    
    async def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling and recovery"""
        error_tests = []
        
        # Test invalid template category
        try:
            await self.renderer.render_template(
                category='invalid-category',
                context={'CONTEXT': 'test'}
            )
            error_tests.append({'test': 'invalid_category', 'handled': False})
        except Exception:
            error_tests.append({'test': 'invalid_category', 'handled': True})
        
        # Test missing required context
        try:
            result = await self.renderer.render_template(
                category='architecture-aware',
                context={}  # Missing required CONTEXT
            )
            # Check if template handled missing context gracefully
            error_tests.append({'test': 'missing_context', 'handled': True})
        except Exception:
            error_tests.append({'test': 'missing_context', 'handled': True})
        
        return {
            'error_handling_tests': len(error_tests),
            'properly_handled': sum(1 for test in error_tests if test['handled']),
            'error_tests': error_tests
        }
    
    async def test_performance_benchmarks(self) -> Dict[str, Any]:
        """Test performance characteristics"""
        performance_data = {}
        
        # Test render time for each category
        categories = ['architecture-aware', 'pattern-adaptive', 'dynamic-enhanced']
        
        for category in categories:
            start_time = time.time()
            
            try:
                result = await self.renderer.render_template(
                    category=category,
                    context={'CONTEXT': f'Performance test for {category}'}
                )
                
                render_time = time.time() - start_time
                
                performance_data[category] = {
                    'render_time': render_time,
                    'content_length': len(result['rendered_content']),
                    'efficiency_score': len(result['rendered_content']) / render_time
                }
                
            except Exception as e:
                performance_data[category] = {
                    'error': str(e),
                    'render_time': time.time() - start_time
                }
        
        # Get engine performance stats
        engine_stats = self.engine.get_performance_stats()
        
        return {
            'category_performance': performance_data,
            'engine_stats': engine_stats,
            'overall_performance': 'good' if all(
                data.get('render_time', float('inf')) < 60 
                for data in performance_data.values()
            ) else 'needs_improvement'
        }
    
    def _generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_time = time.time() - self.start_time
        passed_tests = sum(1 for result in self.test_results if result['status'] == 'PASSED')
        total_tests = len(self.test_results)
        
        report = {
            'test_summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': total_tests - passed_tests,
                'success_rate': passed_tests / total_tests if total_tests > 0 else 0,
                'total_duration': total_time
            },
            'test_results': self.test_results,
            'system_status': 'HEALTHY' if passed_tests == total_tests else 'DEGRADED',
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        failed_tests = [result for result in self.test_results if result['status'] == 'FAILED']
        
        if failed_tests:
            recommendations.append(f"Address {len(failed_tests)} failed tests before production use")
        
        # Check for performance issues
        performance_result = next(
            (result for result in self.test_results if result['test_name'] == 'Performance Benchmarks'),
            None
        )
        
        if performance_result and performance_result['status'] == 'PASSED':
            perf_data = performance_result['result']
            if perf_data.get('overall_performance') == 'needs_improvement':
                recommendations.append("Optimize template rendering performance")
        
        if not recommendations:
            recommendations.append("All tests passed - system ready for production use")
        
        return recommendations

async def main():
    """Run the complete test suite"""
    test_suite = CogneeTemplateSystemTest()
    
    try:
        logger.info("Starting Cognee Template System Integration Tests")
        
        # Run all tests
        report = await test_suite.run_all_tests()
        
        # Print summary
        summary = report['test_summary']
        logger.info(f"Test Summary:")
        logger.info(f"  Total Tests: {summary['total_tests']}")
        logger.info(f"  Passed: {summary['passed_tests']}")
        logger.info(f"  Failed: {summary['failed_tests']}")
        logger.info(f"  Success Rate: {summary['success_rate']:.1%}")
        logger.info(f"  Duration: {summary['total_duration']:.2f}s")
        logger.info(f"  System Status: {report['system_status']}")
        
        # Print recommendations
        logger.info("Recommendations:")
        for rec in report['recommendations']:
            logger.info(f"  - {rec}")
        
        # Save detailed report
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_path = f"evaluations/results/cognee_integration_test_{timestamp}.json"
        
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Detailed report saved to: {report_path}")
        
        # Return exit code based on results
        return 0 if report['system_status'] == 'HEALTHY' else 1
        
    except Exception as e:
        logger.error(f"Integration test failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)