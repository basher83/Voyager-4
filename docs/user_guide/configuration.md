# Configuration Guide

This guide covers all configuration options for Voyager-4, from basic setup to advanced customization. Learn how to optimize the framework for your specific use cases and environment.

## Configuration Overview

Voyager-4 uses a layered configuration system:

1. **Environment Variables** (`.env`): Secrets and environment-specific settings
2. **YAML Configuration** (`config/*.yaml`): Feature settings and parameters
3. **Runtime Configuration**: Programmatic configuration options
4. **Default Settings**: Built-in defaults for all options

## Environment Variables

### Core Configuration

Create a `.env` file in your project root:

```env
# Claude API Configuration
ANTHROPIC_API_KEY=your_api_key_here
CLAUDE_CODE_SDK_KEY=your_sdk_key_here

# Default Model Settings
DEFAULT_MODEL=claude-3-sonnet-20240229
DEFAULT_TEMPERATURE=0.1
DEFAULT_MAX_TOKENS=4000
DEFAULT_TIMEOUT=120

# Cognee Integration
COGNEE_API_URL=https://api.cognee.ai
COGNEE_API_KEY=your_cognee_key_here
COGNEE_CACHE_ENABLED=true

# Storage Paths
DATA_DIR=./data
RESULTS_DIR=./evaluations/results
CACHE_DIR=./data/cache
LOGS_DIR=./logs

# Performance Settings
MAX_CONCURRENT_REQUESTS=5
REQUEST_TIMEOUT=120
CACHE_TTL=3600

# Feature Flags
VOYAGER_COGNEE_ENABLED=true
VOYAGER_ADVANCED_METRICS=true
VOYAGER_PARALLEL_EVALUATION=true
VOYAGER_CACHE_ENABLED=true

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=detailed
LOG_FILE=voyager4.log
```

### Security Configuration

```env
# API Security
API_RATE_LIMIT=100
API_RETRY_ATTEMPTS=3
API_RETRY_DELAY=1.0

# Data Security
ENCRYPT_CACHE=true
SECURE_TEMP_FILES=true
AUTO_CLEANUP=true

# Network Security
VERIFY_SSL=true
PROXY_URL=http://proxy.company.com:8080
PROXY_AUTH=username:password
```

### Environment-Specific Settings

```env
# Development
ENVIRONMENT=development
DEBUG_MODE=true
VERBOSE_LOGGING=true
AUTO_RELOAD=true

# Staging
ENVIRONMENT=staging
DEBUG_MODE=false
PERFORMANCE_MONITORING=true
ALERT_THRESHOLD=0.85

# Production
ENVIRONMENT=production
DEBUG_MODE=false
PERFORMANCE_MONITORING=true
ALERT_THRESHOLD=0.90
ERROR_REPORTING=true
```

## YAML Configuration Files

### Main Configuration (`evaluations/config/default_config.yaml`)

```yaml
# Core evaluation settings
evaluation:
  # Model configuration
  model: "claude-3-sonnet-20240229"
  temperature: 0.1
  max_tokens: 4000
  timeout: 120
  
  # Evaluation methods
  methods:
    - exact_match
    - cosine_similarity
    - llm_grade
    - rouge_score
  
  # Quality thresholds
  thresholds:
    accuracy: 0.85
    consistency: 0.8
    quality: 4.0
    rouge_l: 0.6
  
  # Statistical testing
  statistical:
    confidence_level: 0.95
    min_sample_size: 30
    significance_threshold: 0.05
    use_bonferroni_correction: true
  
  # Performance settings
  performance:
    max_concurrent_requests: 5
    batch_size: 10
    request_timeout: 120
    retry_attempts: 3
    retry_delay: 1.0

# Template system configuration
templates:
  # Template paths
  base_path: "./templates"
  custom_path: "./templates/custom"
  generated_path: "./templates/generated"
  
  # Template processing
  variable_substitution: true
  validation_enabled: true
  auto_formatting: true
  
  # Template hierarchy
  hierarchy:
    - base
    - enhanced
    - advanced
    - structured
    - specialized
    - cognee-powered

# Test case configuration
test_cases:
  # Test case paths
  base_path: "./test_cases"
  examples_path: "./test_cases/examples"
  generated_path: "./test_cases/generated"
  
  # Test case processing
  validation_enabled: true
  auto_generation: false
  shuffle_order: true
  
  # Test case types
  categories:
    - codebase-understanding
    - bug-fixing
    - code-generation
    - testing
    - project-management

# Results and reporting
results:
  # Output paths
  output_dir: "./evaluations/results"
  archive_dir: "./evaluations/results/archive"
  
  # Report formats
  formats:
    - json
    - markdown
    - html
    - csv
  
  # Report content
  include_raw_data: true
  include_visualizations: true
  include_recommendations: true
  
  # Archival settings
  auto_archive: true
  archive_after_days: 30
  max_results_count: 100

# Logging configuration
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "voyager4.log"
  max_file_size: "10MB"
  backup_count: 5
  
  # Component-specific logging
  components:
    evaluation: "INFO"
    templates: "INFO"
    cognee: "DEBUG"
    api: "WARNING"
```

