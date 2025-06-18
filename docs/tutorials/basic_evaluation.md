# Basic Evaluation Tutorial

This tutorial walks you through your first prompt evaluation with Voyager-4, covering the fundamentals of testing Claude Code prompts with statistical validation.

## Learning Objectives

By the end of this tutorial, you will:

1. Understand the evaluation workflow
2. Run your first prompt evaluation
3. Interpret evaluation results
4. Create basic test cases
5. Use different evaluation metrics

## Prerequisites

- Voyager-4 installed and configured ([Installation Guide](../user_guide/installation.md))
- Basic familiarity with Claude Code
- Text editor or IDE

## Tutorial Overview

**Time Required**: 15-20 minutes  
**Difficulty**: Beginner  
**What We'll Build**: A complete evaluation of a codebase analysis prompt

## Step 1: Understanding Evaluation Basics

### What is Prompt Evaluation?

Prompt evaluation measures how well a Claude Code prompt performs against defined criteria. Voyager-4 uses four evaluation methods:

1. **Exact Match**: Binary accuracy for categorical outputs
2. **Cosine Similarity**: Semantic consistency across similar inputs
3. **LLM Grade**: Quality assessment using Claude as a judge
4. **ROUGE Score**: Text overlap analysis

### Why Evaluate Prompts?

- **Reliability**: Ensure consistent performance across different inputs
- **Quality Assurance**: Meet minimum standards before deployment
- **Optimization**: Compare variants to find the best approach
- **Confidence**: Statistical validation for decision-making

## Step 2: Prepare Your First Evaluation

### Create a Simple Prompt

Let's start with a basic codebase analysis prompt:

```bash
# Create a new prompt file
mkdir -p my-templates
cat > my-templates/simple-analysis.md << 'EOF'
# Task: Simple Codebase Analysis

## Objective
Analyze the provided code and identify the primary programming language and main functionality.

## Instructions
1. Examine the code structure and syntax
2. Identify the programming language
3. Describe the main functionality in one sentence
4. List any obvious issues or improvements

## Output Format
- **Language**: [Programming language]
- **Functionality**: [One sentence description]
- **Issues**: [List of issues, or "None identified"]

## Code to Analyze
{CODE_CONTENT}
EOF
```

### Create Test Cases

Now create test cases to evaluate the prompt:

```bash
# Create test cases directory
mkdir -p my-test_cases

# Create test cases file
cat > my-test_cases/simple-analysis.json << 'EOF'
{
  "test_cases": [
    {
      "id": "python_hello_world",
      "input": "print('Hello, World!')",
      "expected_output": {
        "language": "Python",
        "functionality": "Prints a greeting message to the console",
        "issues": "None identified"
      },
      "context": {
        "difficulty": "basic",
        "category": "simple_script"
      }
    },
    {
      "id": "javascript_function",
      "input": "function calculateSum(a, b) {\n  return a + b;\n}\n\nconsole.log(calculateSum(5, 3));",
      "expected_output": {
        "language": "JavaScript",
        "functionality": "Defines a function to calculate sum of two numbers and demonstrates its usage",
        "issues": "None identified"
      },
      "context": {
        "difficulty": "basic",
        "category": "function_definition"
      }
    },
    {
      "id": "java_class",
      "input": "public class Calculator {\n    public int add(int a, int b) {\n        return a + b;\n    }\n}",
      "expected_output": {
        "language": "Java",
        "functionality": "Defines a Calculator class with an add method for integer addition",
        "issues": "None identified"
      },
      "context": {
        "difficulty": "intermediate",
        "category": "class_definition"
      }
    },
    {
      "id": "python_with_issues",
      "input": "import os\npassword = 'hardcoded123'\nprint(password)",
      "expected_output": {
        "language": "Python",
        "functionality": "Imports os module and prints a hardcoded password",
        "issues": "Hardcoded password is a security vulnerability"
      },
      "context": {
        "difficulty": "basic",
        "category": "security_issue"
      }
    },
    {
      "id": "complex_python",
      "input": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\nprint([fibonacci(i) for i in range(10)])",
      "expected_output": {
        "language": "Python",
        "functionality": "Implements recursive Fibonacci sequence generator and prints first 10 numbers",
        "issues": "Inefficient recursive implementation without memoization"
      },
      "context": {
        "difficulty": "intermediate",
        "category": "algorithm"
      }
    }
  ]
}
EOF
```

## Step 3: Run Your First Evaluation

### Basic Evaluation

```bash
# Run the evaluation
python evaluations/scripts/evaluate_prompt.py \
  --prompt my-templates/simple-analysis.md \
  --test_cases my-test_cases/simple-analysis.json \
  --output-dir results/my-first-evaluation

# This will take 1-2 minutes to complete
```

**What happens during evaluation:**

1. **Template Loading**: Voyager-4 loads your prompt template
2. **Test Case Processing**: Each test case is processed individually
3. **Claude API Calls**: Your prompt is sent to Claude with each test input
4. **Response Collection**: Claude's responses are collected and stored
5. **Metric Calculation**: Multiple evaluation methods assess the responses
6. **Report Generation**: Results are compiled into comprehensive reports

