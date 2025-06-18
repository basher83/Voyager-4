# Contributing Guide

Welcome to the Voyager-4 development community! This guide provides everything you need to contribute effectively to the Claude Code Prompt Development Framework.

## Getting Started

### Prerequisites

- **Git**: Version control and collaboration
- **Python 3.8+**: Core development language
- **Claude Code SDK**: For testing integrations
- **Development Tools**: IDE with Python support (VS Code recommended)

### Development Environment Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/yourusername/voyager-4.git
cd voyager-4

# 2. Create development branch
git checkout -b feature/your-feature-name

# 3. Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 5. Install pre-commit hooks
pre-commit install

# 6. Run initial tests
python -m pytest tests/
```

### Development Dependencies

Create `requirements-dev.txt`:

```txt
# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
pytest-asyncio>=0.21.0

# Code Quality
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
isort>=5.12.0

# Development Tools
pre-commit>=3.0.0
jupyter>=1.0.0
ipykernel>=6.23.0

# Documentation
sphinx>=6.0.0
sphinx-rtd-theme>=1.2.0
myst-parser>=1.0.0

# Debugging
pdb++>=0.10.0
icecream>=2.1.0
```

## Development Workflow

### Branch Strategy

We use a feature branch workflow:

```bash
# Main branches
main          # Production-ready code
develop       # Integration branch for features

# Feature branches
feature/evaluation-improvements
feature/cognee-enhancement
feature/template-system-v2

# Release branches
release/v1.1.0

# Hotfix branches
hotfix/critical-bug-fix
```

### Commit Guidelines

Follow conventional commit format:

```bash
# Commit message format
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Changes to build process or auxiliary tools

**Examples:**
```bash
git commit -m "feat(evaluation): add cosine similarity metric"
git commit -m "fix(templates): resolve variable substitution bug"
git commit -m "docs(api): update evaluation API reference"
git commit -m "test(cognee): add integration test suite"
```

### Code Standards

#### Python Style Guide

We follow PEP 8 with these additions:

```python
# File header template
"""
Module: evaluation_engine.py
Description: Core evaluation functionality for prompt testing
Author: Your Name
Date: 2024-06-18
"""

# Import organization
# 1. Standard library imports
import os
import sys
from typing import Dict, List, Optional

# 2. Third-party imports
import numpy as np
import pandas as pd
from anthropic import Anthropic

# 3. Local imports
from evaluations.metrics import BaseMetric
from templates.renderer import TemplateRenderer

# Class documentation
class PromptEvaluator:
    """
    Comprehensive prompt evaluation system.
    
    This class provides statistical validation and assessment
    of Claude Code prompts using multiple evaluation methods.
    
    Attributes:
        config: Configuration object for evaluation parameters
        metrics: List of evaluation metrics to apply
        
    Example:
        >>> evaluator = PromptEvaluator()
        >>> results = evaluator.evaluate(prompt, test_cases)
        >>> print(f"Accuracy: {results['accuracy']:.2%}")
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize evaluator with configuration."""
        self.config = config or self._load_default_config()
        self.metrics = self._initialize_metrics()
    
    def evaluate(self, prompt: str, test_cases: List[Dict]) -> Dict:
        """
        Evaluate prompt against test cases.
        
        Args:
            prompt: Template prompt to evaluate
            test_cases: List of test scenarios
            
        Returns:
            Dictionary containing evaluation results
            
        Raises:
            EvaluationError: If evaluation fails
        """
        pass
```

#### Type Hints

Use comprehensive type hints:

```python
from typing import Dict, List, Optional, Union, Tuple, Any
from pathlib import Path

def evaluate_prompt(
    prompt_file: Union[str, Path],
    test_cases: List[Dict[str, Any]],
    metrics: Optional[List[str]] = None,
    output_dir: Optional[Path] = None
) -> Tuple[Dict[str, float], List[str]]:
    """Evaluate prompt with type safety."""
    pass
```

