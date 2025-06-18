# Evaluation API Reference

This document provides comprehensive API reference for Voyager-4's evaluation system, including classes, methods, and usage examples.

## Core Classes

### PromptEvaluator

Main class for evaluating individual prompts against test cases.

```python
class PromptEvaluator:
    """
    Comprehensive prompt evaluation system.
    
    Provides statistical validation and assessment of Claude Code prompts
    using multiple evaluation methods including exact match, cosine similarity,
    LLM grading, and ROUGE scoring.
    """
```

#### Constructor

```python
def __init__(self, config: Optional[Dict] = None, logger: Optional[Logger] = None)
```

**Parameters:**
- `config` (Optional[Dict]): Configuration dictionary for evaluation parameters
- `logger` (Optional[Logger]): Custom logger instance

**Example:**
```python
from evaluations.scripts.evaluate_prompt import PromptEvaluator

# Default configuration
evaluator = PromptEvaluator()

# Custom configuration
config = {
    'model': 'claude-3-sonnet-20240229',
    'temperature': 0.1,
    'timeout': 120,
    'thresholds': {
        'accuracy': 0.85,
        'consistency': 0.8,
        'quality': 4.0
    }
}
evaluator = PromptEvaluator(config=config)
```

#### Methods

##### evaluate()

```python
def evaluate(
    self,
    prompt_file: Union[str, Path],
    test_cases: Union[str, Path, List[Dict]],
    methods: Optional[List[str]] = None,
    output_dir: Optional[Union[str, Path]] = None,
    save_results: bool = True
) -> EvaluationResult
```

Evaluate a prompt against test cases using specified methods.

**Parameters:**
- `prompt_file`: Path to prompt template file
- `test_cases`: Path to test cases file or list of test case dictionaries
- `methods`: List of evaluation methods to use (default: all available)
- `output_dir`: Directory to save results (default: auto-generated)
- `save_results`: Whether to save results to disk

**Returns:**
- `EvaluationResult`: Object containing evaluation metrics and metadata

**Available Methods:**
- `exact_match`: Binary accuracy for categorical outputs
- `cosine_similarity`: Semantic consistency measurement
- `llm_grade`: Quality assessment using Claude
- `rouge_score`: Text overlap analysis

**Example:**
```python
# Basic evaluation
results = evaluator.evaluate(
    prompt_file="templates/base/codebase-analysis.md",
    test_cases="test_cases/codebase-analysis.json"
)

print(f"Accuracy: {results.accuracy:.2%}")
print(f"Consistency: {results.consistency:.3f}")
print(f"Quality: {results.quality:.1f}/5")

# Custom methods
results = evaluator.evaluate(
    prompt_file="templates/enhanced/bug-fixing.md",
    test_cases="test_cases/bug-fixing.json",
    methods=["exact_match", "llm_grade"],
    output_dir="results/bug-fixing-eval"
)
```

##### evaluate_with_config()

```python
def evaluate_with_config(
    self,
    evaluation_config: EvaluationConfig
) -> EvaluationResult
```

Evaluate using a structured configuration object.

**Parameters:**
- `evaluation_config`: EvaluationConfig object with all parameters

**Example:**
```python
from evaluations.config import EvaluationConfig

config = EvaluationConfig(
    prompt_file="templates/advanced/architecture-analysis.md",
    test_cases="test_cases/architecture.json",
    methods=["cosine_similarity", "llm_grade"],
    model_config={
        'model': 'claude-3-opus-20240229',
        'temperature': 0.0,
        'max_tokens': 4000
    },
    quality_thresholds={
        'consistency': 0.85,
        'quality': 4.5
    }
)

results = evaluator.evaluate_with_config(config)
```

##### batch_evaluate()

```python
def batch_evaluate(
    self,
    prompt_files: List[Union[str, Path]],
    test_cases: Union[str, Path, List[Dict]],
    methods: Optional[List[str]] = None,
    parallel: bool = True,
    max_workers: int = 5
) -> BatchEvaluationResult
```

Evaluate multiple prompts in batch mode.

**Parameters:**
- `prompt_files`: List of prompt template files
- `test_cases`: Test cases to use for all prompts
- `methods`: Evaluation methods to apply
- `parallel`: Whether to run evaluations in parallel
- `max_workers`: Maximum number of parallel workers