### Cognee Configuration (`evaluations/config/cognee_config.yaml`)

```yaml
cognee:
  # Core settings
  enabled: true
  api_url: "https://api.cognee.ai"
  api_key: null  # Use environment variable
  cache_enabled: true
  cache_ttl: 3600
  
  # Analysis settings
  analysis:
    auto_analyze: true
    analysis_depth: "deep"  # shallow, medium, deep
    include_tests: true
    include_docs: true
    include_comments: true
    
    # File filtering
    include_patterns:
      - "*.py"
      - "*.js"
      - "*.ts"
      - "*.java"
      - "*.cpp"
      - "*.c"
      - "*.h"
    
    exclude_patterns:
      - "*/tests/*"
      - "*/test/*"
      - "*/node_modules/*"
      - "*/.git/*"
      - "*/vendor/*"
      - "*/build/*"
      - "*/dist/*"
    
    # Size limits
    max_file_size: "1MB"
    max_files: 1000
    max_analysis_time: 300
  
  # Knowledge graph settings
  knowledge_graph:
    model: "KnowledgeGraph"
    node_types:
      - class
      - function
      - module
      - dependency
      - interface
      - enum
    
    relationship_types:
      - imports
      - calls
      - inherits
      - implements
      - uses
      - configures
    
    # Graph optimization
    prune_isolated_nodes: true
    merge_similar_nodes: true
    calculate_centrality: true
  
  # Template enhancement
  enhancement:
    auto_enhance: true
    enhancement_types:
      - context_enriched
      - pattern_adaptive
      - architecture_aware
      - relationship_informed
    
    # Context injection
    context_injection:
      enabled: true
      max_context_length: 2000
      relevance_threshold: 0.7
      include_examples: true
      include_patterns: true
    
    # Pattern adaptation
    pattern_adaptation:
      enabled: true
      detect_patterns: true
      adapt_instructions: true
      include_pattern_context: true
  
  # Performance settings
  performance:
    parallel_processing: true
    max_workers: 4
    chunk_size: 100
    timeout: 300
    
    # Memory management
    max_memory_usage: "2GB"
    cleanup_interval: 300
    gc_threshold: 0.8
    
    # Caching strategy
    cache_strategy: "moderate"  # conservative, moderate, aggressive
    incremental_updates: true
    smart_invalidation: true
```

### Model-Specific Configuration

```yaml
# evaluations/config/models_config.yaml
models:
  claude-3-opus:
    model_name: "claude-3-opus-20240229"
    max_tokens: 4000
    temperature: 0.1
    timeout: 180
    cost_per_token: 0.000015
    use_cases: ["complex_analysis", "creative_tasks"]
  
  claude-3-sonnet:
    model_name: "claude-3-sonnet-20240229"
    max_tokens: 4000
    temperature: 0.1
    timeout: 120
    cost_per_token: 0.000003
    use_cases: ["general_purpose", "evaluation"]
  
  claude-3-haiku:
    model_name: "claude-3-haiku-20240307"
    max_tokens: 2000
    temperature: 0.0
    timeout: 60
    cost_per_token: 0.00000025
    use_cases: ["simple_tasks", "high_volume"]

# Model selection strategy
model_selection:
  default_model: "claude-3-sonnet"
  
  # Automatic model selection
  auto_select: true
  selection_criteria:
    - task_complexity
    - response_time_requirements
    - cost_constraints
    - accuracy_requirements
  
  # Fallback strategy
  fallback_enabled: true
  fallback_order:
    - claude-3-haiku
    - claude-3-sonnet
    - claude-3-opus
```

## Runtime Configuration

### Programmatic Configuration

