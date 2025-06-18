# Templates Directory

This directory contains reusable prompt templates organized by sophistication level. These templates follow Anthropic's prompt engineering hierarchy and are designed for systematic prompt development.

## 🏗️ Template Hierarchy

Based on [Anthropic's prompt engineering best practices](../anthropic-md/en/docs/build-with-claude/prompt-engineering/overview.md), templates are organized from most broadly effective to more specialized:

### 1. base/ - Clear and Direct
**Foundation level prompts** that follow the core principle: be clear, contextual, and specific.

**Characteristics:**
- Direct instructions without ambiguity
- Explicit context and desired outcomes
- Sequential steps when needed
- Clear success criteria

**When to use:** Starting point for all prompts, simple tasks, quick iterations

### 2. enhanced/ - Examples (Multishot)
**Base prompts enhanced with examples** to demonstrate desired behavior and output format.

**Characteristics:**
- Few-shot learning with 2-5 examples
- Diverse examples covering edge cases
- Consistent example format
- Clear input-output relationships

**When to use:** When format matters, complex output structures, demonstrating edge case handling

### 3. advanced/ - Chain of Thought
**Enhanced prompts with reasoning** that encourage Claude to think through problems step-by-step.

**Characteristics:**
- Explicit thinking instructions
- Step-by-step reasoning guidance
- Problem decomposition
- Verification steps

**When to use:** Complex analysis, multi-step problems, debugging, architectural decisions

### 4. structured/ - XML Tags
**Advanced prompts with XML structure** for maximum clarity and reliable parsing.

**Characteristics:**
- Clear input/output sections with XML tags
- Structured data organization
- Reliable output parsing
- Reduced ambiguity

**When to use:** Complex data structures, API integrations, reliable parsing requirements

### 5. specialized/ - Custom System Prompts
**Structured prompts with role-specific system prompts** for domain expertise.

**Characteristics:**
- Custom system prompts for specific roles
- Domain-specific expertise
- Consistent behavior patterns
- Advanced Claude Code SDK features

**When to use:** Specialized domains, consistent role behavior, production systems

## 📋 Template Components

Each template level includes:

```
level/
├── README.md              # Level overview and best practices
├── template.md           # Base template structure
├── variations/           # Template variations for different use cases
├── examples/             # Usage examples with results
└── guidelines.md         # Customization guidelines
```

## 🎯 Choosing the Right Template

| Use Case | Recommended Level | Rationale |
|----------|------------------|-----------|
| Simple Q&A | Base | Direct communication sufficient |
| Code formatting | Enhanced | Examples show desired format |
| Bug analysis | Advanced | Requires systematic reasoning |
| Data extraction | Structured | XML ensures reliable parsing |
| Code review | Specialized | Domain expertise needed |

## 🔄 Progressive Enhancement

**Recommended workflow:**

1. **Start with Base**: Create clear, direct prompt
2. **Add Examples**: If output format needs demonstration
3. **Include Reasoning**: For complex analysis tasks
4. **Structure with XML**: When reliable parsing is critical
5. **Specialize Role**: For domain-specific expertise

## 📊 Claude 4 Optimizations

Templates incorporate [Claude 4 best practices](../anthropic-md/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices.md):

- **Explicit Instructions**: Clear about desired behavior
- **Context Addition**: Explanation of why behaviors matter
- **Parallel Tool Usage**: Optimized for multiple simultaneous operations
- **Extended Thinking**: Leverage reasoning capabilities

## 🛠️ Template Variables

Common variables used across templates:

- `{CONTEXT}`: Background information
- `{TASK}`: Specific task description
- `{FORMAT}`: Desired output format
- `{EXAMPLES}`: Relevant examples
- `{CONSTRAINTS}`: Limitations or requirements

## 📝 Customization Guide

1. **Select Base Template**: Choose appropriate sophistication level
2. **Add Context**: Include domain-specific information
3. **Customize Examples**: Use relevant examples from your domain
4. **Set Constraints**: Add specific requirements
5. **Test and Iterate**: Validate with your use cases

## 🔗 Related Resources

- [Prompt Engineering Overview](../anthropic-md/en/docs/build-with-claude/prompt-engineering/overview.md)
- [Claude 4 Best Practices](../anthropic-md/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices.md)
- [Claude Code SDK](../anthropic-md/en/docs/claude-code/sdk.md)
- [Evaluation Guidelines](../docs/best-practices/evaluation-guide.md)

---

*Templates are designed to work seamlessly with the Claude Code SDK and follow proven prompt engineering principles.*