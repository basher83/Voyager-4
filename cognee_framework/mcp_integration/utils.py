#!/usr/bin/env python3
"""
MCP Cognee Integration Utilities

This module provides utility functions for integrating the CogneeEnhancedEvaluator
with actual MCP Cognee functions. It demonstrates how to use the prepared data
and queries with real MCP operations.
"""

import json
import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPCogneeIntegrator:
    """Utility class for integrating CogneeEnhancedEvaluator with MCP Cognee functions."""
    
    def __init__(self, mcp_functions: Optional[Dict[str, Callable]] = None):
        """
        Initialize the integrator.
        
        Args:
            mcp_functions: Dictionary of MCP function names to actual function callables.
                          Expected keys: 'cognify', 'search', 'prune', 'cognify_status', 'codify_status'
        """
        self.mcp_functions = mcp_functions or {}
        self.operation_log = []
    
    async def process_evaluator_with_mcp(self, evaluator, use_prune: bool = True) -> Dict[str, Any]:
        """
        Process a CogneeEnhancedEvaluator with real MCP operations.
        
        Args:
            evaluator: CogneeEnhancedEvaluator instance with prepared data
            use_prune: Whether to reset the knowledge base before processing
            
        Returns:
            Dictionary containing MCP operation results
        """
        
        if not evaluator.knowledge_graph_created:
            raise ValueError("Evaluator must have knowledge graph data prepared")
        
        results = {
            "mcp_operations": [],
            "search_results": [],
            "errors": [],
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Step 1: Optional knowledge base reset
            if use_prune and 'prune' in self.mcp_functions:
                await self._execute_prune(results)
            
            # Step 2: Process knowledge data with cognify
            knowledge_data = evaluator.prepare_knowledge_data()
            if knowledge_data and 'cognify' in self.mcp_functions:
                await self._execute_cognify(knowledge_data, results)
                
                # Wait for processing to complete
                if 'cognify_status' in self.mcp_functions:
                    await self._wait_for_cognify_completion(results)
            
            # Step 3: Execute search queries
            mcp_queries = evaluator.get_mcp_queries()
            if mcp_queries.get('search_queries') and 'search' in self.mcp_functions:
                await self._execute_search_queries(mcp_queries['search_queries'], results)
            
            # Step 4: Log summary
            results['summary'] = {
                'total_operations': len(results['mcp_operations']),
                'successful_operations': len([op for op in results['mcp_operations'] if op['success']]),
                'search_results_count': len(results['search_results']),
                'errors_count': len(results['errors'])
            }
            
            logger.info(f"MCP processing completed: {results['summary']}")
            
        except Exception as e:
            logger.error(f"MCP processing failed: {e}")
            results['errors'].append({
                'operation': 'general',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        
        return results
    
    async def _execute_prune(self, results: Dict):
        """Execute prune operation to reset knowledge base."""
        try:
            logger.info("Executing prune operation...")
            prune_result = await self.mcp_functions['prune']()
            
            results['mcp_operations'].append({
                'operation': 'prune',
                'success': True,
                'result': prune_result,
                'timestamp': datetime.now().isoformat()
            })
            
            logger.info("✅ Prune operation completed")
            
        except Exception as e:
            logger.error(f"❌ Prune operation failed: {e}")
            results['errors'].append({
                'operation': 'prune',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            
            results['mcp_operations'].append({
                'operation': 'prune',
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
    
    async def _execute_cognify(self, knowledge_data: str, results: Dict):
        """Execute cognify operation to create knowledge graph."""
        try:
            logger.info(f"Executing cognify operation with {len(knowledge_data)} characters...")
            cognify_result = await self.mcp_functions['cognify'](data=knowledge_data)
            
            results['mcp_operations'].append({
                'operation': 'cognify',
                'success': True,
                'result': cognify_result,
                'data_size': len(knowledge_data),
                'timestamp': datetime.now().isoformat()
            })
            
            logger.info("✅ Cognify operation completed")
            
        except Exception as e:
            logger.error(f"❌ Cognify operation failed: {e}")
            results['errors'].append({
                'operation': 'cognify',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            
            results['mcp_operations'].append({
                'operation': 'cognify',
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
    
    async def _wait_for_cognify_completion(self, results: Dict, max_wait: int = 60):
        """Wait for cognify operation to complete by checking status."""
        try:
            logger.info("Checking cognify status...")
            
            for attempt in range(max_wait):
                status_result = await self.mcp_functions['cognify_status']()
                
                # Log status check
                results['mcp_operations'].append({
                    'operation': 'cognify_status',
                    'success': True,
                    'result': status_result,
                    'attempt': attempt + 1,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Check if status indicates completion
                # This is a simplified check - actual implementation would parse status_result
                status_text = str(status_result).lower()
                if 'complete' in status_text or 'finished' in status_text or 'success' in status_text:
                    logger.info("✅ Cognify processing completed")
                    break
                
                if attempt < max_wait - 1:
                    await asyncio.sleep(1)  # Wait 1 second between checks
            
            else:
                logger.warning("⚠️ Cognify status check timed out")
                
        except Exception as e:
            logger.error(f"❌ Cognify status check failed: {e}")
            results['errors'].append({
                'operation': 'cognify_status',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
    
    async def _execute_search_queries(self, search_queries: List[Dict], results: Dict):
        """Execute all search queries and collect results."""
        logger.info(f"Executing {len(search_queries)} search queries...")
        
        for i, query_data in enumerate(search_queries):
            try:
                search_query = query_data['search_query']
                search_type = query_data['search_type']
                
                logger.info(f"  Executing search query {i+1}/{len(search_queries)}: {search_type}")
                
                # Execute search
                search_result = await self.mcp_functions['search'](
                    search_query=search_query,
                    search_type=search_type
                )
                
                # Store result
                result_data = {
                    'query_index': i,
                    'search_type': search_type,
                    'case_id': query_data.get('case_id', 'unknown'),
                    'description': query_data.get('description', ''),
                    'result': search_result,
                    'success': True,
                    'timestamp': datetime.now().isoformat()
                }
                
                results['search_results'].append(result_data)
                
                # Log operation
                results['mcp_operations'].append({
                    'operation': 'search',
                    'success': True,
                    'search_type': search_type,
                    'case_id': query_data.get('case_id', 'unknown'),
                    'result_length': len(str(search_result)),
                    'timestamp': datetime.now().isoformat()
                })
                
                logger.info(f"    ✅ Search query {i+1} completed")
                
            except Exception as e:
                logger.error(f"    ❌ Search query {i+1} failed: {e}")
                
                # Store error
                results['errors'].append({
                    'operation': 'search',
                    'query_index': i,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
                
                # Log failed operation
                results['mcp_operations'].append({
                    'operation': 'search',
                    'success': False,
                    'search_type': query_data.get('search_type', 'unknown'),
                    'case_id': query_data.get('case_id', 'unknown'),
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        logger.info(f"✅ Search operations completed: {len(results['search_results'])} successful")


def create_mcp_function_map(**kwargs) -> Dict[str, Callable]:
    """
    Create a mapping of MCP function names to actual functions.
    
    Example usage:
        mcp_functions = create_mcp_function_map(
            cognify=mcp__cognee__cognify,
            search=mcp__cognee__search,
            prune=mcp__cognee__prune,
            cognify_status=mcp__cognee__cognify_status
        )
    
    Args:
        **kwargs: Named arguments mapping function names to callables
        
    Returns:
        Dictionary mapping function names to callables
    """
    return kwargs


async def integrate_evaluator_with_mcp(evaluator, mcp_functions: Dict[str, Callable]) -> Dict[str, Any]:
    """
    Convenience function to integrate an evaluator with MCP functions.
    
    Args:
        evaluator: CogneeEnhancedEvaluator instance with prepared data
        mcp_functions: Dictionary of MCP function names to callables
        
    Returns:
        Dictionary containing MCP operation results
    """
    integrator = MCPCogneeIntegrator(mcp_functions)
    return await integrator.process_evaluator_with_mcp(evaluator)


def format_mcp_results_for_evaluator(mcp_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format MCP operation results for use with CogneeEnhancedEvaluator.process_mcp_results().
    
    Args:
        mcp_results: Raw MCP operation results from MCPCogneeIntegrator
        
    Returns:
        Formatted results compatible with CogneeEnhancedEvaluator
    """
    formatted = {
        "cognify_result": None,
        "search_results": [],
        "operation_summary": {}
    }
    
    # Extract cognify result
    cognify_ops = [op for op in mcp_results.get('mcp_operations', []) if op['operation'] == 'cognify']
    if cognify_ops and cognify_ops[0]['success']:
        formatted["cognify_result"] = cognify_ops[0]['result']
    
    # Format search results
    for search_result in mcp_results.get('search_results', []):
        if search_result['success']:
            formatted["search_results"].append({
                "query_index": search_result['query_index'],
                "search_type": search_result['search_type'],
                "case_id": search_result['case_id'],
                "result": search_result['result'],
                "description": search_result['description']
            })
    
    # Create operation summary
    summary = mcp_results.get('summary', {})
    formatted["operation_summary"] = {
        "cognify_executed": bool(formatted["cognify_result"]),
        "search_operations_completed": len(formatted["search_results"]),
        "total_operations": summary.get('total_operations', 0),
        "successful_operations": summary.get('successful_operations', 0),
        "execution_timestamp": mcp_results.get('timestamp')
    }
    
    return formatted


# Example usage function
async def example_usage():
    """Example of how to use the MCP integration utilities."""
    from evaluations.scripts.cognee_enhanced_evaluator import CogneeEnhancedEvaluator
    
    # Note: These would be the actual MCP functions when available
    # For demonstration, we show the function signatures
    
    def example_mcp_cognify(data: str):
        """Example cognify function signature."""
        return f"Processed {len(data)} characters into knowledge graph"
    
    def example_mcp_search(search_query: str, search_type: str):
        """Example search function signature."""
        return f"Search results for {search_type}: {search_query[:100]}..."
    
    def example_mcp_prune():
        """Example prune function signature."""
        return "Knowledge base reset completed"
    
    def example_mcp_cognify_status():
        """Example cognify status function signature."""
        return "Processing complete - ready for queries"
    
    # Create MCP function mapping
    mcp_functions = create_mcp_function_map(
        cognify=example_mcp_cognify,
        search=example_mcp_search,
        prune=example_mcp_prune,
        cognify_status=example_mcp_cognify_status
    )
    
    # Create and prepare evaluator
    evaluator = CogneeEnhancedEvaluator()
    
    # Simulate preparing knowledge graph (normally done during evaluation)
    test_cases = [{"id": "test1", "input": "test input", "expected": "test output"}]
    prompt = "Test prompt"
    await evaluator._create_knowledge_graph(test_cases, prompt)
    
    # Integrate with MCP
    mcp_results = await integrate_evaluator_with_mcp(evaluator, mcp_functions)
    
    # Format results for evaluator processing
    formatted_results = format_mcp_results_for_evaluator(mcp_results)
    
    # Process with evaluator
    processed_results = evaluator.process_mcp_results(formatted_results)
    
    print("MCP Integration Example Completed:")
    print(f"  MCP Operations: {len(mcp_results.get('mcp_operations', []))}")
    print(f"  Search Results: {len(mcp_results.get('search_results', []))}")
    print(f"  Processed Insights: {len(processed_results.get('knowledge_insights', {}))}")


if __name__ == "__main__":
    print("MCP Cognee Integration Utilities")
    print("="*40)
    print("This module provides utilities for integrating CogneeEnhancedEvaluator")
    print("with actual MCP Cognee functions.")
    print()
    print("Key functions:")
    print("- MCPCogneeIntegrator: Main integration class")
    print("- integrate_evaluator_with_mcp(): Convenience function")
    print("- format_mcp_results_for_evaluator(): Result formatting")
    print("- create_mcp_function_map(): Function mapping helper")
    print()
    print("Run example_usage() to see integration example.")
    
    # Uncomment to run example
    # asyncio.run(example_usage())