```python
from evaluations.config import Config, ConfigManager

# Load configuration
config = Config.load("evaluations/config/default_config.yaml")

# Override specific settings
config.evaluation.temperature = 0.0
config.evaluation.max_tokens = 2000
config.cognee.enabled = False

# Create configuration manager
config_manager = ConfigManager(config)

# Use in evaluation
from evaluations.scripts.evaluate_prompt import PromptEvaluator

evaluator = PromptEvaluator(config=config_manager)
```

### Dynamic Configuration

```python
from evaluations.config import DynamicConfig

# Create dynamic configuration
dynamic_config = DynamicConfig()

# Add environment-specific overrides
if environment == "production":
    dynamic_config.update({
        "evaluation.thresholds.accuracy": 0.95,
        "evaluation.statistical.confidence_level": 0.99,
        "logging.level": "WARNING"
    })

# Add user-specific settings
dynamic_config.update_from_user_preferences(user_id)

# Apply configuration
evaluator = PromptEvaluator(config=dynamic_config)
```

## Configuration Validation

### Schema Validation

```python
from evaluations.config.validator import ConfigValidator

validator = ConfigValidator()

# Validate configuration file
validation_result = validator.validate_file(
    "evaluations/config/default_config.yaml"
)

if not validation_result.is_valid:
    print("Configuration errors:")
    for error in validation_result.errors:
        print(f"- {error.path}: {error.message}")
```

### Runtime Validation

```python
from evaluations.config.validator import RuntimeValidator

# Validate configuration at runtime
runtime_validator = RuntimeValidator()

try:
    runtime_validator.validate_environment()
    runtime_validator.validate_api_access()
    runtime_validator.validate_file_paths()
    print("✅ Configuration validation passed")
except ValidationError as e:
    print(f"❌ Configuration error: {e}")
```

## Environment-Specific Configuration

### Development Environment

```yaml
# evaluations/config/development_config.yaml
environment: development

evaluation:
  # Faster iteration
  timeout: 60
  max_concurrent_requests: 3
  
  # Lower quality thresholds for testing
  thresholds:
    accuracy: 0.70
    consistency: 0.70
    quality: 3.5

# Enable debug features
debug:
  enabled: true
  verbose_logging: true
  save_intermediate_results: true
  include_timing_info: true

# Relaxed caching for development
cache:
  enabled: true
  ttl: 300  # 5 minutes
  invalidate_on_change: true
```

### Production Environment

```yaml
# evaluations/config/production_config.yaml
environment: production

evaluation:
  # Strict quality requirements
  thresholds:
    accuracy: 0.95
    consistency: 0.90
    quality: 4.5
  
  # Conservative timeout settings
  timeout: 180
  retry_attempts: 5

# Production monitoring
monitoring:
  enabled: true
  metrics_collection: true
  performance_alerts: true
  error_reporting: true
  
  # Alert thresholds
  alerts:
    accuracy_drop: 0.05
    latency_increase: 2.0
    error_rate: 0.01

# Aggressive caching for performance
cache:
  enabled: true
  ttl: 7200  # 2 hours
  strategy: "aggressive"
```

## Advanced Configuration

### Custom Metrics Configuration

```yaml
# evaluations/config/custom_metrics_config.yaml
custom_metrics:
  code_quality:
    enabled: true
    weight: 0.3
    components:
      - syntax_validity
      - style_compliance
      - test_coverage
      - documentation_quality
    
    thresholds:
      syntax_validity: 1.0
      style_compliance: 0.8
      test_coverage: 0.7
      documentation_quality: 0.6

  domain_specific:
    enabled: true
    weight: 0.2
    evaluator_class: "CustomDomainEvaluator"
    parameters:
      domain: "fintech"
      regulations: ["PCI-DSS", "SOX"]
      risk_threshold: 0.1
```

### Integration Configuration

```yaml
# evaluations/config/integrations_config.yaml
integrations:
  github:
    enabled: true
    webhook_url: "https://api.github.com/repos/owner/repo/hooks"
    events: ["push", "pull_request"]
    quality_gates: true
  
  slack:
    enabled: true
    webhook_url: "https://hooks.slack.com/services/xxx"
    channels:
      alerts: "#voyager-alerts"
      reports: "#voyager-reports"
    
  jira:
    enabled: false
    server_url: "https://company.atlassian.net"
    project_key: "PROMPT"
    issue_type: "Task"
```

### Performance Tuning

