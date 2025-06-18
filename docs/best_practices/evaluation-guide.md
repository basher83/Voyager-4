# Evaluation Framework Guide

This guide provides practical frameworks for testing and measuring Claude Code prompt effectiveness, based on Anthropic's empirical evaluation best practices.

## 🎯 Success Criteria Framework

### Building Strong Criteria

Good success criteria are **SMAR**:
- **Specific**: Clearly define what you want to achieve
- **Measurable**: Use quantitative metrics or well-defined qualitative scales  
- **Achievable**: Base targets on industry benchmarks and model capabilities
- **Relevant**: Align with application purpose and user needs

### Common Success Criteria Types

| Criteria Type | Description | Example Metrics |
|---------------|-------------|-----------------|
| **Task Fidelity** | How well the model performs the task | F1 score ≥ 0.85, Accuracy ≥ 90% |
| **Consistency** | Similar responses for similar inputs | Cosine similarity ≥ 0.8 |
| **Relevance & Coherence** | Direct addressing of questions | ROUGE-L F1 ≥ 0.7 |
| **Tone & Style** | Appropriate communication style | Likert scale 4+ out of 5 |
| **Privacy Preservation** | Handling sensitive information | 0% PHI leakage |
| **Context Utilization** | Effective use of provided context | Context score 4+ out of 5 |
| **Latency** | Response time requirements | 95% responses < 2s |
| **Cost** | Budget constraints | < $0.05 per query |

### Example: Multidimensional Criteria
```
Sentiment Analysis Success Criteria:
- F1 score ≥ 0.85 on 10K diverse Twitter posts
- 99.5% of outputs are non-toxic  
- 90% of errors cause inconvenience, not egregious failure
- 95% response time < 200ms
- Cost < $0.01 per classification
```

## 📊 Evaluation Methods

### 1. Code-Based Grading (Preferred)
**Fastest, most reliable, extremely scalable**

#### Exact Match
```python
def evaluate_exact_match(model_output, correct_answer):
    return model_output.strip().lower() == correct_answer.lower()

# Use for: Classification, categorical outputs, structured data
```

#### String Match
```python
def evaluate_string_match(model_output, required_phrases):
    return all(phrase.lower() in model_output.lower() for phrase in required_phrases)

# Use for: Required content, compliance checking
```

#### Pattern Matching
```python
import re

def evaluate_pattern_match(model_output, pattern):
    return bool(re.search(pattern, model_output))

# Use for: Format validation, structured outputs
```

### 2. LLM-Based Grading (Scalable)
**Fast, flexible, suitable for complex judgment**

#### Rubric-Based Evaluation
```python
def build_grader_prompt(answer, rubric):
    return f"""Grade this answer based on the rubric:
    <rubric>{rubric}</rubric>
    <answer>{answer}</answer>
    
    Think through your reasoning in <thinking> tags, then output 'correct' or 'incorrect' in <result> tags."""

def grade_completion(output, rubric):
    grader_response = client.messages.create(
        model="claude-3-opus-20240229",  # Use different model than tested one
        max_tokens=2048,
        messages=[{"role": "user", "content": build_grader_prompt(output, rubric)}]
    ).content[0].text
    
    return "correct" if "correct" in grader_response.lower() else "incorrect"
```

#### Likert Scale Evaluation
```python
def evaluate_likert(model_output, target_quality):
    tone_prompt = f"""Rate this response on a scale of 1-5 for being {target_quality}:
    <response>{model_output}</response>
    
    1: Not at all {target_quality}
    5: Perfectly {target_quality}
    
    Output only the number."""
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=50, 
        messages=[{"role": "user", "content": tone_prompt}]
    )
    return int(response.content[0].text.strip())
```

### 3. Metric-Based Evaluation
**Specialized metrics for specific use cases**

#### Cosine Similarity (Consistency)
```python
from sentence_transformers import SentenceTransformer
import numpy as np

def evaluate_cosine_similarity(outputs):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = [model.encode(output) for output in outputs]
    
    similarities = np.dot(embeddings, embeddings.T) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(embeddings, axis=1).T
    )
    return np.mean(similarities)

# Use for: Consistency testing, similar input comparison
```

