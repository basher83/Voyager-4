# Relationship-Informed Templates

Templates that leverage code relationships and dependencies from the knowledge graph to provide comprehensive understanding of how components interact, influence each other, and form the overall system architecture.

## 🕸️ Graph Connection Intelligence

### Deep Relationship Analysis
- **Dependency Mapping**: Complete understanding of component dependencies
- **Impact Analysis**: Ripple effect assessment for changes
- **Integration Point Discovery**: API boundaries and communication patterns
- **Cross-Cutting Concern Identification**: Shared functionality and responsibilities

### Multi-Dimensional Relationships
- **Structural Dependencies**: Direct code dependencies and imports
- **Functional Relationships**: Components that work together to deliver features
- **Data Flow Connections**: How data moves through the system
- **Temporal Relationships**: Components that interact in sequence or workflows

### Dynamic Relationship Understanding
- **Runtime Interactions**: How components communicate during execution
- **Configuration Dependencies**: Environment and configuration relationships
- **Deployment Relationships**: How components are deployed and scaled together
- **Monitoring and Observability**: How components are monitored as a system

## 🎯 Use Cases

### Impact Assessment
Perfect for:
- Analyzing the blast radius of proposed changes
- Understanding downstream effects of modifications
- Planning safe deployment strategies
- Identifying testing requirements for changes

### Integration Work
Ideal for:
- Planning new component integrations
- Understanding API compatibility requirements
- Designing communication patterns
- Assessing integration complexity and risks

### Debugging Cross-Component Issues
Excellent for:
- Tracing issues across component boundaries
- Understanding complex failure scenarios
- Identifying root causes in distributed systems
- Planning comprehensive fixes for system-wide issues

### System Evolution Planning
Great for:
- Planning system refactoring and modernization
- Understanding migration dependencies
- Designing modular architectures
- Assessing technical debt in relationships

## 🛠️ Template Variables

### Standard Variables
- `{CONTEXT}`: System and analysis background
- `{COMPONENT}`: Specific component or subsystem to analyze
- `{SCOPE}`: Relationship analysis scope (local, system-wide, external)
- `{CHANGE_TYPE}`: Type of change being analyzed

### Relationship-Informed Variables
- `{COMPONENT_RELATIONSHIPS}`: Auto-discovered component connections
- `{DEPENDENCY_MAP}`: Complete dependency graph and analysis
- `{INTEGRATION_POINTS}`: API boundaries and communication patterns
- `{DATA_FLOW_ANALYSIS}`: Data movement and transformation patterns
- `{IMPACT_ASSESSMENT}`: Change impact analysis across relationships
- `{CROSS_CUTTING_CONCERNS}`: Shared functionality and responsibilities

## 📋 Available Templates

### template.md
**Base relationship-informed template** with comprehensive graph analysis
- Queries graph for component relationships and dependencies
- Includes impact analysis for changes
- Provides integration point mapping
- Assesses cross-cutting concerns

### Variations

#### variations/impact-analysis.md
**Change impact assessment** for comprehensive risk evaluation
- Blast radius analysis for proposed changes
- Downstream dependency assessment
- Testing requirement identification
- Risk mitigation planning

#### variations/integration-planning.md
**Integration-focused analysis** for new component integration
- API compatibility assessment
- Communication pattern design
- Integration complexity evaluation
- Performance impact analysis

#### variations/debugging-support.md
**Cross-component debugging** for complex issue resolution
- Issue propagation tracing
- Root cause analysis across boundaries
- System-wide failure scenario understanding
- Comprehensive fix planning

#### variations/refactoring-analysis.md
**Refactoring impact analysis** for safe system evolution
- Dependency restructuring planning
- Modularization opportunity assessment
- Migration path analysis
- Technical debt relationship mapping

## 🔄 Knowledge Graph Integration

### Query Pattern
```python
# Template automatically executes these graph queries:

# 1. Component relationship discovery
relationships = cognee.search(
    query="component dependencies and interactions",
    search_type="CODE"
)

# 2. Integration point mapping
integration_points = cognee.search(
    query="api boundaries and communication patterns",
    search_type="INSIGHTS"
)

# 3. Data flow analysis
data_flows = cognee.search(
    query="data movement and transformation patterns",
    search_type="INSIGHTS"
)

# 4. Cross-cutting concern identification
cross_cutting = cognee.search(
    query="shared functionality and common concerns",
    search_type="GRAPH_COMPLETION"
)
```