**Example:**
```python
# Batch evaluation
prompt_files = [
    "templates/base/codebase-analysis.md",
    "templates/enhanced/codebase-analysis.md",
    "templates/advanced/codebase-analysis.md"
]

batch_results = evaluator.batch_evaluate(
    prompt_files=prompt_files,
    test_cases="test_cases/codebase-analysis.json",
    parallel=True
)

# Access individual results
for prompt_file, result in batch_results.results.items():
    print(f"{prompt_file}: {result.accuracy:.2%}")
```

### PromptComparator

Class for statistical comparison between prompt variants.

```python
class PromptComparator:
    """
    Statistical comparison tool for prompt variants.
    
    Performs A/B testing with significance testing to determine
    which prompt performs better across multiple metrics.
    """
```

#### Constructor

```python
def __init__(self, config: Optional[Dict] = None)
```

**Parameters:**
- `config`: Configuration for statistical testing parameters

**Example:**
```python
from evaluations.scripts.compare_prompts import PromptComparator

# Default configuration
comparator = PromptComparator()

# Custom statistical configuration
config = {
    'statistical': {
        'confidence_level': 0.99,
        'min_sample_size': 50,
        'significance_threshold': 0.01,
        'use_bonferroni_correction': True
    }
}
comparator = PromptComparator(config=config)
```

#### Methods

##### compare()

```python
def compare(
    self,
    baseline: Union[str, Path],
    variant: Union[str, Path],
    test_cases: Union[str, Path, List[Dict]],
    methods: Optional[List[str]] = None,
    statistical_test: str = 'auto'
) -> ComparisonResult
```

Compare two prompt variants with statistical significance testing.

**Parameters:**
- `baseline`: Path to baseline prompt
- `variant`: Path to variant prompt
- `test_cases`: Test cases for comparison
- `methods`: Evaluation methods to compare
- `statistical_test`: Type of statistical test ('chi_square', 't_test', 'mannwhitney', 'auto')

**Returns:**
- `ComparisonResult`: Statistical comparison results

**Example:**
```python
# Basic comparison
comparison = comparator.compare(
    baseline="templates/base/bug-fixing.md",
    variant="templates/enhanced/bug-fixing.md",
    test_cases="test_cases/bug-fixing.json"
)

print(f"Winner: {comparison.winner}")
print(f"P-value: {comparison.p_value:.4f}")
print(f"Effect size: {comparison.effect_size:.3f}")
print(f"Confidence: {comparison.confidence:.2%}")

# Check statistical significance
if comparison.is_significant:
    print(f"Statistically significant improvement: {comparison.improvement:.2%}")
else:
    print("No statistically significant difference")
```

##### compare_multiple()

```python
def compare_multiple(
    self,
    prompts: Dict[str, Union[str, Path]],
    test_cases: Union[str, Path, List[Dict]],
    methods: Optional[List[str]] = None,
    correction_method: str = 'bonferroni'
) -> MultipleComparisonResult
```

Compare multiple prompt variants simultaneously.

**Parameters:**
- `prompts`: Dictionary mapping names to prompt file paths
- `test_cases`: Test cases for comparison
- `methods`: Evaluation methods to compare
- `correction_method`: Multiple comparison correction method

**Example:**
```python
# Multiple prompt comparison
prompts = {
    'base': 'templates/base/code-generation.md',
    'enhanced': 'templates/enhanced/code-generation.md',
    'advanced': 'templates/advanced/code-generation.md',
    'structured': 'templates/structured/code-generation.md'
}

multi_comparison = comparator.compare_multiple(
    prompts=prompts,
    test_cases="test_cases/code-generation.json"
)

# Get best performer
best_prompt = multi_comparison.get_best_performer()
print(f"Best prompt: {best_prompt.name}")
print(f"Win rate: {best_prompt.win_rate:.2%}")

# Pairwise comparisons
for comparison in multi_comparison.pairwise_comparisons:
    print(f"{comparison.prompt_a} vs {comparison.prompt_b}: "
          f"p-value = {comparison.p_value:.4f}")
```

## Result Classes

### EvaluationResult

```python
class EvaluationResult:
    """Container for evaluation results and metadata."""
    
    def __init__(self, evaluation_id: str, results: Dict, metadata: Dict):
        self.evaluation_id = evaluation_id
        self.results = results
        self.metadata = metadata
        self.timestamp = datetime.now()
```

#### Properties