#### ROUGE Score (Summarization)
```python
from rouge import Rouge

def evaluate_rouge_l(model_output, reference_summary):
    rouge = Rouge()
    scores = rouge.get_scores(model_output, reference_summary)
    return scores[0]['rouge-l']['f']  # ROUGE-L F1 score

# Use for: Summarization quality, content coverage
```

## 🧪 Test Case Design

### Eval Design Principles

1. **Be task-specific**: Mirror your real-world task distribution
2. **Automate when possible**: Structure for automated grading
3. **Prioritize volume over quality**: More automated tests > fewer manual ones

### Test Case Categories

#### Real-World Examples
```python
# Production-like scenarios
real_world_cases = [
    {"input": "Actual user query from production", "expected": "Known good output"},
    {"input": "Support ticket content", "expected": "Correct classification"},
    {"input": "Code snippet from codebase", "expected": "Accurate analysis"}
]
```

#### Edge Cases
```python
# Challenging scenarios
edge_cases = [
    {"input": "Sarcastic comment", "label": "negative", "note": "Sarcasm detection"},
    {"input": "Mixed sentiment text", "label": "mixed", "note": "Ambiguous sentiment"},
    {"input": "Very long input (>2000 chars)", "label": "neutral", "note": "Length handling"},
    {"input": "Empty or minimal input", "label": "unknown", "note": "Insufficient data"}
]
```

#### Synthetic Data
```python
# Generated test cases
def generate_synthetic_cases(base_examples, variations=5):
    """Use Claude to generate variations of base examples"""
    synthetic_cases = []
    for example in base_examples:
        prompt = f"Generate {variations} variations of this example: {example}"
        variations = claude_generate(prompt)
        synthetic_cases.extend(variations)
    return synthetic_cases
```

## 🔧 Implementation Details

### Your Project's Evaluation Framework

This project includes a comprehensive evaluation framework with two main scripts:

#### `evaluate_prompt.py` - Single Prompt Evaluation
- **Multiple evaluation methods**: exact_match, consistency, quality, ROUGE
- **Configurable thresholds**: accuracy >85%, consistency >0.8, quality >4.0/5
- **Statistical analysis**: Chi-square tests, t-tests, cosine similarity
- **Automated reporting**: JSON results + summary with pass/fail status

#### `compare_prompts.py` - A/B Testing Framework
- **Statistical significance testing**: Chi-square for accuracy, t-tests for quality
- **Pairwise comparisons**: All prompt combinations analyzed
- **Visualization**: Bar charts, radar plots, comparison matrices
- **Confidence levels**: High/medium/low based on statistical significance

### Configuration System

The framework uses `evaluations/config/default_config.yaml` for:

```yaml
model: "claude-3-opus-20240229"
max_tokens: 2048
temperature: 0.0
evaluation_methods: ["exact_match", "consistency", "quality"]
metrics:
  accuracy_threshold: 0.85
  consistency_threshold: 0.8
  quality_threshold: 4.0
visualization:
  save_plots: true
  plot_format: "png"
  plot_dpi: 300
```

### Usage Examples

```bash
# Single prompt evaluation
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/base/codebase-overview-template.md \
  --test_cases test_cases/examples/codebase_understanding_examples.json

# Compare multiple prompt variants
python evaluations/scripts/compare_prompts.py \
  --prompts templates/base/ templates/enhanced/ \
  --test_cases test_cases/examples/codebase_understanding_examples.json
```

## 📈 Evaluation Pipeline

### Complete Evaluation Script Template