#### Error Handling

Implement comprehensive error handling:

```python
from evaluations.exceptions import (
    EvaluationError, 
    TemplateError, 
    ConfigurationError
)

class PromptEvaluator:
    def evaluate(self, prompt: str, test_cases: List[Dict]) -> Dict:
        try:
            # Validation
            if not prompt.strip():
                raise ValueError("Prompt cannot be empty")
            
            if not test_cases:
                raise ValueError("Test cases are required")
            
            # Core evaluation logic
            results = self._run_evaluation(prompt, test_cases)
            
            return results
            
        except ValueError as e:
            raise EvaluationError(f"Invalid input: {e}")
        except Exception as e:
            self.logger.error(f"Evaluation failed: {e}")
            raise EvaluationError(f"Evaluation failed: {e}")
```

### Testing Guidelines

#### Test Structure

```
tests/
├── unit/                   # Unit tests
│   ├── test_evaluation.py
│   ├── test_templates.py
│   └── test_cognee.py
├── integration/           # Integration tests
│   ├── test_api_integration.py
│   └── test_end_to_end.py
├── fixtures/              # Test data
│   ├── sample_prompts/
│   └── test_cases/
└── conftest.py           # Pytest configuration
```

#### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch
from evaluations.prompt_evaluator import PromptEvaluator

class TestPromptEvaluator:
    """Test suite for PromptEvaluator class."""
    
    @pytest.fixture
    def evaluator(self):
        """Create evaluator instance for testing."""
        return PromptEvaluator()
    
    @pytest.fixture
    def sample_test_cases(self):
        """Sample test cases for evaluation."""
        return [
            {
                "id": "test_1",
                "input": "Sample input",
                "expected_output": "Expected result",
                "category": "basic"
            }
        ]
    
    def test_evaluate_basic_prompt(self, evaluator, sample_test_cases):
        """Test basic prompt evaluation functionality."""
        prompt = "Analyze the following: {input}"
        
        results = evaluator.evaluate(prompt, sample_test_cases)
        
        assert "accuracy" in results
        assert "consistency" in results
        assert results["accuracy"] >= 0.0
        assert results["accuracy"] <= 1.0
    
    def test_evaluate_empty_prompt_raises_error(self, evaluator, sample_test_cases):
        """Test that empty prompt raises appropriate error."""
        with pytest.raises(ValueError, match="Prompt cannot be empty"):
            evaluator.evaluate("", sample_test_cases)
    
    @patch('evaluations.prompt_evaluator.anthropic.Anthropic')
    def test_evaluate_with_mocked_api(self, mock_anthropic, evaluator, sample_test_cases):
        """Test evaluation with mocked API calls."""
        # Setup mock
        mock_client = Mock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value.content = [
            Mock(text="Mocked response")
        ]
        
        prompt = "Test prompt: {input}"
        results = evaluator.evaluate(prompt, sample_test_cases)
        
        # Verify API was called
        mock_client.messages.create.assert_called()
        assert results is not None
```

#### Test Coverage

Maintain high test coverage:

```bash
# Run tests with coverage
pytest --cov=evaluations --cov=templates --cov-report=html

# Coverage requirements
# - Unit tests: >90%
# - Integration tests: >80%
# - Overall: >85%
```

### Documentation Standards

#### Code Documentation

```python
def compare_prompts(
    baseline: str, 
    variants: List[str], 
    test_cases: List[Dict],
    statistical_test: str = "chi_square"
) -> ComparisonResult:
    """
    Compare multiple prompt variants with statistical significance testing.
    
    This function performs A/B testing between a baseline prompt and one or
    more variant prompts, using statistical tests to determine significant
    differences in performance.
    
    Args:
        baseline: Path to baseline prompt template
        variants: List of paths to variant prompt templates
        test_cases: Test scenarios for evaluation
        statistical_test: Type of statistical test to use
            Options: "chi_square", "t_test", "mannwhitney"
    
    Returns:
        ComparisonResult object containing:
            - winner: Best performing prompt
            - confidence: Statistical confidence level
            - p_value: Statistical significance value
            - detailed_results: Full evaluation metrics
    
    Raises:
        FileNotFoundError: If prompt files don't exist
        StatisticalError: If statistical test fails
        
    Example:
        >>> results = compare_prompts(
        ...     baseline="templates/base/analysis.md",
        ...     variants=["templates/enhanced/analysis.md"],
        ...     test_cases=load_test_cases("analysis.json")
        ... )
        >>> print(f"Winner: {results.winner}")
        >>> print(f"P-value: {results.p_value:.4f}")
        
    Note:
        Requires minimum sample size of 30 for reliable statistical testing.
        Consider using Bonferroni correction for multiple comparisons.
    """
