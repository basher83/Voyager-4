# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Type

**Claude Code Prompt Development Framework** - A systematic approach to building, testing, and optimizing Claude Code prompts using Anthropic's official documentation as the foundation.

## Common Development Commands

```bash
# Environment setup (run once)
python3 setup.py

# Install dependencies
pip install -r requirements.txt

# Single prompt evaluation
python evaluations/scripts/evaluate_prompt.py \
  --prompt templates/base/codebase-overview-template.md \
  --test-cases test-cases/examples/codebase_understanding_examples.json

# Compare prompt variants (A/B testing)
python evaluations/scripts/compare_prompts.py \
  --baseline templates/base/ \
  --variant templates/enhanced/

# Check project progress
cat ROADMAP.md

# Code formatting (when working with Python files)
black .
flake8 .
```

## Architecture Overview

### Core Framework Components

**1. Documentation Foundation (`anthropic-md/`)**
- Scraped official Anthropic documentation serving as authoritative source
- `claude-code/`: SDK reference and workflows
- `build-with-claude/prompt-engineering/`: Core techniques
- `test-and-evaluate/`: Official evaluation methodologies

**2. Hierarchical Template System (`templates/`)**
Progressive enhancement following Anthropic's best practices:
- `base/`: Clear, direct instructions (starting point)
- `enhanced/`: + Examples (few-shot prompting)
- `advanced/`: + Chain of thought reasoning
- `structured/`: + XML tags for reliable parsing
- `specialized/`: + Custom system prompts

**3. Evaluation Infrastructure (`evaluations/`)**
- `scripts/evaluate_prompt.py`: Single prompt testing with multiple metrics
- `scripts/compare_prompts.py`: Statistical A/B testing between variants
- `config/default_config.yaml`: Evaluation parameters and thresholds
- Multi-method assessment: exact match, cosine similarity, LLM grading, ROUGE scores

**4. Use Case Organization (`prompts/`)**
- `codebase-understanding/`: Architecture analysis, component location
- `bug-fixing/`: Error diagnosis and solution generation
- `code-generation/`: Feature implementation and refactoring
- `testing/`: Test generation and validation
- `project-management/`: PR creation and code review

### Key Design Patterns

**Progressive Enhancement**: Templates build complexity systematically from basic instructions to specialized roles, following proven effectiveness order.

**Evaluation-Driven Development**: All prompts must pass statistical thresholds (accuracy >85%, consistency >0.8, quality >4.0/5) before deployment.

**Documentation-First Approach**: Uses official Anthropic docs as authoritative source rather than assumptions or external guidance.

## 🧠 Cognee Knowledge Graph Insights

*Based on AI-powered codebase analysis using [Cognee](https://www.cognee.ai/) MCP integration*

> **About Cognee**: An open-source AI framework for building knowledge graphs from unstructured data. Cognee transforms codebases and documentation into structured, searchable knowledge networks enabling deep architectural insights.
> 
> - **Website**: [cognee.ai](https://www.cognee.ai/)
> - **GitHub**: [github.com/topoteretes/cognee](https://github.com/topoteretes/cognee)
> - **Integration**: Model Context Protocol (MCP) for seamless Claude Code integration

### Architecture Intelligence

**Core Framework Characteristics**:
- **Mature Research-Grade System**: Implements academic-level statistical validation while maintaining practical Claude Code optimization focus
- **Direct Terminal Integration**: Claude Code operates with full project context awareness, enabling file editing and commit creation
- **Scientific Rigor**: Statistical significance testing (Chi-square, t-tests) ensures confident prompt recommendations

### Advanced Evaluation Capabilities

**Statistical Analysis Engine**:
- **4-Method Assessment**: exact_match (accuracy), consistency (cosine similarity), quality (LLM grading), ROUGE (text overlap)
- **Automated A/B Testing**: `PromptComparator` class with weighted ranking and confidence levels
- **Comprehensive Reporting**: JSON results + markdown reports + visualizations (bar charts, radar plots)

**Key Classes Identified**:
- `PromptEvaluator`: Single prompt comprehensive analysis with configurable thresholds
- `PromptComparator`: Multi-prompt statistical comparison with pairwise analysis

### Prompt Engineering Intelligence

**Template Hierarchy Relationships**:
- **Base**: Clear, direct instructions (foundation)
- **Enhanced**: + Examples (few-shot prompting patterns)
- **Advanced**: + Chain of thought reasoning (cognitive scaffolding)
- **Structured**: + XML tags (reliable parsing)
- **Specialized**: + Custom system prompts (role-specific optimization)

**Integration Patterns**:
- Connected to success criteria, cost effectiveness, transparency
- Supports retrieval-augmented generation (RAG) workflows
- Includes prompt generators and template systems
- Compatible with Claude 4 best practices

### Strategic Framework Position

**Evaluation-First Philosophy**: Statistical validation enforced before deployment, ensuring only proven improvements reach production.

**Documentation-Driven Development**: Official Anthropic guidance serves as authoritative foundation rather than external assumptions.

**Progressive Complexity Management**: Systematic enhancement from simple to sophisticated prompts with measurable quality gates.

### Cognee Integration Benefits

**Knowledge Graph Analysis**: Cognee's MCP integration enables real-time codebase intelligence, automatically discovering:
- Architectural patterns and relationships
- Code component dependencies
- Documentation cross-references
- Evaluation methodology insights

**AI-Powered Documentation**: Automated discovery of framework capabilities and strategic positioning through structured knowledge extraction.

## Technology Stack

- **Python 3.8+**: Primary development language
- **Anthropic SDK** (`anthropic>=0.25.0`): Claude API integration
- **Claude Code SDK** (`claude-code-sdk>=1.0.0`): Official toolkit
- **Scientific Computing**: NumPy, SciPy, pandas for statistical analysis
- **NLP**: sentence-transformers, ROUGE, NLTK for text evaluation
- **Visualization**: matplotlib, plotly, seaborn for metrics dashboards

## Development Workflow

1. **Template Development**: Start with `templates/base/`, enhance progressively
2. **Test Case Creation**: Add scenarios to `test-cases/examples/`
3. **Evaluation**: Run systematic testing against multiple metrics
4. **Statistical Validation**: Ensure significance before deployment
5. **Performance Monitoring**: Track latency, cost, and accuracy

## Configuration Files

- `evaluations/config/default_config.yaml`: Evaluation parameters, thresholds, model settings
- `.env`: API keys and environment variables (created by setup.py)
- `requirements.txt`: Python dependencies with specific versions

## Current Project Status

**Phase 1 (Enhanced - 40% complete)**: Foundation established with AI-powered insights
- ✅ Environment and dependencies configured
- ✅ Evaluation framework established and documented
- ✅ Template hierarchy defined with progressive enhancement
- ✅ Documentation foundation scraped and integrated
- ✅ Cognee knowledge graph analysis completed
- ✅ Comprehensive documentation created

**Key Achievements**:
- Advanced statistical evaluation system with 4 assessment methods
- A/B testing framework with confidence-based recommendations
- AI-powered codebase intelligence via Cognee MCP integration
- Research-grade validation ensuring deployment confidence

See `ROADMAP.md` for detailed milestones and progress tracking.