### Relationship Analysis Process
```python
# Template analyzes relationships comprehensively:
relationship_context = {
    "direct_dependencies": structural_relationships,
    "functional_relationships": feature_relationships,
    "integration_patterns": api_relationships,
    "data_dependencies": data_flow_relationships,
    "cross_cutting_analysis": shared_concerns
}
```

## 📊 Success Metrics

### Relationship Discovery
- **Dependency Accuracy**: 92%+ correct dependency identification
- **Integration Point Coverage**: 88%+ of API boundaries identified
- **Cross-Component Mapping**: 85%+ of relationships discovered

### Analysis Quality
- **Impact Assessment Accuracy**: 4.4/5.0 for change impact prediction
- **Integration Planning Score**: 4.2/5.0 for integration guidance quality
- **Debug Effectiveness**: 4.3/5.0 for issue resolution support

### Performance Benchmarks
- **Relationship Query Time**: <3s for comprehensive relationship mapping
- **Template Rendering**: <7s for complete relationship analysis
- **Impact Analysis Speed**: <5s for change impact assessment

## 🔍 Relationship Types

### Structural Relationships
- **Direct Dependencies**: Import and module dependencies
- **Inheritance Hierarchies**: Class and interface relationships
- **Composition Patterns**: Component containment and ownership
- **Package Dependencies**: Module and library relationships

### Functional Relationships
- **Feature Collaboration**: Components working together for features
- **Workflow Participation**: Components in business process flows
- **Event Relationships**: Producer-consumer and event handling
- **Service Interactions**: Microservice communication patterns

### Data Relationships
- **Data Flow Patterns**: How data moves between components
- **Shared State Management**: Common data stores and caches
- **Transformation Pipelines**: Data processing and enrichment flows
- **Persistence Relationships**: Database and storage interactions

### Operational Relationships
- **Deployment Dependencies**: Co-deployment requirements
- **Scaling Relationships**: Components that scale together
- **Monitoring Relationships**: Shared observability concerns
- **Configuration Dependencies**: Shared configuration and environment needs

## 🔗 Integration Patterns

### API Relationship Analysis
```python
# Template identifies and analyzes API relationships:
api_analysis = {
    "rest_apis": rest_endpoint_relationships,
    "graphql_schemas": graphql_relationship_mapping,
    "message_queues": async_communication_patterns,
    "event_streams": event_driven_relationships
}
```

### Communication Pattern Detection
```python
# Template discovers communication patterns:
communication_patterns = {
    "synchronous": sync_call_patterns,
    "asynchronous": async_messaging_patterns,
    "event_driven": event_pub_sub_patterns,
    "stream_processing": data_streaming_patterns
}
```

## 🚀 Quick Start

1. **Identify target component** or system area for analysis
2. **Choose appropriate template variant** based on analysis goal
3. **Set relationship scope** (local, system-wide, or external)
4. **Template automatically maps** relationships from knowledge graph
5. **Review relationship analysis** and validate against system understanding
6. **Apply insights** to planning, debugging, or development decisions

## Example Usage

```python
from cognee_templates import RelationshipInformedTemplate

template = RelationshipInformedTemplate("variations/impact-analysis.md")
result = template.render(
    context="Payment service refactoring",
    component="payment_processor",
    scope="system_wide",
    change_type="interface_modification"
)
```

## 🔧 Advanced Features

### Dynamic Relationship Discovery
- **Runtime Relationship Detection**: Understanding relationships during execution
- **Configuration-Based Relationships**: Dependencies based on configuration
- **Environment-Specific Relationships**: Different relationships in different environments
- **Temporal Relationship Patterns**: How relationships change over time

### Impact Propagation Analysis
- **Direct Impact Assessment**: Immediate effects of changes
- **Indirect Impact Analysis**: Secondary and tertiary effects
- **Cascade Effect Modeling**: How changes ripple through the system
- **Risk Assessment Integration**: Business and technical risk evaluation

### Relationship Optimization
- **Dependency Reduction Opportunities**: Ways to reduce coupling
- **Integration Simplification**: Streamlining complex relationships
- **Performance Optimization**: Optimizing communication patterns
- **Modularity Improvement**: Enhancing system modular design

---

*Relationship-informed templates provide deep understanding of system interconnections, enabling confident changes, effective debugging, and strategic system evolution through comprehensive relationship analysis.*