```

#### API Documentation

Use Sphinx for API documentation:

```python
"""
Evaluation API Reference
========================

The evaluation module provides comprehensive testing and measurement
capabilities for Claude Code prompts.

Classes:
    PromptEvaluator: Main evaluation engine
    PromptComparator: Statistical comparison tool
    MetricCalculator: Individual metric computation

Functions:
    evaluate_prompt(): Single prompt evaluation
    compare_prompts(): Multi-prompt comparison
    batch_evaluate(): Bulk evaluation processing

Examples:
    Basic Usage::
    
        from evaluations import PromptEvaluator
        
        evaluator = PromptEvaluator()
        results = evaluator.evaluate(prompt, test_cases)
        
    Advanced Comparison::
    
        from evaluations import PromptComparator
        
        comparator = PromptComparator()
        comparison = comparator.compare(baseline, variants)
"""
```

## Contributing Areas

### High-Priority Areas

1. **Evaluation Metrics**: New assessment methods and statistical tests
2. **Template System**: Enhanced template generation and validation
3. **Cognee Integration**: Improved AI-powered features
4. **Performance Optimization**: Speed and efficiency improvements
5. **Documentation**: User guides and API references

### Good First Issues

Perfect for new contributors:

- **Documentation Updates**: Fix typos, improve clarity
- **Test Coverage**: Add missing unit tests
- **Example Templates**: Create domain-specific templates
- **Configuration Validation**: Improve error messages
- **Utility Functions**: Small helper functions

### Advanced Contributions

For experienced contributors:

- **New Evaluation Methods**: Statistical algorithms and metrics
- **Machine Learning Integration**: Advanced AI features
- **Performance Optimization**: Algorithmic improvements
- **Architecture Enhancements**: System design improvements
- **Integration Development**: New third-party integrations

## Code Review Process

### Review Checklist

**Functionality**
- [ ] Code works as intended
- [ ] Edge cases are handled
- [ ] Error handling is comprehensive
- [ ] Performance is acceptable

**Code Quality**
- [ ] Follows coding standards
- [ ] Type hints are complete
- [ ] Documentation is clear
- [ ] No code duplication

**Testing**
- [ ] Unit tests are comprehensive
- [ ] Integration tests cover interactions
- [ ] Test coverage meets requirements
- [ ] Tests are maintainable

**Documentation**
- [ ] API documentation is complete
- [ ] User-facing changes are documented
- [ ] Examples are provided
- [ ] README is updated if needed

### Review Process

1. **Self-Review**: Review your own code thoroughly
2. **Automated Checks**: Ensure CI passes
3. **Peer Review**: Request review from team members
4. **Address Feedback**: Respond to review comments
5. **Final Approval**: Obtain approval from maintainers

### Review Standards

```python
# Good: Clear, documented, tested
def calculate_accuracy(predictions: List[bool], actuals: List[bool]) -> float:
    """
    Calculate prediction accuracy.
    
    Args:
        predictions: List of predicted boolean values
        actuals: List of actual boolean values
        
    Returns:
        Accuracy score between 0.0 and 1.0
        
    Raises:
        ValueError: If lists have different lengths
    """
    if len(predictions) != len(actuals):
        raise ValueError("Predictions and actuals must have same length")
    
    if not predictions:
        return 0.0
    
    correct = sum(p == a for p, a in zip(predictions, actuals))
    return correct / len(predictions)