### Check the Results

```bash
# List generated files
ls results/my-first-evaluation/

# View the summary report
cat results/my-first-evaluation/evaluation_summary.md
```

**Expected output structure:**
```
results/my-first-evaluation/
├── evaluation_results.json      # Raw evaluation data
├── evaluation_summary.md        # Human-readable report
├── detailed_analysis.json       # Per-test-case breakdown
├── metrics_breakdown.csv        # Metrics in tabular format
└── visualization.html           # Interactive charts (if enabled)
```

## Step 4: Interpret Your Results

### Understanding the Summary Report

Your `evaluation_summary.md` will look like this:

```markdown
# Evaluation Summary

## Overview
- **Prompt File**: my-templates/simple-analysis.md
- **Test Cases**: 5
- **Execution Time**: 1.2 minutes
- **Evaluation ID**: eval_20240618_143022

## Performance Metrics

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| Accuracy | 85.4% | >85% | ✅ PASS |
| Consistency | 0.82 | >0.8 | ✅ PASS |
| Quality | 4.1/5 | >4.0 | ✅ PASS |
| ROUGE-L | 0.73 | >0.6 | ✅ PASS |

## Recommendations
✅ Prompt meets all quality thresholds
🎯 Ready for production use
💡 Consider adding more examples for edge cases
```

### Metric Explanations

**Accuracy (85.4%)**
- Measures how often Claude correctly identifies the language and functionality
- Based on exact or near-exact matches with expected outputs
- 85.4% means 4-5 out of 5 test cases were answered correctly

**Consistency (0.82)**
- Measures semantic similarity between responses to similar inputs
- Uses cosine similarity on sentence embeddings
- 0.82 indicates high consistency in response style and content

**Quality (4.1/5)**
- Claude grades the responses based on accuracy, completeness, and clarity
- Uses a rubric to assess response quality objectively
- 4.1/5 indicates good quality responses

**ROUGE-L (0.73)**
- Measures text overlap between actual and expected responses
- Based on longest common subsequences
- 0.73 indicates good alignment with expected content

### Detailed Analysis

Check the detailed breakdown:

```bash
# View detailed results
python -c "
import json
with open('results/my-first-evaluation/detailed_analysis.json', 'r') as f:
    data = json.load(f)

for test_case in data['test_cases']:
    print(f'Test: {test_case[\"id\"]}')
    print(f'Expected: {test_case[\"expected_language\"]}')
    print(f'Actual: {test_case[\"actual_language\"]}')
    print(f'Match: {\"✅\" if test_case[\"language_match\"] else \"❌\"}')
    print(f'Quality Score: {test_case[\"quality_score\"]}/5')
    print('---')
"
```

## Step 5: Improve Your Prompt

### Analyze Failures

If any test cases failed, examine why:

```bash
# Check for failures
python -c "
import json
with open('results/my-first-evaluation/detailed_analysis.json', 'r') as f:
    data = json.load(f)

failures = [tc for tc in data['test_cases'] if not tc.get('overall_success', True)]
if failures:
    print(f'Found {len(failures)} failures:')
    for failure in failures:
        print(f'- {failure[\"id\"]}: {failure.get(\"failure_reason\", \"Unknown\")}')
else:
    print('No failures found!')
"
```

### Common Issues and Solutions

**Language Identification Failures**
```bash
# If Claude misidentified languages, add more specific instructions
cat >> my-templates/simple-analysis-v2.md << 'EOF'
# Task: Simple Codebase Analysis

## Objective
Analyze the provided code and identify the primary programming language and main functionality.

## Instructions
1. Examine the code structure and syntax carefully
2. Look for language-specific keywords and syntax patterns
   - Python: def, print(), indentation-based blocks
   - JavaScript: function, console.log(), curly braces
   - Java: public class, System.out.print(), typed variables
3. Identify the programming language with confidence
4. Describe the main functionality in one sentence
5. List any obvious issues or improvements

## Output Format
- **Language**: [Programming language]
- **Functionality**: [One sentence description]
- **Issues**: [List of issues, or "None identified"]

## Code to Analyze
{CODE_CONTENT}
EOF
```

**Inconsistent Output Format**
```bash
# Add examples to show the desired format
cat >> my-templates/simple-analysis-v2.md << 'EOF'

## Example
**Input**: `print("Hello")`
**Output**:
- **Language**: Python
- **Functionality**: Prints a greeting message to the console
- **Issues**: None identified
EOF
```

### Test Your Improvements

```bash
# Evaluate the improved prompt
python evaluations/scripts/evaluate_prompt.py \
  --prompt my-templates/simple-analysis-v2.md \
  --test_cases my-test_cases/simple-analysis.json \
  --output-dir results/improved-evaluation

# Compare with original
python evaluations/scripts/compare_prompts.py \
  --baseline my-templates/simple-analysis.md \
  --variant my-templates/simple-analysis-v2.md \
  --test_cases my-test_cases/simple-analysis.json \
  --output-dir results/comparison
```

