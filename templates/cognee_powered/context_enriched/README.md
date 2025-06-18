# Context-Enriched Templates

Templates with deep semantic understanding of code purpose and business logic. These templates automatically inject relevant context from the knowledge graph to provide comprehensive understanding beyond just code structure.

## 🧠 Semantic Context Intelligence

### Deep Context Understanding
- **Business Logic Comprehension**: Understanding the "why" behind code decisions
- **Cross-Component Context**: How different parts of the system relate functionally
- **Historical Context**: Evolution of features and design decisions over time
- **Domain Knowledge Integration**: Industry-specific patterns and requirements

### Automatic Context Injection
- **Workflow Context**: Understanding business processes and user journeys
- **Feature Relationships**: How features interact and depend on each other
- **Stakeholder Requirements**: User needs and business constraints
- **Integration Context**: How the system fits into larger ecosystems

### Intent-Driven Analysis
- **Purpose Recognition**: Understanding the intended function of code components
- **Business Value Assessment**: Evaluating code changes against business objectives
- **User Impact Analysis**: How changes affect end-user experience
- **Compliance Considerations**: Regulatory and policy implications

## 🎯 Use Cases

### Feature Development
Perfect for:
- Planning new feature implementations
- Understanding feature integration requirements
- Assessing business logic complexity
- Identifying cross-cutting concerns

### Bug Analysis with Business Context
Ideal for:
- Understanding impact of bugs on business processes
- Prioritizing fixes based on business criticality
- Analyzing root causes in business workflow context
- Planning comprehensive fixes that consider downstream effects

### Code Review with Semantic Understanding
Excellent for:
- Reviewing changes against business requirements
- Ensuring code aligns with intended functionality
- Validating business logic correctness
- Checking compliance with domain requirements

### Documentation Generation
Great for:
- Creating business-focused technical documentation
- Explaining code behavior in business terms
- Generating user-impact assessments
- Creating stakeholder-friendly technical summaries

## 🛠️ Template Variables

### Standard Variables
- `{CONTEXT}`: Business and technical background
- `{FEATURE}`: Specific feature or functionality to analyze
- `{SCOPE}`: Analysis scope (feature-level, workflow, integration)
- `{STAKEHOLDERS}`: Target audience for the analysis

### Context-Enriched Variables
- `{BUSINESS_CONTEXT}`: Auto-discovered business logic and workflows
- `{FEATURE_RELATIONSHIPS}`: Feature dependencies and interactions
- `{USER_WORKFLOWS}`: User journeys and process flows
- `{DOMAIN_REQUIREMENTS}`: Industry-specific requirements and constraints
- `{COMPLIANCE_CONTEXT}`: Regulatory and policy considerations
- `{HISTORICAL_CONTEXT}`: Evolution and change history

## 📋 Available Templates

### template.md
**Base context-enriched template** with semantic understanding
- Queries graph for business context and workflows
- Includes feature relationship analysis
- Provides domain-specific insights
- Considers user impact and business value

### Variations

#### variations/feature-development.md
**Feature-focused analysis** for new development planning
- Business requirement mapping
- Feature integration planning
- User workflow considerations
- Business value assessment

#### variations/bug-impact-analysis.md
**Business-aware bug analysis** for critical issue resolution
- Business process impact assessment
- Stakeholder notification requirements
- Priority assessment based on business criticality
- Comprehensive fix planning

#### variations/workflow-optimization.md
**Business workflow optimization** for process improvement
- Current workflow analysis
- Bottleneck identification
- Optimization opportunity assessment
- Business impact projection

#### variations/compliance-review.md
**Compliance-focused analysis** for regulatory requirements
- Regulatory requirement mapping
- Compliance gap analysis
- Risk assessment and mitigation
- Audit trail considerations

## 🔄 Knowledge Graph Integration

### Query Pattern
```python
# Template automatically executes these graph queries:

# 1. Business context discovery
business_context = cognee.search(
    query="business logic workflows and processes",
    search_type="GRAPH_COMPLETION"
)

# 2. Feature relationship mapping
feature_relationships = cognee.search(
    query="feature dependencies and user workflows",
    search_type="INSIGHTS"
)

# 3. Domain requirements analysis
domain_requirements = cognee.search(
    query="domain specific requirements and constraints",
    search_type="GRAPH_COMPLETION"
)

# 4. Historical context extraction
historical_context = cognee.search(
    query="feature evolution and change history",
    search_type="INSIGHTS"
)
```

### Context Enhancement Process
```python
# Template enriches prompt with semantic understanding:
semantic_context = {
    "business_workflows": business_context,
    "feature_map": feature_relationships,
    "domain_knowledge": domain_requirements,
    "evolution_history": historical_context,
    "user_impact_analysis": user_insights
}
```

## 📊 Success Metrics

### Context Understanding
- **Business Logic Accuracy**: 88%+ correct business process identification
- **Feature Relationship Completeness**: 82%+ of feature interactions identified
- **Domain Knowledge Coverage**: 90%+ of relevant domain concepts included

### Analysis Quality
- **Business Relevance Score**: 4.3/5.0 for business value alignment
- **Stakeholder Clarity Score**: 4.5/5.0 for non-technical understanding
- **Actionability Score**: 4.2/5.0 for practical business recommendations

### Context Integration Performance
- **Context Query Time**: <2.5s for comprehensive context gathering
- **Template Rendering**: <6s for complete business-aware analysis
- **Context Relevance**: >90% of injected context rated as valuable

## 🔍 Context Types

### Business Process Context
- **Workflow Understanding**: How code supports business processes
- **Process Dependencies**: Inter-process relationships and dependencies
- **Business Rules**: Encoded business logic and validation rules
- **Process Optimization**: Opportunities for workflow improvement

### User Experience Context
- **User Journey Mapping**: How code affects user experiences
- **Interaction Patterns**: Common user behavior patterns
- **Performance Impact**: User-facing performance implications
- **Accessibility Considerations**: Inclusive design requirements

### Domain Knowledge Context
- **Industry Standards**: Relevant industry best practices
- **Regulatory Requirements**: Compliance and legal considerations
- **Domain Terminology**: Industry-specific language and concepts
- **Best Practice Guidelines**: Established domain conventions

### Stakeholder Context
- **Stakeholder Requirements**: Different stakeholder needs and priorities
- **Communication Preferences**: How to present technical information
- **Decision Criteria**: Factors that influence stakeholder decisions
- **Success Metrics**: How stakeholders measure project success

## 🚀 Quick Start

1. **Identify analysis focus** (feature, bug, workflow, compliance)
2. **Choose appropriate template variant** based on focus area
3. **Set business context variables** for your specific domain
4. **Template automatically enriches** with semantic context from knowledge graph
5. **Review and customize** the business-aware analysis
6. **Validate insights** with domain experts and stakeholders

## Example Usage

```python
from cognee_templates import ContextEnrichedTemplate

template = ContextEnrichedTemplate("variations/feature-development.md")
result = template.render(
    context="E-commerce checkout optimization",
    feature="one_click_checkout",
    scope="end_to_end_workflow",
    stakeholders="product_managers_and_users"
)
```

## 🔗 Integration Points

- **Business Analysis Tools**: Integration with business process modeling
- **User Research Data**: Connection to user behavior analytics
- **Compliance Systems**: Link to regulatory requirement databases
- **Documentation Platforms**: Export to business-focused documentation

---

*Context-enriched templates bridge the gap between technical implementation and business value, providing semantic understanding that goes beyond code structure to include business purpose and stakeholder impact.*