```python
import anthropic
import json
from typing import List, Dict, Any
from datetime import datetime

class PromptEvaluator:
    def __init__(self, model="claude-3-opus-20240229"):
        self.client = anthropic.Anthropic()
        self.model = model
        
    def run_evaluation(self, prompt: str, test_cases: List[Dict], 
                      eval_methods: List[str]) -> Dict[str, Any]:
        """Run comprehensive evaluation on a prompt"""
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "test_cases_count": len(test_cases),
            "eval_methods": eval_methods,
            "results": {}
        }
        
        # Generate responses
        responses = []
        for case in test_cases:
            response = self._get_completion(prompt + "\n\n" + case["input"])
            responses.append({
                "input": case["input"],
                "output": response,
                "expected": case.get("expected"),
                "metadata": case.get("metadata", {})
            })
        
        # Run evaluations
        for method in eval_methods:
            if method == "exact_match":
                results["results"][method] = self._evaluate_exact_match(responses)
            elif method == "consistency":
                results["results"][method] = self._evaluate_consistency(responses)
            elif method == "quality":
                results["results"][method] = self._evaluate_quality(responses)
                
        return results
    
    def _get_completion(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    def _evaluate_exact_match(self, responses: List[Dict]) -> Dict:
        correct = 0
        total = 0
        for resp in responses:
            if resp.get("expected"):
                total += 1
                if resp["output"].strip().lower() == resp["expected"].lower():
                    correct += 1
        
        return {
            "accuracy": correct / total if total > 0 else 0,
            "correct": correct,
            "total": total
        }
    
    def _evaluate_consistency(self, responses: List[Dict]) -> Dict:
        # Group similar inputs and measure output consistency
        # Implementation depends on similarity criteria
        pass
    
    def _evaluate_quality(self, responses: List[Dict]) -> Dict:
        # LLM-based quality assessment
        pass

# Usage example
evaluator = PromptEvaluator()
test_cases = [
    {"input": "Test input 1", "expected": "Expected output 1"},
    {"input": "Test input 2", "expected": "Expected output 2"}
]

results = evaluator.run_evaluation(
    prompt="Analyze this code and provide feedback:",
    test_cases=test_cases,
    eval_methods=["exact_match", "quality"]
)

# Save results
with open(f"evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
    json.dump(results, f, indent=2)
```

### Your Project's A/B Testing Framework

The `compare_prompts.py` script provides advanced statistical comparison:

```python
# Key features implemented in your framework:

class PromptComparator:
    def compare_prompts(self, prompt_paths: List[str], test_cases_path: str):
        # 1. Evaluate each prompt individually
        results = {}
        for prompt_path in prompt_paths:
            results[f"prompt_{i}"] = self.evaluator.evaluate_prompt(...)
        
        # 2. Statistical comparison with multiple methods
        comparison_results = self._perform_statistical_comparison(results)
        
        # 3. Generate visualizations (bar charts, radar plots)
        self._generate_visualizations(results, output_dir)
        
        # 4. Create comprehensive markdown report
        self._generate_markdown_report(final_results, output_dir)

    def _compare_two_prompts(self, metrics_a, metrics_b):
        # Chi-square test for accuracy differences
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
        
        # T-test for quality score comparisons
        t_stat, p_value = ttest_ind(scores_a, scores_b)
        
        # Determine statistical significance
        significant = p_value < self.config["significance_level"]
        
        return comparison_results

# Advanced features:
# - Pairwise comparison matrix for multiple prompts
# - Overall ranking with weighted scoring
# - Confidence levels (high/medium/low)
# - Automated recommendation generation
```

### Statistical Methods Used

| Method | Use Case | Implementation |
|--------|----------|----------------|
| **Chi-square test** | Accuracy differences | `chi2_contingency()` on correct/incorrect counts |
| **T-test** | Quality score differences | `ttest_ind()` on LLM-graded scores |
| **Cosine similarity** | Response consistency | Sentence transformer embeddings |
| **ROUGE scores** | Summarization quality | `rouge_scorer` for text overlap |

### Sample A/B Testing Workflow

```bash
# Compare baseline vs enhanced template
python evaluations/scripts/compare_prompts.py \
  --prompts templates/base/codebase-overview-template.md templates/enhanced/codebase-overview-template.md \
  --test_cases test_cases/examples/codebase_understanding_examples.json \
  --output-dir comparison_results_$(date +%Y%m%d)

# Results include:
# - comparison_results.json (full statistical analysis)
# - comparison_report.md (executive summary)
# - comparison_plots.png (visualizations)
# - evaluation_1.json, evaluation_2.json (individual results)
```

## 📊 Metrics Dashboard

### Key Performance Indicators

