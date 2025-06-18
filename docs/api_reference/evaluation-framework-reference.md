# Evaluation Framework Technical Reference

This document provides detailed technical documentation for the Claude Code Prompt Development Framework's evaluation system.

## 🏗️ Architecture Overview

```
evaluations/
├── scripts/
│   ├── evaluate_prompt.py      # Single prompt evaluation
│   └── compare_prompts.py      # A/B testing framework
├── config/
│   └── default_config.yaml    # Configuration settings
├── metrics/                    # Custom metrics implementations
└── results/                    # Generated evaluation reports
```

## 📋 PromptEvaluator Class

### Core Configuration

```yaml
# evaluations/config/default_config.yaml
model: "claude-3-opus-20240229"
max_tokens: 2048
temperature: 0.0
evaluation_methods: ["exact_match", "consistency", "quality"]
metrics:
  accuracy_threshold: 0.85
  consistency_threshold: 0.8
  quality_threshold: 4.0
```

### Evaluation Methods

#### 1. Exact Match Evaluation
- **Purpose**: Measures accuracy against expected outputs
- **Implementation**: `_evaluate_exact_match()`
- **Metrics**: accuracy, correct_count, total_count, meets_threshold
- **Use cases**: Classification tasks, structured outputs

```python
def _evaluate_exact_match(self, responses: List[Dict]) -> Dict:
    correct = 0
    total = 0
    for resp in responses:
        if resp.get("expected"):
            total += 1
            if resp["output"].strip().lower() == resp["expected"].lower():
                correct += 1
    
    accuracy = correct / total if total > 0 else 0
    return {
        "accuracy": accuracy,
        "correct": correct,
        "total": total,
        "meets_threshold": accuracy >= self.config["metrics"]["accuracy_threshold"]
    }
```

#### 2. Consistency Evaluation
- **Purpose**: Measures response consistency using cosine similarity
- **Implementation**: `_evaluate_consistency()`
- **Model**: `all-MiniLM-L6-v2` sentence transformer
- **Threshold**: ≥0.8 cosine similarity

```python
def _evaluate_consistency(self, responses: List[Dict]) -> Dict:
    outputs = [resp["output"] for resp in responses if not resp.get("error")]
    
    if len(outputs) < 2:
        return {"consistency_score": 0, "note": "Insufficient responses"}
    
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
```

#### 3. Quality Evaluation
- **Purpose**: LLM-based quality grading (1-5 scale)
- **Implementation**: `_evaluate_quality()`
- **Grader model**: `claude-3-haiku-20240307` (faster, separate from tested model)
- **Threshold**: ≥4.0/5 average quality

```python
def _evaluate_quality(self, responses: List[Dict]) -> Dict:
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
    
    quality_scores = []
    for resp in responses:
        if resp.get("error"):
            continue
            
        try:
            grade_response = self.client.messages.create(
                model="claude-3-haiku-20240307",
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
```

#### 4. ROUGE Evaluation
- **Purpose**: Text similarity for summarization tasks
- **Implementation**: `_evaluate_rouge()`
- **Metrics**: ROUGE-1, ROUGE-2, ROUGE-L F1 scores

## 🔄 PromptComparator Class

### Statistical Comparison Methods

#### Chi-Square Test (Accuracy)
```python
def _compare_two_prompts(self, metrics_a: Dict, metrics_b: Dict):
    if "correct_count" in metrics_a and "total_count" in metrics_a:
        contingency_table = [
            [metrics_a["correct_count"], metrics_a["total_count"] - metrics_a["correct_count"]],
            [metrics_b["correct_count"], metrics_b["total_count"] - metrics_b["correct_count"]]
        ]
        
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
        significant = p_value < self.config["significance_level"]
        
        return {
            "p_value": p_value,
            "statistically_significant": significant,
            "winner": prompt_b if acc_b > acc_a and significant else "tie"
        }
```

#### T-Test (Quality Scores)
```python
if "quality_scores" in metrics_a and "quality_scores" in metrics_b:
    scores_a = metrics_a["quality_scores"]
    scores_b = metrics_b["quality_scores"]
    
    if len(scores_a) > 0 and len(scores_b) > 0:
        t_stat, p_value = ttest_ind(scores_a, scores_b)
        significant = p_value < self.config["significance_level"]
        
        return {
            "p_value": p_value,
            "statistically_significant": significant,
            "winner": prompt_b if mean_b > mean_a and significant else "tie"
        }
```

### Ranking Algorithm

```python
def _perform_statistical_comparison(self, results: Dict):
    # Weighted scoring system
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
    return sorted(ranking_scores.items(), key=lambda x: x[1], reverse=True)
```

## 📊 Visualization System

### Comparison Plots
- **Bar charts**: Accuracy, consistency, quality comparisons
- **Radar chart**: Overall performance comparison
- **Threshold lines**: Visual indicators for pass/fail criteria
- **Export formats**: PNG, SVG configurable via `plot_format`

### Generated Files
```
comparison_results_20240618/
├── comparison_results.json      # Full statistical analysis
├── comparison_report.md         # Executive summary
├── comparison_plots.png         # Visualizations
├── evaluation_1.json           # Individual prompt 1 results
└── evaluation_2.json           # Individual prompt 2 results
```

