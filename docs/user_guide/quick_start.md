# Quick Start Guide

Get up and running with Voyager-4 in 5 minutes! This guide walks you through your first prompt evaluation and shows you the core features of the framework.

## Prerequisites

- Voyager-4 installed ([Installation Guide](installation.md))
- Claude API access configured
- Basic familiarity with Claude Code

## Your First Evaluation

### Step 1: Verify Installation

```bash
# Navigate to your Voyager-4 directory
cd voyager-4

# Quick verification
python -c "import anthropic, cognee; print('✅ Ready to go!')"
```

### Step 2: Run a Basic Evaluation

Let's evaluate a simple codebase understanding prompt:

```bash
# Run your first evaluation
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/base/codebase-overview-template.md \
  --test_cases test_cases/examples/codebase_understanding_examples.json \
  --output-dir evaluations/results/quickstart

# This will take 1-2 minutes...
```

**What this does:**
- Tests a basic codebase analysis prompt
- Runs 10 evaluation scenarios
- Measures accuracy, consistency, and quality
- Generates a detailed report

### Step 3: View Results

```bash
# Check the results directory
ls evaluations/results/quickstart/

# View the summary report
cat evaluations/results/quickstart/evaluation_summary.md
```

**Expected output:**
```
📊 Evaluation Summary
====================
Prompt: codebase-overview-template.md
Test Cases: 10
Execution Time: 1.2 minutes

📈 Performance Metrics:
- Accuracy: 89.2% (target: >85%) ✅
- Consistency: 0.87 (target: >0.8) ✅
- Quality Score: 4.2/5 (target: >4.0) ✅
- Average Response Time: 1.4s

🎯 Recommendation: APPROVED for production use
```

## Core Features Overview

### 1. Template System

Voyager-4 uses a hierarchical template system for progressive enhancement:

```bash
# Explore available templates
ls templates/

# View template hierarchy
base/          # Clear, direct instructions
enhanced/      # + Examples (few-shot)
advanced/      # + Chain of thought
structured/    # + XML tags
specialized/   # + Custom system prompts
cognee-powered/ # + AI enhancement
```

**Try different templates:**

```bash
# Compare base vs enhanced template
python evaluations/scripts/compare_prompts.py \
  --baseline templates/base/codebase-overview-template.md \
  --variant templates/enhanced/codebase-overview-template.md \
  --test_cases test_cases/examples/codebase_understanding_examples.json
```

### 2. Evaluation Metrics

Voyager-4 uses 4 evaluation methods:

1. **Exact Match**: For categorical outputs
2. **Cosine Similarity**: For consistency testing
3. **LLM Grading**: For quality assessment
4. **ROUGE Score**: For text overlap analysis

**Customize metrics:**

```bash
# Run evaluation with specific metrics
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/base/codebase-overview-template.md \
  --test_cases test_cases/examples/codebase_understanding_examples.json \
  --metrics accuracy consistency quality \
  --output-dir evaluations/results/custom
```

### 3. AI-Enhanced Templates

Use Cognee for intelligent prompt generation:

```bash
# Generate AI-enhanced prompts
python evaluations/scripts/cognee_intelligent_prompts_demo.py
```

**What this creates:**
- Analyzes your codebase structure
- Generates context-aware prompts
- Incorporates architectural insights
- Optimizes for your specific use case

## Common Use Cases

### Use Case 1: Codebase Understanding

```bash
# Evaluate architecture analysis prompts
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/advanced/architecture-analysis-template.md \
  --test_cases test_cases/examples/architecture_examples.json
```

### Use Case 2: Bug Fixing

```bash
# Test bug diagnosis capabilities
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/structured/bug-diagnosis-template.md \
  --test_cases test_cases/examples/bug_fixing_examples.json
```

### Use Case 3: Code Generation

```bash
# Evaluate code generation prompts
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/specialized/code-generation-template.md \
  --test_cases test_cases/examples/code_generation_examples.json
```

## Next Steps: 5-Minute Workflow

### 1. Create Your Own Template (2 minutes)

```bash
# Copy a base template
cp templates/base/codebase-overview-template.md templates/base/my-custom-template.md

# Edit for your specific use case
nano templates/base/my-custom-template.md
```