## Step 6: Advanced Evaluation Options

### Use Specific Metrics

```bash
# Evaluate with only accuracy and quality metrics
python evaluations/scripts/evaluate_prompt.py \
  --prompt my-templates/simple-analysis.md \
  --test_cases my-test_cases/simple-analysis.json \
  --methods exact_match llm_grade \
  --output-dir results/custom-metrics
```

### Custom Configuration

Create a custom configuration file:

```bash
cat > my-config.yaml << 'EOF'
evaluation:
  model: "claude-3-haiku-20240307"  # Faster, cheaper model
  temperature: 0.0                  # More deterministic
  timeout: 60                       # Shorter timeout
  
  methods:
    - exact_match
    - llm_grade
  
  thresholds:
    accuracy: 0.80                  # Lower threshold for testing
    quality: 3.5
    
  statistical:
    confidence_level: 0.90          # Lower confidence for faster testing
EOF

# Use custom configuration
python evaluations/scripts/evaluate_prompt.py \
  --prompt my-templates/simple-analysis.md \
  --test_cases my-test_cases/simple-analysis.json \
  --config my-config.yaml \
  --output-dir results/custom-config
```

### Batch Evaluation

Evaluate multiple prompts at once:

```bash
# Create multiple prompt variants
cp my-templates/simple-analysis.md my-templates/variant-1.md
cp my-templates/simple-analysis.md my-templates/variant-2.md

# Edit variants with different approaches...

# Batch evaluate
python evaluations/scripts/batch_evaluate.py \
  --prompt-dir my-templates/ \
  --test_cases my-test_cases/simple-analysis.json \
  --output-dir results/batch-evaluation
```

## Step 7: Understand What Makes a Good Evaluation

### Quality Test Cases

**Characteristics of good test cases:**

1. **Representative**: Cover real-world scenarios you'll encounter
2. **Diverse**: Include different languages, complexity levels, and edge cases
3. **Clear**: Have unambiguous expected outputs
4. **Comprehensive**: Test both normal and edge cases

**Example of a comprehensive test case:**

```json
{
  "id": "edge_case_mixed_languages",
  "input": "<!DOCTYPE html>\n<html>\n<script>\nfunction greet() {\n  alert('Hello!');\n}\n</script>\n</html>",
  "expected_output": {
    "language": "HTML with JavaScript",
    "functionality": "HTML document with embedded JavaScript function for displaying alert",
    "issues": "Inline JavaScript reduces maintainability"
  },
  "context": {
    "difficulty": "intermediate",
    "category": "mixed_languages",
    "edge_case": true
  }
}
```

### Effective Prompts

**Characteristics of evaluable prompts:**

1. **Clear Instructions**: Unambiguous task description
2. **Consistent Format**: Structured output that can be parsed
3. **Appropriate Scope**: Not too broad or too narrow
4. **Context-Aware**: Include relevant background information

### Meaningful Metrics

**Choose metrics that align with your goals:**

- **Exact Match**: For tasks with clear right/wrong answers
- **Cosine Similarity**: For consistency across similar inputs
- **LLM Grade**: For subjective quality assessment
- **ROUGE Score**: For content similarity and completeness

## Common Troubleshooting

### Issue: Low Accuracy Scores

**Symptoms**: Accuracy below expected threshold
**Solutions**:
1. Review failed test cases for patterns
2. Clarify instructions in the prompt
3. Add examples of correct outputs
4. Adjust expected outputs in test cases

### Issue: Inconsistent Results

**Symptoms**: High variance in cosine similarity scores
**Solutions**:
1. Make instructions more specific
2. Reduce temperature for more deterministic outputs
3. Add constraints to limit response variation
4. Review test cases for clarity

### Issue: API Timeouts

**Symptoms**: Evaluation fails with timeout errors
**Solutions**:
1. Increase timeout in configuration
2. Simplify the prompt to reduce processing time
3. Use a faster model (Claude Haiku instead of Opus)
4. Reduce the number of test cases for initial testing

## Next Steps

Congratulations! You've completed your first prompt evaluation. Here's what to explore next:

1. **Advanced Evaluation**: Try our [Advanced Evaluation Tutorial](advanced_evaluation.md)
2. **Template Creation**: Learn [Template Creation](template_creation.md)
3. **A/B Testing**: Compare multiple prompt variants
4. **AI Enhancement**: Explore [Cognee Integration](cognee_enhancement.md)

### Recommended Practice

1. **Start Simple**: Begin with basic prompts and gradually add complexity
2. **Iterate Frequently**: Run evaluations often during development
3. **Document Learnings**: Keep notes on what works and what doesn't
4. **Build Test Libraries**: Create reusable test cases for different domains

---

**Congratulations!** You've successfully run your first prompt evaluation and understand the basics of the Voyager-4 evaluation system.

*Ready for more advanced techniques? Check out our [Advanced Evaluation Tutorial](advanced_evaluation.md) or explore [Template Creation](template_creation.md).*