```python
@property
def accuracy(self) -> float:
    """Overall accuracy score (0.0 to 1.0)."""
    return self.results.get('exact_match', {}).get('accuracy', 0.0)

@property
def consistency(self) -> float:
    """Consistency score based on cosine similarity (0.0 to 1.0)."""
    return self.results.get('cosine_similarity', {}).get('mean_similarity', 0.0)

@property
def quality(self) -> float:
    """Quality score from LLM grading (1.0 to 5.0)."""
    return self.results.get('llm_grade', {}).get('overall_score', 0.0)

@property
def rouge_l(self) -> float:
    """ROUGE-L score for text overlap (0.0 to 1.0)."""
    return self.results.get('rouge_score', {}).get('rougeL', 0.0)

@property
def passes_thresholds(self) -> bool:
    """Whether results meet configured quality thresholds."""
    return (
        self.accuracy >= self.metadata.get('thresholds', {}).get('accuracy', 0.0) and
        self.consistency >= self.metadata.get('thresholds', {}).get('consistency', 0.0) and
        self.quality >= self.metadata.get('thresholds', {}).get('quality', 0.0)
    )
```

#### Methods

```python
def to_dict(self) -> Dict:
    """Convert result to dictionary format."""
    return {
        'evaluation_id': self.evaluation_id,
        'timestamp': self.timestamp.isoformat(),
        'results': self.results,
        'metadata': self.metadata,
        'summary': {
            'accuracy': self.accuracy,
            'consistency': self.consistency,
            'quality': self.quality,
            'passes_thresholds': self.passes_thresholds
        }
    }

def to_markdown(self) -> str:
    """Generate markdown report."""
    return self._generate_markdown_report()

def save(self, output_dir: Union[str, Path], formats: List[str] = None):
    """Save results in specified formats."""
    formats = formats or ['json', 'markdown']
    
    for format_type in formats:
        if format_type == 'json':
            self._save_json(output_dir)
        elif format_type == 'markdown':
            self._save_markdown(output_dir)
        elif format_type == 'csv':
            self._save_csv(output_dir)
```

### ComparisonResult

```python
class ComparisonResult:
    """Container for prompt comparison results."""
    
    def __init__(self, baseline_result: EvaluationResult, 
                 variant_result: EvaluationResult,
                 statistical_analysis: Dict):
        self.baseline_result = baseline_result
        self.variant_result = variant_result
        self.statistical_analysis = statistical_analysis
```

#### Properties

```python
@property
def winner(self) -> str:
    """Name of the winning prompt ('baseline' or 'variant')."""
    return self.statistical_analysis.get('winner', 'baseline')

@property
def p_value(self) -> float:
    """Statistical significance p-value."""
    return self.statistical_analysis.get('p_value', 1.0)

@property
def is_significant(self) -> bool:
    """Whether difference is statistically significant."""
    threshold = self.statistical_analysis.get('significance_threshold', 0.05)
    return self.p_value < threshold

@property
def effect_size(self) -> float:
    """Effect size of the difference."""
    return self.statistical_analysis.get('effect_size', 0.0)

@property
def confidence(self) -> float:
    """Confidence in the result (0.0 to 1.0)."""
    return 1.0 - self.p_value

@property
def improvement(self) -> float:
    """Relative improvement of winner over loser."""
    if self.winner == 'variant':
        baseline_score = self.baseline_result.accuracy
        variant_score = self.variant_result.accuracy
        return (variant_score - baseline_score) / baseline_score
    else:
        return 0.0
```

## Metric Classes

### BaseMetric

```python
class BaseMetric(ABC):
    """Abstract base class for evaluation metrics."""
    
    @abstractmethod
    def calculate(self, predictions: List, actuals: List, context: Dict = None) -> Dict:
        """Calculate metric value."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return metric name."""
        pass
```

### ExactMatchMetric

```python
class ExactMatchMetric(BaseMetric):
    """Exact match accuracy metric for categorical outputs."""
    
    def calculate(self, predictions: List[str], actuals: List[str], 
                  context: Dict = None) -> Dict:
        """
        Calculate exact match accuracy.
        
        Args:
            predictions: List of predicted values
            actuals: List of actual/expected values
            context: Additional context (case_sensitive, normalize, etc.)
            
        Returns:
            Dictionary with accuracy metrics
        """
        # Implementation details...
        
        return {
            'accuracy': accuracy_score,
            'correct_count': correct_count,
            'total_count': total_count,
            'error_analysis': error_breakdown
        }
```

### CosineSimilarityMetric

