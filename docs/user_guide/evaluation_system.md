# Evaluation System Guide

The Voyager-4 evaluation system provides comprehensive testing and measurement capabilities for Claude Code prompts. Built on statistical validation principles and Anthropic's best practices, it ensures your prompts are production-ready.

## Overview

### What Makes Our Evaluation Different

- **4-Method Assessment**: Multiple validation approaches for comprehensive analysis
- **Statistical Significance**: Chi-square and t-tests ensure confident decisions
- **Production-Focused**: Metrics that matter for real-world deployment
- **Automated A/B Testing**: Compare variants with statistical confidence
- **AI-Enhanced Insights**: Cognee integration for deeper analysis

### Core Philosophy

1. **Volume Over Perfection**: Many automated tests over few manual reviews
2. **Statistical Rigor**: Evidence-based decisions with confidence intervals
3. **Real-World Focus**: Test scenarios that mirror production usage
4. **Continuous Improvement**: Iterative optimization based on data

## Evaluation Methods

### 1. Exact Match Evaluation

Best for categorical outputs and structured responses.

**When to use:**
- Classification tasks (sentiment, category, priority)
- Yes/no questions
- Structured data extraction
- Code syntax validation

**Example:**
```python
from evaluations.scripts.evaluate_prompt import PromptEvaluator

evaluator = PromptEvaluator()
results = evaluator.evaluate(
    prompt_file="templates/base/classification-template.md",
    test_cases="test_cases/classification.json",
    methods=["exact_match"]
)

print(f"Accuracy: {results['exact_match']['accuracy']:.2%}")
```

**Configuration:**
```yaml
exact_match:
  case_sensitive: false
  strip_whitespace: true
  normalize_text: true
```

### 2. Cosine Similarity Evaluation

Measures consistency and semantic similarity between responses.

**When to use:**
- Consistency testing across similar inputs
- Semantic similarity analysis
- Response stability validation
- Content alignment measurement

**How it works:**
1. Converts text responses to embeddings using sentence transformers
2. Calculates cosine similarity between response vectors
3. Averages similarity scores across test cases
4. Provides consistency metrics and variance analysis

**Example:**
```python
results = evaluator.evaluate(
    prompt_file="templates/enhanced/summary-template.md",
    test_cases="test_cases/summarization.json",
    methods=["cosine_similarity"]
)

consistency = results['cosine_similarity']['mean_similarity']
variance = results['cosine_similarity']['similarity_variance']

print(f"Consistency: {consistency:.3f} (variance: {variance:.3f})")
```

**Configuration:**
```yaml
cosine_similarity:
  model: "all-MiniLM-L6-v2"
  similarity_threshold: 0.8
  batch_size: 32
```

### 3. LLM-Based Evaluation

Uses Claude to grade response quality against rubrics.

**When to use:**
- Subjective quality assessment
- Complex reasoning evaluation
- Creative output grading
- Multi-dimensional scoring

**Grading dimensions:**
- **Accuracy**: Factual correctness
- **Completeness**: Coverage of requirements
- **Clarity**: Communication effectiveness
- **Relevance**: Alignment with task

**Example:**
```python
# Custom rubric evaluation
rubric = {
    "accuracy": "Is the response factually correct?",
    "completeness": "Does it address all aspects of the question?",
    "clarity": "Is the explanation clear and well-structured?",
    "relevance": "Is the response relevant to the specific context?"
}

results = evaluator.evaluate_with_rubric(
    prompt_file="templates/advanced/analysis-template.md",
    test_cases="test_cases/analysis.json",
    rubric=rubric
)

print(f"Overall Quality: {results['llm_grade']['overall_score']:.1f}/5")
```

**Configuration:**
```yaml
llm_grade:
  grader_model: "claude-3-sonnet-20240229"
  temperature: 0.0
  max_tokens: 1000
  scoring_scale: 5
  grading_prompt: "Grade this response on a scale of 1-5..."
```

### 4. ROUGE Score Evaluation

Measures text overlap and similarity for content comparison.

**When to use:**
- Summarization tasks
- Content similarity analysis
- Translation evaluation
- Text generation assessment

**ROUGE variants:**
- **ROUGE-1**: Unigram overlap
- **ROUGE-2**: Bigram overlap
- **ROUGE-L**: Longest common subsequence

**Example:**
```python
results = evaluator.evaluate(
    prompt_file="templates/structured/documentation-template.md",
    test_cases="test_cases/documentation.json",
    methods=["rouge_score"]
)

rouge_scores = results['rouge_score']
print(f"ROUGE-1: {rouge_scores['rouge1']:.3f}")
print(f"ROUGE-2: {rouge_scores['rouge2']:.3f}")
print(f"ROUGE-L: {rouge_scores['rougeL']:.3f}")
```

## Evaluation Configuration

### Default Configuration

