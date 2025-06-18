# Installation Guide

This guide walks you through setting up Voyager-4, the Claude Code Prompt Development Framework, on your local machine.

## Prerequisites

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: macOS, Linux, or Windows with WSL2
- **Memory**: Minimum 8GB RAM (16GB recommended for Cognee features)
- **Storage**: At least 2GB free space for dependencies and data
- **Internet**: Required for Claude API access and package installation

### Required Accounts

1. **Claude Code Access**: Active Claude Code subscription
2. **Anthropic API**: API key for Claude access (if using direct API)

### Development Tools (Optional)

- **Git**: For version control and collaboration
- **VS Code**: Recommended IDE with Claude Code extension
- **Docker**: For containerized development (optional)

## Installation Methods

### Method 1: Quick Setup (Recommended)

The fastest way to get started with Voyager-4:

```bash
# Clone the repository
git clone https://github.com/yourusername/voyager-4.git
cd voyager-4

# Run automated setup
python3 setup.py

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import anthropic; import cognee; print('Installation successful!')"
```

### Method 2: Manual Setup

For more control over the installation process:

```bash
# Clone the repository
git clone https://github.com/yourusername/voyager-4.git
cd voyager-4

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install base dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install optional dependencies
pip install jupyter black flake8  # Development tools
pip install plotly seaborn        # Advanced visualization
```

### Method 3: Docker Setup

For containerized development:

```bash
# Clone the repository
git clone https://github.com/yourusername/voyager-4.git
cd voyager-4

# Build Docker image
docker build -t voyager-4 .

# Run container
docker run -it --name voyager-4-dev \
  -v $(pwd):/workspace \
  -p 8888:8888 \
  voyager-4
```

## Configuration

### 1. Environment Variables

Create a `.env` file in the project root:

```bash
# Copy template
cp .env.template .env

# Edit with your credentials
nano .env
```

Required environment variables:

```env
# Claude API Configuration
ANTHROPIC_API_KEY=your_api_key_here
CLAUDE_CODE_SDK_KEY=your_sdk_key_here

# Cognee Configuration (optional)
COGNEE_API_URL=https://api.cognee.ai
COGNEE_API_KEY=your_cognee_key_here

# Evaluation Configuration
DEFAULT_MODEL=claude-3-sonnet-20240229
EVALUATION_TIMEOUT=120
MAX_CONCURRENT_REQUESTS=5

# Storage Configuration
DATA_DIR=./data
RESULTS_DIR=./evaluations/results
CACHE_DIR=./data/cache
```

### 2. Configuration Files

Update the main configuration file:

```bash
# Edit evaluation configuration
nano evaluations/config/default_config.yaml
```

Example configuration:

```yaml
# evaluations/config/default_config.yaml
evaluation:
  # Model settings
  model: "claude-3-sonnet-20240229"
  temperature: 0.1
  max_tokens: 4000
  timeout: 120

  # Evaluation metrics
  metrics:
    - exact_match
    - cosine_similarity
    - llm_grade
    - rouge_score
  
  # Quality thresholds
  thresholds:
    accuracy: 0.85
    consistency: 0.8
    quality: 4.0

  # Statistical testing
  statistical:
    confidence_level: 0.95
    min_sample_size: 30
    significance_threshold: 0.05

# Cognee integration
cognee:
  enabled: true
  cache_enabled: true
  graph_model: "KnowledgeGraph"
  
# Logging
logging:
  level: "INFO"
  file: "voyager4.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## Verification

### Basic Functionality Test

Run the built-in verification script:

```bash
# Test basic functionality
python -m evaluations.scripts.test_installation

# Expected output:
# ✅ Python version: 3.x.x
# ✅ Dependencies installed
# ✅ Claude API connection
# ✅ Cognee integration
# ✅ Evaluation framework
# ✅ Template system
# Installation verification complete!
```

### Manual Testing

Test individual components:

```bash
# Test Claude API connection
python -c "
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model='claude-3-haiku-20240307',
    max_tokens=10,
    messages=[{'role': 'user', 'content': 'Hello'}]
)
print('Claude API: ✅')
"

# Test Cognee integration
python -c "
import cognee
print('Cognee: ✅')
"

# Test evaluation framework
python evaluations/scripts/evaluate_prompt.py --help
```

### Run Example Evaluation

Test with a sample prompt:

```bash
# Run basic evaluation
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/base/codebase-overview-template.md \
  --test_cases test_cases/examples/codebase_understanding_examples.json \
  --output-dir evaluations/results/test

# Check results
ls evaluations/results/test/
```

## Troubleshooting

### Common Issues

**1. API Key Issues**

```bash
# Error: AuthenticationError
# Solution: Check your API key configuration
echo $ANTHROPIC_API_KEY  # Should not be empty
```

**2. Import Errors**

```bash
# Error: ModuleNotFoundError
# Solution: Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**3. Permission Issues**

```bash
# Error: Permission denied
# Solution: Check file permissions
chmod +x setup.py
chmod -R 755 evaluations/scripts/
```

**4. Cognee Connection Issues**

```bash
# Error: Cognee API connection failed
# Solution: Check Cognee configuration
python -c "
from evaluations.scripts.test_cognee_integration import test_connection
test_connection()
"
```

### Getting Help

If you encounter issues:

1. **Check the logs**: `tail -f voyager4.log`
2. **Review configuration**: Ensure all required variables are set
3. **Test connectivity**: Verify API access and internet connection
4. **Update dependencies**: `pip install --upgrade -r requirements.txt`
5. **Reset environment**: Remove `venv/` and start fresh

### Advanced Configuration

**Custom Models**

```yaml
# Add custom model configurations
models:
  claude-3-opus:
    model_name: "claude-3-opus-20240229"
    max_tokens: 4000
    temperature: 0.1
  
  claude-3-haiku:
    model_name: "claude-3-haiku-20240307"
    max_tokens: 2000
    temperature: 0.0
```

**Performance Tuning**

```yaml
# Optimize for your hardware
performance:
  max_concurrent_requests: 5    # Adjust based on API limits
  request_timeout: 120          # Increase for complex prompts
  cache_size: 1000             # Memory usage vs. speed
  batch_size: 10               # Evaluation batch processing
```

## Next Steps

After successful installation:

1. **Quick Start**: Follow the [Quick Start Guide](quick_start.md)
2. **Learn Templates**: Explore the [Template System](template_system.md)
3. **Run Evaluations**: Try the [Evaluation System](evaluation_system.md)
4. **AI Enhancement**: Enable [Cognee Integration](cognee_integration.md)

## Development Setup

For contributors, see the [Development Setup Guide](../developer_guide/development_setup.md) for additional configuration including:

- Pre-commit hooks
- Testing framework setup
- Documentation generation
- Code formatting tools

---

**Installation complete!** You're ready to start optimizing your Claude Code prompts with Voyager-4.

*Need help? Check our [Troubleshooting Guide](troubleshooting.md) or [Common Issues](../developer_guide/troubleshooting.md).*