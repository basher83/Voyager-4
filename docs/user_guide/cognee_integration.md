# Cognee Integration Guide

Voyager-4 integrates with [Cognee](https://cognee.ai), an AI framework that transforms codebases into structured knowledge graphs. This integration enables AI-powered prompt enhancement, architectural insights, and context-aware template generation.

## What is Cognee?

Cognee is an open-source AI framework that creates knowledge graphs from unstructured data, particularly codebases. It uses advanced AI techniques to understand code relationships, architectural patterns, and documentation insights.

### Key Capabilities

- **Code Analysis**: Deep understanding of codebase architecture and patterns
- **Relationship Mapping**: Identification of component dependencies and interactions  
- **Pattern Recognition**: Automatic detection of architectural and design patterns
- **Context Generation**: Creation of contextual insights for enhanced prompts
- **Knowledge Graphs**: Structured representation of codebase knowledge

### Why Cognee + Voyager-4?

The integration provides:

1. **Intelligent Templates**: AI-enhanced prompts based on codebase analysis
2. **Context Awareness**: Templates that adapt to your specific architecture
3. **Pattern-Specific Optimization**: Prompts optimized for detected patterns
4. **Real-Time Insights**: Dynamic enhancement based on codebase changes
5. **Knowledge-Driven Evaluation**: Smarter testing based on architectural understanding

## Installation and Setup

### Prerequisites

- Voyager-4 installed and configured
- Python 3.8+ with pip
- Claude Code SDK access
- Internet connection for Cognee services

### Installation

Cognee is included in Voyager-4's requirements:

```bash
# Cognee is already included in requirements.txt
pip install cognee>=0.1.43

# Verify installation
python -c "import cognee; print('Cognee installed successfully!')"
```

### Configuration

#### Environment Variables

Add to your `.env` file:

```env
# Cognee Configuration
COGNEE_API_URL=https://api.cognee.ai
COGNEE_API_KEY=your_cognee_key_here  # Optional for local use
COGNEE_CACHE_ENABLED=true
COGNEE_GRAPH_MODEL=KnowledgeGraph

# Integration Settings
VOYAGER_COGNEE_ENABLED=true
VOYAGER_COGNEE_AUTO_ANALYZE=true
VOYAGER_COGNEE_CACHE_TTL=3600
```

#### Configuration File

Update `evaluations/config/cognee_config.yaml`:

```yaml
cognee:
  # Core settings
  enabled: true
  api_url: "https://api.cognee.ai"
  cache_enabled: true
  cache_ttl: 3600
  
  # Analysis settings
  auto_analyze: true
  analysis_depth: "deep"
  include_tests: true
  include_docs: true
  
  # Knowledge graph settings
  graph_model: "KnowledgeGraph"
  node_types: ["class", "function", "module", "dependency"]
  relationship_types: ["imports", "calls", "inherits", "implements"]
  
  # Integration settings
  template_enhancement: true
  context_injection: true
  pattern_detection: true
  
  # Performance settings
  max_files: 1000
  timeout: 300
  parallel_processing: true
```

## Core Features

### 1. Codebase Analysis

Cognee analyzes your codebase to create a structured knowledge graph:

```python
from evaluations.scripts.cognee_mcp_integration_utils import CogneeMCPIntegration

# Initialize Cognee integration
cognee_integration = CogneeMCPIntegration()

# Analyze codebase
analysis_results = cognee_integration.analyze_codebase(
    repo_path="/path/to/your/codebase",
    analysis_type="comprehensive"
)

print(f"Analysis complete: {analysis_results['status']}")
print(f"Components found: {analysis_results['component_count']}")
print(f"Architecture type: {analysis_results['architecture_type']}")
```

**What gets analyzed:**
- File structure and organization
- Code dependencies and imports
- Class and function relationships
- Architectural patterns
- Documentation and comments
- Test coverage and structure

### 2. AI-Enhanced Template Generation

Generate context-aware templates based on codebase analysis:

```python
from templates.cognee_powered.engine import CogneePromptEngine

engine = CogneePromptEngine()

# Generate enhanced template
enhanced_template = engine.generate(
    task_type="architecture_analysis",
    language="python",
    architecture_type="microservices",
    context="e-commerce platform with high scalability requirements"
)

print("Generated enhanced template:")
print(enhanced_template)
```

**Enhancement types:**
- **Architecture-Aware**: Templates optimized for detected architecture patterns
- **Context-Enriched**: Templates with relevant codebase context
- **Pattern-Adaptive**: Templates that adapt to specific design patterns
- **Relationship-Informed**: Templates that understand component relationships

### 3. Intelligent Evaluation

Enhanced evaluation using architectural insights:

```python
from evaluations.scripts.cognee_enhanced_evaluator import CogneeEnhancedEvaluator

evaluator = CogneeEnhancedEvaluator()

# Enhanced evaluation with architectural context
results = evaluator.evaluate_with_context(
    prompt_file="templates/cognee-powered/architecture-analysis.md",
    test_cases="test_cases/architecture-analysis.json",
    codebase_path="/path/to/codebase"
)

print(f"Context-aware accuracy: {results['context_accuracy']:.2%}")
print(f"Pattern recognition score: {results['pattern_score']:.2f}")
print(f"Architectural alignment: {results['architecture_alignment']:.2f}")
```

## Using Cognee Features

### Architecture Detection

Automatically detect architectural patterns in your codebase:

```python
from evaluations.scripts.cognee_mcp_integration_utils import detect_architecture

# Detect architecture pattern
architecture_info = detect_architecture("/path/to/codebase")

print(f"Primary architecture: {architecture_info['primary_pattern']}")
print(f"Secondary patterns: {architecture_info['secondary_patterns']}")
print(f"Confidence: {architecture_info['confidence']:.2%}")

# Architecture-specific insights
insights = architecture_info['insights']
for insight in insights:
    print(f"- {insight['type']}: {insight['description']}")
```

**Supported architecture patterns:**
- Monolithic applications
- Microservices architecture
- Layered/N-tier architecture
- Event-driven architecture
- Component-based architecture
- MVC/MVP/MVVM patterns

### Knowledge Graph Exploration

Explore the generated knowledge graph:

```python
from evaluations.scripts.cognee_mcp_integration_utils import explore_knowledge_graph

# Search knowledge graph
search_results = explore_knowledge_graph(
    query="Find all classes related to user authentication",
    search_type="CODE"
)

for result in search_results:
    print(f"Component: {result['name']}")
    print(f"Type: {result['type']}")
    print(f"Relationships: {result['relationships']}")
    print(f"Description: {result['description']}")
```

**Query types:**
- `CODE`: Search for code components and relationships
- `INSIGHTS`: Find architectural insights and patterns
- `GRAPH_COMPLETION`: Get AI responses based on graph knowledge
- `CHUNKS`: Retrieve raw code chunks

### Template Enhancement

Enhance existing templates with Cognee insights:

```python
from templates.cognee_powered.enhancer import TemplateEnhancer

enhancer = TemplateEnhancer()

# Enhance existing template
enhanced_template = enhancer.enhance(
    base_template="templates/base/bug-fixing.md",
    codebase_path="/path/to/codebase",
    enhancement_type="context_enriched"
)

# Save enhanced template
with open("templates/cognee-powered/enhanced-bug-fixing.md", "w") as f:
    f.write(enhanced_template)
```

**Enhancement types:**
- `context_enriched`: Add relevant codebase context
- `pattern_adaptive`: Adapt to detected patterns
- `relationship_informed`: Include component relationships
- `architecture_aware`: Optimize for architecture type

## Practical Examples

### Example 1: Architecture Analysis

```python
# Analyze architecture with Cognee enhancement
from demo_cognee_enhanced_evaluation import run_architecture_analysis

results = run_architecture_analysis(
    codebase_path="/path/to/microservices-app",
    output_dir="evaluations/results/cognee-architecture"
)

print("Architecture Analysis Results:")
print(f"- Detected pattern: {results['architecture_pattern']}")
print(f"- Service count: {results['service_count']}")
print(f"- Communication patterns: {results['communication_patterns']}")
print(f"- Analysis quality: {results['quality_score']:.1f}/5")
```

### Example 2: Bug Analysis Enhancement

```python
# Enhanced bug analysis with codebase context
from evaluations.scripts.cognee_enhanced_evaluator import analyze_bug_with_context

bug_analysis = analyze_bug_with_context(
    bug_description="Authentication failing intermittently",
    codebase_path="/path/to/app",
    template="templates/cognee-powered/context-enriched/bug-analysis.md"
)

print("Enhanced Bug Analysis:")
print(f"- Root cause confidence: {bug_analysis['confidence']:.2%}")
print(f"- Related components: {bug_analysis['related_components']}")
print(f"- Suggested fixes: {bug_analysis['suggested_fixes']}")
```

### Example 3: Code Generation

```python
# Context-aware code generation
from templates.cognee_powered.generator import generate_contextual_code

generated_code = generate_contextual_code(
    task="Create a new service for user notifications",
    codebase_path="/path/to/microservices",
    template="templates/cognee-powered/pattern-adaptive/service-generation.md"
)

print("Generated Service Code:")
print(generated_code['service_code'])
print(f"Architectural compliance: {generated_code['compliance_score']:.2%}")
```

## Configuration Options

### Analysis Configuration

Fine-tune Cognee analysis for your needs:

```yaml
# evaluations/config/cognee_config.yaml
analysis:
  # Scope settings
  include_patterns: ["*.py", "*.js", "*.ts", "*.java"]
  exclude_patterns: ["*/tests/*", "*/node_modules/*", "*/.git/*"]
  max_file_size: "1MB"
  max_files: 1000
  
  # Depth settings
  analysis_depth: "deep"  # shallow, medium, deep
  relationship_depth: 3
  pattern_detection: true
  documentation_analysis: true
  
  # Performance settings
  parallel_processing: true
  cache_results: true
  incremental_analysis: true
```

### Enhancement Configuration

Control template enhancement behavior:

```yaml
enhancement:
  # Template enhancement
  auto_enhance: true
  enhancement_types:
    - context_enriched
    - pattern_adaptive
    - architecture_aware
  
  # Context injection
  context_injection:
    max_context_length: 2000
    relevance_threshold: 0.7
    include_examples: true
  
  # Pattern adaptation
  pattern_adaptation:
    detect_patterns: true
    adapt_instructions: true
    include_pattern_context: true
```

## Advanced Features

### Custom Knowledge Models

Define custom graph models for specific domains:

```python
# Create custom knowledge model
custom_model = """
class CustomCodeAnalysisModel:
    def __init__(self):
        self.node_types = [
            "Service", "Controller", "Model", "Repository",
            "Utility", "Configuration", "Test"
        ]
        self.relationship_types = [
            "depends_on", "implements", "uses", "calls",
            "configures", "tests", "extends"
        ]
    
    def analyze(self, code_component):
        # Custom analysis logic
        pass
"""

# Use custom model
analysis_results = cognee_integration.analyze_with_custom_model(
    codebase_path="/path/to/codebase",
    model_definition=custom_model
)
```

### Real-Time Enhancement

Enable real-time template enhancement based on codebase changes:

```python
from templates.cognee_powered.realtime import RealtimeEnhancer

# Set up real-time enhancement
enhancer = RealtimeEnhancer(
    watch_directory="/path/to/codebase",
    template_directory="templates/cognee-powered/",
    auto_regenerate=True
)

# Start watching for changes
enhancer.start_watching()

print("Real-time enhancement active...")
print("Templates will auto-update when codebase changes")
```

### Performance Optimization

Optimize Cognee integration for large codebases:

```yaml
performance:
  # Caching strategy
  cache_strategy: "aggressive"  # conservative, moderate, aggressive
  cache_ttl: 3600  # 1 hour
  
  # Processing optimization
  batch_size: 100
  max_concurrent: 5
  timeout: 300
  
  # Memory management
  max_memory_usage: "2GB"
  cleanup_interval: 300
  
  # Incremental updates
  incremental_analysis: true
  change_detection: true
  smart_invalidation: true
```

## Troubleshooting

### Common Issues

**Cognee Connection Issues**

```bash
# Test Cognee connectivity
python -c "
from evaluations.scripts.test_cognee_integration import test_connection
test_connection()
"
```

**Analysis Failures**

```python
# Debug analysis issues
from evaluations.scripts.cognee_mcp_integration_utils import debug_analysis

debug_info = debug_analysis(
    codebase_path="/path/to/problematic/codebase",
    verbose=True
)

print(f"Issues found: {len(debug_info['issues'])}")
for issue in debug_info['issues']:
    print(f"- {issue['type']}: {issue['description']}")
    print(f"  Solution: {issue['suggested_fix']}")
```

**Performance Issues**

```yaml
# Optimize for large codebases
performance_config:
  # Reduce analysis scope
  max_files: 500
  exclude_patterns: ["*/vendor/*", "*/dist/*", "*/build/*"]
  
  # Use shallow analysis
  analysis_depth: "shallow"
  
  # Enable aggressive caching
  cache_strategy: "aggressive"
  incremental_analysis: true
```

### Getting Help

1. **Check Logs**: `tail -f voyager4.log | grep -i cognee`
2. **Test Integration**: Use built-in diagnostic scripts
3. **Verify Configuration**: Ensure all settings are correct
4. **Update Dependencies**: `pip install --upgrade cognee`

## Best Practices

### Effective Usage

1. **Start Small**: Begin with focused analysis on key components
2. **Iterate Gradually**: Expand analysis scope as understanding improves
3. **Cache Aggressively**: Use caching for large codebases
4. **Monitor Performance**: Track analysis time and resource usage
5. **Validate Results**: Cross-check AI insights with manual review

### Integration Workflow

```bash
# Recommended workflow
# 1. Initial analysis
python evaluations/scripts/cognee_mcp_integration_utils.py analyze /path/to/codebase

# 2. Generate enhanced templates
python templates/cognee_powered/generator.py --codebase /path/to/codebase

# 3. Evaluate enhanced templates
python evaluations/scripts/cognee_enhanced_evaluator.py --enhanced-templates

# 4. Compare with baseline
python evaluations/scripts/compare_prompts.py --baseline base/ --variant cognee-powered/
```

### Quality Assurance

- **Verify Insights**: Cross-check Cognee analysis with manual code review
- **Test Enhancements**: Compare enhanced vs. baseline templates
- **Monitor Accuracy**: Track improvement in evaluation metrics
- **Validate Context**: Ensure injected context is relevant and accurate

---

**Ready to enhance your prompts with AI?** Start with our [Cognee Enhancement Tutorial](../tutorials/cognee_enhancement.md) or explore [Integration Examples](../examples/integration_examples.md).

*Need help with specific Cognee features? Check our [API Reference](../api_reference/cognee_api.md) or [Cognee Documentation](https://docs.cognee.ai).*