```yaml
# evaluations/config/default_config.yaml
evaluation:
  # Model settings
  model: "claude-3-sonnet-20240229"
  temperature: 0.1
  max_tokens: 4000
  timeout: 120
  
  # Evaluation methods
  methods:
    - exact_match
    - cosine_similarity
    - llm_grade
    - rouge_score
  
  # Quality thresholds
  thresholds:
    accuracy: 0.85        # 85% accuracy minimum
    consistency: 0.8      # 0.8 cosine similarity minimum
    quality: 4.0          # 4.0/5 quality score minimum
    rouge_l: 0.6          # 0.6 ROUGE-L minimum
  
  # Statistical testing
  statistical:
    confidence_level: 0.95
    min_sample_size: 30
    significance_threshold: 0.05
  
  # Performance settings
  performance:
    max_concurrent: 5
    batch_size: 10
    cache_results: true
```

### Custom Configuration

Create specialized configurations for different use cases:

```yaml
# evaluations/config/code_generation_config.yaml
evaluation:
  model: "claude-3-opus-20240229"  # Use most capable model
  temperature: 0.0                 # Deterministic for code
  
  methods:
    - exact_match      # For syntax validation
    - llm_grade       # For code quality
  
  thresholds:
    accuracy: 0.90    # Higher accuracy for code
    quality: 4.5      # Higher quality standards
  
  code_specific:
    syntax_check: true
    style_check: true
    test_execution: true
```

## Statistical Analysis

### Significance Testing

Voyager-4 includes statistical validation to ensure evaluation results are meaningful:

**Chi-Square Test**: For categorical accuracy differences
```python
from evaluations.metrics.statistical_tests import chi_square_test

# Compare accuracy between templates
p_value = chi_square_test(
    baseline_results=[1, 1, 0, 1, 1, 0, 1],
    variant_results=[1, 1, 1, 1, 1, 1, 1]
)

if p_value < 0.05:
    print("Statistically significant improvement!")
```

**T-Test**: For continuous metrics like quality scores
```python
from evaluations.metrics.statistical_tests import t_test

# Compare quality scores
p_value = t_test(
    baseline_scores=[4.1, 3.8, 4.2, 3.9, 4.0],
    variant_scores=[4.3, 4.1, 4.5, 4.2, 4.4]
)
```

**Confidence Intervals**: For result reliability
```python
from evaluations.metrics.confidence_intervals import calculate_ci

accuracy_ci = calculate_ci(
    accuracy_scores=[0.89, 0.91, 0.87, 0.93, 0.88],
    confidence_level=0.95
)

print(f"Accuracy: 90% ± {accuracy_ci['margin_of_error']:.2%}")
```

## A/B Testing Framework

### Basic Comparison

Compare two prompt variants:

```bash
python evaluations/scripts/compare_prompts.py \
  --baseline templates/base/codebase-analysis.md \
  --variant templates/enhanced/codebase-analysis.md \
  --test_cases test_cases/examples/codebase.json \
  --output-dir evaluations/results/ab-test
```

### Multi-Variant Testing

Compare multiple variants simultaneously:

```bash
python evaluations/scripts/compare_prompts.py \
  --baseline templates/base/ \
  --variants templates/enhanced/ templates/advanced/ templates/structured/ \
  --test_cases test_cases/examples/ \
  --output-dir evaluations/results/multi-variant
```

### Programmatic A/B Testing

```python
from evaluations.scripts.compare_prompts import PromptComparator

comparator = PromptComparator()
comparison = comparator.compare_multiple(
    prompts={
        "baseline": "templates/base/bug-fixing.md",
        "enhanced": "templates/enhanced/bug-fixing.md", 
        "advanced": "templates/advanced/bug-fixing.md"
    },
    test_cases="test_cases/bug-fixing.json"
)

# Get statistical recommendation
recommendation = comparison.get_recommendation()
print(f"Best performer: {recommendation['winner']}")
print(f"Confidence: {recommendation['confidence']:.2%}")
print(f"P-value: {recommendation['p_value']:.4f}")
```

## Results Analysis

### Evaluation Reports

Voyager-4 generates comprehensive reports in multiple formats:

**JSON Results**: Machine-readable detailed data
```json
{
  "evaluation_id": "eval_20240618_143022",
  "prompt_file": "templates/base/codebase-overview.md",
  "timestamp": "2024-06-18T14:30:22Z",
  "results": {
    "exact_match": {
      "accuracy": 0.892,
      "total_cases": 25,
      "correct_cases": 22
    },
    "cosine_similarity": {
      "mean_similarity": 0.874,
      "std_deviation": 0.103,
      "consistency_score": 0.871
    },
    "llm_grade": {
      "overall_score": 4.2,
      "accuracy_score": 4.1,
      "completeness_score": 4.3,
      "clarity_score": 4.2
    }
  }
}
```

**Markdown Reports**: Human-readable summaries
```markdown
# Evaluation Report

## Summary
- **Prompt**: codebase-overview-template.md
- **Test Cases**: 25
- **Execution Time**: 2.3 minutes
- **Overall Status**: ✅ APPROVED

## Performance Metrics
| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| Accuracy | 89.2% | >85% | ✅ |
| Consistency | 0.87 | >0.8 | ✅ |
| Quality | 4.2/5 | >4.0 | ✅ |

## Recommendations
1. Consider enhancing with examples for edge cases
2. Monitor consistency on complex scenarios
3. Ready for production deployment
```