```yaml
# evaluations/config/performance_config.yaml
performance:
  # Concurrency settings
  max_concurrent_requests: 10
  max_concurrent_evaluations: 3
  thread_pool_size: 20
  
  # Memory management
  max_memory_usage: "4GB"
  gc_threshold: 0.8
  cleanup_interval: 300
  temp_file_cleanup: true
  
  # Caching optimization
  cache:
    strategy: "adaptive"
    max_size: "1GB"
    eviction_policy: "LRU"
    compression: true
    
  # Network optimization
  connection_pool_size: 20
  keep_alive: true
  compression: true
  timeout_strategy: "exponential_backoff"
```

## Configuration Management

### Configuration Profiles

```python
from evaluations.config import ConfigProfile

# Create configuration profiles
profiles = {
    "development": ConfigProfile.load("config/development_config.yaml"),
    "staging": ConfigProfile.load("config/staging_config.yaml"),
    "production": ConfigProfile.load("config/production_config.yaml")
}

# Select profile based on environment
current_profile = profiles[os.getenv("ENVIRONMENT", "development")]

# Use profile in application
evaluator = PromptEvaluator(config=current_profile)
```

### Configuration Hot Reloading

```python
from evaluations.config import ConfigWatcher

# Set up configuration watcher
config_watcher = ConfigWatcher(
    config_files=["config/default_config.yaml", "config/cognee_config.yaml"],
    callback=lambda config: evaluator.update_config(config)
)

# Start watching for changes
config_watcher.start()

print("Configuration hot reloading enabled")
```

### Configuration Backup and Versioning

```bash
# Create configuration backup
python -m evaluations.config.backup create --name "before-production-deploy"

# List configuration versions
python -m evaluations.config.backup list

# Restore configuration
python -m evaluations.config.backup restore --name "before-production-deploy"

# Compare configurations
python -m evaluations.config.backup compare --from "v1.0" --to "v2.0"
```

## Troubleshooting Configuration

### Common Issues

**Configuration File Not Found**
```python
# Check file paths
import os
config_paths = [
    "evaluations/config/default_config.yaml",
    "evaluations/config/cognee_config.yaml"
]

for path in config_paths:
    if os.path.exists(path):
        print(f"✅ {path}")
    else:
        print(f"❌ {path} - Not found")
```

**Invalid Configuration Values**
```python
# Validate specific configuration
from evaluations.config.validator import validate_config

errors = validate_config("evaluations/config/default_config.yaml")
if errors:
    print("Configuration errors found:")
    for error in errors:
        print(f"- {error}")
```

**Environment Variable Issues**
```bash
# Check environment variables
echo "ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:+SET}"
echo "COGNEE_API_KEY: ${COGNEE_API_KEY:+SET}"
echo "DEFAULT_MODEL: $DEFAULT_MODEL"
```

### Configuration Debugging

```python
from evaluations.config.debug import ConfigDebugger

debugger = ConfigDebugger()

# Debug configuration loading
debug_info = debugger.debug_loading(
    config_file="evaluations/config/default_config.yaml"
)

print(f"Configuration loaded successfully: {debug_info.success}")
print(f"Warnings: {len(debug_info.warnings)}")
print(f"Errors: {len(debug_info.errors)}")

# Debug runtime configuration
runtime_info = debugger.debug_runtime()
print(f"Active configuration: {runtime_info.active_config}")
print(f"Environment overrides: {runtime_info.env_overrides}")
```

## Best Practices

### Configuration Organization

1. **Separate Concerns**: Use different files for different aspects
2. **Environment Isolation**: Maintain separate configs for each environment
3. **Version Control**: Track configuration changes in version control
4. **Documentation**: Document all configuration options
5. **Validation**: Always validate configuration before deployment

### Security Best Practices

1. **Use Environment Variables**: Store secrets in environment variables
2. **Encrypt Sensitive Data**: Use encryption for sensitive configuration
3. **Access Control**: Limit who can modify configuration files
4. **Audit Changes**: Track configuration changes and access
5. **Regular Rotation**: Rotate API keys and secrets regularly

### Performance Optimization

1. **Cache Configuration**: Cache loaded configuration for performance
2. **Lazy Loading**: Load configuration only when needed
3. **Profile-Based Loading**: Load only necessary configuration sections
4. **Monitoring**: Monitor configuration impact on performance
5. **Regular Review**: Regularly review and optimize configuration

---

**Ready to optimize your configuration?** Start with the [Installation Guide](installation.md) to set up your environment, then explore [Advanced Features](../developer_guide/architecture.md) for complex setups.

*Need help with specific configuration scenarios? Check our [Troubleshooting Guide](../developer_guide/troubleshooting.md) or [API Reference](../api_reference/).*