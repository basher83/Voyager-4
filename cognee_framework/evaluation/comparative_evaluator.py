#!/usr/bin/env python3
"""
Claude Code Prompt Comparison Script

This script compares multiple prompt variants using A/B testing methodology
with statistical significance analysis.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
import yaml

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    import numpy as np
    from scipy.stats import chi2_contingency, ttest_ind
    import matplotlib.pyplot as plt
    import seaborn as sns
    from .base_evaluator import PromptEvaluator
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)


class PromptComparator:
    """A/B testing framework for prompt comparison."""
    
    def __init__(self, config_path: str = None):
        """Initialize comparator with configuration."""
        self.config = self._load_config(config_path)
        self.evaluator = PromptEvaluator(config_path)
        
    def _load_config(self, config_path: str) -> Dict:
        """Load comparison configuration."""
        default_config = {
            "significance_level": 0.05,
            "minimum_sample_size": 30,
            "comparison_metrics": ["accuracy", "consistency_score", "average_quality"],
            "visualization": {
                "save_plots": True,
                "plot_format": "png",
                "plot_dpi": 300
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                default_config.update(user_config)
                
        return default_config
    
    def compare_prompts(self, prompt_paths: List[str], test_cases_path: str,
                       output_dir: str = None) -> Dict[str, Any]:
        """Compare multiple prompts and determine the best performer."""
        
        if len(prompt_paths) < 2:
            raise ValueError("Need at least 2 prompts to compare")
            
        print(f"Comparing {len(prompt_paths)} prompts:")
        for i, path in enumerate(prompt_paths):
            print(f"  {i+1}. {path}")
        
        # Create output directory
        if not output_dir:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"comparison_results_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Evaluate each prompt
        print("\\nEvaluating prompts...")
        results = {}
        for i, prompt_path in enumerate(prompt_paths):
            print(f"\\nEvaluating prompt {i+1}: {prompt_path}")
            
            result = self.evaluator.evaluate_prompt(
                prompt_path=prompt_path,
                test_cases_path=test_cases_path,
                output_path=os.path.join(output_dir, f"evaluation_{i+1}.json")
            )
            
            results[f"prompt_{i+1}"] = {
                "path": prompt_path,
                "results": result
            }
        
        # Perform statistical comparison
        print("\\nPerforming statistical analysis...")
        comparison_results = self._perform_statistical_comparison(results)
        
        # Generate visualizations
        if self.config["visualization"]["save_plots"]:
            print("Generating visualizations...")
            self._generate_visualizations(results, output_dir)
        
        # Create comprehensive comparison report
        final_results = {
            "timestamp": datetime.now().isoformat(),
            "prompt_paths": prompt_paths,
            "test_cases_path": test_cases_path,
            "config": self.config,
            "individual_results": results,
            "statistical_comparison": comparison_results,
            "recommendation": self._generate_recommendation(comparison_results)
        }
        
        # Save comparison results
        comparison_path = os.path.join(output_dir, "comparison_results.json")
        with open(comparison_path, 'w') as f:
            json.dump(final_results, f, indent=2)
        
        # Generate markdown report
        self._generate_markdown_report(final_results, output_dir)
        
        print(f"\\nComparison results saved to: {output_dir}")
        
        return final_results
    
    def _perform_statistical_comparison(self, results: Dict) -> Dict[str, Any]:
        """Perform statistical significance testing between prompts."""
        comparison_results = {
            "pairwise_comparisons": {},
            "overall_ranking": [],
            "statistical_significance": {}
        }
        
        # Extract metrics for each prompt
        prompt_metrics = {}
        for prompt_id, data in results.items():
            metrics = {}
            eval_results = data["results"]["results"]
            
            # Extract accuracy
            if "exact_match" in eval_results:
                metrics["accuracy"] = eval_results["exact_match"].get("accuracy", 0)
                metrics["correct_count"] = eval_results["exact_match"].get("correct", 0)
                metrics["total_count"] = eval_results["exact_match"].get("total", 0)
            
            # Extract consistency
            if "consistency" in eval_results:
                metrics["consistency_score"] = eval_results["consistency"].get("consistency_score", 0)
            
            # Extract quality
            if "quality" in eval_results:
                metrics["average_quality"] = eval_results["quality"].get("average_quality", 0)
                metrics["quality_scores"] = eval_results["quality"].get("quality_scores", [])
            
            prompt_metrics[prompt_id] = metrics
        
        # Pairwise comparisons
        prompt_ids = list(prompt_metrics.keys())
        for i in range(len(prompt_ids)):
            for j in range(i + 1, len(prompt_ids)):
                prompt_a = prompt_ids[i]
                prompt_b = prompt_ids[j]
                
                comparison_key = f"{prompt_a}_vs_{prompt_b}"
                comparison_results["pairwise_comparisons"][comparison_key] = self._compare_two_prompts(
                    prompt_metrics[prompt_a], prompt_metrics[prompt_b], prompt_a, prompt_b
                )
        
        # Overall ranking based on combined metrics
        ranking_scores = {}
        for prompt_id, metrics in prompt_metrics.items():
            score = 0
            weight_sum = 0
            
            if "accuracy" in metrics:
                score += metrics["accuracy"] * 0.4  # 40% weight
                weight_sum += 0.4
            
            if "consistency_score" in metrics:
                score += metrics["consistency_score"] * 0.3  # 30% weight
                weight_sum += 0.3
                
            if "average_quality" in metrics:
                score += (metrics["average_quality"] / 5.0) * 0.3  # 30% weight, normalized
                weight_sum += 0.3
            
            ranking_scores[prompt_id] = score / weight_sum if weight_sum > 0 else 0
        
        # Sort by score
        comparison_results["overall_ranking"] = sorted(
            ranking_scores.items(), key=lambda x: x[1], reverse=True
        )
        
        return comparison_results
    
    def _compare_two_prompts(self, metrics_a: Dict, metrics_b: Dict, 
                           prompt_a: str, prompt_b: str) -> Dict[str, Any]:
        """Compare two prompts statistically."""
        comparison = {
            "prompt_a": prompt_a,
            "prompt_b": prompt_b,
            "metrics_comparison": {},
            "overall_winner": None,
            "significant_differences": []
        }
        
        # Compare accuracy (if available)
        if "accuracy" in metrics_a and "accuracy" in metrics_b:
            acc_a = metrics_a["accuracy"]
            acc_b = metrics_b["accuracy"]
            
            # Chi-square test for accuracy difference
            if "correct_count" in metrics_a and "total_count" in metrics_a:
                contingency_table = [
                    [metrics_a["correct_count"], metrics_a["total_count"] - metrics_a["correct_count"]],
                    [metrics_b["correct_count"], metrics_b["total_count"] - metrics_b["correct_count"]]
                ]
                
                try:
                    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                    significant = p_value < self.config["significance_level"]
                    
                    comparison["metrics_comparison"]["accuracy"] = {
                        "prompt_a_value": acc_a,
                        "prompt_b_value": acc_b,
                        "difference": acc_b - acc_a,
                        "p_value": p_value,
                        "statistically_significant": significant,
                        "winner": prompt_b if acc_b > acc_a and significant else prompt_a if acc_a > acc_b and significant else "tie"
                    }
                    
                    if significant:
                        comparison["significant_differences"].append("accuracy")
                        
                except Exception as e:
                    print(f"Error in chi-square test: {e}")
        
        # Compare quality scores (if available)
        if "quality_scores" in metrics_a and "quality_scores" in metrics_b:
            scores_a = metrics_a["quality_scores"]
            scores_b = metrics_b["quality_scores"]
            
            if len(scores_a) > 0 and len(scores_b) > 0:
                try:
                    t_stat, p_value = ttest_ind(scores_a, scores_b)
                    significant = p_value < self.config["significance_level"]
                    
                    mean_a = np.mean(scores_a)
                    mean_b = np.mean(scores_b)
                    
                    comparison["metrics_comparison"]["quality"] = {
                        "prompt_a_value": mean_a,
                        "prompt_b_value": mean_b,
                        "difference": mean_b - mean_a,
                        "p_value": p_value,
                        "statistically_significant": significant,
                        "winner": prompt_b if mean_b > mean_a and significant else prompt_a if mean_a > mean_b and significant else "tie"
                    }
                    
                    if significant:
                        comparison["significant_differences"].append("quality")
                        
                except Exception as e:
                    print(f"Error in t-test: {e}")
        
        # Compare consistency
        if "consistency_score" in metrics_a and "consistency_score" in metrics_b:
            cons_a = metrics_a["consistency_score"]
            cons_b = metrics_b["consistency_score"]
            
            comparison["metrics_comparison"]["consistency"] = {
                "prompt_a_value": cons_a,
                "prompt_b_value": cons_b,
                "difference": cons_b - cons_a,
                "descriptive_winner": prompt_b if cons_b > cons_a else prompt_a if cons_a > cons_b else "tie"
            }
        
        # Determine overall winner
        winners = []
        for metric_comparison in comparison["metrics_comparison"].values():
            if "winner" in metric_comparison and metric_comparison["winner"] not in ["tie", None]:
                winners.append(metric_comparison["winner"])
        
        if winners:
            # Majority vote
            winner_counts = {}
            for winner in winners:
                winner_counts[winner] = winner_counts.get(winner, 0) + 1
            comparison["overall_winner"] = max(winner_counts, key=winner_counts.get)
        else:
            comparison["overall_winner"] = "tie"
        
        return comparison
    
    def _generate_visualizations(self, results: Dict, output_dir: str):
        """Generate comparison visualizations."""
        # Extract metrics for plotting
        prompt_names = []
        accuracies = []
        consistencies = []
        qualities = []
        
        for prompt_id, data in results.items():
            prompt_names.append(prompt_id)
            eval_results = data["results"]["results"]
            
            # Extract metrics
            accuracies.append(eval_results.get("exact_match", {}).get("accuracy", 0))
            consistencies.append(eval_results.get("consistency", {}).get("consistency_score", 0))
            qualities.append(eval_results.get("quality", {}).get("average_quality", 0))
        
        # Create comparison plots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Prompt Comparison Results', fontsize=16, fontweight='bold')
        
        # Accuracy comparison
        axes[0, 0].bar(prompt_names, accuracies, color='skyblue', alpha=0.7)
        axes[0, 0].set_title('Accuracy Comparison')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].set_ylim(0, 1)
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Add accuracy threshold line
        threshold = self.evaluator.config["metrics"]["accuracy_threshold"]
        axes[0, 0].axhline(y=threshold, color='red', linestyle='--', alpha=0.7, label=f'Threshold ({threshold})')
        axes[0, 0].legend()
        
        # Consistency comparison
        axes[0, 1].bar(prompt_names, consistencies, color='lightgreen', alpha=0.7)
        axes[0, 1].set_title('Consistency Comparison')
        axes[0, 1].set_ylabel('Consistency Score')
        axes[0, 1].set_ylim(0, 1)
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Quality comparison
        axes[1, 0].bar(prompt_names, qualities, color='lightcoral', alpha=0.7)
        axes[1, 0].set_title('Quality Comparison')
        axes[1, 0].set_ylabel('Quality Score')
        axes[1, 0].set_ylim(0, 5)
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Combined radar chart
        angles = np.linspace(0, 2 * np.pi, 3, endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        axes[1, 1].remove()
        ax_radar = fig.add_subplot(2, 2, 4, projection='polar')
        
        for i, prompt_name in enumerate(prompt_names):
            values = [
                accuracies[i],
                consistencies[i],
                qualities[i] / 5.0  # Normalize to 0-1
            ]
            values += values[:1]  # Complete the circle
            
            ax_radar.plot(angles, values, 'o-', linewidth=2, label=prompt_name)
            ax_radar.fill(angles, values, alpha=0.25)
        
        ax_radar.set_xticks(angles[:-1])
        ax_radar.set_xticklabels(['Accuracy', 'Consistency', 'Quality'])
        ax_radar.set_ylim(0, 1)
        ax_radar.set_title('Overall Performance Comparison')
        ax_radar.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
        
        plt.tight_layout()
        
        # Save plot
        plot_path = os.path.join(output_dir, f"comparison_plots.{self.config['visualization']['plot_format']}")
        plt.savefig(plot_path, dpi=self.config["visualization"]["plot_dpi"], bbox_inches='tight')
        plt.close()
        
        print(f"Visualizations saved to: {plot_path}")
    
    def _generate_recommendation(self, comparison_results: Dict) -> Dict[str, Any]:
        """Generate final recommendation based on comparison results."""
        ranking = comparison_results["overall_ranking"]
        
        if not ranking:
            return {"recommended_prompt": None, "reason": "No valid ranking available"}
        
        best_prompt = ranking[0][0]
        best_score = ranking[0][1]
        
        # Check if the difference is significant
        significant_improvements = []
        for comparison in comparison_results["pairwise_comparisons"].values():
            if comparison["overall_winner"] == best_prompt and comparison["significant_differences"]:
                significant_improvements.extend(comparison["significant_differences"])
        
        recommendation = {
            "recommended_prompt": best_prompt,
            "ranking_score": best_score,
            "significant_improvements": list(set(significant_improvements)),
            "confidence": "high" if significant_improvements else "medium"
        }
        
        if len(ranking) > 1:
            second_best = ranking[1][0]
            score_difference = best_score - ranking[1][1]
            recommendation["score_advantage"] = score_difference
            recommendation["runner_up"] = second_best
            
            if score_difference < 0.05:  # Very close
                recommendation["confidence"] = "low"
                recommendation["note"] = "Results are very close. Consider additional testing."
        
        return recommendation
    
    def _generate_markdown_report(self, results: Dict, output_dir: str):
        """Generate a comprehensive markdown report."""
        report_path = os.path.join(output_dir, "comparison_report.md")
        
        with open(report_path, 'w') as f:
            f.write("# Claude Code Prompt Comparison Report\\n\\n")
            f.write(f"**Generated**: {results['timestamp']}\\n\\n")
            
            # Executive Summary
            f.write("## Executive Summary\\n\\n")
            recommendation = results["recommendation"]
            f.write(f"**Recommended Prompt**: {recommendation['recommended_prompt']}\\n")
            f.write(f"**Confidence Level**: {recommendation['confidence']}\\n\\n")
            
            if recommendation.get("note"):
                f.write(f"⚠️ **Note**: {recommendation['note']}\\n\\n")
            
            # Ranking
            f.write("## Overall Ranking\\n\\n")
            f.write("| Rank | Prompt | Score | Path |\\n")
            f.write("|------|--------|-------|------|\\n")
            
            for i, (prompt_id, score) in enumerate(results["statistical_comparison"]["overall_ranking"]):
                path = results["individual_results"][prompt_id]["path"]
                f.write(f"| {i+1} | {prompt_id} | {score:.3f} | {path} |\\n")
            
            # Detailed Results
            f.write("\\n## Detailed Results\\n\\n")
            
            for prompt_id, data in results["individual_results"].items():
                f.write(f"### {prompt_id}\\n\\n")
                f.write(f"**Path**: `{data['path']}`\\n\\n")
                
                eval_results = data["results"]["results"]
                
                # Metrics table
                f.write("| Metric | Value | Meets Threshold |\\n")
                f.write("|--------|-------|----------------|\\n")
                
                if "exact_match" in eval_results:
                    acc = eval_results["exact_match"]
                    f.write(f"| Accuracy | {acc.get('accuracy', 0):.2%} | {'✅' if acc.get('meets_threshold') else '❌'} |\\n")
                
                if "consistency" in eval_results:
                    cons = eval_results["consistency"]
                    f.write(f"| Consistency | {cons.get('consistency_score', 0):.3f} | {'✅' if cons.get('meets_threshold') else '❌'} |\\n")
                
                if "quality" in eval_results:
                    qual = eval_results["quality"]
                    f.write(f"| Quality | {qual.get('average_quality', 0):.1f}/5 | {'✅' if qual.get('meets_threshold') else '❌'} |\\n")
                
                f.write("\\n")
            
            # Statistical Analysis
            f.write("## Statistical Analysis\\n\\n")
            
            for comparison_key, comparison in results["statistical_comparison"]["pairwise_comparisons"].items():
                f.write(f"### {comparison_key}\\n\\n")
                f.write(f"**Overall Winner**: {comparison['overall_winner']}\\n")
                
                if comparison["significant_differences"]:
                    f.write(f"**Significant Differences**: {', '.join(comparison['significant_differences'])}\\n")
                else:
                    f.write("**Significant Differences**: None\\n")
                
                f.write("\\n")
                
                for metric, details in comparison["metrics_comparison"].items():
                    f.write(f"**{metric.title()}**:\\n")
                    f.write(f"- {comparison['prompt_a']}: {details.get('prompt_a_value', 'N/A')}\\n")
                    f.write(f"- {comparison['prompt_b']}: {details.get('prompt_b_value', 'N/A')}\\n")
                    
                    if "p_value" in details:
                        f.write(f"- p-value: {details['p_value']:.4f}\\n")
                        f.write(f"- Significant: {'Yes' if details.get('statistically_significant') else 'No'}\\n")
                    
                    f.write("\\n")
            
            # Recommendations
            f.write("## Recommendations\\n\\n")
            
            if recommendation["confidence"] == "high":
                f.write(f"✅ **Strong recommendation**: Use {recommendation['recommended_prompt']}\\n\\n")
                f.write("The recommended prompt shows statistically significant improvements over alternatives.\\n\\n")
            elif recommendation["confidence"] == "medium":
                f.write(f"⚠️ **Moderate recommendation**: Consider {recommendation['recommended_prompt']}\\n\\n")
                f.write("The recommended prompt shows better performance but without strong statistical significance.\\n\\n")
            else:
                f.write(f"❓ **Weak recommendation**: Results are inconclusive\\n\\n")
                f.write("Consider collecting more test data or refining prompts further.\\n\\n")
            
            if recommendation.get("significant_improvements"):
                f.write(f"**Key improvements**: {', '.join(recommendation['significant_improvements'])}\\n\\n")
        
        print(f"Comparison report saved to: {report_path}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Compare Claude Code prompts")
    parser.add_argument("--prompts", nargs="+", required=True, help="Paths to prompt files to compare")
    parser.add_argument("--test_cases", required=True, help="Path to test cases JSON file")
    parser.add_argument("--config", help="Path to comparison config file")
    parser.add_argument("--output-dir", help="Output directory for results")
    
    args = parser.parse_args()
    
    # Initialize comparator
    comparator = PromptComparator(args.config)
    
    # Run comparison
    try:
        results = comparator.compare_prompts(
            prompt_paths=args.prompts,
            test_cases_path=args.test_cases,
            output_dir=args.output_dir
        )
        
        print("\\n" + "="*60)
        print("COMPARISON COMPLETE")
        print("="*60)
        
        recommendation = results["recommendation"]
        print(f"Recommended Prompt: {recommendation['recommended_prompt']}")
        print(f"Confidence: {recommendation['confidence']}")
        
        if recommendation.get("note"):
            print(f"Note: {recommendation['note']}")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"Comparison failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()