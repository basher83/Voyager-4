# Cognee-Enhanced Templates User Guide

This guide provides comprehensive instructions for using the AI-enhanced template system that leverages knowledge graph intelligence through Cognee integration.

## 🎯 Overview

Cognee-enhanced templates represent the next evolution in prompt engineering, combining traditional template techniques with AI-powered intelligence that:

- **Automatically discovers** patterns and relationships in your codebase
- **Adapts dynamically** based on context and feedback
- **Provides intelligent insights** from knowledge graph analysis
- **Continuously improves** through success pattern learning
- **Personalizes responses** based on user preferences and team conventions

## 🏗️ Template Categories

### 1. Architecture-Aware Templates
**Purpose**: Comprehensive architectural analysis using knowledge graph intelligence

**When to Use**:
- System design reviews and architectural assessments
- Migration planning and technical debt analysis
- Architecture documentation generation
- Component relationship mapping

**Key Features**:
- Automatic architectural pattern recognition
- Component dependency mapping
- Technology stack analysis
- Design decision context understanding

### 2. Context-Enriched Templates  
**Purpose**: Business-focused analysis with semantic understanding

**When to Use**:
- Feature development with business context
- Stakeholder communication and reporting
- Cross-functional collaboration
- Business impact assessments

**Key Features**:
- Business logic understanding
- Stakeholder perspective integration
- Domain knowledge application
- User workflow analysis

### 3. Relationship-Informed Templates
**Purpose**: System analysis based on component relationships and dependencies

**When to Use**:
- Impact assessment for changes
- Integration planning and analysis
- Debugging cross-component issues
- System dependency mapping

**Key Features**:
- Comprehensive dependency analysis
- Integration point mapping
- Change impact propagation assessment
- Cross-cutting concern identification

### 4. Pattern-Adaptive Templates
**Purpose**: Development that automatically adapts to team patterns and conventions

**When to Use**:
- New feature development
- Code refactoring for consistency
- Team onboarding and standardization
- Cross-team collaboration

**Key Features**:
- Automatic pattern recognition
- Convention compliance enforcement
- Best practice integration
- Style adaptation

### 5. Dynamic-Enhanced Templates
**Purpose**: Self-improving intelligence with continuous optimization

**When to Use**:
- Production systems requiring high performance
- Mission-critical applications
- Long-term projects with evolution needs
- High-volume processing scenarios

**Key Features**:
- Performance analytics and optimization
- Success pattern learning
- Failure mode detection and prevention
- Continuous improvement mechanisms

## 🚀 Getting Started

### Prerequisites

1. **Cognee MCP Integration**: Ensure Cognee MCP server is configured and running
2. **Knowledge Graph Data**: Have your codebase analyzed and stored in the knowledge graph
3. **Template Engine**: The Cognee template engine should be properly configured

### Basic Usage

#### 1. Using the Template Renderer

```python
from templates.cognee_powered.template_renderer import CogneeTemplateRenderer

# Initialize the renderer
renderer = CogneeTemplateRenderer()

# Render a template with context
context = {
    'CONTEXT': 'E-commerce platform analysis',
    'SCOPE': 'full_codebase',
    'FOCUS': 'scalability',
    'AUDIENCE': 'development_team'
}

result = await renderer.render_template(
    category='architecture-aware',
    context=context,
    enable_graph_enhancement=True
)

print(result['rendered_content'])
```

#### 2. Direct Engine Usage

```python
from templates.cognee_powered.engine import CogneeTemplateEngine

# Initialize the engine
engine = CogneeTemplateEngine()

# Query knowledge graph directly
graph_result = await engine.query_knowledge_graph(
    query="architectural patterns in microservices",
    search_type="INSIGHTS"
)

# Enhance context with graph insights
enhanced_context = await engine.enhance_context(
    base_context=context,
    template_category='architecture-aware'
)
```

### Template Selection Guide

| Use Case | Recommended Template | Rationale |
|----------|---------------------|-----------|
| System architecture review | architecture-aware | Needs structural understanding and pattern recognition |
| Feature planning with business context | context-enriched | Requires business logic and stakeholder considerations |
| Change impact assessment | relationship-informed | Needs dependency analysis and propagation understanding |
| Code generation with team standards | pattern-adaptive | Should follow established conventions and patterns |
| Production system optimization | dynamic-enhanced | Requires continuous improvement and performance focus |

