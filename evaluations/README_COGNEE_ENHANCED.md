# Cognee-Enhanced Evaluation System

This document describes the AI-powered evaluation system that extends the base PromptEvaluator with knowledge graph analysis using Cognee MCP integration.

## Overview

The Cognee-Enhanced Evaluation System adds artificial intelligence and knowledge graph capabilities to prompt evaluation, providing:

- **Contextual Analysis**: Understanding relationships between test cases
- **Pattern Recognition**: Identifying evaluation patterns and optimization opportunities  
- **AI-Powered Recommendations**: Generating specific, actionable improvement suggestions
- **Knowledge Graph Insights**: Leveraging graph relationships for deeper evaluation understanding

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cognee Enhanced Evaluator                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌──────────────────┐    ┌─────────────┐ │
│  │  Base Evaluator │    │ Knowledge Graph  │    │ MCP Cognee  │ │
│  │                 │    │    Preparation   │    │ Integration │ │
│  │ • Accuracy      │───▶│                  │───▶│             │ │
│  │ • Consistency   │    │ • Test Case      │    │ • cognify() │ │
│  │ • Quality       │    │   Analysis       │    │ • search()  │ │
│  │ • ROUGE         │    │ • Prompt Context │    │ • status()  │ │
│  └─────────────────┘    │ • Relationships  │    └─────────────┘ │
│                         └──────────────────┘                    │
│                                   │                             │
│  ┌─────────────────────────────────▼─────────────────────────┐   │
│  │              AI-Powered Analysis                         │   │
│  │                                                          │   │
│  │ • Pattern Recognition    • Insight Generation           │   │
│  │ • Challenge Identification • Optimization Suggestions   │   │
│  │ • Relationship Analysis   • Recommendation Engine       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. CogneeEnhancedEvaluator

The main class that extends `PromptEvaluator` with AI capabilities:

```python
from evaluations.scripts.cognee_enhanced_evaluator import CogneeEnhancedEvaluator

evaluator = CogneeEnhancedEvaluator(
    cognee_config={
        "use_knowledge_context": True,
        "create_test_case_graph": True, 
        "analyze_evaluation_patterns": True,
        "search_types": ["GRAPH_COMPLETION", "CODE", "INSIGHTS"],
        "knowledge_weight": 0.3
    }
)
```

**Key Features:**
- Extends all base evaluator functionality
- Adds knowledge graph preparation and analysis
- Integrates with MCP Cognee functions
- Provides AI-powered recommendations
- Generates comprehensive reports with insights

### 2. Knowledge Graph Integration

Transforms evaluation data into structured knowledge for analysis:

```python
# Prepare knowledge graph from test cases
await evaluator._create_knowledge_graph(test_cases, prompt)

# Get prepared data for MCP processing
knowledge_data = evaluator.prepare_knowledge_data()
mcp_queries = evaluator.get_mcp_queries()
```

**Knowledge Structure:**
- Test case relationships and patterns
- Evaluation methodology context
- Prompt analysis and categorization
- Challenge and opportunity identification

### 3. MCP Cognee Integration

Utilizes Cognee MCP functions for advanced analysis:

- `mcp__cognee__cognify()`: Creates knowledge graphs from evaluation data
- `mcp__cognee__search()`: Performs contextual searches with multiple types
- `mcp__cognee__prune()`: Resets knowledge base for clean processing
- `mcp__cognee__cognify_status()`: Monitors processing status

## Usage Examples

### Basic Enhanced Evaluation

```python
import asyncio
from evaluations.scripts.cognee_enhanced_evaluator import run_enhanced_evaluation

# Run evaluation with AI enhancement
results = await run_enhanced_evaluation(
    prompt_path="templates/base/codebase-overview-template.md",
    test_cases_path="test_cases/examples/codebase_understanding_examples.json",
    cognee_config={
        "use_knowledge_context": True,
        "search_types": ["GRAPH_COMPLETION", "INSIGHTS"]
    }
)
```

### Full MCP Integration

```python
from evaluations.scripts.cognee_enhanced_evaluator import run_full_mcp_evaluation

# MCP function mapping (when available)
mcp_functions = {
    "cognify": mcp__cognee__cognify,
    "search": mcp__cognee__search,
    "prune": mcp__cognee__prune,
    "cognify_status": mcp__cognee__cognify_status
}

# Run complete MCP-enhanced evaluation
results = await run_full_mcp_evaluation(
    prompt_path="templates/base/codebase-overview-template.md",
    test_cases_path="test_cases/examples/codebase_understanding_examples.json",
    mcp_functions=mcp_functions
)
```

