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

### A/B Testing Framework

```python
def compare_prompts(prompt_a: str, prompt_b: str, test_cases: List[Dict], 
                   significance_level: float = 0.05) -> Dict:
    """Compare two prompts with statistical significance testing"""
    
    results_a = evaluator.run_evaluation(prompt_a, test_cases, ["exact_match"])
    results_b = evaluator.run_evaluation(prompt_b, test_cases, ["exact_match"])
    
    # Statistical significance test
    from scipy.stats import chi2_contingency
    
    # Create contingency table
    correct_a = results_a["results"]["exact_match"]["correct"]
    correct_b = results_b["results"]["exact_match"]["correct"]
    total = len(test_cases)
    
    contingency_table = [
        [correct_a, total - correct_a],
        [correct_b, total - correct_b]
    ]
    
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    
    return {
        "prompt_a_accuracy": correct_a / total,
        "prompt_b_accuracy": correct_b / total,
        "improvement": (correct_b - correct_a) / total,
        "statistically_significant": p_value < significance_level,
        "p_value": p_value,
        "recommendation": "Use Prompt B" if correct_b > correct_a and p_value < significance_level else "No significant difference"
    }
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

### Evaluation Loop Best Practices

1. **Regular Evaluation**: Run weekly evaluations on production prompts
2. **Version Control**: Track prompt changes with git
3. **Automated Testing**: CI/CD integration for prompt validation
4. **Failure Analysis**: Document and learn from edge cases
5. **Performance Monitoring**: Track degradation over time

### Improvement Workflow

```bash
# 1. Create baseline evaluation
python scripts/evaluate_prompt.py --prompt current_prompt.md --baseline

# 2. Test new prompt variant
python scripts/evaluate_prompt.py --prompt new_variant.md --compare-to baseline

# 3. If improvement is significant, deploy
python scripts/deploy_prompt.py --prompt new_variant.md --environment production

# 4. Monitor performance
python scripts/monitor_metrics.py --environment production --alert-threshold 0.85
```

## 🔗 Related Resources

- [Define Success Criteria](../../anthropic-md/en/docs/test-and-evaluate/define-success.md)
- [Develop Tests](../../anthropic-md/en/docs/test-and-evaluate/develop-tests.md)
- [Prompt Engineering Guide](./prompt-engineering-guide.md)
- [Evaluation Scripts](../../evaluations/scripts/)

---

*Comprehensive evaluation framework based on Anthropic's empirical testing best practices and proven measurement methodologies.*