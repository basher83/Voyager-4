#!/usr/bin/env python3
"""
Claude Code Prompt Evaluation Script

This script provides comprehensive evaluation capabilities for Claude Code prompts,
following Anthropic's best practices for empirical testing.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    import anthropic
    import numpy as np
    from sentence_transformers import SentenceTransformer
    from rouge_score import rouge_scorer
    from tqdm import tqdm
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)


class PromptEvaluator:
    """Comprehensive prompt evaluation framework."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize evaluator with configuration."""
        self.config = self._load_config(config_path)
        self.client = anthropic.Anthropic()
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load evaluation configuration."""
        default_config = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 2048,
            "temperature": 0.0,
            "evaluation_methods": ["exact_match", "consistency", "quality"],
            "metrics": {
                "accuracy_threshold": 0.85,
                "consistency_threshold": 0.8,
                "quality_threshold": 4.0
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                default_config.update(user_config)
                
        return default_config
    
    def evaluate_prompt(self, prompt_path: str, test_cases_path: str, 
                       output_path: Optional[str] = None) -> Dict[str, Any]:
        """Run comprehensive evaluation on a prompt."""
        
        # Load prompt and test cases
        prompt = self._load_prompt(prompt_path)
        test_cases = self._load_test_cases(test_cases_path)
        
        print(f"Evaluating prompt: {prompt_path}")
        print(f"Test cases: {len(test_cases)}")
        print(f"Methods: {', '.join(self.config['evaluation_methods'])}")
        
        # Initialize results structure
        results = {
            "timestamp": datetime.now().isoformat(),
            "prompt_path": prompt_path,
            "test_cases_path": test_cases_path,
            "test_cases_count": len(test_cases),
            "config": self.config,
            "results": {},
            "summary": {}
        }
        
        # Generate responses
        print("\\nGenerating responses...")
        responses = []
        for i, case in enumerate(tqdm(test_cases)):
            try:
                response = self._get_completion(prompt, case["input"])
                responses.append({
                    "case_id": i,
                    "input": case["input"],
                    "output": response,
                    "expected": case.get("expected"),
                    "metadata": case.get("metadata", {})
                })
            except Exception as e:
                print(f"Error processing case {i}: {e}")
                responses.append({
                    "case_id": i,
                    "input": case["input"],
                    "output": f"ERROR: {str(e)}",
                    "expected": case.get("expected"),
                    "metadata": case.get("metadata", {}),
                    "error": True
                })
        
        # Run evaluations
        print("\\nRunning evaluations...")
        
        if "exact_match" in self.config["evaluation_methods"]:
            print("- Exact match evaluation")
            results["results"]["exact_match"] = self._evaluate_exact_match(responses)
            
        if "consistency" in self.config["evaluation_methods"]:
            print("- Consistency evaluation")
            results["results"]["consistency"] = self._evaluate_consistency(responses)
            
        if "quality" in self.config["evaluation_methods"]:
            print("- Quality evaluation")
            results["results"]["quality"] = self._evaluate_quality(responses)
            
        if "rouge" in self.config["evaluation_methods"]:
            print("- ROUGE evaluation")
            results["results"]["rouge"] = self._evaluate_rouge(responses)
        
        # Generate summary
        results["summary"] = self._generate_summary(results["results"])
        
        # Save results
        if output_path:
            self._save_results(results, output_path)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"evaluation_results_{timestamp}.json"
            self._save_results(results, output_path)
        
        return results
    
    def _load_prompt(self, prompt_path: str) -> str:
        """Load prompt from file."""
        with open(prompt_path, 'r') as f:
            return f.read().strip()
    
    def _load_test_cases(self, test_cases_path: str) -> List[Dict]:
        """Load test cases from JSON file."""
        with open(test_cases_path, 'r') as f:
            return json.load(f)
    
    def _get_completion(self, prompt: str, user_input: str) -> str:
        """Get completion from Claude."""
        full_prompt = f"{prompt}\\n\\n{user_input}"
        
        try:
            response = self.client.messages.create(
                model=self.config["model"],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"],
                messages=[{"role": "user", "content": full_prompt}]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"API Error: {str(e)}")
    
    def _evaluate_exact_match(self, responses: List[Dict]) -> Dict:
        """Evaluate exact match accuracy."""
        correct = 0
        total = 0
        errors = 0
        
        for resp in responses:
            if resp.get("error"):
                errors += 1
                continue
                
            if resp.get("expected"):
                total += 1
                if resp["output"].strip().lower() == resp["expected"].strip().lower():
                    correct += 1
        
        accuracy = correct / total if total > 0 else 0
        
        return {
            "accuracy": accuracy,
            "correct": correct,
            "total": total,
            "errors": errors,
            "meets_threshold": accuracy >= self.config["metrics"]["accuracy_threshold"]
        }
    
    def _evaluate_consistency(self, responses: List[Dict]) -> Dict:
        """Evaluate response consistency using cosine similarity."""
        # Group responses by similar inputs (simplified: just compare all pairs)
        outputs = [resp["output"] for resp in responses if not resp.get("error")]
        
        if len(outputs) < 2:
            return {"consistency_score": 0, "note": "Insufficient responses for consistency check"}
        
        # Generate embeddings
        embeddings = self.sentence_model.encode(outputs)
        
        # Calculate pairwise similarities
        similarities = []
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                similarity = np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
                )
                similarities.append(similarity)
        
        avg_similarity = np.mean(similarities)
        
        return {
            "consistency_score": float(avg_similarity),
            "total_comparisons": len(similarities),
            "meets_threshold": avg_similarity >= self.config["metrics"]["consistency_threshold"]
        }
    
    def _evaluate_quality(self, responses: List[Dict]) -> Dict:
        """Evaluate response quality using LLM grading."""
        quality_scores = []
        
        quality_prompt = """Rate the quality of this response on a scale of 1-5:
        1: Very poor quality
        2: Poor quality  
        3: Average quality
        4: Good quality
        5: Excellent quality
        
        Consider factors like:
        - Accuracy and correctness
        - Clarity and coherence
        - Completeness
        - Helpfulness
        
        Response to evaluate:
        {response}
        
        Output only the number (1-5):"""
        
        for resp in responses:
            if resp.get("error"):
                continue
                
            try:
                grade_response = self.client.messages.create(
                    model="claude-3-haiku-20240307",  # Use faster model for grading
                    max_tokens=10,
                    temperature=0,
                    messages=[{
                        "role": "user", 
                        "content": quality_prompt.format(response=resp["output"])
                    }]
                )
                
                score = int(grade_response.content[0].text.strip())
                if 1 <= score <= 5:
                    quality_scores.append(score)
                    
            except Exception as e:
                print(f"Error in quality evaluation: {e}")
                continue
        
        if not quality_scores:
            return {"average_quality": 0, "note": "No valid quality scores"}
        
        avg_quality = np.mean(quality_scores)
        
        return {
            "average_quality": float(avg_quality),
            "quality_scores": quality_scores,
            "total_evaluated": len(quality_scores),
            "meets_threshold": avg_quality >= self.config["metrics"]["quality_threshold"]
        }
    
    def _evaluate_rouge(self, responses: List[Dict]) -> Dict:
        """Evaluate ROUGE scores for summarization tasks."""
        rouge_scores = {"rouge1": [], "rouge2": [], "rougeL": []}
        
        for resp in responses:
            if resp.get("error") or not resp.get("expected"):
                continue
                
            scores = self.rouge_scorer.score(resp["expected"], resp["output"])
            
            rouge_scores["rouge1"].append(scores["rouge1"].fmeasure)
            rouge_scores["rouge2"].append(scores["rouge2"].fmeasure)
            rouge_scores["rougeL"].append(scores["rougeL"].fmeasure)
        
        # Calculate averages
        avg_scores = {}
        for metric, score_list in rouge_scores.items():
            avg_scores[f"avg_{metric}"] = float(np.mean(score_list)) if score_list else 0
        
        return {
            **avg_scores,
            "total_evaluated": len(rouge_scores["rouge1"])
        }
    
    def _generate_summary(self, results: Dict) -> Dict:
        """Generate evaluation summary."""
        summary = {
            "overall_status": "PASS",
            "failed_criteria": [],
            "recommendations": []
        }
        
        # Check each evaluation method
        for method, result in results.items():
            if isinstance(result, dict) and "meets_threshold" in result:
                if not result["meets_threshold"]:
                    summary["overall_status"] = "FAIL"
                    summary["failed_criteria"].append(method)
        
        # Generate recommendations
        if "exact_match" in results and not results["exact_match"].get("meets_threshold", True):
            summary["recommendations"].append("Improve prompt clarity and specificity")
            
        if "consistency" in results and not results["consistency"].get("meets_threshold", True):
            summary["recommendations"].append("Add examples to improve output consistency")
            
        if "quality" in results and not results["quality"].get("meets_threshold", True):
            summary["recommendations"].append("Enhance prompt with better context and instructions")
        
        return summary
    
    def _save_results(self, results: Dict, output_path: str):
        """Save evaluation results to file."""
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\\nResults saved to: {output_path}")
        
        # Print summary
        print("\\n" + "="*50)
        print("EVALUATION SUMMARY")
        print("="*50)
        
        summary = results["summary"]
        print(f"Overall Status: {summary['overall_status']}")
        
        if summary["failed_criteria"]:
            print(f"Failed Criteria: {', '.join(summary['failed_criteria'])}")
            
        if summary["recommendations"]:
            print("\\nRecommendations:")
            for rec in summary["recommendations"]:
                print(f"- {rec}")
        
        # Print key metrics
        print("\\nKey Metrics:")
        for method, result in results["results"].items():
            if method == "exact_match" and "accuracy" in result:
                print(f"- Accuracy: {result['accuracy']:.2%}")
            elif method == "consistency" and "consistency_score" in result:
                print(f"- Consistency: {result['consistency_score']:.3f}")
            elif method == "quality" and "average_quality" in result:
                print(f"- Quality: {result['average_quality']:.1f}/5")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Evaluate Claude Code prompts")
    parser.add_argument("--prompt", required=True, help="Path to prompt file")
    parser.add_argument("--test_cases", required=True, help="Path to test cases JSON file")
    parser.add_argument("--config", help="Path to evaluation config file")
    parser.add_argument("--output", help="Output path for results")
    parser.add_argument("--methods", nargs="+", help="Evaluation methods to run", 
                       choices=["exact_match", "consistency", "quality", "rouge"])
    
    args = parser.parse_args()
    
    # Initialize evaluator
    evaluator = PromptEvaluator(args.config)
    
    # Override methods if specified
    if args.methods:
        evaluator.config["evaluation_methods"] = args.methods
    
    # Run evaluation
    try:
        results = evaluator.evaluate_prompt(
            prompt_path=args.prompt,
            test_cases_path=args.test_cases,
            output_path=args.output
        )
        
        # Exit with appropriate code
        sys.exit(0 if results["summary"]["overall_status"] == "PASS" else 1)
        
    except Exception as e:
        print(f"Evaluation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()