```python
class CosineSimilarityMetric(BaseMetric):
    """Cosine similarity metric for semantic consistency."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize with sentence transformer model."""
        self.model = SentenceTransformer(model_name)
    
    def calculate(self, predictions: List[str], actuals: List[str], 
                  context: Dict = None) -> Dict:
        """
        Calculate cosine similarity metrics.
        
        Returns:
            Dictionary with similarity metrics including mean, std, and distribution
        """
        # Implementation details...
        
        return {
            'mean_similarity': mean_similarity,
            'std_similarity': std_similarity,
            'min_similarity': min_similarity,
            'max_similarity': max_similarity,
            'similarity_distribution': distribution
        }
```

### LLMGradeMetric

```python
class LLMGradeMetric(BaseMetric):
    """LLM-based quality grading metric."""
    
    def __init__(self, grader_model: str = 'claude-3-sonnet-20240229',
                 rubric: Dict = None):
        """Initialize with grader model and rubric."""
        self.grader_model = grader_model
        self.rubric = rubric or self._default_rubric()
        self.client = Anthropic()
    
    def calculate(self, predictions: List[str], actuals: List[str], 
                  context: Dict = None) -> Dict:
        """
        Calculate LLM-based quality scores.
        
        Uses Claude to grade responses based on rubric criteria.
        """
        # Implementation details...
        
        return {
            'overall_score': overall_score,
            'accuracy_score': accuracy_score,
            'completeness_score': completeness_score,
            'clarity_score': clarity_score,
            'relevance_score': relevance_score,
            'score_distribution': distribution
        }
```

## Configuration Classes

### EvaluationConfig

```python
class EvaluationConfig:
    """Configuration class for evaluation parameters."""
    
    def __init__(self, **kwargs):
        # Model configuration
        self.model = kwargs.get('model', 'claude-3-sonnet-20240229')
        self.temperature = kwargs.get('temperature', 0.1)
        self.max_tokens = kwargs.get('max_tokens', 4000)
        self.timeout = kwargs.get('timeout', 120)
        
        # Evaluation methods
        self.methods = kwargs.get('methods', ['exact_match', 'cosine_similarity', 'llm_grade'])
        
        # Quality thresholds
        thresholds = kwargs.get('thresholds', {})
        self.accuracy_threshold = thresholds.get('accuracy', 0.85)
        self.consistency_threshold = thresholds.get('consistency', 0.8)
        self.quality_threshold = thresholds.get('quality', 4.0)
        
        # Statistical configuration
        statistical = kwargs.get('statistical', {})
        self.confidence_level = statistical.get('confidence_level', 0.95)
        self.min_sample_size = statistical.get('min_sample_size', 30)
        self.significance_threshold = statistical.get('significance_threshold', 0.05)
    
    @classmethod
    def from_file(cls, config_file: Union[str, Path]) -> 'EvaluationConfig':
        """Load configuration from YAML file."""
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data.get('evaluation', {}))
    
    def to_dict(self) -> Dict:
        """Convert configuration to dictionary."""
        return {
            'model': self.model,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'timeout': self.timeout,
            'methods': self.methods,
            'thresholds': {
                'accuracy': self.accuracy_threshold,
                'consistency': self.consistency_threshold,
                'quality': self.quality_threshold
            },
            'statistical': {
                'confidence_level': self.confidence_level,
                'min_sample_size': self.min_sample_size,
                'significance_threshold': self.significance_threshold
            }
        }
```

## Utility Functions

### Statistical Tests

```python
def chi_square_test(group_a: List[bool], group_b: List[bool]) -> Tuple[float, float]:
    """
    Perform chi-square test for categorical data.
    
    Args:
        group_a: Boolean results for group A
        group_b: Boolean results for group B
        
    Returns:
        Tuple of (chi_square_statistic, p_value)
    """
    from scipy.stats import chi2_contingency
    
    # Create contingency table
    a_success = sum(group_a)
    a_failure = len(group_a) - a_success
    b_success = sum(group_b)
    b_failure = len(group_b) - b_success
    
    contingency_table = [[a_success, a_failure], [b_success, b_failure]]
    
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    return chi2, p_value

def t_test(group_a: List[float], group_b: List[float], 
           paired: bool = False) -> Tuple[float, float]:
    """
    Perform t-test for continuous data.
    
    Args:
        group_a: Continuous values for group A
        group_b: Continuous values for group B
        paired: Whether to perform paired t-test
        
    Returns:
        Tuple of (t_statistic, p_value)
    """
    from scipy.stats import ttest_ind, ttest_rel
    
    if paired:
        t_stat, p_value = ttest_rel(group_a, group_b)
    else:
        t_stat, p_value = ttest_ind(group_a, group_b)
    
    return t_stat, p_value

def calculate_effect_size(group_a: List[float], group_b: List[float]) -> float:
    """
    Calculate Cohen's d effect size.
    
    Args:
        group_a: Values for group A
        group_b: Values for group B
        
    Returns:
        Cohen's d effect size
    """
    import numpy as np
    
    mean_a = np.mean(group_a)
    mean_b = np.mean(group_b)
    std_a = np.std(group_a, ddof=1)
    std_b = np.std(group_b, ddof=1)
    
    # Pooled standard deviation
    n_a, n_b = len(group_a), len(group_b)
    pooled_std = np.sqrt(((n_a - 1) * std_a**2 + (n_b - 1) * std_b**2) / (n_a + n_b - 2))
    
    # Cohen's d
    cohens_d = (mean_a - mean_b) / pooled_std
    return abs(cohens_d)
```

