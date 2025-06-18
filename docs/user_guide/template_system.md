# Template System Guide

The Voyager-4 template system provides a hierarchical approach to prompt engineering, following Anthropic's best practices for progressive enhancement. This guide explains how to use, customize, and create effective prompt templates.

## Template Hierarchy

### Progressive Enhancement Philosophy

Templates are organized by sophistication level, from most broadly effective to more specialized:

```
templates/
├── base/           # Level 1: Clear and Direct
├── enhanced/       # Level 2: + Examples (Multishot)
├── advanced/       # Level 3: + Chain of Thought
├── structured/     # Level 4: + XML Tags
├── specialized/    # Level 5: + Custom System Prompts
└── cognee-powered/ # Level 6: + AI Enhancement
```

Each level builds upon the previous, incorporating proven techniques for specific use cases.

## Template Levels Explained

### Level 1: Base Templates

**Principle**: Be clear, contextual, and specific.

**Characteristics:**
- Direct instructions without ambiguity
- Explicit context and desired outcomes
- Sequential steps when needed
- Clear success criteria

**Example Structure:**
```markdown
# Task: Codebase Overview Analysis

## Objective
Analyze the provided codebase and generate a comprehensive overview including architecture, key components, and technology stack.

## Instructions
1. Examine the codebase structure and organization
2. Identify the main architectural patterns
3. List key components and their relationships
4. Document the technology stack and dependencies
5. Provide a summary of the overall design approach

## Output Format
- **Architecture Pattern**: [pattern name and description]
- **Key Components**: [list with brief descriptions]
- **Technology Stack**: [languages, frameworks, tools]
- **Design Summary**: [2-3 sentence overview]

## Context
{CODEBASE_CONTEXT}

## Codebase to Analyze
{CODEBASE_CONTENT}
```

**When to use:**
- Simple, well-defined tasks
- Quick iterations and testing
- Clear input-output relationships
- First version of any prompt

### Level 2: Enhanced Templates

**Principle**: Add examples to demonstrate desired behavior.

**Characteristics:**
- 2-5 examples showing input-output relationships
- Diverse examples covering edge cases
- Consistent example format
- Clear pattern demonstration

**Example Enhancement:**
```markdown
# Task: Codebase Overview Analysis

[Base instructions remain the same]

## Examples

### Example 1: React Web Application
**Input**: React app with Redux state management
**Output**:
- **Architecture Pattern**: Component-based architecture with unidirectional data flow
- **Key Components**: App container, feature modules, Redux store, API services
- **Technology Stack**: React 18, Redux Toolkit, TypeScript, Webpack
- **Design Summary**: Modern React application following Redux patterns with TypeScript for type safety and modular component organization.

### Example 2: Python API Service
**Input**: Flask REST API with database integration
**Output**:
- **Architecture Pattern**: RESTful API with layered architecture
- **Key Components**: Flask app, database models, API routes, authentication middleware
- **Technology Stack**: Python 3.9, Flask, SQLAlchemy, PostgreSQL
- **Design Summary**: Clean Flask API following REST principles with proper separation of concerns and database abstraction.

## Your Task
{CODEBASE_CONTEXT}
{CODEBASE_CONTENT}
```

**When to use:**
- Complex output formats
- Demonstrating edge case handling
- Showing style and tone expectations
- Consistent formatting requirements

### Level 3: Advanced Templates

**Principle**: Include chain of thought reasoning.

**Characteristics:**
- Explicit thinking instructions
- Step-by-step reasoning guidance
- Problem decomposition
- Verification steps

**Example Enhancement:**
```markdown
# Task: Codebase Overview Analysis

[Previous instructions remain]

## Reasoning Process

Before providing your analysis, think through the following:

### Step 1: Initial Assessment
- What type of application is this?
- What's the primary purpose and domain?
- What's the overall complexity level?

### Step 2: Structural Analysis
- How is the code organized into directories?
- What are the main entry points?
- How are dependencies managed?

### Step 3: Pattern Recognition
- What architectural patterns are evident?
- Are there consistent naming conventions?
- How is separation of concerns handled?

### Step 4: Technology Identification
- What languages and frameworks are used?
- What version information is available?
- What external dependencies exist?

### Step 5: Synthesis
- How do all components work together?
- What are the key design decisions?
- What does this reveal about the system's purpose?

## Your Analysis

<reasoning>
[Show your thinking process here]
</reasoning>

<analysis>
[Provide your structured analysis]
</analysis>
```