```python
class MetricsDashboard:
    def __init__(self):
        self.metrics = {}
    
    def track_metrics(self, evaluation_results: Dict):
        timestamp = evaluation_results["timestamp"]
        
        # Task fidelity metrics
        accuracy = evaluation_results["results"].get("exact_match", {}).get("accuracy", 0)
        
        # Performance metrics  
        avg_response_time = self._calculate_response_time(evaluation_results)
        cost_per_query = self._calculate_cost(evaluation_results)
        
        # Quality metrics
        quality_score = evaluation_results["results"].get("quality", {}).get("average", 0)
        
        self.metrics[timestamp] = {
            "accuracy": accuracy,
            "response_time": avg_response_time,
            "cost_per_query": cost_per_query,
            "quality_score": quality_score
        }
    
    def generate_report(self) -> str:
        """Generate markdown report of current metrics"""
        if not self.metrics:
            return "No metrics available"
            
        latest = list(self.metrics.values())[-1]
        
        return f"""
# Metrics Report

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Accuracy | {latest['accuracy']:.2%} | >85% | {'✅' if latest['accuracy'] > 0.85 else '❌'} |
| Response Time | {latest['response_time']:.2f}s | <2s | {'✅' if latest['response_time'] < 2 else '❌'} |
| Cost per Query | ${latest['cost_per_query']:.4f} | <$0.05 | {'✅' if latest['cost_per_query'] < 0.05 else '❌'} |
| Quality Score | {latest['quality_score']:.1f}/5 | >4.0 | {'✅' if latest['quality_score'] > 4.0 else '❌'} |

## Trends
- Accuracy: {"📈 Improving" if len(self.metrics) > 1 else "📊 Baseline"}
- Performance: {"⚡ Stable" if len(self.metrics) > 1 else "📊 Baseline"}
"""
```

## 🔄 Continuous Improvement

### Evaluation-Driven Development Workflow

This project follows **evaluation-driven development** - all prompts must pass statistical validation:

1. **Template Development**: Start with `templates/base/`, enhance progressively
2. **Test Case Creation**: Add scenarios to `test_cases/examples/`
3. **Single Evaluation**: Test individual prompts with `evaluate_prompt.py`
4. **A/B Comparison**: Compare variants with `compare_prompts.py`
5. **Statistical Validation**: Ensure significance before deployment
6. **Performance Monitoring**: Track accuracy, cost, and latency

### Your Project's Improvement Workflow

```bash
# 1. Evaluate current template
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/base/codebase-overview-template.md \
  --test_cases test_cases/examples/codebase_understanding_examples.json

# 2. Create enhanced variant
# Edit templates/enhanced/codebase-overview-template.md

# 3. Compare statistically
python evaluations/scripts/compare_prompts.py \
  --prompts templates/base/codebase-overview-template.md templates/enhanced/codebase-overview-template.md \
  --test_cases test_cases/examples/codebase_understanding_examples.json

# 4. Deploy if statistically significant improvement
# Move enhanced template to production use

# 5. Monitor with ongoing evaluations
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/enhanced/codebase-overview-template.md \
  --test_cases test_cases/real-world/production_examples.json
```

### Deployment Criteria

A prompt variant is ready for deployment when:

- ✅ **Accuracy**: ≥85% on test cases
- ✅ **Consistency**: ≥0.8 cosine similarity
- ✅ **Quality**: ≥4.0/5 LLM-graded score
- ✅ **Statistical significance**: p-value <0.05 vs baseline
- ✅ **No regressions**: Maintains performance on edge cases

## 🔗 Related Resources

- [Define Success Criteria](../../anthropic-md/en/docs/test-and-evaluate/define-success.md)
- [Develop Tests](../../anthropic-md/en/docs/test-and-evaluate/develop-tests.md)
- [Prompt Engineering Guide](./prompt-engineering-guide.md)
- [Evaluation Scripts](../../evaluations/scripts/)
- [Technical Reference](../guides/evaluation-framework-reference.md)
- [Cognee AI Insights](../guides/cognee-insights.md)

---

*Comprehensive evaluation framework based on Anthropic's empirical testing best practices, enhanced with AI-powered codebase intelligence from [Cognee](https://www.cognee.ai/) analysis.*