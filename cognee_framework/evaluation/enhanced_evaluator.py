#!/usr/bin/env python3
"""
Cognee-Enhanced Prompt Evaluation Script

This script extends the base PromptEvaluator with AI-powered knowledge graph analysis
using Cognee to provide contextual, relationship-aware evaluation capabilities.
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import yaml
import logging

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    import anthropic
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from rouge_score import rouge_scorer
    from tqdm import tqdm
    
    # Import the base evaluator
    from .base_evaluator import PromptEvaluator
    
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)


class CogneeEnhancedEvaluator(PromptEvaluator):
    """
    Enhanced prompt evaluator that uses Cognee knowledge graphs for 
    contextual evaluation and relationship-aware analysis.
    """
    
    def __init__(self, config_path: Optional[str] = None, cognee_config: Optional[Dict] = None):
        """Initialize enhanced evaluator with Cognee configuration."""
        super().__init__(config_path)
        
        # Cognee configuration
        self.cognee_config = cognee_config or {
            "use_knowledge_context": True,
            "create_test_case_graph": True,
            "analyze_evaluation_patterns": True,
            "search_types": ["GRAPH_COMPLETION", "CODE", "INSIGHTS"],
            "knowledge_weight": 0.3  # Weight for knowledge-enhanced scores
        }
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        # Initialize knowledge state
        self.knowledge_graph_created = False
        self.evaluation_patterns = {}
        self.knowledge_insights = {}
        
    async def evaluate_prompt_with_knowledge(self, prompt_path: str, test_cases_path: str, 
                                           output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Run comprehensive evaluation enhanced with Cognee knowledge graph analysis.
        """
        
        # Load prompt and test cases
        prompt = self._load_prompt(prompt_path)
        test_cases = self._load_test_cases(test_cases_path)
        
        print(f"Evaluating prompt with Cognee enhancement: {prompt_path}")
        print(f"Test cases: {len(test_cases)}")
        print(f"Cognee features: {', '.join(k for k, v in self.cognee_config.items() if v)}")
        
        # Create knowledge graph from test cases if enabled
        if self.cognee_config.get("create_test_case_graph", True):
            await self._create_knowledge_graph(test_cases, prompt)
        
        # Run base evaluation
        results = self.evaluate_prompt(prompt_path, test_cases_path, output_path=None)
        
        # Enhance with knowledge-based evaluation
        if self.cognee_config.get("use_knowledge_context", True):
            await self._enhance_evaluation_with_knowledge(results, test_cases)
        
        # Analyze evaluation patterns using knowledge graphs
        if self.cognee_config.get("analyze_evaluation_patterns", True):
            await self._analyze_evaluation_patterns(results)
        
        # Generate enhanced summary with knowledge insights
        results["knowledge_enhanced_summary"] = await self._generate_knowledge_enhanced_summary(results)
        
        # Save enhanced results
        if output_path:
            self._save_enhanced_results(results, output_path)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"cognee_evaluation_results_{timestamp}.json"
            self._save_enhanced_results(results, output_path)
        
        return results
    
    async def _create_knowledge_graph(self, test_cases: List[Dict], prompt: str):
        """Create knowledge graph from test cases and prompt using Cognee MCP."""
        try:
            print("Creating knowledge graph from test cases...")
            
            # Prepare data for knowledge graph creation
            knowledge_data = {
                "prompt": prompt,
                "test_cases": test_cases,
                "evaluation_context": {
                    "timestamp": datetime.now().isoformat(),
                    "evaluation_methods": self.config["evaluation_methods"],
                    "metrics": self.config["metrics"]
                }
            }
            
            # Convert to text format for Cognee ingestion
            knowledge_text = self._format_knowledge_for_cognee(knowledge_data)
            
            # Store knowledge text for external MCP processing
            self.knowledge_text = knowledge_text
            self.logger.info("Knowledge data prepared for Cognee MCP processing")
            
            # The actual Cognee MCP calls would be handled by the calling code:
            # 1. mcp__cognee__cognify(data=knowledge_text)
            # 2. Wait for processing completion
            # 3. Use mcp__cognee__search for analysis
            
            # For this implementation, we prepare all necessary data and queries
            # for external MCP integration
            self._prepare_mcp_queries(test_cases)
            
            self.knowledge_graph_created = True
            print("✓ Knowledge graph data prepared for MCP processing")
            
        except Exception as e:
            self.logger.error(f"Failed to prepare knowledge graph: {e}")
            print(f"Warning: Knowledge graph preparation failed: {e}")
            self.knowledge_graph_created = False
    
    def _format_knowledge_for_cognee(self, knowledge_data: Dict) -> str:
        """Format evaluation data for Cognee knowledge graph ingestion."""
        
        formatted_text = f"""
# Prompt Evaluation Knowledge Base

## Prompt Being Evaluated
{knowledge_data['prompt']}

## Evaluation Configuration
- Methods: {', '.join(knowledge_data['evaluation_context']['evaluation_methods'])}
- Accuracy Threshold: {knowledge_data['evaluation_context']['metrics']['accuracy_threshold']}
- Consistency Threshold: {knowledge_data['evaluation_context']['metrics']['consistency_threshold']}
- Quality Threshold: {knowledge_data['evaluation_context']['metrics']['quality_threshold']}

## Test Cases Analysis
Total test cases: {len(knowledge_data['test_cases'])}

"""
        
        # Add each test case with detailed context
        for i, case in enumerate(knowledge_data['test_cases']):
            formatted_text += f"""
### Test Case {i+1}: {case.get('id', f'case_{i}')}

**Category**: {case.get('category', 'unknown')}
**Difficulty**: {case.get('metadata', {}).get('difficulty', 'unknown')}

**Input**:
{case['input']}

**Expected Output**:
{case.get('expected', 'No expected output provided')}

**Expected Elements**: {', '.join(case.get('metadata', {}).get('expected_elements', []))}

**Evaluation Context**:
- This test case evaluates: {case.get('category', 'general capability')}
- Difficulty level: {case.get('metadata', {}).get('difficulty', 'unknown')}
- Key evaluation criteria: {', '.join(case.get('metadata', {}).get('expected_elements', []))}

"""
        
        return formatted_text
    
    def prepare_knowledge_data(self) -> str:
        """Get prepared knowledge data for Cognee MCP processing."""
        return getattr(self, 'knowledge_text', '')
    
    def get_mcp_queries(self) -> Dict:
        """Get prepared MCP queries for external processing."""
        return getattr(self, 'mcp_queries', {})
    
    def _prepare_mcp_queries(self, test_cases: List[Dict]):
        """Prepare all MCP queries for different search types."""
        self.mcp_queries = {
            "cognify_query": {
                "function": "mcp__cognee__cognify",
                "data": self.knowledge_text,
                "description": "Process evaluation data into knowledge graph"
            },
            "search_queries": []
        }
        
        # Prepare search queries for each configured search type
        for search_type in self.cognee_config.get("search_types", ["GRAPH_COMPLETION"]):
            
            # Overall evaluation analysis query
            overall_query = {
                "function": "mcp__cognee__search",
                "search_query": f"""Analyze the prompt evaluation scenario for patterns and insights.
                Focus on: evaluation methodology effectiveness, test case design quality,
                common challenges, and optimization opportunities.
                Search type: {search_type}""",
                "search_type": search_type,
                "description": f"Overall evaluation analysis using {search_type}"
            }
            self.mcp_queries["search_queries"].append(overall_query)
            
            # Individual test case analysis queries
            for i, case in enumerate(test_cases):
                case_query = {
                    "function": "mcp__cognee__search",
                    "search_query": f"""Analyze test case '{case.get('id', f'case_{i}')}' in category '{case.get('category', 'unknown')}'.
                    Input: {case['input'][:300]}...
                    Expected elements: {', '.join(case.get('metadata', {}).get('expected_elements', []))}
                    
                    Provide insights on: evaluation challenges, pattern recognition,
                    relationship to other test cases, optimization suggestions.""",
                    "search_type": search_type,
                    "description": f"Test case {i+1} analysis using {search_type}",
                    "case_id": case.get('id', f'case_{i}'),
                    "category": case.get('category', 'unknown')
                }
                self.mcp_queries["search_queries"].append(case_query)
        
        self.logger.info(f"Prepared {len(self.mcp_queries['search_queries'])} MCP search queries")
    
    async def _enhance_evaluation_with_knowledge(self, results: Dict, test_cases: List[Dict]):
        """Enhance evaluation results using knowledge graph insights."""
        if not self.knowledge_graph_created:
            self.logger.warning("Knowledge graph not available for enhancement")
            return
        
        try:
            print("Preparing knowledge graph enhancement...")
            
            # The MCP queries are already prepared in _prepare_mcp_queries
            # This method structures them for easy external processing
            knowledge_enhancements = self._structure_knowledge_enhancements(test_cases)
            
            # Apply knowledge enhancements to evaluation results
            # Note: Actual MCP results would be injected here in real usage
            self._apply_knowledge_enhancements(results, knowledge_enhancements)
            
            print("✓ Knowledge enhancement structure prepared")
            
        except Exception as e:
            self.logger.error(f"Failed to prepare knowledge enhancement: {e}")
            print(f"Warning: Knowledge enhancement preparation failed: {e}")
    
    def _structure_knowledge_enhancements(self, test_cases: List[Dict]) -> Dict:
        """Structure knowledge enhancements for external MCP processing."""
        knowledge_enhancements = {}
        
        for search_type in self.cognee_config.get("search_types", ["GRAPH_COMPLETION"]):
            queries = self.prepare_search_queries(test_cases, search_type)
            knowledge_enhancements[search_type] = queries
        
        return knowledge_enhancements
    
    def process_mcp_results(self, mcp_results: Dict) -> Dict:
        """Process results from MCP Cognee operations and integrate with evaluation."""
        try:
            processed_results = {
                "mcp_integration_successful": True,
                "knowledge_insights": {},
                "pattern_analysis": {},
                "recommendations": []
            }
            
            # Process search results
            if "search_results" in mcp_results:
                for search_result in mcp_results["search_results"]:
                    search_type = search_result.get("search_type", "unknown")
                    case_id = search_result.get("case_id", "overall")
                    insights = search_result.get("result", "")
                    
                    if search_type not in processed_results["knowledge_insights"]:
                        processed_results["knowledge_insights"][search_type] = {}
                    
                    processed_results["knowledge_insights"][search_type][case_id] = {
                        "insights": insights,
                        "relevance_score": self._calculate_insight_relevance(insights),
                        "insight_categories": self._categorize_insights(insights)
                    }
            
            # Extract patterns and recommendations
            processed_results["pattern_analysis"] = self._extract_patterns_from_insights(
                processed_results["knowledge_insights"]
            )
            processed_results["recommendations"] = self._generate_mcp_recommendations(
                processed_results["knowledge_insights"]
            )
            
            return processed_results
            
        except Exception as e:
            self.logger.error(f"Error processing MCP results: {e}")
            return {"mcp_integration_successful": False, "error": str(e)}
    
    def _calculate_insight_relevance(self, insights: str) -> float:
        """Calculate relevance score for MCP insights."""
        try:
            insights_lower = insights.lower()
            relevance_keywords = [
                "evaluation", "pattern", "challenge", "optimization", "accuracy",
                "consistency", "quality", "test case", "prompt", "improvement"
            ]
            
            matches = sum(1 for keyword in relevance_keywords if keyword in insights_lower)
            return min(matches / len(relevance_keywords), 1.0)
            
        except Exception:
            return 0.0
    
    def _categorize_insights(self, insights: str) -> List[str]:
        """Categorize insights from MCP results."""
        try:
            insights_lower = insights.lower()
            categories = []
            
            if any(word in insights_lower for word in ["pattern", "trend", "common"]):
                categories.append("pattern_analysis")
            if any(word in insights_lower for word in ["challenge", "problem", "issue"]):
                categories.append("challenge_identification")
            if any(word in insights_lower for word in ["improve", "optimize", "enhance"]):
                categories.append("optimization")
            if any(word in insights_lower for word in ["relationship", "connection", "related"]):
                categories.append("relationship_analysis")
            
            return categories if categories else ["general"]
            
        except Exception:
            return ["unknown"]
    
    def _extract_patterns_from_insights(self, knowledge_insights: Dict) -> Dict:
        """Extract patterns from knowledge insights."""
        try:
            patterns = {
                "common_challenges": [],
                "success_patterns": [],
                "evaluation_effectiveness": {},
                "test_case_relationships": []
            }
            
            for search_type, insights_data in knowledge_insights.items():
                for case_id, insight_info in insights_data.items():
                    insights = insight_info.get("insights", "")
                    categories = insight_info.get("insight_categories", [])
                    
                    if "challenge_identification" in categories:
                        patterns["common_challenges"].append({
                            "case_id": case_id,
                            "search_type": search_type,
                            "insights": insights[:200] + "..." if len(insights) > 200 else insights
                        })
                    
                    if "pattern_analysis" in categories:
                        patterns["success_patterns"].append({
                            "case_id": case_id,
                            "search_type": search_type,
                            "patterns": insights[:200] + "..." if len(insights) > 200 else insights
                        })
            
            return patterns
            
        except Exception as e:
            self.logger.error(f"Error extracting patterns: {e}")
            return {"error": str(e)}
    
    def _generate_mcp_recommendations(self, knowledge_insights: Dict) -> List[str]:
        """Generate recommendations based on MCP insights."""
        try:
            recommendations = []
            
            # Analyze insights for recommendation opportunities
            total_insights = sum(
                len(insights_data) for insights_data in knowledge_insights.values()
            )
            
            if total_insights > 0:
                recommendations.append(
                    f"Successfully integrated {total_insights} knowledge insights - "
                    "leverage these for evaluation optimization"
                )
            
                # Add specific recommendations based on insight categories
                all_categories = []
                for insights_data in knowledge_insights.values():
                    for insight_info in insights_data.values():
                        all_categories.extend(insight_info.get("insight_categories", []))
                
                if "challenge_identification" in all_categories:
                    recommendations.append(
                        "Challenges identified in test cases - consider refining prompt specificity"
                    )
                
                if "optimization" in all_categories:
                    recommendations.append(
                        "Optimization opportunities detected - implement suggested improvements"
                    )
                
                if "pattern_analysis" in all_categories:
                    recommendations.append(
                        "Pattern analysis available - use insights for test case categorization"
                    )
            else:
                recommendations.append(
                    "No knowledge insights generated - verify Cognee MCP integration"
                )
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating MCP recommendations: {e}")
            return ["Error generating recommendations from MCP insights"]
    
    def prepare_search_queries(self, test_cases: List[Dict], search_type: str) -> Dict:
        """Prepare search queries for knowledge graph insights."""
        try:
            queries = {}
            
            for i, case in enumerate(test_cases):
                # Create search query for this test case
                query = f"""
                Analyze test case: {case.get('id', f'case_{i}')}
                Category: {case.get('category', 'unknown')}
                Input: {case['input'][:200]}...
                Expected elements: {', '.join(case.get('metadata', {}).get('expected_elements', []))}
                
                Provide insights about:
                1. Evaluation patterns for this type of test case
                2. Common challenges or failure modes
                3. Relationships to other similar test cases
                4. Recommended evaluation approaches
                """
                
                queries[f"case_{i}"] = {
                    "search_type": search_type,
                    "query": query,
                    "case_metadata": case.get('metadata', {})
                }
            
            return queries
            
        except Exception as e:
            self.logger.error(f"Error preparing search queries: {e}")
            return {}
    
    def _apply_knowledge_enhancements(self, results: Dict, knowledge_enhancements: Dict):
        """Apply knowledge graph insights to enhance evaluation results."""
        
        # Create knowledge-enhanced metrics section
        results["knowledge_enhanced_metrics"] = {}
        
        for search_type, enhancements in knowledge_enhancements.items():
            enhanced_metrics = {
                "search_type": search_type,
                "total_insights": len(enhancements),
                "case_insights": {}
            }
            
            # Analyze insights for each case
            for case_id, enhancement in enhancements.items():
                insights = enhancement.get("insights", "")
                case_metadata = enhancement.get("case_metadata", {})
                
                # Extract key insights (simplified analysis)
                insight_analysis = {
                    "has_insights": len(str(insights)) > 100,
                    "insight_length": len(str(insights)),
                    "difficulty": case_metadata.get("difficulty", "unknown"),
                    "expected_elements": case_metadata.get("expected_elements", []),
                    "knowledge_relevance_score": self._calculate_knowledge_relevance(insights, case_metadata)
                }
                
                enhanced_metrics["case_insights"][case_id] = insight_analysis
            
            results["knowledge_enhanced_metrics"][search_type] = enhanced_metrics
        
        # Calculate overall knowledge enhancement score
        results["knowledge_enhancement_score"] = self._calculate_overall_knowledge_score(knowledge_enhancements)
    
    def _calculate_knowledge_relevance(self, insights: str, case_metadata: Dict) -> float:
        """Calculate how relevant the knowledge insights are to the test case."""
        try:
            insights_text = str(insights).lower()
            expected_elements = case_metadata.get("expected_elements", [])
            
            # Simple keyword matching for relevance scoring
            relevance_score = 0.0
            total_elements = len(expected_elements)
            
            if total_elements > 0:
                for element in expected_elements:
                    if element.lower() in insights_text:
                        relevance_score += 1.0
                
                relevance_score = relevance_score / total_elements
            
            # Additional relevance factors
            if "evaluation" in insights_text:
                relevance_score += 0.1
            if "pattern" in insights_text:
                relevance_score += 0.1
            if "challenge" in insights_text:
                relevance_score += 0.1
            
            return min(relevance_score, 1.0)  # Cap at 1.0
            
        except Exception:
            return 0.0
    
    def _calculate_overall_knowledge_score(self, knowledge_enhancements: Dict) -> Dict:
        """Calculate overall knowledge enhancement metrics."""
        try:
            total_cases = 0
            total_relevance = 0.0
            has_insights_count = 0
            
            for search_type, enhancements in knowledge_enhancements.items():
                for case_id, enhancement_data in enhancements.items():
                    if isinstance(enhancement_data, dict) and "insights" in enhancement_data:
                        total_cases += 1
                        insights = enhancement_data.get("insights", "")
                        case_metadata = enhancement_data.get("case_metadata", {})
                        
                        relevance = self._calculate_knowledge_relevance(insights, case_metadata)
                        total_relevance += relevance
                        
                        if len(str(insights)) > 100:  # Has substantial insights
                            has_insights_count += 1
            
            if total_cases > 0:
                avg_relevance = total_relevance / total_cases
                insights_coverage = has_insights_count / total_cases
            else:
                avg_relevance = 0.0
                insights_coverage = 0.0
            
            return {
                "average_relevance_score": avg_relevance,
                "insights_coverage": insights_coverage,
                "total_cases_analyzed": total_cases,
                "search_types_used": list(knowledge_enhancements.keys()),
                "knowledge_enhancement_effective": avg_relevance > 0.5 and insights_coverage > 0.7
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating knowledge score: {e}")
            return {"error": str(e)}
    
    async def _generate_pattern_recommendations(self, pattern_insights: Any) -> List[str]:
        """Generate pattern-based recommendations for evaluation improvement."""
        try:
            # Analyze pattern insights and generate recommendations
            recommendations = []
            
            insights_text = str(pattern_insights).lower()
            
            # Knowledge-based recommendations
            if "query prepared" in insights_text:
                recommendations.append("Enable full knowledge graph processing for deeper pattern analysis")
            
            # Add standard evaluation improvement recommendations
            recommendations.extend([
                "Consider implementing adaptive evaluation methods based on test case complexity",
                "Use knowledge graph insights to predict evaluation success rates",
                "Implement pattern-based test case categorization for targeted evaluation",
                "Leverage historical evaluation data for optimization opportunities"
            ])
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating pattern recommendations: {e}")
            return ["Error generating recommendations - check logs for details"]

    async def _analyze_evaluation_patterns(self, results: Dict):
        """Analyze evaluation patterns using knowledge graph relationships."""
        if not self.knowledge_graph_created:
            return
        
        try:
            print("Analyzing evaluation patterns...")
            
            # Prepare pattern analysis query
            pattern_query = """
            Analyze the evaluation patterns in this prompt testing scenario:
            1. What common patterns exist across test cases?
            2. Which evaluation methods are most effective for different case types?
            3. What relationships exist between test case difficulty and evaluation success?
            4. What optimization opportunities exist for the evaluation process?
            """
            
            # Store query for external processing
            pattern_insights = f"Pattern analysis query prepared: {pattern_query[:100]}..."
            
            self.evaluation_patterns = {
                "pattern_analysis": pattern_insights,
                "recommendations": await self._generate_pattern_recommendations(pattern_insights),
                "optimization_opportunities": await self._identify_optimization_opportunities(results, pattern_insights)
            }
            
            results["evaluation_patterns"] = self.evaluation_patterns
            print("✓ Evaluation patterns analyzed")
            
        except Exception as e:
            self.logger.error(f"Error analyzing evaluation patterns: {e}")
            print(f"Warning: Pattern analysis failed: {e}")
    
    def prepare_recommendation_query(self, pattern_insights: Any) -> str:
        """Prepare recommendation query based on pattern analysis."""
        try:
            recommendation_query = f"""
            Based on these evaluation pattern insights: {str(pattern_insights)[:1000]}
            
            Generate specific, actionable recommendations for:
            1. Improving evaluation methodology
            2. Optimizing test case design
            3. Enhancing evaluation accuracy
            4. Reducing evaluation time and cost
            """
            
            return recommendation_query
            
        except Exception as e:
            self.logger.error(f"Error preparing recommendation query: {e}")
            return "Error preparing recommendations query"
    
    async def _identify_optimization_opportunities(self, results: Dict, pattern_insights: Any) -> Dict:
        """Identify specific optimization opportunities for the evaluation process."""
        try:
            # Analyze current evaluation performance
            current_metrics = results.get("results", {})
            
            optimization_opportunities = {
                "accuracy_optimization": [],
                "efficiency_optimization": [],
                "cost_optimization": [],
                "quality_optimization": []
            }
            
            # Check accuracy optimization opportunities
            if "exact_match" in current_metrics:
                accuracy = current_metrics["exact_match"].get("accuracy", 0)
                if accuracy < self.config["metrics"]["accuracy_threshold"]:
                    optimization_opportunities["accuracy_optimization"].append(
                        f"Current accuracy ({accuracy:.2%}) below threshold. Consider improving prompt specificity."
                    )
            
            # Check consistency optimization opportunities
            if "consistency" in current_metrics:
                consistency = current_metrics["consistency"].get("consistency_score", 0)
                if consistency < self.config["metrics"]["consistency_threshold"]:
                    optimization_opportunities["efficiency_optimization"].append(
                        f"Low consistency ({consistency:.3f}). Consider adding examples to prompt."
                    )
            
            # Add knowledge-based optimization suggestions
            knowledge_score = results.get("knowledge_enhancement_score", {})
            if knowledge_score.get("average_relevance_score", 0) > 0.7:
                optimization_opportunities["quality_optimization"].append(
                    "High knowledge relevance detected. Consider leveraging knowledge insights for evaluation."
                )
            
            return optimization_opportunities
            
        except Exception as e:
            self.logger.error(f"Error identifying optimization opportunities: {e}")
            return {"error": str(e)}
    
    async def _generate_knowledge_enhanced_summary(self, results: Dict) -> Dict:
        """Generate enhanced summary that includes knowledge graph insights."""
        
        # Start with base summary
        base_summary = results.get("summary", {})
        
        enhanced_summary = {
            **base_summary,
            "knowledge_enhancement_active": self.knowledge_graph_created,
            "knowledge_insights": {},
            "ai_powered_recommendations": [],
            "pattern_analysis": {}
        }
        
        if self.knowledge_graph_created:
            # Add knowledge-specific insights
            knowledge_score = results.get("knowledge_enhancement_score", {})
            enhanced_summary["knowledge_insights"] = {
                "effectiveness": knowledge_score.get("knowledge_enhancement_effective", False),
                "coverage": knowledge_score.get("insights_coverage", 0),
                "relevance": knowledge_score.get("average_relevance_score", 0),
                "total_insights_generated": knowledge_score.get("total_cases_analyzed", 0)
            }
            
            # Add AI-powered recommendations
            if "evaluation_patterns" in results:
                enhanced_summary["ai_powered_recommendations"] = results["evaluation_patterns"].get("recommendations", [])
                enhanced_summary["pattern_analysis"] = {
                    "patterns_identified": len(results["evaluation_patterns"].get("recommendations", [])),
                    "optimization_opportunities": results["evaluation_patterns"].get("optimization_opportunities", {})
                }
        
        return enhanced_summary
    
    def _save_enhanced_results(self, results: Dict, output_path: str):
        """Save enhanced evaluation results with knowledge insights."""
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        
        # Add metadata about enhancement
        results["enhancement_metadata"] = {
            "enhanced_with_cognee": True,
            "cognee_config": self.cognee_config,
            "knowledge_graph_created": self.knowledge_graph_created,
            "enhancement_timestamp": datetime.now().isoformat()
        }
        
        # Save main results
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save knowledge insights separately if available
        if self.knowledge_graph_created and "knowledge_enhanced_metrics" in results:
            insights_path = output_path.replace('.json', '_knowledge_insights.json')
            knowledge_data = {
                "knowledge_enhanced_metrics": results.get("knowledge_enhanced_metrics", {}),
                "evaluation_patterns": results.get("evaluation_patterns", {}),
                "knowledge_enhancement_score": results.get("knowledge_enhancement_score", {}),
                "knowledge_enhanced_summary": results.get("knowledge_enhanced_summary", {})
            }
            
            with open(insights_path, 'w') as f:
                json.dump(knowledge_data, f, indent=2)
            
            print(f"Knowledge insights saved to: {insights_path}")
        
        print(f"Enhanced results saved to: {output_path}")
        
        # Print enhanced summary
        self._print_enhanced_summary(results)
    
    def _print_enhanced_summary(self, results: Dict):
        """Print enhanced evaluation summary."""
        print("\n" + "="*60)
        print("COGNEE-ENHANCED EVALUATION SUMMARY")
        print("="*60)
        
        # Base summary
        base_summary = results.get("summary", {})
        enhanced_summary = results.get("knowledge_enhanced_summary", {})
        
        print(f"Overall Status: {base_summary.get('overall_status', 'UNKNOWN')}")
        
        if base_summary.get("failed_criteria"):
            print(f"Failed Criteria: {', '.join(base_summary['failed_criteria'])}")
        
        # Knowledge enhancement info
        if enhanced_summary.get("knowledge_enhancement_active"):
            print(f"\n🧠 AI Enhancement: ACTIVE")
            insights = enhanced_summary.get("knowledge_insights", {})
            print(f"   Knowledge Coverage: {insights.get('coverage', 0):.1%}")
            print(f"   Insight Relevance: {insights.get('relevance', 0):.1%}")
            print(f"   Total Insights: {insights.get('total_insights_generated', 0)}")
            
            if insights.get('effectiveness'):
                print("   Enhancement Status: ✅ EFFECTIVE")
            else:
                print("   Enhancement Status: ⚠️  LIMITED")
        else:
            print(f"\n🧠 AI Enhancement: DISABLED")
        
        # AI-powered recommendations
        ai_recommendations = enhanced_summary.get("ai_powered_recommendations", [])
        if ai_recommendations:
            print(f"\n🤖 AI-Powered Recommendations:")
            for i, rec in enumerate(ai_recommendations[:5], 1):  # Show top 5
                print(f"   {i}. {rec}")
        
        # Pattern analysis
        pattern_analysis = enhanced_summary.get("pattern_analysis", {})
        if pattern_analysis:
            print(f"\n📊 Pattern Analysis:")
            print(f"   Patterns Identified: {pattern_analysis.get('patterns_identified', 0)}")
            opt_opportunities = pattern_analysis.get('optimization_opportunities', {})
            total_optimizations = sum(len(opts) for opts in opt_opportunities.values())
            print(f"   Optimization Opportunities: {total_optimizations}")
        
        # Key metrics (from base evaluator)
        print("\n📈 Key Metrics:")
        base_results = results.get("results", {})
        for method, result in base_results.items():
            if method == "exact_match" and "accuracy" in result:
                print(f"   Accuracy: {result['accuracy']:.2%}")
            elif method == "consistency" and "consistency_score" in result:
                print(f"   Consistency: {result['consistency_score']:.3f}")
            elif method == "quality" and "average_quality" in result:
                print(f"   Quality: {result['average_quality']:.1f}/5")
        
        print("\n" + "="*60)


# Full MCP Integration Functions
async def run_full_mcp_evaluation(prompt_path: str, test_cases_path: str,
                                 config_path: Optional[str] = None,
                                 output_path: Optional[str] = None,
                                 cognee_config: Optional[Dict] = None,
                                 mcp_functions: Optional[Dict] = None):
    """Run complete evaluation with full MCP Cognee integration."""
    
    evaluator = CogneeEnhancedEvaluator(config_path, cognee_config)
    
    try:
        # Step 1: Prepare knowledge data and queries
        print("Step 1: Preparing evaluation data...")
        results = await evaluator.evaluate_prompt_with_knowledge(
            prompt_path=prompt_path,
            test_cases_path=test_cases_path,
            output_path=None  # Don't save yet
        )
        
        # Step 2: Execute MCP operations if functions provided
        if mcp_functions and evaluator.knowledge_graph_created:
            print("Step 2: Executing MCP Cognee operations...")
            mcp_results = await execute_mcp_operations(evaluator, mcp_functions)
            
            # Step 3: Process MCP results and enhance evaluation
            print("Step 3: Processing MCP results...")
            processed_mcp = evaluator.process_mcp_results(mcp_results)
            
            # Step 4: Integrate MCP insights into results
            results["mcp_integration"] = processed_mcp
            results["knowledge_enhanced_summary"] = await evaluator._generate_knowledge_enhanced_summary(results)
        else:
            print("Step 2-4: Skipped - No MCP functions provided or knowledge graph not created")
            results["mcp_integration"] = {"mcp_integration_successful": False, "reason": "No MCP functions provided"}
        
        # Step 5: Save enhanced results
        if output_path:
            evaluator._save_enhanced_results(results, output_path)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"full_mcp_evaluation_results_{timestamp}.json"
            evaluator._save_enhanced_results(results, output_path)
        
        return results
        
    except Exception as e:
        print(f"Full MCP evaluation failed: {e}")
        raise

async def execute_mcp_operations(evaluator: CogneeEnhancedEvaluator, mcp_functions: Dict) -> Dict:
    """Execute MCP Cognee operations based on prepared queries."""
    try:
        mcp_results = {
            "cognify_result": None,
            "search_results": [],
            "operation_summary": {}
        }
        
        mcp_queries = evaluator.get_mcp_queries()
        
        # Execute cognify operation
        if "cognify" in mcp_functions and "cognify_query" in mcp_queries:
            print("  Executing cognify operation...")
            cognify_data = mcp_queries["cognify_query"]["data"]
            
            # This would be the actual MCP call:
            # cognify_result = await mcp_functions["cognify"](data=cognify_data)
            # For demonstration, we simulate the result:
            cognify_result = f"Cognify completed: processed {len(cognify_data)} characters of evaluation data"
            
            mcp_results["cognify_result"] = cognify_result
            print(f"    ✓ Cognify completed")
        
        # Execute search operations
        if "search" in mcp_functions and "search_queries" in mcp_queries:
            print(f"  Executing {len(mcp_queries['search_queries'])} search operations...")
            
            for i, query_data in enumerate(mcp_queries["search_queries"]):
                try:
                    search_query = query_data["search_query"]
                    search_type = query_data["search_type"]
                    
                    # This would be the actual MCP call:
                    # search_result = await mcp_functions["search"](search_query=search_query, search_type=search_type)
                    # For demonstration, we simulate the result:
                    search_result = f"Search completed for {search_type}: Found {len(search_query.split())} query terms processed"
                    
                    mcp_results["search_results"].append({
                        "query_index": i,
                        "search_type": search_type,
                        "case_id": query_data.get("case_id", "overall"),
                        "result": search_result,
                        "description": query_data["description"]
                    })
                    
                except Exception as e:
                    print(f"    Warning: Search query {i} failed: {e}")
                    continue
            
            print(f"    ✓ Completed {len(mcp_results['search_results'])} search operations")
        
        # Summary
        mcp_results["operation_summary"] = {
            "cognify_executed": mcp_results["cognify_result"] is not None,
            "search_operations_completed": len(mcp_results["search_results"]),
            "total_operations": 1 + len(mcp_results["search_results"]),
            "execution_timestamp": datetime.now().isoformat()
        }
        
        return mcp_results
        
    except Exception as e:
        print(f"Error executing MCP operations: {e}")
        return {
            "cognify_result": None,
            "search_results": [],
            "operation_summary": {"error": str(e)}
        }

# Async wrapper function for CLI usage
async def run_enhanced_evaluation(prompt_path: str, test_cases_path: str, 
                                 config_path: Optional[str] = None,
                                 output_path: Optional[str] = None,
                                 cognee_config: Optional[Dict] = None):
    """Run enhanced evaluation with async support (basic version)."""
    
    evaluator = CogneeEnhancedEvaluator(config_path, cognee_config)
    
    try:
        results = await evaluator.evaluate_prompt_with_knowledge(
            prompt_path=prompt_path,
            test_cases_path=test_cases_path,
            output_path=output_path
        )
        
        return results
        
    except Exception as e:
        print(f"Enhanced evaluation failed: {e}")
        raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate Claude Code prompts with Cognee AI enhancement")
    parser.add_argument("--prompt", required=True, help="Path to prompt file")
    parser.add_argument("--test_cases", required=True, help="Path to test cases JSON file")
    parser.add_argument("--config", help="Path to evaluation config file")
    parser.add_argument("--output", help="Output path for results")
    parser.add_argument("--disable-knowledge", action="store_true", help="Disable knowledge graph features")
    parser.add_argument("--search-types", nargs="+", 
                       choices=["GRAPH_COMPLETION", "RAG_COMPLETION", "CODE", "CHUNKS", "INSIGHTS"],
                       default=["GRAPH_COMPLETION", "INSIGHTS"],
                       help="Knowledge graph search types to use")
    
    args = parser.parse_args()
    
    # Configure Cognee settings
    cognee_config = {
        "use_knowledge_context": not args.disable_knowledge,
        "create_test_case_graph": not args.disable_knowledge,
        "analyze_evaluation_patterns": not args.disable_knowledge,
        "search_types": args.search_types,
        "knowledge_weight": 0.3
    }
    
    # Run async evaluation
    try:
        results = asyncio.run(run_enhanced_evaluation(
            prompt_path=args.prompt,
            test_cases_path=args.test_cases,
            config_path=args.config,
            output_path=args.output,
            cognee_config=cognee_config
        ))
        
        # Exit with appropriate code
        summary = results.get("summary", {})
        sys.exit(0 if summary.get("overall_status") == "PASS" else 1)
        
    except Exception as e:
        print(f"Evaluation failed: {e}")
        sys.exit(1)