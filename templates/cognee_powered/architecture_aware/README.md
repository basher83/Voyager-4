# Architecture-Aware Templates

Templates that understand codebase architecture through knowledge graph analysis. These templates automatically query the Cognee knowledge graph to understand structural patterns, component relationships, and architectural decisions before generating responses.

## 🏗️ Core Capabilities

### Automatic Pattern Detection
- **Architectural Patterns**: MVC, microservices, component-based, layered, etc.
- **Design Patterns**: Factory, Observer, Strategy, Repository, etc.
- **Framework Patterns**: Django MVT, React component hierarchy, Spring Boot structure

### Component Analysis
- **Dependency Mapping**: Understanding how components relate and depend on each other
- **Responsibility Analysis**: What each component/module is responsible for
- **Interface Discovery**: APIs, contracts, and communication patterns

### Technology Intelligence
- **Stack Detection**: Frameworks, libraries, and tools in use
- **Version Awareness**: Understanding compatibility and upgrade paths
- **Integration Points**: External services, databases, and third-party systems

## 🎯 Use Cases

### Architecture Analysis
Perfect for:
- New team member onboarding
- Architecture documentation generation
- Technical debt assessment
- Refactoring planning

### Integration Planning
Ideal for:
- Adding new components
- Planning API integrations
- Understanding impact of changes
- Cross-team collaboration

### Code Review
Excellent for:
- Architectural compliance checking
- Pattern consistency validation
- Design decision evaluation
- Best practice enforcement

## 🛠️ Template Variables

### Standard Variables
- `{CONTEXT}`: Project background and requirements
- `{SCOPE}`: Analysis scope (full codebase, specific module, etc.)
- `{FOCUS}`: Specific architectural aspect to emphasize
- `{OUTPUT_FORMAT}`: Desired output structure

### Architecture-Aware Variables
- `{ARCHITECTURAL_PATTERNS}`: Auto-discovered patterns from knowledge graph
- `{COMPONENT_RELATIONSHIPS}`: Dependency and interaction mappings
- `{TECHNOLOGY_STACK}`: Framework and tool analysis
- `{DESIGN_DECISIONS}`: Historical architectural choices
- `{INTEGRATION_POINTS}`: External dependencies and services

## 📋 Available Templates

### template.md
**Base architecture-aware template** with knowledge graph integration
- Queries graph for architectural patterns
- Includes component relationship analysis
- Provides technology stack assessment

### Variations

#### variations/detailed-analysis.md
**Comprehensive architectural assessment** for complex systems
- Deep component analysis
- Cross-cutting concern identification
- Performance and scalability considerations

#### variations/quick-overview.md
**Rapid architectural summary** for time-sensitive analysis
- High-level pattern identification
- Key component overview
- Critical dependency highlights

#### variations/integration-focused.md
**Integration-specific analysis** for API and service planning
- Service boundary identification
- Integration pattern analysis
- API design recommendations

#### variations/migration-planning.md
**Migration and modernization assessment** for legacy systems
- Legacy pattern identification
- Modernization opportunity analysis
- Migration risk assessment

## 🔄 Knowledge Graph Integration

### Query Pattern
```python
# Template automatically executes these graph queries:

# 1. Architectural pattern discovery
patterns = cognee.search(
    query="architectural patterns and design structures",
    search_type="INSIGHTS"
)

# 2. Component relationship mapping
relationships = cognee.search(
    query="component dependencies and interactions",
    search_type="CODE"
)

# 3. Technology stack analysis
technologies = cognee.search(
    query="frameworks libraries and technology stack",
    search_type="GRAPH_COMPLETION"
)
```

### Context Enhancement
```python
# Template enriches prompt with discovered information:
enhanced_context = {
    "discovered_patterns": patterns,
    "component_map": relationships,
    "tech_stack": technologies,
    "architectural_insights": graph_insights
}
```

## 📊 Success Metrics

### Architecture Understanding
- **Pattern Recognition Accuracy**: 90%+ correct pattern identification
- **Component Mapping Completeness**: 85%+ of relationships identified
- **Technology Stack Coverage**: 95%+ of technologies detected

### Analysis Quality
- **Clarity Score**: 4.5/5.0 for explanation clarity
- **Completeness Score**: 4.2/5.0 for comprehensive coverage
- **Actionability Score**: 4.0/5.0 for practical recommendations

### Performance Benchmarks
- **Query Response Time**: <2s for graph queries
- **Template Rendering**: <5s for complete analysis
- **Accuracy Maintenance**: >95% over time with graph updates

## 🚀 Quick Start

1. **Choose template variant** based on analysis depth needed
2. **Set context variables** for your specific project
3. **Template automatically queries** knowledge graph for architectural information
4. **Review and customize** the generated analysis
5. **Validate results** against actual codebase structure

## Example Usage

```python
from cognee_templates import ArchitectureAwareTemplate

template = ArchitectureAwareTemplate("template.md")
result = template.render(
    context="Legacy e-commerce platform modernization",
    scope="full_codebase",
    focus="microservices_migration"
)
```

## 🔗 Integration Points

- **Evaluation Framework**: Full compatibility with existing metrics
- **Template Engine**: Jinja2-based with Cognee extensions
- **Knowledge Graph**: Real-time queries with caching
- **CI/CD Integration**: Automated architecture validation

---

*Architecture-aware templates bridge the gap between static documentation and dynamic code understanding, providing intelligent architectural insights powered by knowledge graph analysis.*