**When to use:**
- Complex analysis tasks
- Multi-step reasoning required
- Debugging and problem-solving
- Architectural decisions

### Level 4: Structured Templates

**Principle**: Use XML tags for maximum clarity.

**Characteristics:**
- Clear input/output sections with XML tags
- Structured data organization
- Reliable output parsing
- Reduced ambiguity

**Example Structure:**
```markdown
# Task: Codebase Overview Analysis

<instructions>
Analyze the provided codebase and generate a comprehensive overview.
</instructions>

<input>
<codebase_context>
{CODEBASE_CONTEXT}
</codebase_context>

<codebase_content>
{CODEBASE_CONTENT}
</codebase_content>
</input>

<output_format>
<analysis>
  <architecture_pattern>
    <name>[Pattern name]</name>
    <description>[Pattern description]</description>
  </architecture_pattern>
  
  <key_components>
    <component>
      <name>[Component name]</name>
      <description>[Component description]</description>
      <role>[Component role]</role>
    </component>
  </key_components>
  
  <technology_stack>
    <languages>[List of languages]</languages>
    <frameworks>[List of frameworks]</frameworks>
    <tools>[List of tools]</tools>
  </technology_stack>
  
  <design_summary>
    [2-3 sentence summary]
  </design_summary>
</analysis>
</output_format>

<thinking>
Work through your analysis step by step before providing the structured output.
</thinking>
```

**When to use:**
- Complex data structures
- API integrations
- Reliable parsing requirements
- Formal documentation

### Level 5: Specialized Templates

**Principle**: Custom system prompts for domain expertise.

**Characteristics:**
- Role-specific system prompts
- Domain expertise context
- Consistent behavior patterns
- Advanced Claude Code SDK features

**Example System Prompt:**
```markdown
<system>
You are a Senior Software Architect with 15+ years of experience in enterprise software development. You specialize in analyzing codebases and providing architectural insights.

Your expertise includes:
- Distributed systems design
- Microservices architecture
- Cloud-native applications
- Performance optimization
- Security best practices

When analyzing code, you:
- Focus on architectural patterns and design principles
- Identify potential scalability issues
- Consider security implications
- Evaluate maintainability and technical debt
- Provide actionable recommendations

Your analysis should be:
- Technically accurate and detailed
- Focused on architectural concerns
- Supportive of best practices
- Practical for implementation teams
</system>

# Senior Architect Code Review

[Rest of template with specialized instructions]
```

**When to use:**
- Specialized domains
- Consistent role behavior
- Production systems
- Expert-level analysis

### Level 6: Cognee-Powered Templates

**Principle**: AI-enhanced templates with architectural intelligence.

**Characteristics:**
- Knowledge graph integration
- Context-aware enhancement
- Dynamic adaptation
- Real-time optimization

**Example Enhancement:**
```markdown
# AI-Enhanced Codebase Analysis

<cognee_context>
Based on knowledge graph analysis of this codebase:
- Architecture type: {DETECTED_ARCHITECTURE}
- Key patterns: {IDENTIFIED_PATTERNS}
- Dependencies: {DEPENDENCY_GRAPH}
- Similar projects: {RELATED_PROJECTS}
</cognee_context>

<adaptive_instructions>
Given the detected architecture type "{DETECTED_ARCHITECTURE}", focus your analysis on:
- {ARCHITECTURE_SPECIFIC_CONCERNS}
- {PATTERN_SPECIFIC_ISSUES}
- {TECHNOLOGY_SPECIFIC_CONSIDERATIONS}
</adaptive_instructions>

[Rest of template with AI-enhanced context]
```

**When to use:**
- Complex architectural analysis
- Pattern-specific optimization
- Context-aware enhancement
- Production-scale systems

## Template Variables

### Common Variables

Templates use placeholders for dynamic content:

