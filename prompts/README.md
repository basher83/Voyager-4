# Prompts Directory

This directory contains organized collections of Claude Code prompts categorized by use case. Each category includes prompts at different sophistication levels to support various scenarios and requirements.

## 📁 Categories

### 🔍 codebase-understanding/
Prompts for analyzing and understanding codebases:
- **Overview Generation**: High-level codebase summaries
- **Architecture Analysis**: System design and patterns
- **Component Location**: Finding relevant code sections
- **Dependency Mapping**: Understanding relationships between modules

### 🐛 bug-fixing/
Prompts for debugging and error resolution:
- **Error Diagnosis**: Analyzing error messages and stack traces
- **Solution Generation**: Providing fix recommendations
- **Root Cause Analysis**: Deep investigation of underlying issues
- **Testing Fixes**: Validating proposed solutions

### 💻 code-generation/
Prompts for creating and modifying code:
- **Feature Implementation**: Building new functionality
- **Refactoring**: Improving existing code structure
- **Documentation**: Generating comments and docs
- **Code Translation**: Converting between languages/frameworks

### 🧪 testing/
Prompts for test creation and validation:
- **Test Generation**: Creating unit and integration tests
- **Coverage Analysis**: Identifying untested code
- **Test Validation**: Ensuring test quality and effectiveness
- **Edge Case Discovery**: Finding boundary conditions

### 📋 project-management/
Prompts for development workflow support:
- **PR Creation**: Generating pull request descriptions
- **Code Review**: Analyzing changes for quality issues
- **Planning**: Breaking down tasks and estimating effort
- **Documentation**: Creating project documentation

## 🎯 Prompt Structure

Each category follows a consistent structure:

```
category/
├── README.md           # Category overview and usage guide
├── basic/             # Simple, direct prompts
├── intermediate/      # Enhanced prompts with examples
├── advanced/          # Complex prompts with reasoning
└── examples/          # Usage examples and results
```

## 📝 Usage Guidelines

1. **Start Simple**: Begin with basic prompts and enhance as needed
2. **Test Thoroughly**: Validate prompts with your specific use cases
3. **Iterate**: Refine prompts based on results and feedback
4. **Document**: Record what works and what doesn't
5. **Share**: Contribute successful patterns back to the collection

## 🔧 Customization

Prompts can be customized for your specific needs:

- **Context**: Add domain-specific information
- **Style**: Adjust tone and formatting preferences
- **Constraints**: Include specific requirements or limitations
- **Examples**: Provide relevant examples from your codebase

## 📊 Evaluation

Use the evaluation framework in `/evaluations/` to:
- Measure prompt effectiveness
- Compare different approaches
- Track performance over time
- Identify improvement opportunities

## 🚀 Getting Started

1. Browse category READMEs to understand available prompts
2. Start with basic prompts for your use case
3. Test with sample data from `/test-cases/`
4. Enhance prompts based on results
5. Document successful patterns

---

*Each prompt is designed to work with the Claude Code SDK and follows Anthropic's prompt engineering best practices.*