## 📋 Template Context Variables

### Common Variables (All Templates)

```yaml
CONTEXT: "Description of the analysis or task context"
SCOPE: "Scope of analysis (component, service, full_codebase)"
```

### Architecture-Aware Specific

```yaml
FOCUS: "Primary focus area (scalability, maintainability, performance)"
AUDIENCE: "Target audience (development_team, architecture_team, stakeholders)"
```

### Context-Enriched Specific

```yaml
FEATURE: "Specific feature being analyzed"
STAKEHOLDERS: "Primary stakeholders involved"
SUCCESS_METRICS: "Key success metrics for the analysis"
```

### Relationship-Informed Specific

```yaml
COMPONENT: "Target component for relationship analysis"
CHANGE_TYPE: "Type of change being assessed"
RISK_TOLERANCE: "Risk tolerance level (low, medium, high)"
```

### Pattern-Adaptive Specific

```yaml
LANGUAGE: "Primary programming language"
TEAM_SIZE: "Size of development team"
PROJECT_PHASE: "Current project phase (development, maintenance, refactoring)"
QUALITY_LEVEL: "Required quality level (development, staging, production)"
```

### Dynamic-Enhanced Specific

```yaml
SUCCESS_METRICS: "Array of metrics to optimize for"
OPTIMIZATION_GOALS: "Specific optimization objectives"
USER_PROFILE: "User profile for personalization"
CONSTRAINTS: "Performance or resource constraints"
TIMELINE: "Timeline for optimization implementation"
```

## 🔧 Advanced Configuration

### Template Metadata Configuration

Each template category includes a `metadata.yaml` file for advanced configuration:

```yaml
# Example metadata configuration
template_configuration:
  input_variables:
    - name: "CONTEXT"
      type: "string"
      required: true
      description: "Context of the analysis"
    
quality_metrics:
  success_criteria:
    - metric: "pattern_accuracy"
      threshold: 0.85
      description: "Accuracy of pattern identification"

performance_characteristics:
  expected_response_time: "45-90 seconds"
  knowledge_graph_queries: 3
  complexity_level: "high"
```

### Cognee Integration Configuration

Configure knowledge graph integration in `evaluations/config/cognee_config.yaml`:

```yaml
cognee:
  llm_provider: 'anthropic'
  default_model: 'claude-3-haiku-20240307'

search:
  default_search_type: 'GRAPH_COMPLETION'
  max_results: 20
  similarity_threshold: 0.7

performance:
  cache_duration: 86400  # 24 hours
  use_async_processing: true
```

## 📊 Evaluation and Testing

### Running Template Evaluations

```python
# Evaluate a specific template
evaluation_result = await renderer.evaluate_template(
    category='architecture-aware',
    template_name='template.md',
    test_cases=[
        {
            'name': 'microservices_analysis',
            'context': {
                'CONTEXT': 'Microservices architecture analysis',
                'SCOPE': 'full_codebase',
                'FOCUS': 'scalability'
            }
        }
    ]
)

print(f"Success rate: {evaluation_result['success_rate']:.2%}")
```

### Integration Testing

Run the complete integration test suite:

```bash
cd /path/to/project
python evaluations/scripts/test_cognee_templates.py
```

This will test:
- Template discovery and metadata loading
- Knowledge graph query functionality
- Template rendering for all categories
- Pattern adaptation capabilities
- Dynamic enhancement features
- Batch processing and error handling
- Performance benchmarks

## 💡 Best Practices

### 1. Context Preparation

**Provide Rich Context**:
```python
# Good: Rich, specific context
context = {
    'CONTEXT': 'E-commerce checkout service in microservices architecture',
    'SCOPE': 'checkout_service',
    'FOCUS': 'performance_optimization',
    'AUDIENCE': 'senior_development_team',
    'BUSINESS_PRIORITY': 'conversion_rate_improvement'
}

# Avoid: Vague, minimal context
context = {
    'CONTEXT': 'service analysis',
    'SCOPE': 'service'
}
```

**Match Context to Template Category**:
- Architecture-aware: Focus on structural and design aspects
- Context-enriched: Include business goals and stakeholder needs  
- Relationship-informed: Specify target components and change types
- Pattern-adaptive: Include team and project characteristics
- Dynamic-enhanced: Define success metrics and optimization goals