## 📈 Output Formats

### Evaluation Results JSON
```json
{
  "timestamp": "2024-06-18T01:14:40.123456",
  "prompt_path": "templates/base/codebase-overview-template.md",
  "test_cases_path": "test_cases/examples/codebase_understanding_examples.json",
  "test_cases_count": 25,
  "config": { /* evaluation config */ },
  "results": {
    "exact_match": {
      "accuracy": 0.88,
      "correct": 22,
      "total": 25,
      "meets_threshold": true
    },
    "consistency": {
      "consistency_score": 0.834,
      "total_comparisons": 300,
      "meets_threshold": true
    },
    "quality": {
      "average_quality": 4.2,
      "quality_scores": [4, 5, 4, 3, 5, ...],
      "total_evaluated": 25,
      "meets_threshold": true
    }
  },
  "summary": {
    "overall_status": "PASS",
    "failed_criteria": [],
    "recommendations": []
  }
}
```

### Comparison Results Structure
```json
{
  "timestamp": "2024-06-18T01:14:40.123456",
  "prompt_paths": ["templates/base/...", "templates/enhanced/..."],
  "individual_results": { /* results for each prompt */ },
  "statistical_comparison": {
    "pairwise_comparisons": {
      "prompt_1_vs_prompt_2": {
        "overall_winner": "prompt_2",
        "significant_differences": ["accuracy", "quality"],
        "metrics_comparison": { /* detailed stats */ }
      }
    },
    "overall_ranking": [
      ["prompt_2", 0.892],
      ["prompt_1", 0.847]
    ]
  },
  "recommendation": {
    "recommended_prompt": "prompt_2",
    "ranking_score": 0.892,
    "significant_improvements": ["accuracy", "quality"],
    "confidence": "high"
  }
}
```

## 🔧 Usage Examples

### Command Line Interface

```bash
# Basic single evaluation
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/base/codebase-overview-template.md \
  --test_cases test_cases/examples/codebase_understanding_examples.json

# Custom configuration
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/base/codebase-overview-template.md \
  --test_cases test_cases/examples/codebase_understanding_examples.json \
  --config evaluations/config/custom_config.yaml \
  --output results/custom_evaluation.json

# Specific evaluation methods
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/base/codebase-overview-template.md \
  --test_cases test_cases/examples/codebase_understanding_examples.json \
  --methods exact_match quality

# A/B comparison
python evaluations/scripts/compare_prompts.py \
  --prompts templates/base/template.md templates/enhanced/template.md \
  --test_cases test_cases/examples/codebase_understanding_examples.json \
  --output-dir comparison_results_$(date +%Y%m%d)
```

### Programmatic Usage

```python
from evaluations.scripts.evaluate_prompt import PromptEvaluator
from evaluations.scripts.compare_prompts import PromptComparator

# Single evaluation
evaluator = PromptEvaluator("evaluations/config/default_config.yaml")
results = evaluator.evaluate_prompt(
    prompt_path="templates/base/codebase-overview-template.md",
    test_cases_path="test_cases/examples/codebase_understanding_examples.json",
    output_path="results/evaluation.json"
)

# A/B comparison
comparator = PromptComparator("evaluations/config/default_config.yaml")
comparison = comparator.compare_prompts(
    prompt_paths=[
        "templates/base/codebase-overview-template.md",
        "templates/enhanced/codebase-overview-template.md"
    ],
    test_cases_path="test_cases/examples/codebase_understanding_examples.json",
    output_dir="comparison_results"
)
```

## 🎯 Performance Thresholds

| Metric | Threshold | Purpose |
|--------|-----------|---------|
| **Accuracy** | ≥85% | Task completion success rate |
| **Consistency** | ≥0.8 | Response similarity for similar inputs |
| **Quality** | ≥4.0/5 | LLM-judged response quality |
| **Statistical Significance** | p < 0.05 | Confidence in A/B test results |

## 🔍 Error Handling

### Common Issues and Solutions

1. **API Errors**: Automatic retry with exponential backoff
2. **Malformed Responses**: Error flagging and exclusion from metrics
3. **Missing Expected Outputs**: Graceful degradation to available metrics
4. **Insufficient Data**: Minimum sample size warnings

### Debug Mode
```bash
# Enable verbose logging
python evaluations/scripts/evaluate_prompt.py \
  --prompt template.md \
  --test_cases cases.json \
  --debug
```

## 📚 Dependencies

### Required Packages
```txt
anthropic>=0.25.0
numpy>=1.21.0
scipy>=1.7.0
sentence-transformers>=2.2.0
rouge-score>=0.1.2
matplotlib>=3.5.0
seaborn>=0.11.0
plotly>=5.0.0
tqdm>=4.62.0
pyyaml>=6.0
```

### Optional Packages
```txt
jupyter>=1.0.0          # For notebook-based analysis
pandas>=1.3.0           # For data manipulation
plotly>=5.0.0          # Interactive visualizations
```

---

*This technical reference documents the implementation details of the Claude Code Prompt Development Framework's evaluation system. For usage examples, see the [Evaluation Guide](../best-practices/evaluation-guide.md).*