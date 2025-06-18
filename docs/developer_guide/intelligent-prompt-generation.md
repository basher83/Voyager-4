# Intelligent Prompt Generation with Cognee Integration

This guide explains how to use the intelligent prompt generator that analyzes codebase architecture using Cognee's knowledge graph capabilities to create context-aware, specialized prompts.

## Overview

The intelligent prompt generation system combines:
- **Codebase Analysis**: Automated detection of architectural patterns, technologies, and complexity
- **Cognee Knowledge Graphs**: Deep understanding of code relationships and patterns
- **Context-Aware Templates**: Prompts tailored to specific codebase characteristics
- **MCP Integration**: Real-time enhancement using Cognee's capabilities

## Quick Start

### Basic Usage

```bash
# Analyze codebase and generate prompts
python evaluations/scripts/codebase_intelligent_prompts.py analyze . \
  --types architecture_analysis code_generation bug_fixing \
  --output templates/cognee-powered/generated

# Run Cognee-enhanced version
python evaluations/scripts/cognee_intelligent_prompts_demo.py
```

### MCP Integration (Claude Code Environment)

```python
# Step 1: Generate code graph
mcp__cognee__codify("/path/to/codebase")

# Step 2: Add domain knowledge
mcp__cognee__cognify("This codebase uses microservices architecture with Docker containers")

# Step 3: Search for insights
insights = mcp__cognee__search("microservices patterns dependencies", "CODE")

# Step 4: Generate enhanced prompts using insights
# (Use insights to populate template variables)
```

## System Architecture

### Core Components

1. **PromptIntelligenceGenerator**: Main analysis and generation engine
2. **CogneeEnhancedPromptGenerator**: Extended version with knowledge graph integration
3. **Architectural Pattern Detection**: Identifies MVC, microservices, layered architecture, etc.
4. **Technology Stack Analysis**: Language, framework, and dependency detection
5. **Template Factory System**: Dynamic template generation based on analysis

### Analysis Pipeline

```
Codebase Input → Structure Analysis → Pattern Detection → Technology Detection
       ↓
Complexity Calculation → Insight Extraction → Template Generation → Enhancement
       ↓
Cognee Integration → Knowledge Graph Search → Context Enrichment → Final Templates
```

## Features

### Architectural Pattern Recognition

The system automatically detects:

- **MVC Pattern**: Models, Views, Controllers organization
- **Microservices**: Docker files + multiple service directories
- **Layered Architecture**: Service/Repository/Data layer separation
- **REST API**: API endpoints and route organization

### Technology Stack Detection

Supports analysis of:

- **Languages**: Python, JavaScript, TypeScript, Java, C++, etc.
- **Frameworks**: Django, Flask, React, Angular, Express, Spring
- **Dependencies**: Automatic parsing of requirements.txt, package.json, pom.xml
- **Testing Patterns**: Unit test detection and framework identification

### Template Types

Generates specialized templates for:

1. **Architecture Analysis**: Pattern-aware structural analysis
2. **Bug Fixing**: Technology-specific debugging strategies
3. **Code Generation**: Framework-compliant implementation guidance
4. **Refactoring**: Pattern-based improvement suggestions
5. **Testing**: Architecture-appropriate testing strategies
6. **Documentation**: Structure-aware documentation generation

## Cognee Integration

### MCP Functions

The system uses these Cognee MCP functions:

- `mcp__cognee__codify(repo_path)`: Generate code structure graph
- `mcp__cognee__cognify(data)`: Ingest domain knowledge
- `mcp__cognee__search(query, type)`: Query knowledge graph
- `mcp__cognee__codify_status()`: Check processing status
- `mcp__cognee__cognify_status()`: Monitor knowledge ingestion

### Search Types

- **CODE**: Find specific code patterns and structures
- **INSIGHTS**: Discover component relationships
- **GRAPH_COMPLETION**: Get LLM-powered analysis and recommendations

### Enhancement Process

1. **Base Analysis**: Standard codebase pattern detection
2. **Knowledge Ingestion**: Add project context to Cognee
3. **Graph Search**: Query for architectural insights
4. **Template Enhancement**: Integrate insights into prompts
5. **Metadata Enrichment**: Add relationship awareness

## Generated Templates

### Template Structure

Each generated template includes:

```markdown
# Context-Aware [Template Type]

## Codebase-Specific Context
- Architecture: [Detected Pattern]
- Languages: [Primary Languages]
- Frameworks: [Detected Frameworks] 
- Complexity: [Calculated Level]

## Intelligence-Enhanced Instructions
[Pattern-specific guidance]

## Technology-Specific Insights
[Language and framework best practices]

## Cognee Knowledge Graph Enhancement
[Relationship awareness and pattern recognition]
```

### Variable System

Templates include context variables:

- **CODEBASE_PATH**: Target analysis path
- **ANALYSIS_FOCUS**: Specific analysis area
- **TARGET_AUDIENCE**: Developer/Architect/QA
- **KNOWLEDGE_GRAPH_CONTEXT**: Cognee insights
- **RELATIONSHIP_INSIGHTS**: Component connections
- **PATTERN_AWARENESS**: Architectural pattern details

## Configuration

### Default Configuration