### 2. Template Selection

**Start Simple, Scale Up**:
1. Begin with basic templates for straightforward tasks
2. Use enhanced templates for complex analysis
3. Apply dynamic templates for production systems

**Consider Performance vs. Quality Trade-offs**:
- Simple variants: Faster responses, basic analysis
- Full templates: Comprehensive analysis, longer processing time
- Efficiency-optimized variants: Balanced approach

### 3. Knowledge Graph Preparation

**Ensure Quality Data**:
- Keep knowledge graph updated with latest code changes
- Include comprehensive codebase coverage
- Maintain business context and documentation

**Optimize for Your Use Cases**:
- Focus graph content on your primary analysis needs
- Include team conventions and standards
- Document architectural decisions and patterns

### 4. Performance Optimization

**Use Caching Effectively**:
```python
# Templates automatically cache graph queries
# Adjust cache duration based on code change frequency
engine = CogneeTemplateEngine()
engine.config['performance']['cache_duration'] = 3600  # 1 hour for active development
```

**Batch Processing for Efficiency**:
```python
# Process multiple templates together
render_configs = [
    {'category': 'architecture-aware', 'context': context1},
    {'category': 'pattern-adaptive', 'context': context2}
]

batch_results = await renderer.batch_render_templates(render_configs)
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Template Not Found
```
FileNotFoundError: Template not found: category/template.md
```
**Solution**: Verify template category and filename are correct. Use `list_available_templates()` to see available options.

#### 2. Cognee Connection Issues
```
Warning: Cognee not available. Using mock data.
```
**Solution**: Ensure Cognee MCP server is running and accessible. Check network connectivity and authentication.

#### 3. Knowledge Graph Empty Results
```
No relevant information found in knowledge graph.
```
**Solution**: Verify your codebase has been analyzed and stored in the knowledge graph. Check query specificity and graph data quality.

#### 4. Performance Issues
```
Template rendering taking >120 seconds
```
**Solution**: 
- Enable caching in configuration
- Use simpler template variants for faster results
- Optimize knowledge graph queries
- Consider batch processing for multiple requests

### Debug Mode

Enable detailed logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# This will show detailed information about:
# - Knowledge graph queries and results
# - Template rendering steps
# - Performance metrics
# - Cache hit/miss information
```

## 📈 Performance Monitoring

### Key Metrics to Track

1. **Rendering Performance**:
   - Template rendering time
   - Knowledge graph query time
   - Success rate of completions

2. **Quality Metrics**:
   - Pattern recognition accuracy
   - Context relevance scores
   - User satisfaction ratings

3. **System Health**:
   - Cache hit rates
   - Error frequencies
   - Resource utilization

### Monitoring Dashboard

Access performance statistics:

```python
engine = CogneeTemplateEngine()
stats = engine.get_performance_stats()

print("Performance Statistics:")
for operation, metrics in stats.items():
    print(f"  {operation}:")
    print(f"    Average duration: {metrics['avg_duration']:.2f}s")
    print(f"    Total operations: {metrics['count']}")
```

## 🔄 Template Evolution

### Continuous Improvement

The dynamic-enhanced templates automatically improve over time through:

1. **Success Pattern Learning**: Identifies and reinforces successful approaches
2. **Failure Mode Detection**: Learns to avoid problematic patterns
3. **User Feedback Integration**: Incorporates user satisfaction and preferences
4. **Performance Optimization**: Continuously optimizes for speed and quality

### Custom Template Development

To create custom templates:

1. **Follow Template Structure**: Use existing templates as starting points
2. **Define Clear Metadata**: Specify configuration and quality metrics
3. **Test Thoroughly**: Use the evaluation framework to validate quality
4. **Document Usage**: Provide clear examples and use case descriptions

### Contributing Improvements

1. **Submit Performance Enhancements**: Optimize existing templates
2. **Add New Categories**: Create templates for new use cases
3. **Improve Knowledge Integration**: Enhance graph query strategies
4. **Extend Evaluation Coverage**: Add new test scenarios and metrics

---

*The Cognee-enhanced template system represents a new paradigm in prompt engineering, combining traditional techniques with AI-powered intelligence for superior results and continuous improvement.*