### Integration Utilities

```python
from evaluations.scripts.mcp_cognee_integration_utils import (
    MCPCogneeIntegrator,
    integrate_evaluator_with_mcp,
    create_mcp_function_map
)

# Create MCP function mapping
mcp_functions = create_mcp_function_map(
    cognify=mcp__cognee__cognify,
    search=mcp__cognee__search,
    prune=mcp__cognee__prune,
    cognify_status=mcp__cognee__cognify_status
)

# Integrate evaluator with MCP
mcp_results = await integrate_evaluator_with_mcp(evaluator, mcp_functions)
```

## Search Types

The system supports multiple Cognee search types for different analysis perspectives:

### GRAPH_COMPLETION
Provides comprehensive analysis using full knowledge graph context:
```
- Architectural pattern identification
- Evaluation challenge analysis  
- Optimization opportunity detection
- Relationship-based insights
```

### CODE
Focuses on technical and code-related patterns:
```
- Technical pattern recognition
- Implementation quality assessment
- Code structure analysis
- Technology stack evaluation
```

### INSIGHTS
Emphasizes relationships and cross-cutting analysis:
```
- Cross-test case relationships
- Pattern correlation analysis
- Predictive insights
- Optimization recommendations
```

## Output and Reporting

### Enhanced Results Structure

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "results": { /* Base evaluation results */ },
  "knowledge_enhanced_metrics": {
    "GRAPH_COMPLETION": {
      "total_insights": 5,
      "case_insights": { /* Per-case analysis */ }
    }
  },
  "evaluation_patterns": {
    "pattern_analysis": "...",
    "recommendations": [...],
    "optimization_opportunities": {...}
  },
  "mcp_integration": {
    "mcp_integration_successful": true,
    "knowledge_insights": {...},
    "pattern_analysis": {...},
    "recommendations": [...]
  },
  "comprehensive_report": {
    "executive_summary": {...},
    "evaluation_performance": {...},
    "ai_enhancement_analysis": {...},
    "key_findings": [...],
    "actionable_recommendations": [...]
  }
}
```

### Report Sections

1. **Executive Summary**: High-level evaluation status and AI enhancement effectiveness
2. **Performance Metrics**: Accuracy, consistency, quality scores with threshold status
3. **AI Enhancement Analysis**: Knowledge integration success and insight quality
4. **Key Findings**: Important discoveries from evaluation and AI analysis
5. **Actionable Recommendations**: Prioritized, specific improvement suggestions

## Configuration

### Cognee Configuration Options

```python
cognee_config = {
    "use_knowledge_context": True,        # Enable knowledge-based enhancement
    "create_test_case_graph": True,       # Create knowledge graph from test cases
    "analyze_evaluation_patterns": True,  # Perform pattern analysis
    "search_types": ["GRAPH_COMPLETION", "CODE", "INSIGHTS"],  # Search methods
    "knowledge_weight": 0.3               # Weight for knowledge-enhanced scores
}
```

### Evaluation Configuration

Extends base evaluator configuration with AI-specific options:

```yaml
# evaluations/config/cognee_config.yaml
model: "claude-3-opus-20240229"
evaluation_methods: ["exact_match", "consistency", "quality"]
metrics:
  accuracy_threshold: 0.85
  consistency_threshold: 0.8
  quality_threshold: 4.0

# Cognee-specific configuration
cognee:
  enabled: true
  search_types: ["GRAPH_COMPLETION", "INSIGHTS"]
  knowledge_weight: 0.3
  pattern_analysis: true
```

## Installation and Setup

### Prerequisites

```bash
# Install base requirements
pip install -r requirements.txt

# Additional dependencies for enhanced evaluation
pip install asyncio logging
```

### MCP Cognee Setup

1. Ensure MCP Cognee server is running
2. Configure MCP connection in your environment
3. Test MCP functions are accessible

### File Structure

```
evaluations/
├── scripts/
│   ├── cognee_enhanced_evaluator.py      # Main enhanced evaluator
│   ├── mcp_cognee_integration_utils.py   # MCP integration utilities
│   ├── demo_cognee_mcp_integration.py    # Basic demonstration
│   ├── real_mcp_integration_demo.py      # Advanced MCP demo
│   └── evaluate_prompt.py                # Base evaluator
├── config/
│   ├── cognee_config.yaml                # Enhanced configuration
│   └── default_config.yaml               # Base configuration
└── results/
    └── [evaluation_results.json]         # Output files