```markdown
# Standard Variables
{CONTEXT}                 # Background information
{TASK}                   # Specific task description
{FORMAT}                 # Desired output format
{EXAMPLES}               # Relevant examples
{CONSTRAINTS}            # Limitations or requirements

# Domain-Specific Variables
{CODEBASE_CONTEXT}       # Codebase background
{LANGUAGE}               # Programming language
{FRAMEWORK}              # Framework information
{ARCHITECTURE_TYPE}      # Architecture pattern
{COMPLEXITY_LEVEL}       # Complexity assessment
```

### Variable Substitution

```python
from templates.template_renderer import TemplateRenderer

renderer = TemplateRenderer()
rendered_prompt = renderer.render(
    template_file="templates/base/codebase-analysis.md",
    variables={
        "CODEBASE_CONTEXT": "E-commerce platform with microservices",
        "LANGUAGE": "Python",
        "FRAMEWORK": "FastAPI",
        "ARCHITECTURE_TYPE": "Microservices"
    }
)
```

## Using Templates

### Template Selection Guide

| Use Case | Recommended Level | Rationale |
|----------|------------------|-----------|
| Simple Q&A | Base | Direct communication sufficient |
| Code formatting | Enhanced | Examples show desired format |
| Bug analysis | Advanced | Requires systematic reasoning |
| Data extraction | Structured | XML ensures reliable parsing |
| Code review | Specialized | Domain expertise needed |
| Architecture analysis | Cognee-powered | AI insights enhance accuracy |

### Template Customization

#### 1. Start with Base Template

```bash
# Copy appropriate base template
cp templates/base/codebase-analysis.md templates/base/my-analysis.md

# Edit for your specific use case
nano templates/base/my-analysis.md
```

#### 2. Add Context and Examples

```markdown
# Customize for your domain
## Context
This analysis is for {DOMAIN} applications using {TECHNOLOGY_STACK}.

## Examples
[Add domain-specific examples]

## Special Considerations
- {DOMAIN_SPECIFIC_CONCERN_1}
- {DOMAIN_SPECIFIC_CONCERN_2}
```

#### 3. Test and Iterate

```bash
# Test your customized template
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/base/my-analysis.md \
  --test_cases test_cases/my-domain.json
```

#### 4. Progressive Enhancement

```bash
# Enhance based on results
cp templates/base/my-analysis.md templates/enhanced/my-analysis.md

# Add examples and reasoning
nano templates/enhanced/my-analysis.md

# Test improvement
python evaluations/scripts/compare_prompts.py \
  --baseline templates/base/my-analysis.md \
  --variant templates/enhanced/my-analysis.md
```

## Creating New Templates

### Template Development Process

1. **Define Objective**: Clear task definition and success criteria
2. **Choose Base Level**: Start with appropriate sophistication level
3. **Add Context**: Include relevant background information
4. **Create Examples**: Demonstrate desired outputs
5. **Test and Validate**: Ensure effectiveness with evaluations
6. **Iterate and Improve**: Refine based on results

### Template Structure

```markdown
# Template: [Template Name]

## Metadata
- **Version**: 1.0
- **Author**: [Your name]
- **Date**: [Creation date]
- **Use Case**: [Primary use case]
- **Level**: [Template level]

## Description
[Brief description of template purpose and use case]

## Instructions
[Clear, specific instructions for the task]

## Context
[Background information and constraints]

## Examples (if applicable)
[Relevant examples showing input-output relationships]

## Output Format
[Specification of desired output structure]

## Variables
[List of template variables and their purposes]

## Notes
[Additional guidance or considerations]
```

### Template Validation

```python
from templates.template_validator import TemplateValidator

validator = TemplateValidator()
validation_results = validator.validate(
    template_file="templates/base/my-new-template.md",
    requirements={
        "has_clear_instructions": True,
        "has_output_format": True,
        "has_examples": False,  # Not required for base level
        "has_variables": True
    }
)

if validation_results.is_valid:
    print("✅ Template validation passed")
else:
    print("❌ Validation issues:", validation_results.issues)
```

## Best Practices

### Template Design Principles