**HTML Dashboards**: Interactive visualizations
- Performance trend charts
- Distribution plots
- Comparison matrices
- Statistical significance indicators

### Performance Tracking

Track prompt performance over time:

```python
from evaluations.metrics.performance_tracker import PerformanceTracker

tracker = PerformanceTracker()

# Log evaluation results
tracker.log_evaluation(
    prompt_id="codebase-analysis-v1",
    results=evaluation_results,
    timestamp=datetime.now()
)

# Generate trend analysis
trends = tracker.analyze_trends(
    prompt_id="codebase-analysis-v1",
    time_window="30d"
)

print(f"Performance trend: {trends['direction']}")
print(f"Average improvement: {trends['improvement_rate']:.2%}")
```

## Best Practices

### Test Case Design

**Comprehensive Coverage**
```python
# Create diverse test cases
test_cases = {
    "simple_cases": ["basic functionality tests"],
    "edge_cases": ["boundary conditions", "error scenarios"],
    "real_world": ["production examples", "user scenarios"],
    "adversarial": ["challenging inputs", "corner cases"]
}
```

**Quality Indicators**
- **Representativeness**: Mirror real usage patterns
- **Diversity**: Cover different scenarios and contexts
- **Specificity**: Clear expected outcomes
- **Maintainability**: Easy to update and extend

### Evaluation Strategy

**Progressive Testing**
1. **Quick validation**: Small test set for rapid feedback
2. **Comprehensive testing**: Full test suite for thorough analysis
3. **Production validation**: Real-world scenario testing
4. **Continuous monitoring**: Ongoing performance tracking

**Threshold Management**
```yaml
# Environment-specific thresholds
development:
  accuracy: 0.75    # Lower bar for rapid iteration
  
staging:
  accuracy: 0.85    # Production-like standards
  
production:
  accuracy: 0.90    # Strict quality requirements
  degradation_alert: 0.05  # Alert if performance drops
```

## Advanced Features

### Custom Metrics

Create domain-specific evaluation metrics:

```python
from evaluations.metrics.base import BaseMetric

class CodeQualityMetric(BaseMetric):
    def evaluate(self, response, expected, context):
        score = 0
        
        # Syntax validation
        if self.is_valid_syntax(response):
            score += 2
            
        # Style compliance
        if self.follows_style_guide(response):
            score += 2
            
        # Test coverage
        if self.has_tests(response):
            score += 1
            
        return score / 5.0
```

### Batch Processing

Evaluate multiple prompts efficiently:

```python
from evaluations.scripts.batch_evaluator import BatchEvaluator

batch = BatchEvaluator()
results = batch.evaluate_directory(
    prompt_dir="templates/specialized/",
    test_cases_dir="test_cases/specialized/",
    methods=["accuracy", "quality"],
    parallel=True
)

# Analyze batch results
summary = batch.generate_summary(results)
print(summary.to_markdown())
```

### Integration Workflows

**GitHub Actions Integration**
```yaml
# .github/workflows/prompt-evaluation.yml
name: Prompt Evaluation
on: [push, pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Evaluate Prompts
        run: |
          python evaluations/scripts/batch_evaluate.py \
            --prompt-dir templates/ \
            --test_cases test_cases/ \
            --threshold-file .github/quality-gates.yaml
```

**CI/CD Quality Gates**
```yaml
# .github/quality-gates.yaml
quality_gates:
  accuracy: 0.85
  consistency: 0.8
  quality: 4.0
  
fail_on_regression: true
alert_on_degradation: 0.05
```

## Troubleshooting

### Common Issues

**Low Accuracy Scores**
- Review test case quality and expectations
- Check prompt clarity and instructions
- Validate model configuration
- Consider template enhancement

**Inconsistent Results**
- Increase test case sample size
- Check for ambiguous instructions
- Review temperature settings
- Add examples for edge cases

**Statistical Significance Issues**
- Ensure sufficient sample size (n≥30)
- Check for systematic biases
- Validate test case distribution
- Consider paired testing approaches

### Performance Optimization

**Speed Improvements**
```yaml
performance:
  max_concurrent: 10      # Increase parallel requests
  batch_size: 25          # Optimize batch processing
  cache_enabled: true     # Enable result caching
  timeout: 60             # Reduce timeout for speed
```

**Cost Optimization**
```yaml
cost_optimization:
  model: "claude-3-haiku-20240307"  # Use faster, cheaper model
  max_tokens: 1000                   # Limit response length
  early_stopping: true               # Stop on clear failures
```

---

**Ready to run comprehensive evaluations?** Start with our [Basic Evaluation Tutorial](../tutorials/basic_evaluation.md) or explore [Advanced Testing Techniques](../tutorials/advanced_evaluation.md).

*Need help with specific metrics or use cases? Check our [API Reference](../api_reference/evaluation_api.md) or [Examples](../examples/evaluation_examples.md).*