**Template customization tips:**
- Add specific context for your domain
- Include examples relevant to your codebase
- Define clear success criteria
- Use consistent formatting

### 2. Create Test Cases (2 minutes)

```bash
# Copy example test cases
cp test_cases/examples/codebase_understanding_examples.json test_cases/examples/my-test_cases.json

# Edit with your scenarios
nano test_cases/examples/my-test_cases.json
```

**Test case structure:**
```json
{
  "test_cases": [
    {
      "id": "test_1",
      "input": "Your test input",
      "expected_output": "Expected result",
      "context": "Additional context",
      "category": "test_category"
    }
  ]
}
```

### 3. Run Evaluation (1 minute)

```bash
# Test your custom template
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/base/my-custom-template.md \
  --test_cases test_cases/examples/my-test_cases.json \
  --output-dir evaluations/results/my-evaluation
```

## Advanced Features Preview

### A/B Testing

Compare multiple prompt variants:

```bash
# Statistical comparison
python evaluations/scripts/compare_prompts.py \
  --baseline templates/base/ \
  --variants templates/enhanced/ templates/advanced/ \
  --test_cases test_cases/examples/ \
  --output-dir evaluations/results/ab-test
```

### Batch Processing

Evaluate multiple prompts simultaneously:

```bash
# Batch evaluation
python evaluations/scripts/batch_evaluate.py \
  --prompt-dir templates/base/ \
  --test_cases test_cases/examples/ \
  --output-dir evaluations/results/batch
```

### Performance Monitoring

Track prompt performance over time:

```bash
# Generate performance dashboard
python evaluations/scripts/generate_dashboard.py \
  --results-dir evaluations/results/ \
  --output dashboard.html
```

## Configuration Quick Reference

### Essential Settings

Edit `evaluations/config/default_config.yaml`:

```yaml
# Quick configuration for getting started
evaluation:
  model: "claude-3-sonnet-20240229"
  temperature: 0.1
  max_tokens: 4000
  
  metrics: ["accuracy", "consistency", "quality"]
  
  thresholds:
    accuracy: 0.85
    consistency: 0.8
    quality: 4.0

# Enable AI features
cognee:
  enabled: true
  cache_enabled: true
```

### Environment Variables

Ensure these are set in your `.env` file:

```env
ANTHROPIC_API_KEY=your_key_here
CLAUDE_CODE_SDK_KEY=your_sdk_key_here
DEFAULT_MODEL=claude-3-sonnet-20240229
```

## Troubleshooting Quick Fixes

### Common Issues

**"Import Error"**
```bash
# Activate virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

**"API Key Error"**
```bash
# Check environment variables
echo $ANTHROPIC_API_KEY
# Should not be empty
```

**"No test results"**
```bash
# Check file paths
ls templates/base/codebase-overview-template.md
ls test_cases/examples/codebase_understanding_examples.json
```

## What's Next?

Now that you've completed the quick start:

1. **Deep Dive into Templates**: [Template System Guide](template_system.md)
2. **Learn Evaluation Methods**: [Evaluation System Guide](evaluation_system.md)
3. **Enable AI Features**: [Cognee Integration Guide](cognee_integration.md)
4. **Advanced Techniques**: [Best Practices](../best-practices/evaluation-guide.md)

## Example Workflow Summary

Here's what you just accomplished:

1. ✅ **Verified installation** - Confirmed all components work
2. ✅ **Ran first evaluation** - Tested a template with real metrics
3. ✅ **Viewed results** - Understood performance indicators
4. ✅ **Explored features** - Saw template hierarchy and AI enhancement
5. ✅ **Created custom content** - Built your own template and test cases

**Time invested**: 5 minutes  
**Knowledge gained**: Core framework capabilities  
**Next milestone**: Production-ready prompt optimization

---

**Congratulations!** You've successfully completed the Voyager-4 quick start. You now have a working prompt evaluation system and understand the core workflow.

*Ready for more advanced features? Check out our [Tutorial Series](../tutorials/) or dive into [Template Creation](../tutorials/template_creation.md).*