1. **Clarity First**: Instructions should be unambiguous
2. **Context Matters**: Provide relevant background information
3. **Examples Guide**: Show desired behavior and format
4. **Progressive Enhancement**: Start simple, add complexity gradually
5. **Consistent Structure**: Follow established patterns

### Common Pitfalls

**❌ Avoid:**
- Ambiguous instructions
- Missing context
- Inconsistent formatting
- Overly complex initial versions
- Untested templates

**✅ Do:**
- Test thoroughly before deployment
- Use consistent variable naming
- Document template purpose and usage
- Provide clear success criteria
- Include relevant examples

### Template Maintenance

```bash
# Regular template evaluation
python evaluations/scripts/batch_evaluate.py \
  --template-dir templates/ \
  --test_cases test_cases/ \
  --output-dir evaluations/results/template-health-check

# Performance monitoring
python evaluations/scripts/template_performance_monitor.py \
  --template-dir templates/ \
  --time-window 30d
```

## Advanced Features

### Dynamic Template Generation

```python
from templates.cognee_powered.engine import CogneePromptEngine

engine = CogneePromptEngine()

# Generate context-aware template
enhanced_template = engine.generate_template(
    base_template="templates/base/code-review.md",
    codebase_context=codebase_analysis,
    enhancement_level="advanced"
)

# Save generated template
with open("templates/generated/enhanced-code-review.md", "w") as f:
    f.write(enhanced_template)
```

### Template Versioning

```bash
# Create versioned templates
git tag -a template-v1.0 -m "Initial template release"
git push origin template-v1.0

# Track template changes
git log --oneline templates/base/codebase-analysis.md
```

### Template Analytics

```python
from templates.analytics import TemplateAnalytics

analytics = TemplateAnalytics()

# Analyze template usage
usage_stats = analytics.analyze_usage(
    template_dir="templates/",
    time_window="30d"
)

print(f"Most used template: {usage_stats.most_popular}")
print(f"Average performance: {usage_stats.avg_performance:.2f}")
print(f"Success rate: {usage_stats.success_rate:.2%}")
```

## Integration with Evaluation System

### Template-Specific Evaluations

```python
from evaluations.template_evaluator import TemplateEvaluator

evaluator = TemplateEvaluator()

# Evaluate template across all levels
level_comparison = evaluator.compare_levels(
    base_template="codebase-analysis",
    test_cases="test_cases/codebase-analysis.json"
)

# Find optimal level for use case
optimal_level = level_comparison.get_optimal_level()
print(f"Recommended level: {optimal_level}")
```

### A/B Testing Templates

```python
from evaluations.scripts.template_ab_test import TemplateABTest

ab_test = TemplateABTest()

results = ab_test.run(
    template_variants=[
        "templates/base/bug-analysis.md",
        "templates/enhanced/bug-analysis.md",
        "templates/advanced/bug-analysis.md"
    ],
    test_cases="test_cases/bug-analysis.json",
    statistical_significance=0.05
)

print(f"Winner: {results.winner}")
print(f"Confidence: {results.confidence:.2%}")
```

## Troubleshooting

### Common Issues

**Template Not Working**
- Check variable substitution
- Validate file paths
- Verify template syntax
- Test with simple examples

**Inconsistent Results**
- Add more examples
- Clarify instructions
- Reduce ambiguity
- Consider structured format

**Poor Performance**
- Simplify complex instructions
- Add reasoning steps
- Enhance with examples
- Consider level upgrade

### Template Debugging

```python
from templates.debugger import TemplateDebugger

debugger = TemplateDebugger()

# Debug template issues
debug_info = debugger.analyze(
    template_file="templates/base/problematic-template.md",
    test_case="test_cases/debug-case.json"
)

print(f"Issues found: {len(debug_info.issues)}")
for issue in debug_info.issues:
    print(f"- {issue.description}")
    print(f"  Suggestion: {issue.suggestion}")
```

---

**Ready to create effective templates?** Start with our [Template Creation Tutorial](../tutorials/template_creation.md) or explore [Template Examples](../examples/template_examples.md) for inspiration.

*Need help with specific template patterns? Check our [API Reference](../api_reference/template_api.md) or [Best Practices Guide](../best-practices/prompt-engineering-guide.md).*