```yaml
analysis:
  min_confidence_threshold: 0.6
  max_patterns_per_category: 5
  complexity_thresholds:
    low: 0.3
    medium: 0.6
    high: 0.8

cognee:
  enable_code_graph: true
  search_types: ["CODE", "INSIGHTS", "GRAPH_COMPLETION"]
  analysis_depth: "comprehensive"

templates:
  supported_types:
    - architecture_analysis
    - bug_fixing
    - code_generation
    - refactoring
    - testing
    - documentation
```

### Environment Setup

Required environment variables:

```bash
COGNEE_LLM_PROVIDER=anthropic
COGNEE_DEFAULT_MODEL=claude-3-sonnet-20240229
ANTHROPIC_API_KEY=your_api_key
```

## Usage Examples

### Example 1: Django Application Analysis

```bash
# Analyze Django codebase
python evaluations/scripts/codebase_intelligent_prompts.py analyze ./my-django-app

# Output: 
# - Detects MVC pattern
# - Identifies Django framework
# - Generates Django-specific templates
# - Includes middleware and URL routing guidance
```

### Example 2: Microservices Architecture

```bash
# Analyze microservices project
python evaluations/scripts/cognee_intelligent_prompts_demo.py --repo-path ./microservices-project

# Output:
# - Detects microservices pattern
# - Identifies service boundaries
# - Generates inter-service communication templates
# - Includes Docker and orchestration guidance
```

### Example 3: Real-time Enhancement

```python
# In Claude Code environment
codify_result = mcp__cognee__codify("./my-project")

# Add specific context
mcp__cognee__cognify("""
This project uses:
- FastAPI for REST API
- PostgreSQL for data persistence  
- Redis for caching
- Celery for background tasks
""")

# Search for patterns
api_patterns = mcp__cognee__search("FastAPI REST patterns", "CODE")
db_patterns = mcp__cognee__search("PostgreSQL integration FastAPI", "INSIGHTS")

# Use results to enhance templates
```

## Advanced Features

### Template Optimization

The system includes automatic optimization:

- **Usage Pattern Analysis**: Tracks template effectiveness
- **Feedback Integration**: Learns from user interactions
- **Performance Monitoring**: Measures accuracy and consistency
- **Automatic Enhancement**: Suggests improvements based on usage

### Extensibility

Easy to extend with:

- **Custom Pattern Detectors**: Add new architectural pattern recognition
- **Framework Plugins**: Support additional frameworks
- **Template Generators**: Create specialized template types
- **Cognee Integrations**: Add custom knowledge graph queries

## File Organization

```
evaluations/scripts/
├── codebase_intelligent_prompts.py       # Core analysis engine
├── cognee_intelligent_prompts_demo.py    # Enhanced demo with Cognee
├── cognee_mcp_usage_example.py           # MCP integration examples
└── test_cognee_integration.py            # Integration tests

templates/cognee-powered/
├── generated/                            # Basic generated templates
├── cognee-enhanced/                      # Cognee-enhanced templates
└── architecture-aware/                   # Pattern-specific templates

docs/guides/
├── intelligent-prompt-generation.md      # This guide
├── cognee-insights.md                    # Cognee-specific documentation
└── evaluation-framework-reference.md     # Evaluation system docs
```

## Troubleshooting

### Common Issues

1. **Pattern Detection Failures**
   - Ensure codebase has clear structural organization
   - Check for standard naming conventions
   - Verify framework-specific files are present

2. **Cognee Integration Issues**
   - Verify MCP server configuration
   - Check processing status with status functions
   - Ensure sufficient processing time for large codebases

3. **Template Quality Issues**
   - Review confidence scores in metadata
   - Check complexity alignment
   - Validate against real use cases

### Debug Commands

```bash
# Check analysis results
cat templates/cognee-powered/generated/index.json

# Review template metadata
cat templates/cognee-powered/cognee-enhanced/*_metadata.json

# Monitor Cognee processing
# In Claude Code: mcp__cognee__codify_status()
```

## Best Practices

1. **Codebase Preparation**
   - Ensure clean, well-organized code structure
   - Include framework-specific configuration files
   - Maintain consistent naming conventions

2. **Template Usage**
   - Populate all context variables appropriately
   - Use Cognee insights to enhance prompts
   - Validate generated code against codebase patterns

3. **Continuous Improvement**
   - Monitor template performance metrics
   - Collect user feedback for optimization
   - Update knowledge base with new patterns

4. **Integration Strategy**
   - Start with base templates for testing
   - Gradually integrate Cognee enhancements
   - Use MCP functions for real-time adaptation

## Contributing

To extend the intelligent prompt generation system:

1. **Add Pattern Detectors**: Extend `_detect_architectural_patterns()`
2. **Add Framework Support**: Update framework detection in `_detect_frameworks_and_dependencies()`
3. **Create Template Generators**: Add new methods to `PromptIntelligenceGenerator`
4. **Enhance Cognee Integration**: Extend `CogneeEnhancedPromptGenerator`

## Support

For issues and questions:
- Review logs in `cognee_integration_test.log`
- Check configuration in `evaluations/config/cognee_config.yaml`
- Consult Cognee MCP documentation
- Review generated template metadata for debugging

---

*This system represents a significant advancement in AI-assisted development, providing intelligent, context-aware assistance that understands your specific codebase architecture and patterns.*