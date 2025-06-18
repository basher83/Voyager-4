#!/usr/bin/env python3
"""
Runner script for CogneeEnhancedEvaluator demonstration
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from cognee_framework.evaluation import CogneeEnhancedEvaluator

async def run_demo():
    """Run enhanced evaluation demonstration."""
    
    # Configure paths
    prompt_path = "/Users/basher8383/dev/learning/Voyager-4/templates/base/codebase-overview-template.md"
    test_cases_path = "/Users/basher8383/dev/learning/Voyager-4/test_cases/examples/codebase_understanding_examples.json"
    output_path = "/Users/basher8383/dev/learning/Voyager-4/evaluations/results/cognee_demo_results.json"
    
    # Enhanced cognee configuration
    cognee_config = {
        "use_knowledge_context": True,
        "create_test_case_graph": True,
        "analyze_evaluation_patterns": True,
        "search_types": ["GRAPH_COMPLETION", "CODE", "INSIGHTS"],
        "knowledge_weight": 0.3
    }
    
    print("Starting Cognee-Enhanced Evaluation Demonstration...")
    print("=" * 60)
    
    # Initialize evaluator
    evaluator = CogneeEnhancedEvaluator(
        config_path="/Users/basher8383/dev/learning/Voyager-4/evaluations/config/default_config.yaml",
        cognee_config=cognee_config
    )
    
    try:
        # Run enhanced evaluation
        results = await evaluator.evaluate_prompt_with_knowledge(
            prompt_path=prompt_path,
            test_cases_path=test_cases_path,
            output_path=output_path
        )
        
        print("\n" + "=" * 60)
        print("ENHANCED EVALUATION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
        return results
        
    except Exception as e:
        print(f"Enhanced evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    results = asyncio.run(run_demo())
    sys.exit(0 if results and results.get("summary", {}).get("overall_status") == "PASS" else 1)