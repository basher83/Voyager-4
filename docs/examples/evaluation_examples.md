# Evaluation Examples

This document provides comprehensive examples of using Voyager-4's evaluation system across different domains and use cases.

## Table of Contents

1. [Quick Start Examples](#quick-start-examples)
2. [Domain-Specific Examples](#domain-specific-examples)
3. [Advanced Evaluation Patterns](#advanced-evaluation-patterns)
4. [Real-World Use Cases](#real-world-use-cases)
5. [Integration Examples](#integration-examples)

## Quick Start Examples

### Basic Prompt Evaluation

**Use Case**: Evaluate a simple code explanation prompt

```python
from evaluations.scripts.evaluate_prompt import PromptEvaluator

# Initialize evaluator
evaluator = PromptEvaluator()

# Run evaluation
results = evaluator.evaluate(
    prompt_file="templates/base/code-explanation.md",
    test_cases="test_cases/code-explanation.json",
    output_dir="results/code-explanation"
)

# Check results
print(f"Accuracy: {results.accuracy:.2%}")
print(f"Quality: {results.quality:.1f}/5")
print(f"Passes thresholds: {results.passes_thresholds}")

# Quick pass/fail decision
if results.passes_thresholds:
    print("✅ Prompt approved for production")
else:
    print("❌ Prompt needs improvement")
```

### A/B Testing Two Prompts

**Use Case**: Compare baseline vs enhanced prompt

```python
from evaluations.scripts.compare_prompts import PromptComparator

comparator = PromptComparator()

# Compare prompts
comparison = comparator.compare(
    baseline="templates/base/bug-analysis.md",
    variant="templates/enhanced/bug-analysis.md",
    test_cases="test_cases/bug-analysis.json"
)

# Statistical analysis
if comparison.is_significant:
    print(f"🏆 Winner: {comparison.winner}")
    print(f"Improvement: {comparison.improvement:.2%}")
    print(f"P-value: {comparison.p_value:.4f}")
    print(f"Effect size: {comparison.effect_size:.3f}")
else:
    print("No statistically significant difference")
```

### Batch Evaluation

**Use Case**: Test multiple prompt variants simultaneously

```python
from evaluations.scripts.evaluate_prompt import PromptEvaluator

evaluator = PromptEvaluator()

# Define prompt variants
prompts = [
    "templates/base/architecture-analysis.md",
    "templates/enhanced/architecture-analysis.md",
    "templates/advanced/architecture-analysis.md",
    "templates/structured/architecture-analysis.md"
]

# Batch evaluation
batch_results = evaluator.batch_evaluate(
    prompt_files=prompts,
    test_cases="test_cases/architecture-analysis.json",
    parallel=True
)

# Find best performer
best_prompt = max(batch_results.results.items(), 
                  key=lambda x: x[1].accuracy)

print(f"Best performing prompt: {best_prompt[0]}")
print(f"Accuracy: {best_prompt[1].accuracy:.2%}")
```

## Domain-Specific Examples

### Software Development

#### Code Review Prompt Evaluation

```python
# Evaluate code review prompt with security focus
config = {
    'model': 'claude-3-opus-20240229',  # Use most capable model
    'temperature': 0.0,                  # Deterministic for consistency
    'methods': ['exact_match', 'llm_grade'],
    'thresholds': {
        'accuracy': 0.90,               # High accuracy for security
        'quality': 4.5                  # High quality standards
    }
}

evaluator = PromptEvaluator(config=config)

results = evaluator.evaluate(
    prompt_file="templates/specialized/security-code-review.md",
    test_cases="test_cases/security-vulnerabilities.json"
)

# Security-specific analysis
security_score = results.results.get('llm_grade', {}).get('security_score', 0)
print(f"Security awareness score: {security_score:.1f}/5")

if security_score < 4.0:
    print("⚠️ Prompt may miss security vulnerabilities")
```

#### Bug Fixing Prompt with Custom Metrics

```python
from evaluations.metrics.custom import CodeQualityMetric

# Custom metric for code quality assessment
class BugFixQualityMetric:
    def evaluate(self, predictions, actuals, context=None):
        scores = []
        for pred, actual in zip(predictions, actuals):
            score = 0
            
            # Check if bug is correctly identified
            if actual['bug_identified'] in pred.lower():
                score += 2
            
            # Check if root cause is mentioned
            if actual['root_cause'] in pred.lower():
                score += 2
            
            # Check if solution is provided
            if any(sol in pred.lower() for sol in actual['solutions']):
                score += 1
            
            scores.append(score / 5.0)
        
        return {
            'bug_fix_quality': sum(scores) / len(scores),
            'perfect_fixes': sum(1 for s in scores if s == 1.0),
            'total_cases': len(scores)
        }

# Register custom metric
evaluator.add_custom_metric('bug_fix_quality', BugFixQualityMetric())

# Evaluate with custom metric
results = evaluator.evaluate(
    prompt_file="templates/advanced/bug-fixing.md",
    test_cases="test_cases/bug-scenarios.json",
    methods=['exact_match', 'bug_fix_quality']
)

print(f"Bug fix quality: {results.results['bug_fix_quality']['bug_fix_quality']:.2%}")
```

### Data Science

#### Data Analysis Prompt Evaluation

```python
# Evaluate data analysis prompt with statistical rigor
config = {
    'statistical': {
        'confidence_level': 0.99,       # High confidence for scientific work
        'min_sample_size': 50,          # Larger sample size
        'significance_threshold': 0.01   # Strict significance level
    }
}

evaluator = PromptEvaluator(config=config)

# Test data analysis prompt
results = evaluator.evaluate(
    prompt_file="templates/specialized/data-analysis.md",
    test_cases="test_cases/datasets/analysis-scenarios.json"
)

# Check statistical interpretation accuracy
stats_accuracy = results.results.get('exact_match', {}).get('stats_accuracy', 0)
print(f"Statistical interpretation accuracy: {stats_accuracy:.2%}")

# Validate methodology suggestions
methodology_score = results.results.get('llm_grade', {}).get('methodology_score', 0)
print(f"Methodology quality: {methodology_score:.1f}/5")
```

### Documentation

#### API Documentation Generation

```python
# Evaluate API documentation prompt
test_cases = [
    {
        "id": "rest_endpoint",
        "input": """
        @app.route('/api/users/<int:user_id>', methods=['GET'])
        def get_user(user_id):
            user = User.query.get_or_404(user_id)
            return jsonify(user.to_dict())
        """,
        "expected_output": {
            "endpoint": "/api/users/{user_id}",
            "method": "GET",
            "description": "Retrieve a specific user by ID",
            "parameters": [{"name": "user_id", "type": "integer", "required": True}],
            "responses": {
                "200": "User object in JSON format",
                "404": "User not found"
            }
        }
    }
]

results = evaluator.evaluate(
    prompt_file="templates/structured/api-documentation.md",
    test_cases=test_cases
)

# Check documentation completeness
completeness = results.results.get('llm_grade', {}).get('completeness_score', 0)
print(f"Documentation completeness: {completeness:.1f}/5")
```

## Advanced Evaluation Patterns

### Multi-Stage Evaluation

**Use Case**: Complex prompts requiring multiple evaluation stages

```python
class MultiStageEvaluator:
    def __init__(self):
        self.evaluator = PromptEvaluator()
    
    def evaluate_architecture_analysis(self, prompt_file, test_cases):
        """Multi-stage evaluation for architecture analysis."""
        
        # Stage 1: Component identification
        stage1_results = self.evaluator.evaluate(
            prompt_file=prompt_file,
            test_cases=test_cases,
            methods=['exact_match'],
            stage_config={'focus': 'component_identification'}
        )
        
        # Stage 2: Relationship analysis
        stage2_results = self.evaluator.evaluate(
            prompt_file=prompt_file,
            test_cases=test_cases,
            methods=['cosine_similarity'],
            stage_config={'focus': 'relationship_analysis'}
        )
        
        # Stage 3: Overall quality
        stage3_results = self.evaluator.evaluate(
            prompt_file=prompt_file,
            test_cases=test_cases,
            methods=['llm_grade'],
            stage_config={'focus': 'overall_quality'}
        )
        
        # Combine results
        combined_score = (
            stage1_results.accuracy * 0.4 +
            stage2_results.consistency * 0.3 +
            stage3_results.quality / 5.0 * 0.3
        )
        
        return {
            'component_accuracy': stage1_results.accuracy,
            'relationship_consistency': stage2_results.consistency,
            'overall_quality': stage3_results.quality,
            'combined_score': combined_score,
            'recommendation': 'APPROVE' if combined_score > 0.85 else 'REVISE'
        }

# Use multi-stage evaluator
multi_evaluator = MultiStageEvaluator()
results = multi_evaluator.evaluate_architecture_analysis(
    "templates/advanced/architecture-analysis.md",
    "test_cases/complex-architectures.json"
)

print(f"Combined score: {results['combined_score']:.2%}")
print(f"Recommendation: {results['recommendation']}")
```

### Confidence-Based Evaluation

**Use Case**: Different evaluation strategies based on confidence levels

```python
class ConfidenceBasedEvaluator:
    def __init__(self):
        self.evaluator = PromptEvaluator()
    
    def evaluate_with_confidence(self, prompt_file, test_cases):
        """Adjust evaluation rigor based on prompt confidence."""
        
        # Initial evaluation to assess confidence
        initial_results = self.evaluator.evaluate(
            prompt_file=prompt_file,
            test_cases=test_cases[:5],  # Subset for quick assessment
            methods=['exact_match', 'cosine_similarity']
        )
        
        # Determine confidence level
        confidence = min(initial_results.accuracy, initial_results.consistency)
        
        if confidence >= 0.9:
            # High confidence: lighter evaluation
            config = {
                'methods': ['exact_match'],
                'statistical': {'confidence_level': 0.90}
            }
        elif confidence >= 0.7:
            # Medium confidence: standard evaluation
            config = {
                'methods': ['exact_match', 'cosine_similarity', 'llm_grade'],
                'statistical': {'confidence_level': 0.95}
            }
        else:
            # Low confidence: rigorous evaluation
            config = {
                'methods': ['exact_match', 'cosine_similarity', 'llm_grade', 'rouge_score'],
                'statistical': {'confidence_level': 0.99, 'min_sample_size': 50}
            }
        
        # Full evaluation with appropriate rigor
        evaluator = PromptEvaluator(config=config)
        final_results = evaluator.evaluate(
            prompt_file=prompt_file,
            test_cases=test_cases
        )
        
        return {
            'initial_confidence': confidence,
            'evaluation_rigor': 'high' if confidence < 0.7 else 'medium' if confidence < 0.9 else 'light',
            'final_results': final_results
        }

# Use confidence-based evaluation
confidence_evaluator = ConfidenceBasedEvaluator()
results = confidence_evaluator.evaluate_with_confidence(
    "templates/experimental/new-approach.md",
    "test_cases/challenging-scenarios.json"
)

print(f"Initial confidence: {results['initial_confidence']:.2%}")
print(f"Evaluation rigor: {results['evaluation_rigor']}")
print(f"Final accuracy: {results['final_results'].accuracy:.2%}")
```

### Domain-Adaptive Evaluation

**Use Case**: Automatically adjust evaluation criteria based on domain

```python
class DomainAdaptiveEvaluator:
    def __init__(self):
        self.evaluator = PromptEvaluator()
        self.domain_configs = {
            'security': {
                'thresholds': {'accuracy': 0.95, 'quality': 4.5},
                'required_metrics': ['exact_match', 'llm_grade'],
                'security_weights': {'vulnerability_detection': 0.4, 'severity_assessment': 0.3, 'remediation': 0.3}
            },
            'performance': {
                'thresholds': {'accuracy': 0.85, 'consistency': 0.9},
                'required_metrics': ['exact_match', 'cosine_similarity'],
                'performance_weights': {'bottleneck_identification': 0.5, 'optimization_suggestions': 0.5}
            },
            'documentation': {
                'thresholds': {'quality': 4.0, 'rouge_l': 0.8},
                'required_metrics': ['llm_grade', 'rouge_score'],
                'documentation_weights': {'completeness': 0.4, 'clarity': 0.3, 'accuracy': 0.3}
            }
        }
    
    def detect_domain(self, test_cases):
        """Automatically detect domain based on test case content."""
        security_keywords = ['vulnerability', 'security', 'exploit', 'authentication']
        performance_keywords = ['performance', 'optimization', 'bottleneck', 'latency']
        documentation_keywords = ['documentation', 'api', 'reference', 'guide']
        
        content = ' '.join([str(tc) for tc in test_cases]).lower()
        
        security_score = sum(1 for kw in security_keywords if kw in content)
        performance_score = sum(1 for kw in performance_keywords if kw in content)
        documentation_score = sum(1 for kw in documentation_keywords if kw in content)
        
        scores = {
            'security': security_score,
            'performance': performance_score,
            'documentation': documentation_score
        }
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def evaluate_adaptive(self, prompt_file, test_cases):
        """Evaluate with domain-adaptive configuration."""
        # Detect domain
        domain = self.detect_domain(test_cases)
        print(f"Detected domain: {domain}")
        
        # Get domain-specific configuration
        domain_config = self.domain_configs.get(domain, {})
        
        # Create adapted evaluator
        adapted_evaluator = PromptEvaluator(config=domain_config)
        
        # Run evaluation
        results = adapted_evaluator.evaluate(
            prompt_file=prompt_file,
            test_cases=test_cases,
            methods=domain_config.get('required_metrics', ['exact_match', 'llm_grade'])
        )
        
        # Domain-specific scoring
        if domain == 'security':
            security_score = self._calculate_security_score(results, domain_config)
            results.domain_score = security_score
        elif domain == 'performance':
            performance_score = self._calculate_performance_score(results, domain_config)
            results.domain_score = performance_score
        elif domain == 'documentation':
            documentation_score = self._calculate_documentation_score(results, domain_config)
            results.domain_score = documentation_score
        
        return results
    
    def _calculate_security_score(self, results, config):
        """Calculate domain-specific security score."""
        weights = config['security_weights']
        
        # Extract security-specific metrics from LLM grading
        llm_results = results.results.get('llm_grade', {})
        vulnerability_score = llm_results.get('vulnerability_detection', 0) / 5.0
        severity_score = llm_results.get('severity_assessment', 0) / 5.0
        remediation_score = llm_results.get('remediation_quality', 0) / 5.0
        
        security_score = (
            vulnerability_score * weights['vulnerability_detection'] +
            severity_score * weights['severity_assessment'] +
            remediation_score * weights['remediation']
        )
        
        return security_score

# Use domain-adaptive evaluation
adaptive_evaluator = DomainAdaptiveEvaluator()

# Security-focused test
security_results = adaptive_evaluator.evaluate_adaptive(
    "templates/specialized/security-analysis.md",
    "test_cases/security-vulnerabilities.json"
)

print(f"Domain score: {security_results.domain_score:.2%}")
print(f"Security evaluation complete")
```

## Real-World Use Cases

### CI/CD Integration

**Use Case**: Automated prompt validation in deployment pipeline

```python
# ci_cd_evaluation.py
import sys
import json
from pathlib import Path
from evaluations.scripts.evaluate_prompt import PromptEvaluator

def validate_prompt_for_deployment(prompt_file, test_cases_file, min_accuracy=0.90):
    """Validate prompt meets deployment criteria."""
    
    # Strict configuration for production
    config = {
        'model': 'claude-3-sonnet-20240229',
        'temperature': 0.0,
        'thresholds': {
            'accuracy': min_accuracy,
            'consistency': 0.85,
            'quality': 4.0
        },
        'statistical': {
            'confidence_level': 0.99,
            'min_sample_size': 30
        }
    }
    
    evaluator = PromptEvaluator(config=config)
    
    try:
        results = evaluator.evaluate(
            prompt_file=prompt_file,
            test_cases=test_cases_file,
            output_dir="ci_results"
        )
        
        # Deployment decision
        if results.passes_thresholds:
            print("✅ DEPLOYMENT APPROVED")
            print(f"Accuracy: {results.accuracy:.2%}")
            print(f"Quality: {results.quality:.1f}/5")
            return 0  # Success exit code
        else:
            print("❌ DEPLOYMENT REJECTED")
            print(f"Accuracy: {results.accuracy:.2%} (required: {min_accuracy:.2%})")
            print(f"Quality: {results.quality:.1f}/5 (required: 4.0)")
            return 1  # Failure exit code
            
    except Exception as e:
        print(f"❌ EVALUATION FAILED: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ci_cd_evaluation.py <prompt_file> <test_cases_file>")
        sys.exit(1)
    
    prompt_file = sys.argv[1]
    test_cases_file = sys.argv[2]
    
    exit_code = validate_prompt_for_deployment(prompt_file, test_cases_file)
    sys.exit(exit_code)
```

**GitHub Actions integration:**

```yaml
# .github/workflows/prompt-validation.yml
name: Prompt Validation
on:
  pull_request:
    paths: 
      - 'templates/**'
      - 'test_cases/**'

jobs:
  validate-prompts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          
      - name: Validate changed prompts
        run: |
          for prompt in $(git diff --name-only HEAD^ | grep "templates/"); do
            if [[ -f "$prompt" ]]; then
              test_case=$(echo "$prompt" | sed 's|templates/|test_cases/|' | sed 's|\.md$|.json|')
              if [[ -f "$test_case" ]]; then
                python ci_cd_evaluation.py "$prompt" "$test_case"
              fi
            fi
          done
```

### Performance Monitoring

**Use Case**: Monitor prompt performance over time

```python
# performance_monitor.py
import json
import datetime
from pathlib import Path
from evaluations.scripts.evaluate_prompt import PromptEvaluator

class PromptPerformanceMonitor:
    def __init__(self, monitoring_dir="monitoring"):
        self.monitoring_dir = Path(monitoring_dir)
        self.monitoring_dir.mkdir(exist_ok=True)
        self.evaluator = PromptEvaluator()
    
    def monitor_prompt(self, prompt_id, prompt_file, test_cases, alert_threshold=0.05):
        """Monitor prompt performance and alert on degradation."""
        
        # Run current evaluation
        current_results = self.evaluator.evaluate(
            prompt_file=prompt_file,
            test_cases=test_cases,
            output_dir=self.monitoring_dir / "current"
        )
        
        # Load historical performance
        history_file = self.monitoring_dir / f"{prompt_id}_history.json"
        history = self._load_history(history_file)
        
        # Calculate baseline (average of last 10 successful runs)
        baseline = self._calculate_baseline(history)
        
        # Check for performance degradation
        if baseline:
            accuracy_change = current_results.accuracy - baseline['accuracy']
            quality_change = current_results.quality - baseline['quality']
            
            if accuracy_change < -alert_threshold or quality_change < -1.0:
                self._send_alert(prompt_id, current_results, baseline, {
                    'accuracy_change': accuracy_change,
                    'quality_change': quality_change
                })
        
        # Update history
        history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'accuracy': current_results.accuracy,
            'consistency': current_results.consistency,
            'quality': current_results.quality,
            'evaluation_id': current_results.evaluation_id
        })
        
        # Save updated history
        self._save_history(history_file, history)
        
        return current_results
    
    def _load_history(self, history_file):
        """Load performance history."""
        if history_file.exists():
            with open(history_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_history(self, history_file, history):
        """Save performance history."""
        # Keep only last 100 entries
        history = history[-100:]
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def _calculate_baseline(self, history):
        """Calculate baseline from recent successful runs."""
        if len(history) < 5:
            return None
        
        recent = history[-10:]  # Last 10 runs
        return {
            'accuracy': sum(h['accuracy'] for h in recent) / len(recent),
            'quality': sum(h['quality'] for h in recent) / len(recent)
        }
    
    def _send_alert(self, prompt_id, current, baseline, changes):
        """Send performance degradation alert."""
        alert_message = f"""
        🚨 PERFORMANCE ALERT: {prompt_id}
        
        Current Performance:
        - Accuracy: {current.accuracy:.2%}
        - Quality: {current.quality:.1f}/5
        
        Baseline Performance:
        - Accuracy: {baseline['accuracy']:.2%}
        - Quality: {baseline['quality']:.1f}/5
        
        Changes:
        - Accuracy: {changes['accuracy_change']:+.2%}
        - Quality: {changes['quality_change']:+.1f}
        
        Evaluation ID: {current.evaluation_id}
        """
        
        print(alert_message)
        
        # In production, send to Slack, email, etc.
        # self._send_slack_alert(alert_message)
        # self._send_email_alert(alert_message)

# Usage example
monitor = PromptPerformanceMonitor()

# Regular monitoring (run daily via cron)
results = monitor.monitor_prompt(
    prompt_id="production_code_review",
    prompt_file="templates/production/code-review.md",
    test_cases="test_cases/production/code-review-samples.json"
)

print(f"Monitoring complete. Current accuracy: {results.accuracy:.2%}")
```

### A/B Testing in Production

**Use Case**: Gradual rollout with performance comparison

```python
# production_ab_test.py
import random
from evaluations.scripts.compare_prompts import PromptComparator

class ProductionABTest:
    def __init__(self, control_prompt, treatment_prompt, test_cases):
        self.control_prompt = control_prompt
        self.treatment_prompt = treatment_prompt
        self.test_cases = test_cases
        self.comparator = PromptComparator()
        self.traffic_split = 0.1  # Start with 10% treatment traffic
        self.results = {'control': [], 'treatment': []}
    
    def route_request(self, request_data):
        """Route request to control or treatment based on traffic split."""
        if random.random() < self.traffic_split:
            return self._process_with_treatment(request_data)
        else:
            return self._process_with_control(request_data)
    
    def _process_with_control(self, request_data):
        """Process request with control prompt."""
        # In production, this would call your prompt processing system
        result = self._simulate_prompt_processing(self.control_prompt, request_data)
        self.results['control'].append(result)
        return result
    
    def _process_with_treatment(self, request_data):
        """Process request with treatment prompt."""
        result = self._simulate_prompt_processing(self.treatment_prompt, request_data)
        self.results['treatment'].append(result)
        return result
    
    def analyze_results(self, min_samples=100):
        """Analyze A/B test results when sufficient data is available."""
        if len(self.results['treatment']) < min_samples:
            return None
        
        # Run statistical comparison
        comparison = self.comparator.compare(
            baseline=self.control_prompt,
            variant=self.treatment_prompt,
            test_cases=self.test_cases
        )
        
        # Decision logic
        if comparison.is_significant and comparison.winner == 'variant':
            decision = 'SCALE_UP'
            self.traffic_split = min(self.traffic_split * 2, 1.0)
        elif comparison.is_significant and comparison.winner == 'baseline':
            decision = 'SCALE_DOWN'
            self.traffic_split = max(self.traffic_split * 0.5, 0.0)
        else:
            decision = 'CONTINUE'
        
        return {
            'decision': decision,
            'new_traffic_split': self.traffic_split,
            'p_value': comparison.p_value,
            'effect_size': comparison.effect_size,
            'control_samples': len(self.results['control']),
            'treatment_samples': len(self.results['treatment'])
        }
    
    def _simulate_prompt_processing(self, prompt, request_data):
        """Simulate prompt processing (replace with actual implementation)."""
        # This would be your actual prompt processing logic
        return {
            'response': f"Processed with {prompt}",
            'quality_score': random.uniform(3.5, 5.0),
            'processing_time': random.uniform(0.5, 2.0)
        }

# Usage in production system
ab_test = ProductionABTest(
    control_prompt="templates/production/current-version.md",
    treatment_prompt="templates/production/new-version.md",
    test_cases="test_cases/production/validation-set.json"
)

# Simulate production traffic
for i in range(1000):
    request_data = {"user_id": i, "request": f"sample request {i}"}
    response = ab_test.route_request(request_data)
    
    # Analyze every 100 requests
    if i % 100 == 0:
        analysis = ab_test.analyze_results()
        if analysis:
            print(f"A/B Test Update: {analysis['decision']}")
            print(f"Traffic split: {analysis['new_traffic_split']:.1%}")
```

## Integration Examples

### Slack Bot Integration

**Use Case**: Slack bot for on-demand prompt evaluation

```python
# slack_bot.py
from slack_bolt import App
from evaluations.scripts.evaluate_prompt import PromptEvaluator

app = App(token="your-slack-bot-token")

@app.command("/evaluate-prompt")
def evaluate_prompt_command(ack, respond, command):
    ack()
    
    # Parse command arguments
    args = command['text'].split()
    if len(args) < 2:
        respond("Usage: /evaluate-prompt <prompt_file> <test_cases_file>")
        return
    
    prompt_file = args[0]
    test_cases_file = args[1]
    
    # Show loading message
    respond("🔄 Evaluating prompt... This may take a few minutes.")
    
    try:
        # Run evaluation
        evaluator = PromptEvaluator()
        results = evaluator.evaluate(
            prompt_file=f"templates/{prompt_file}",
            test_cases=f"test_cases/{test_cases_file}",
            output_dir=f"slack_results/{command['user_id']}"
        )
        
        # Format results for Slack
        status_emoji = "✅" if results.passes_thresholds else "❌"
        message = f"""
        {status_emoji} *Prompt Evaluation Results*
        
        *Metrics:*
        • Accuracy: {results.accuracy:.1%}
        • Consistency: {results.consistency:.3f}
        • Quality: {results.quality:.1f}/5
        
        *Status:* {'APPROVED' if results.passes_thresholds else 'NEEDS IMPROVEMENT'}
        *Evaluation ID:* {results.evaluation_id}
        """
        
        respond(message)
        
    except Exception as e:
        respond(f"❌ Evaluation failed: {str(e)}")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
```

### Jupyter Notebook Integration

**Use Case**: Interactive evaluation in Jupyter notebooks

```python
# notebook_evaluation.py
import ipywidgets as widgets
from IPython.display import display, HTML
import plotly.graph_objects as go
from evaluations.scripts.evaluate_prompt import PromptEvaluator

class InteractiveEvaluator:
    def __init__(self):
        self.evaluator = PromptEvaluator()
        self.setup_widgets()
    
    def setup_widgets(self):
        """Setup interactive widgets for Jupyter."""
        self.prompt_dropdown = widgets.Dropdown(
            options=['base/code-review.md', 'enhanced/code-review.md'],
            description='Prompt:'
        )
        
        self.test_cases_dropdown = widgets.Dropdown(
            options=['code-review.json', 'security-review.json'],
            description='Test Cases:'
        )
        
        self.evaluate_button = widgets.Button(
            description='Evaluate',
            button_style='primary'
        )
        
        self.output_area = widgets.Output()
        
        self.evaluate_button.on_click(self.on_evaluate_click)
    
    def display(self):
        """Display the interactive interface."""
        display(widgets.VBox([
            self.prompt_dropdown,
            self.test_cases_dropdown,
            self.evaluate_button,
            self.output_area
        ]))
    
    def on_evaluate_click(self, button):
        """Handle evaluate button click."""
        with self.output_area:
            self.output_area.clear_output()
            print("🔄 Running evaluation...")
            
            try:
                results = self.evaluator.evaluate(
                    prompt_file=f"templates/{self.prompt_dropdown.value}",
                    test_cases=f"test_cases/{self.test_cases_dropdown.value}"
                )
                
                self.display_results(results)
                
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def display_results(self, results):
        """Display results with interactive charts."""
        # Metrics summary
        print(f"✅ Evaluation Complete!")
        print(f"Accuracy: {results.accuracy:.1%}")
        print(f"Quality: {results.quality:.1f}/5")
        print(f"Status: {'PASS' if results.passes_thresholds else 'FAIL'}")
        
        # Create interactive chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=['Accuracy', 'Consistency', 'Quality/5', 'ROUGE-L'],
            y=[results.accuracy, results.consistency, results.quality/5, results.rouge_l],
            marker_color=['green' if results.accuracy > 0.85 else 'red',
                         'green' if results.consistency > 0.8 else 'red',
                         'green' if results.quality > 4.0 else 'red',
                         'green' if results.rouge_l > 0.6 else 'red']
        ))
        
        fig.update_layout(
            title="Evaluation Metrics",
            yaxis_title="Score",
            showlegend=False
        )
        
        fig.show()

# Usage in Jupyter notebook
evaluator_widget = InteractiveEvaluator()
evaluator_widget.display()
```

---

**These examples demonstrate the versatility and power of Voyager-4's evaluation system.** Adapt them to your specific use cases and requirements.

*Need more examples or have specific questions? Check our [API Reference](../api_reference/evaluation_api.md) or [Tutorial Series](../tutorials/).*