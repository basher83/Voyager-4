# Cognee Framework

## AI-Powered Prompt Development and Evaluation System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The Cognee Framework is a systematic approach to building, testing, and optimizing Claude Code prompts using AI knowledge graphs and advanced evaluation techniques. Built on Anthropic's official documentation and best practices, it provides a comprehensive toolkit for prompt engineering at scale.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/cognee-framework.git
cd cognee-framework

# Set up the environment
python3 setup.py

# Install dependencies
pip install -r requirements.txt

# Alternative: Install as package
pip install -e .
```

### Basic Usage

```bash
# Basic prompt evaluation
./scripts/evaluate --prompt templates/basic/codebase-overview-template.md \
                   --test_cases test_cases/examples/codebase_understanding_examples.json

# Enhanced evaluation with Cognee knowledge graphs
./scripts/evaluate --prompt templates/cognee_powered/architecture-aware/template.md \
                   --test_cases test_cases/examples/codebase_understanding_examples.json \
                   --enhanced

# Compare prompt variants
./scripts/compare --baseline templates/basic/ \
                  --variant templates/cognee_powered/ \
                  --test_cases test_cases/examples/codebase_understanding_examples.json
```

## 🏗️ Architecture

### Core Components

```
cognee_framework/
├── core/              # Base classes and abstractions
├── evaluation/        # Evaluation engines and metrics
├── templates/         # Template management system
├── utils/             # Common utilities and helpers
└── mcp_integration/   # MCP server integration
```

### Directory Structure

```
├── cognee_framework/     # Main framework package
├── templates/           # Hierarchical template system
│   ├── basic/          # Clear, direct instructions
│   ├── enhanced/       # + Examples (few-shot prompting)
│   ├── advanced/       # + Chain of thought reasoning
│   ├── specialized/    # + Custom system prompts
│   └── cognee_powered/ # AI-enhanced with knowledge graphs
├── evaluations/         # Evaluation configurations and results
├── test_cases/         # Test scenarios and examples
├── scripts/            # CLI utilities and tools
├── examples/           # Demonstrations and tutorials
├── tests/              # Test suite (unit + integration)
├── docs/               # Comprehensive documentation
└── data/               # Runtime data and knowledge graphs
```

## 🎯 Key Features

### Progressive Template Enhancement
- **Basic**: Clear, direct instructions (starting point)
- **Enhanced**: + Examples (few-shot prompting)
- **Advanced**: + Chain of thought reasoning
- **Specialized**: + Custom system prompts
- **Cognee-Powered**: + AI knowledge graph integration

### Multi-Method Evaluation
- Exact match accuracy
- Semantic similarity (cosine similarity)
- LLM-based quality grading
- ROUGE scores for text generation
- Statistical significance testing

### AI-Enhanced Capabilities
- Knowledge graph-powered context injection
- Intelligent template generation
- Relationship-aware prompt optimization
- Historical evaluation learning

## 📊 Evaluation Framework

The framework provides comprehensive evaluation capabilities with multiple metrics:

```python
from cognee_framework.evaluation import CogneeEnhancedEvaluator

# Initialize with knowledge graph enhancement
evaluator = CogneeEnhancedEvaluator(config_path="evaluations/config/default_config.yaml")

# Run evaluation with AI-powered insights
results = evaluator.evaluate_with_knowledge(
    prompt_path="templates/cognee_powered/architecture-aware/template.md",
    test_cases_path="test_cases/examples/codebase_understanding_examples.json"
)
```

### Evaluation Metrics

- **Accuracy**: Exact match and threshold-based scoring
- **Consistency**: Cross-validation and response stability
- **Quality**: LLM-based subjective evaluation
- **Efficiency**: Token usage and response time
- **Semantic Similarity**: Vector-based content comparison

## 🧠 Cognee Integration

### Knowledge Graph Features

The framework integrates with Cognee to provide AI-powered enhancements:

```python
from cognee_framework.mcp_integration import MCPCogneeClient

# Connect to Cognee knowledge graph
client = MCPCogneeClient()

# Ingest knowledge for enhanced prompts
client.cognify("Your codebase and documentation")

# Search for relevant context
context = client.search("How to implement error handling?", "GRAPH_COMPLETION")

# Generate enhanced templates
template = client.generate_template(
    task="code_generation",
    context=context,
    template_type="architecture-aware"
)
```

### Available Template Types

- **Architecture-Aware**: Uses code structure knowledge
- **Context-Enriched**: Injects relevant context from knowledge graph
- **Relationship-Informed**: Leverages entity relationships
- **Pattern-Adaptive**: Adapts based on recognized patterns
- **Dynamic-Enhanced**: Real-time optimization based on performance

## 🔧 Configuration

### Environment Setup

Create a `.env` file with your API keys:

```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional Cognee settings
COGNEE_LLM_PROVIDER=anthropic
COGNEE_DEFAULT_MODEL=claude-3-haiku-20240307
COGNEE_REASONING_MODEL=claude-3-opus-20240229
```

### Evaluation Configuration

Configure evaluation parameters in `evaluations/config/default_config.yaml`:

```yaml
model: "claude-3-opus-20240229"
max_tokens: 2048
temperature: 0.0
evaluation_methods:
  - "exact_match"
  - "consistency"
  - "quality"
metrics:
  accuracy_threshold: 0.85
  consistency_threshold: 0.8
  quality_threshold: 4.0
```

## 📚 Documentation

- [**Architecture Guide**](docs/architecture/) - System design and components
- [**Evaluation Guide**](docs/best-practices/evaluation-guide.md) - Testing methodologies
- [**Prompt Engineering Guide**](docs/best-practices/prompt-engineering-guide.md) - Best practices
- [**Cognee Integration Guide**](docs/guides/cognee-integration-guide.md) - AI enhancement setup
- [**API Reference**](docs/api/) - Complete API documentation

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/unit_tests/

# Run integration tests
python -m pytest tests/integration_tests/

# Run all tests with coverage
python -m pytest tests/ --cov=cognee_framework --cov-report=html
```

## 🚀 Development

### Setting up Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install

# Format code
black cognee_framework/
flake8 cognee_framework/
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `pytest tests/`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on [Anthropic's Claude Code](https://claude.ai/code) platform
- Powered by [Cognee](https://github.com/topoteretes/cognee) knowledge graphs
- Inspired by Anthropic's prompt engineering documentation
- Follows best practices from the AI safety research community

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Examples**: [examples/](examples/)
- **Issues**: [GitHub Issues](https://github.com/your-username/cognee-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/cognee-framework/discussions)

---

**Built with ❤️ for the Claude Code community**