```

## Command Line Usage

### Basic Enhanced Evaluation

```bash
python evaluations/scripts/cognee_enhanced_evaluator.py \
  --prompt templates/base/codebase-overview-template.md \
  --test_cases test_cases/examples/codebase_understanding_examples.json \
  --search-types GRAPH_COMPLETION INSIGHTS
```

### Demo Scripts

```bash
# Run basic demonstration
python evaluations/scripts/demo_cognee_mcp_integration.py

# Run advanced MCP integration demo
python evaluations/scripts/real_mcp_integration_demo.py
```

## Performance and Optimization

### Evaluation Performance Impact

- **Knowledge Graph Creation**: +2-5 seconds per evaluation
- **MCP Operations**: +10-30 seconds depending on data size
- **Search Queries**: +1-3 seconds per query
- **Overall Enhancement**: 15-45 seconds additional processing time

### Optimization Strategies

1. **Batch Processing**: Process multiple evaluations in sequence
2. **Cached Results**: Reuse knowledge graphs for similar test cases  
3. **Selective Enhancement**: Use specific search types for targeted analysis
4. **Parallel Processing**: Execute multiple search queries concurrently

### Resource Usage

- **Memory**: +50-200MB for knowledge graph processing
- **CPU**: Moderate increase during MCP operations
- **Network**: Depends on MCP server communication

## Troubleshooting

### Common Issues

1. **MCP Connection Failed**
   - Verify MCP Cognee server is running
   - Check network connectivity and ports
   - Validate MCP function availability

2. **Knowledge Graph Creation Failed**
   - Check test case data format
   - Verify sufficient memory available
   - Review error logs for specific issues

3. **Search Queries Timeout**
   - Reduce query complexity
   - Use shorter search queries
   - Check MCP server performance

4. **Integration Results Missing**
   - Verify MCP functions completed successfully
   - Check result formatting and processing
   - Review operation logs for errors

### Debug Mode

Enable detailed logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run evaluation with detailed logs
evaluator = CogneeEnhancedEvaluator(...)
```

## Advanced Features

### Custom Search Types

Extend the evaluator with custom search implementations:

```python
class CustomEnhancedEvaluator(CogneeEnhancedEvaluator):
    def prepare_custom_search(self, test_cases):
        # Custom search query preparation
        pass
```

### Integration with Other Tools

Combine with other evaluation tools and frameworks:
- Statistical analysis packages
- Visualization libraries  
- Reporting systems
- CI/CD pipelines

### Batch Processing

Process multiple evaluations efficiently:

```python
async def batch_enhanced_evaluation(evaluation_configs):
    results = []
    for config in evaluation_configs:
        result = await run_enhanced_evaluation(**config)
        results.append(result)
    return results
```

## Best Practices

### Evaluation Design

1. **Test Case Quality**: Ensure comprehensive, well-structured test cases
2. **Prompt Clarity**: Use clear, specific prompts for better analysis
3. **Expected Elements**: Define detailed expected elements for pattern recognition
4. **Difficulty Levels**: Include varied difficulty levels for robust analysis

### MCP Usage

1. **Resource Management**: Monitor MCP server resources during processing
2. **Error Handling**: Implement comprehensive error handling for MCP operations
3. **Result Validation**: Validate MCP results before processing
4. **Performance Monitoring**: Track MCP operation performance over time

### Analysis Interpretation

1. **Context Awareness**: Consider evaluation context when interpreting AI insights
2. **Pattern Validation**: Cross-validate pattern insights with domain expertise
3. **Recommendation Prioritization**: Focus on high-impact, actionable recommendations
4. **Continuous Improvement**: Use insights to improve evaluation methodology

## Contributing

### Development Setup

1. Fork the repository
2. Install development dependencies
3. Run tests to ensure base functionality
4. Implement enhancements following existing patterns

### Testing

```bash
# Run basic tests
python -m pytest evaluations/tests/

# Test MCP integration (requires MCP server)
python evaluations/scripts/demo_cognee_mcp_integration.py
```

### Code Quality

- Follow existing code style and patterns
- Add comprehensive docstrings
- Include error handling and logging
- Write tests for new functionality

## License and Support

This enhanced evaluation system is part of the Claude Code Prompt Development Framework. See the main project documentation for license information and support resources.