### Data Loading

```python
def load_test_cases(file_path: Union[str, Path]) -> List[Dict]:
    """
    Load test cases from JSON file.
    
    Args:
        file_path: Path to JSON file containing test cases
        
    Returns:
        List of test case dictionaries
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is invalid
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Test cases file not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'test_cases' in data:
            return data['test_cases']
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Invalid test cases format")
            
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

def save_results(results: Union[EvaluationResult, ComparisonResult], 
                 output_dir: Union[str, Path],
                 formats: List[str] = None) -> List[Path]:
    """
    Save evaluation results in multiple formats.
    
    Args:
        results: Results object to save
        output_dir: Directory to save results
        formats: List of formats ('json', 'markdown', 'csv', 'html')
        
    Returns:
        List of created file paths
    """
    formats = formats or ['json', 'markdown']
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    created_files = []
    
    for format_type in formats:
        if format_type == 'json':
            file_path = output_dir / f"results_{results.evaluation_id}.json"
            with open(file_path, 'w') as f:
                json.dump(results.to_dict(), f, indent=2)
            created_files.append(file_path)
            
        elif format_type == 'markdown':
            file_path = output_dir / f"report_{results.evaluation_id}.md"
            with open(file_path, 'w') as f:
                f.write(results.to_markdown())
            created_files.append(file_path)
    
    return created_files
```

## Examples

### Complete Evaluation Workflow

```python
from evaluations.scripts.evaluate_prompt import PromptEvaluator
from evaluations.scripts.compare_prompts import PromptComparator
from evaluations.config import EvaluationConfig

# 1. Setup configuration
config = EvaluationConfig(
    model='claude-3-sonnet-20240229',
    temperature=0.1,
    methods=['exact_match', 'cosine_similarity', 'llm_grade'],
    thresholds={
        'accuracy': 0.85,
        'consistency': 0.8,
        'quality': 4.0
    }
)

# 2. Initialize evaluator
evaluator = PromptEvaluator(config=config.to_dict())

# 3. Evaluate baseline prompt
baseline_results = evaluator.evaluate(
    prompt_file="templates/base/code-review.md",
    test_cases="test_cases/code-review.json",
    output_dir="results/baseline"
)

print(f"Baseline accuracy: {baseline_results.accuracy:.2%}")
print(f"Baseline quality: {baseline_results.quality:.1f}/5")

# 4. Evaluate enhanced prompt
enhanced_results = evaluator.evaluate(
    prompt_file="templates/enhanced/code-review.md",
    test_cases="test_cases/code-review.json",
    output_dir="results/enhanced"
)

# 5. Statistical comparison
comparator = PromptComparator(config=config.to_dict())
comparison = comparator.compare(
    baseline="templates/base/code-review.md",
    variant="templates/enhanced/code-review.md",
    test_cases="test_cases/code-review.json"
)

# 6. Analysis and decision
if comparison.is_significant:
    improvement = comparison.improvement
    print(f"✅ Significant improvement: {improvement:.2%}")
    print(f"P-value: {comparison.p_value:.4f}")
    print(f"Effect size: {comparison.effect_size:.3f}")
    
    if comparison.winner == 'variant':
        print("🏆 Enhanced template is significantly better")
    else:
        print("🏆 Baseline template is significantly better")
else:
    print("❌ No significant difference found")
    print(f"P-value: {comparison.p_value:.4f}")

# 7. Save detailed results
comparison.save("results/comparison", formats=['json', 'markdown', 'html'])
```

---

**This API reference provides comprehensive documentation for the evaluation system.** For additional examples and use cases, see the [Tutorial Series](../tutorials/) and [Usage Examples](../examples/).

*Questions about specific APIs? Check our [FAQ](../faq.md) or explore the [source code examples](../../evaluations/scripts/).*