# Bad: Unclear, undocumented, untested
def calc_acc(p, a):
    return sum(x == y for x, y in zip(p, a)) / len(p)
```

## Release Process

### Version Management

We use semantic versioning (SemVer):

```
MAJOR.MINOR.PATCH
1.2.3

MAJOR: Breaking changes
MINOR: New features, backward compatible
PATCH: Bug fixes, backward compatible
```

### Release Workflow

```bash
# 1. Create release branch
git checkout -b release/v1.2.0

# 2. Update version numbers
# Update version in setup.py, __init__.py, etc.

# 3. Update CHANGELOG.md
# Document all changes since last release

# 4. Run full test suite
python -m pytest tests/
python -m pytest tests/integration/

# 5. Build and test package
python setup.py sdist bdist_wheel
twine check dist/*

# 6. Create pull request
# Review and approve release PR

# 7. Merge and tag
git checkout main
git merge release/v1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin main --tags

# 8. Deploy to PyPI
twine upload dist/*
```

### Changelog Format

```markdown
# Changelog

## [1.2.0] - 2024-06-18

### Added
- New cosine similarity evaluation metric
- Cognee-powered template enhancement
- Batch evaluation capabilities
- Performance monitoring dashboard

### Changed
- Improved error handling in evaluation engine
- Updated template hierarchy structure
- Enhanced configuration validation

### Fixed
- Template variable substitution bug
- Memory leak in batch processing
- API timeout handling issues

### Deprecated
- Legacy evaluation methods (use new metrics API)

### Removed
- Unused utility functions
- Deprecated configuration options

### Security
- Updated dependencies to fix vulnerabilities
```

## Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment:

1. **Be Respectful**: Treat all contributors with respect
2. **Be Collaborative**: Work together constructively
3. **Be Inclusive**: Welcome diverse perspectives
4. **Be Professional**: Maintain professional standards
5. **Be Helpful**: Support new contributors

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community discussion
- **Slack**: Real-time chat (invite-only)
- **Email**: Direct contact with maintainers

### Recognition

We recognize contributions through:

- **Contributor Credits**: Listed in README and releases
- **Contributor Badges**: GitHub profile recognition
- **Community Spotlight**: Featured contributions
- **Maintainer Opportunities**: Path to core team membership

## Getting Help

### Resources

- **Documentation**: Comprehensive guides and references
- **Examples**: Real-world usage patterns
- **Tests**: Working code examples
- **Issues**: Search existing problems and solutions

### Asking Questions

When asking for help:

1. **Search First**: Check existing issues and documentation
2. **Provide Context**: Include relevant code and error messages
3. **Be Specific**: Clearly describe the problem
4. **Share Environment**: Include Python version, OS, etc.
5. **Follow Up**: Update when issue is resolved

### Mentorship

New contributors can get mentorship:

- **Pair Programming**: Work with experienced contributors
- **Code Reviews**: Learning through feedback
- **Office Hours**: Regular Q&A sessions
- **Mentoring Program**: One-on-one guidance

## License and Legal

### License

Voyager-4 is licensed under the MIT License. By contributing, you agree that your contributions will be licensed under the same license.

### Contributor License Agreement

All contributors must agree to the Contributor License Agreement (CLA) before their contributions can be merged.

### Copyright

- **Individual Contributions**: Copyright remains with the contributor
- **Significant Contributions**: May require copyright assignment
- **Company Contributions**: Require corporate CLA

---

**Ready to contribute?** Start by exploring our [Good First Issues](https://github.com/yourusername/voyager-4/labels/good%20first%20issue) or join our community discussions.

*Questions about contributing? Check our [FAQ](../faq.md) or reach out to the maintainers.*