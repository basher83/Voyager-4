#!/usr/bin/env python3
"""
Codebase Intelligent Prompt Generator

This module creates context-aware prompts based on codebase analysis using Cognee's 
code graph pipeline. It extracts architectural patterns, dependencies, and relationships
to generate specialized prompt templates that understand the specific codebase structure.
"""

import asyncio
import json
import os
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
import logging
from dataclasses import dataclass, asdict
import re
from collections import defaultdict

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    import anthropic
    import numpy as np
    from tqdm import tqdm
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)


@dataclass
class ArchitecturalPattern:
    """Represents an identified architectural pattern in the codebase."""
    name: str
    description: str
    evidence: List[str]
    confidence: float
    components: List[str]
    relationships: List[str]
    implications: List[str]


@dataclass
class CodebaseInsight:
    """Represents insights extracted from codebase analysis."""
    architecture_type: str
    primary_languages: List[str]
    frameworks: List[str]
    dependencies: Dict[str, str]
    patterns: List[ArchitecturalPattern]
    module_structure: Dict[str, Any]
    complexity_metrics: Dict[str, float]
    documentation_coverage: float
    testing_patterns: List[str]


@dataclass
class PromptTemplate:
    """Represents a generated prompt template."""
    name: str
    template_type: str
    content: str
    variables: List[str]
    use_cases: List[str]
    specializations: Dict[str, str]
    metadata: Dict[str, Any]


class PromptIntelligenceGenerator:
    """
    Main class for generating intelligent, context-aware prompts based on 
    codebase analysis using Cognee's code graph capabilities.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the prompt intelligence generator."""
        self.config = self._load_config(config_path)
        self.logger = logging.getLogger(__name__)
        
        # Initialize state
        self.codebase_insights: Optional[CodebaseInsight] = None
        self.generated_templates: List[PromptTemplate] = []
        self.optimization_suggestions: List[str] = []
        
        # Template paths
        self.template_root = Path(__file__).parent.parent.parent / "templates"
        self.cognee_templates_dir = self.template_root / "cognee-powered"
        
        # Knowledge storage
        self.knowledge_data = {}
        self.search_queries = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration for prompt generation."""
        default_config = {
            "analysis": {
                "min_confidence_threshold": 0.6,
                "max_patterns_per_category": 5,
                "complexity_thresholds": {
                    "low": 0.3,
                    "medium": 0.6,
                    "high": 0.8
                }
            },
            "templates": {
                "base_template_dir": "templates/base",
                "output_dir": "templates/generated",
                "supported_types": [
                    "architecture_analysis",
                    "bug_fixing",
                    "code_generation", 
                    "refactoring",
                    "testing",
                    "documentation"
                ]
            },
            "cognee": {
                "enable_code_graph": True,
                "search_types": ["CODE", "INSIGHTS", "GRAPH_COMPLETION"],
                "analysis_depth": "comprehensive"
            },
            "optimization": {
                "enable_auto_optimization": True,
                "learning_rate": 0.1,
                "feedback_integration": True
            }
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = yaml.safe_load(f)
                    default_config.update(user_config)
            except Exception as e:
                self.logger.warning(f"Failed to load config from {config_path}: {e}")
        
        return default_config
    
    async def analyze_codebase(self, repo_path: str) -> CodebaseInsight:
        """
        Analyze codebase using Cognee's code graph pipeline and extract insights.
        """
        self.logger.info(f"Starting codebase analysis for: {repo_path}")
        
        try:
            # Prepare codebase for analysis
            codebase_info = await self._prepare_codebase_analysis(repo_path)
            
            # Store data for Cognee MCP processing
            self.knowledge_data["codebase_analysis"] = codebase_info
            
            # Use Cognee MCP integration if available
            if self.config.get("cognee", {}).get("enable_code_graph", False):
                self.logger.info("Attempting to use Cognee MCP integration for enhanced analysis")
                try:
                    # This would be called via MCP in Claude Code environment
                    # For now, we'll prepare the data and note it in the insights
                    cognee_data = self.prepare_cognee_data()
                    self.knowledge_data["cognee_formatted"] = cognee_data
                    self.logger.info("Cognee data prepared for MCP processing")
                except Exception as e:
                    self.logger.warning(f"Cognee MCP integration not available: {e}")
            
            # Extract insights from prepared data
            insights = await self._extract_codebase_insights(codebase_info)
            self.codebase_insights = insights
            
            self.logger.info("Codebase analysis completed successfully")
            return insights
            
        except Exception as e:
            self.logger.error(f"Codebase analysis failed: {e}")
            raise
    
    async def _prepare_codebase_analysis(self, repo_path: str) -> Dict[str, Any]:
        """Prepare codebase data for Cognee analysis."""
        repo_path = Path(repo_path)
        
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        codebase_info = {
            "repo_path": str(repo_path.absolute()),
            "timestamp": datetime.now().isoformat(),
            "structure": {},
            "files": {},
            "metadata": {}
        }
        
        # Analyze repository structure
        structure_analysis = await self._analyze_repository_structure(repo_path)
        codebase_info["structure"] = structure_analysis
        
        # Collect file information
        files_analysis = await self._analyze_files(repo_path)
        codebase_info["files"] = files_analysis
        
        # Extract metadata
        metadata = await self._extract_repository_metadata(repo_path)
        codebase_info["metadata"] = metadata
        
        return codebase_info
    
    def prepare_cognee_data(self) -> str:
        """Prepare codebase data for Cognee processing."""
        if not self.knowledge_data.get("codebase_analysis"):
            return ""
        
        codebase_info = self.knowledge_data["codebase_analysis"]
        
        formatted_text = f"""
# Codebase Analysis for Intelligent Prompt Generation

## Repository Information
- **Path**: {codebase_info['repo_path']}
- **Analysis Date**: {codebase_info['timestamp']}
- **Primary Language**: {codebase_info['metadata'].get('primary_language', 'Unknown')}
- **Framework**: {codebase_info['metadata'].get('framework', 'Unknown')}

## Repository Structure
"""
        
        # Add structure information
        structure = codebase_info.get("structure", {})
        for component, details in structure.items():
            formatted_text += f"""
### {component.title()}
- **Count**: {details.get('count', 0)}
- **Types**: {', '.join(details.get('types', []))}
- **Main Files**: {', '.join(details.get('main_files', [])[:5])}
"""
        
        # Add file analysis
        files = codebase_info.get("files", {})
        formatted_text += f"""
## File Analysis Summary
- **Total Files**: {files.get('total_count', 0)}
- **Code Files**: {files.get('code_count', 0)}
- **Test Files**: {files.get('test_count', 0)}
- **Documentation Files**: {files.get('doc_count', 0)}

### Key Components Identified:
"""
        
        for category, file_list in files.get("by_category", {}).items():
            if file_list:
                formatted_text += f"- **{category.title()}**: {len(file_list)} files\n"
        
        # Add metadata
        metadata = codebase_info.get("metadata", {})
        formatted_text += f"""
## Technical Metadata
- **Dependencies**: {len(metadata.get('dependencies', {}))} identified
- **Frameworks**: {', '.join(metadata.get('frameworks', []))}
- **Architecture Patterns**: {', '.join(metadata.get('patterns', []))}
- **Complexity Score**: {metadata.get('complexity_score', 'Not calculated')}

## Context for Prompt Generation
This codebase analysis will be used to generate context-aware prompts that understand:
1. The specific architectural patterns used in this codebase
2. The technology stack and framework conventions
3. The module organization and dependency structure
4. The testing and documentation patterns
5. The complexity level and development patterns

The goal is to create prompts that can provide more accurate, contextual assistance for working with this specific codebase.
"""
        
        return formatted_text
    
    async def _analyze_repository_structure(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze the high-level structure of the repository."""
        structure = {
            "directories": {"count": 0, "types": [], "main_dirs": []},
            "modules": {"count": 0, "types": [], "main_modules": []},
            "packages": {"count": 0, "types": [], "main_packages": []},
            "configuration": {"count": 0, "types": [], "main_files": []}
        }
        
        try:
            # Count directories and identify types
            for item in repo_path.rglob("*"):
                if item.is_dir() and not item.name.startswith('.'):
                    structure["directories"]["count"] += 1
                    structure["directories"]["main_dirs"].append(str(item.relative_to(repo_path)))
                    
                    # Identify directory types
                    dir_name = item.name.lower()
                    if any(word in dir_name for word in ['test', 'spec']):
                        if "tests" not in structure["directories"]["types"]:
                            structure["directories"]["types"].append("tests")
                    elif any(word in dir_name for word in ['doc', 'docs']):
                        if "documentation" not in structure["directories"]["types"]:
                            structure["directories"]["types"].append("documentation")
                    elif any(word in dir_name for word in ['src', 'lib', 'app']):
                        if "source" not in structure["directories"]["types"]:
                            structure["directories"]["types"].append("source")
            
            # Limit main directories list
            structure["directories"]["main_dirs"] = structure["directories"]["main_dirs"][:10]
            
            # Identify configuration files
            config_patterns = ['*.json', '*.yaml', '*.yml', '*.toml', '*.ini', '*.cfg', '*.conf']
            for pattern in config_patterns:
                for config_file in repo_path.glob(pattern):
                    if config_file.is_file():
                        structure["configuration"]["count"] += 1
                        structure["configuration"]["main_files"].append(config_file.name)
                        
                        # Identify config types
                        if config_file.suffix.lower() in ['.json', '.yaml', '.yml']:
                            if "yaml_json" not in structure["configuration"]["types"]:
                                structure["configuration"]["types"].append("yaml_json")
                        elif config_file.suffix.lower() in ['.toml', '.ini', '.cfg']:
                            if "ini_toml" not in structure["configuration"]["types"]:
                                structure["configuration"]["types"].append("ini_toml")
            
            return structure
            
        except Exception as e:
            self.logger.error(f"Error analyzing repository structure: {e}")
            return structure
    
    async def _analyze_files(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze files in the repository."""
        files_analysis = {
            "total_count": 0,
            "code_count": 0,
            "test_count": 0,
            "doc_count": 0,
            "by_category": defaultdict(list),
            "languages": defaultdict(int),
            "file_sizes": {"small": 0, "medium": 0, "large": 0}
        }
        
        try:
            # Define file categories
            code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rs', '.rb', '.php'}
            test_patterns = ['test_', '_test', '.test.', '.spec.', '/tests/', '/test/']
            doc_extensions = {'.md', '.rst', '.txt', '.doc', '.docx'}
            
            for file_path in repo_path.rglob("*"):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    files_analysis["total_count"] += 1
                    
                    # Categorize by extension
                    extension = file_path.suffix.lower()
                    if extension:
                        files_analysis["languages"][extension] += 1
                    
                    # Categorize by type
                    file_str = str(file_path).lower()
                    relative_path = str(file_path.relative_to(repo_path))
                    
                    if extension in code_extensions:
                        files_analysis["code_count"] += 1
                        files_analysis["by_category"]["code"].append(relative_path)
                        
                        # Check if it's a test file
                        if any(pattern in file_str for pattern in test_patterns):
                            files_analysis["test_count"] += 1
                            files_analysis["by_category"]["tests"].append(relative_path)
                    
                    elif extension in doc_extensions:
                        files_analysis["doc_count"] += 1
                        files_analysis["by_category"]["documentation"].append(relative_path)
                    
                    # File size categorization
                    try:
                        size = file_path.stat().st_size
                        if size < 1024:  # < 1KB
                            files_analysis["file_sizes"]["small"] += 1
                        elif size < 10240:  # < 10KB
                            files_analysis["file_sizes"]["medium"] += 1
                        else:
                            files_analysis["file_sizes"]["large"] += 1
                    except OSError:
                        pass
            
            return files_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing files: {e}")
            return files_analysis
    
    async def _extract_repository_metadata(self, repo_path: Path) -> Dict[str, Any]:
        """Extract metadata about the repository."""
        metadata = {
            "primary_language": "Unknown",
            "framework": "Unknown",
            "dependencies": {},
            "frameworks": [],
            "patterns": [],
            "complexity_score": 0.0
        }
        
        try:
            # Detect primary language from file extensions
            language_counts = defaultdict(int)
            for file_path in repo_path.rglob("*"):
                if file_path.is_file() and file_path.suffix:
                    ext = file_path.suffix.lower()
                    if ext in {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rs', '.rb', '.php'}:
                        language_counts[ext] += 1
            
            if language_counts:
                primary_ext = max(language_counts, key=language_counts.get)
                language_map = {
                    '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
                    '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.cs': 'C#',
                    '.go': 'Go', '.rs': 'Rust', '.rb': 'Ruby', '.php': 'PHP'
                }
                metadata["primary_language"] = language_map.get(primary_ext, "Unknown")
            
            # Detect frameworks and dependencies
            await self._detect_frameworks_and_dependencies(repo_path, metadata)
            
            # Detect architectural patterns
            await self._detect_architectural_patterns(repo_path, metadata)
            
            # Calculate complexity score
            metadata["complexity_score"] = await self._calculate_complexity_score(repo_path)
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error extracting repository metadata: {e}")
            return metadata
    
    async def _detect_frameworks_and_dependencies(self, repo_path: Path, metadata: Dict[str, Any]):
        """Detect frameworks and dependencies in the repository."""
        try:
            # Check for Python dependencies
            requirements_files = ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile']
            for req_file in requirements_files:
                req_path = repo_path / req_file
                if req_path.exists():
                    metadata["frameworks"].extend(await self._parse_python_dependencies(req_path))
            
            # Check for JavaScript dependencies
            package_json = repo_path / 'package.json'
            if package_json.exists():
                metadata["frameworks"].extend(await self._parse_js_dependencies(package_json))
            
            # Check for common framework indicators
            framework_indicators = {
                'Django': ['manage.py', 'settings.py', 'django'],
                'Flask': ['app.py', 'flask'],
                'FastAPI': ['fastapi', 'uvicorn'],
                'React': ['react', 'jsx', 'tsx'],
                'Vue': ['vue', '.vue'],
                'Angular': ['angular', '@angular'],
                'Express': ['express', 'app.js'],
                'Spring': ['pom.xml', 'spring'],
                'Laravel': ['composer.json', 'laravel']
            }
            
            for framework, indicators in framework_indicators.items():
                if await self._check_framework_indicators(repo_path, indicators):
                    if framework not in metadata["frameworks"]:
                        metadata["frameworks"].append(framework)
            
        except Exception as e:
            self.logger.error(f"Error detecting frameworks: {e}")
    
    async def _parse_python_dependencies(self, file_path: Path) -> List[str]:
        """Parse Python dependency files to extract framework information."""
        frameworks = []
        try:
            if file_path.name == 'requirements.txt':
                with open(file_path, 'r') as f:
                    for line in f:
                        line = line.strip().lower()
                        if 'django' in line:
                            frameworks.append('Django')
                        elif 'flask' in line:
                            frameworks.append('Flask')
                        elif 'fastapi' in line:
                            frameworks.append('FastAPI')
                        elif 'tornado' in line:
                            frameworks.append('Tornado')
        except Exception as e:
            self.logger.warning(f"Error parsing {file_path}: {e}")
        
        return frameworks
    
    async def _parse_js_dependencies(self, package_json: Path) -> List[str]:
        """Parse package.json to extract JavaScript framework information."""
        frameworks = []
        try:
            with open(package_json, 'r') as f:
                data = json.load(f)
                
                dependencies = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                
                for dep in dependencies:
                    dep_lower = dep.lower()
                    if 'react' in dep_lower:
                        frameworks.append('React')
                    elif 'vue' in dep_lower:
                        frameworks.append('Vue')
                    elif 'angular' in dep_lower:
                        frameworks.append('Angular')
                    elif 'express' in dep_lower:
                        frameworks.append('Express')
                    elif 'next' in dep_lower:
                        frameworks.append('Next.js')
                    elif 'nuxt' in dep_lower:
                        frameworks.append('Nuxt.js')
        except Exception as e:
            self.logger.warning(f"Error parsing package.json: {e}")
        
        return frameworks
    
    async def _check_framework_indicators(self, repo_path: Path, indicators: List[str]) -> bool:
        """Check if framework indicators exist in the repository."""
        try:
            for indicator in indicators:
                # Check for files
                if '.' in indicator:
                    if list(repo_path.rglob(indicator)):
                        return True
                else:
                    # Check for mentions in files or directory names
                    for file_path in repo_path.rglob("*"):
                        if indicator.lower() in str(file_path).lower():
                            return True
            return False
        except Exception:
            return False
    
    async def _detect_architectural_patterns(self, repo_path: Path, metadata: Dict[str, Any]):
        """Detect architectural patterns in the repository."""
        patterns = []
        
        try:
            # Check for MVC pattern
            mvc_indicators = ['models', 'views', 'controllers']
            if all(any(repo_path.rglob(f"*{indicator}*")) for indicator in mvc_indicators):
                patterns.append("MVC")
            
            # Check for microservices pattern
            docker_files = list(repo_path.rglob("Dockerfile")) + list(repo_path.rglob("docker-compose*"))
            if docker_files and len(list(repo_path.rglob("*/requirements.txt"))) > 1:
                patterns.append("Microservices")
            
            # Check for layered architecture
            layer_indicators = ['services', 'repositories', 'data', 'business', 'presentation']
            layer_count = sum(1 for layer in layer_indicators if any(repo_path.rglob(f"*{layer}*")))
            if layer_count >= 3:
                patterns.append("Layered Architecture")
            
            # Check for API pattern
            api_indicators = ['api', 'endpoints', 'routes', 'handlers']
            if any(any(repo_path.rglob(f"*{api}*")) for api in api_indicators):
                patterns.append("REST API")
            
            metadata["patterns"] = patterns
            
        except Exception as e:
            self.logger.error(f"Error detecting architectural patterns: {e}")
    
    async def _calculate_complexity_score(self, repo_path: Path) -> float:
        """Calculate a simple complexity score for the repository."""
        try:
            total_files = 0
            total_size = 0
            code_files = 0
            
            for file_path in repo_path.rglob("*"):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    total_files += 1
                    try:
                        size = file_path.stat().st_size
                        total_size += size
                        
                        if file_path.suffix in {'.py', '.js', '.ts', '.java', '.cpp', '.c'}:
                            code_files += 1
                    except OSError:
                        pass
            
            # Simple complexity calculation based on file count, size, and code ratio
            if total_files == 0:
                return 0.0
            
            file_complexity = min(total_files / 100, 1.0)  # Normalize to 0-1
            size_complexity = min(total_size / (1024 * 1024), 1.0)  # Normalize to 0-1 (1MB)
            code_ratio = code_files / total_files if total_files > 0 else 0
            
            complexity = (file_complexity * 0.4 + size_complexity * 0.3 + code_ratio * 0.3)
            return round(complexity, 2)
            
        except Exception as e:
            self.logger.error(f"Error calculating complexity: {e}")
            return 0.0
    
    async def _extract_codebase_insights(self, codebase_info: Dict[str, Any]) -> CodebaseInsight:
        """Extract structured insights from codebase analysis data."""
        metadata = codebase_info.get("metadata", {})
        structure = codebase_info.get("structure", {})
        files = codebase_info.get("files", {})
        
        # Create architectural patterns
        patterns = []
        for pattern_name in metadata.get("patterns", []):
            pattern = ArchitecturalPattern(
                name=pattern_name,
                description=f"Detected {pattern_name} pattern in codebase structure",
                evidence=[f"Found in repository structure analysis"],
                confidence=0.7,  # Default confidence
                components=[],
                relationships=[],
                implications=[f"Code organization follows {pattern_name} principles"]
            )
            patterns.append(pattern)
        
        # Extract complexity metrics
        complexity_metrics = {
            "overall_complexity": metadata.get("complexity_score", 0.0),
            "file_count_complexity": min(files.get("total_count", 0) / 100, 1.0),
            "structure_complexity": len(structure.get("directories", {}).get("types", [])) / 5
        }
        
        # Create insights object
        insights = CodebaseInsight(
            architecture_type=patterns[0].name if patterns else "Unknown",
            primary_languages=[metadata.get("primary_language", "Unknown")],
            frameworks=metadata.get("frameworks", []),
            dependencies=metadata.get("dependencies", {}),
            patterns=patterns,
            module_structure=structure,
            complexity_metrics=complexity_metrics,
            documentation_coverage=files.get("doc_count", 0) / max(files.get("total_count", 1), 1),
            testing_patterns=["Unit Testing"] if files.get("test_count", 0) > 0 else []
        )
        
        return insights
    
    def prepare_search_queries(self) -> Dict[str, str]:
        """Prepare search queries for Cognee analysis."""
        if not self.codebase_insights:
            return {}
        
        queries = {
            "architectural_patterns": f"""
            Analyze the architectural patterns in this codebase:
            - Primary architecture: {self.codebase_insights.architecture_type}
            - Patterns detected: {[p.name for p in self.codebase_insights.patterns]}
            - Framework: {', '.join(self.codebase_insights.frameworks)}
            
            Provide insights about:
            1. How these patterns affect code organization
            2. Best practices for working with this architecture
            3. Common challenges with this pattern
            4. Optimal prompt strategies for this codebase
            """,
            
            "component_relationships": f"""
            Analyze the component relationships in this codebase:
            - Languages: {', '.join(self.codebase_insights.primary_languages)}
            - Module structure complexity: {self.codebase_insights.complexity_metrics.get('structure_complexity', 0)}
            - Testing coverage: {len(self.codebase_insights.testing_patterns)} patterns identified
            
            Provide insights about:
            1. How components interact in this codebase
            2. Key integration points and dependencies
            3. Testing strategies that work best here
            4. Code generation patterns that fit this structure
            """,
            
            "technology_stack": f"""
            Analyze the technology stack in this codebase:
            - Primary languages: {', '.join(self.codebase_insights.primary_languages)}
            - Frameworks: {', '.join(self.codebase_insights.frameworks)}
            - Complexity level: {self.codebase_insights.complexity_metrics.get('overall_complexity', 0)}
            
            Provide insights about:
            1. Technology-specific best practices
            2. Framework conventions and patterns
            3. Common development patterns in this stack
            4. Prompt templates that work best with these technologies
            """
        }
        
        self.search_queries = queries
        return queries
    
    async def generate_context_aware_prompts(self, prompt_types: Optional[List[str]] = None) -> List[PromptTemplate]:
        """
        Generate context-aware prompt templates based on codebase analysis.
        """
        if not self.codebase_insights:
            raise ValueError("Codebase analysis must be completed before generating prompts")
        
        if prompt_types is None:
            prompt_types = self.config["templates"]["supported_types"]
        
        self.logger.info(f"Generating {len(prompt_types)} context-aware prompt templates")
        
        generated_templates = []
        
        for prompt_type in prompt_types:
            try:
                template = await self._generate_template_for_type(prompt_type)
                if template:
                    generated_templates.append(template)
                    self.logger.info(f"Generated template: {template.name}")
                    
            except Exception as e:
                self.logger.error(f"Failed to generate template for {prompt_type}: {e}")
        
        self.generated_templates = generated_templates
        return generated_templates
    
    async def _generate_template_for_type(self, prompt_type: str) -> Optional[PromptTemplate]:
        """Generate a specific prompt template type based on codebase insights."""
        
        template_generators = {
            "architecture_analysis": self._generate_architecture_analysis_template,
            "bug_fixing": self._generate_bug_fixing_template,
            "code_generation": self._generate_code_generation_template,
            "refactoring": self._generate_refactoring_template,
            "testing": self._generate_testing_template,
            "documentation": self._generate_documentation_template
        }
        
        generator = template_generators.get(prompt_type)
        if not generator:
            self.logger.warning(f"No generator found for template type: {prompt_type}")
            return None
        
        return await generator()
    
    async def _generate_architecture_analysis_template(self) -> PromptTemplate:
        """Generate an architecture analysis template based on codebase insights."""
        
        insights = self.codebase_insights
        primary_pattern = insights.patterns[0] if insights.patterns else None
        
        # Build context-specific instructions
        architecture_context = f"""
## Codebase-Specific Context

**Architecture Type**: {insights.architecture_type}
**Primary Language**: {', '.join(insights.primary_languages)}
**Frameworks**: {', '.join(insights.frameworks) if insights.frameworks else 'None detected'}
**Complexity Level**: {self._get_complexity_level(insights.complexity_metrics['overall_complexity'])}
"""
        
        if primary_pattern:
            architecture_context += f"""
**Primary Pattern**: {primary_pattern.name}
**Pattern Implications**: {', '.join(primary_pattern.implications)}
"""
        
        # Build specialized instructions based on detected patterns
        specialized_instructions = self._build_pattern_specific_instructions(insights.patterns)
        
        # Build technology-specific guidance
        tech_guidance = self._build_technology_guidance(insights.primary_languages, insights.frameworks)
        
        template_content = f"""# Context-Aware Architecture Analysis

You are an expert software architect analyzing a codebase with deep understanding of the specific architectural patterns, technology stack, and organizational structure discovered in this repository.

{architecture_context}

## Intelligence-Enhanced Analysis Instructions

### 1. Pattern-Aware Analysis
{specialized_instructions}

### 2. Technology-Specific Insights
{tech_guidance}

### 3. Codebase-Specific Analysis Steps

#### Phase 1: Validate Discovered Patterns
- Confirm the presence of **{primary_pattern.name if primary_pattern else 'detected patterns'}** in the codebase
- Assess how well the implementation follows pattern conventions
- Identify any deviations or customizations from standard patterns

#### Phase 2: Technology Stack Assessment
- Analyze **{', '.join(insights.primary_languages)}** code quality and conventions
- Evaluate **{', '.join(insights.frameworks) if insights.frameworks else 'framework usage'}** implementation
- Assess integration between different technology components

#### Phase 3: Structural Quality Evaluation
- Review module organization (complexity: {insights.complexity_metrics['overall_complexity']:.2f})
- Analyze component relationships and dependencies
- Evaluate testing coverage (patterns: {', '.join(insights.testing_patterns) if insights.testing_patterns else 'None detected'})

## Output Format

```markdown
## Architecture Analysis Report

### Discovered Pattern Validation
**Primary Pattern**: {primary_pattern.name if primary_pattern else 'Unknown'}
- **Implementation Quality**: [Excellent/Good/Fair/Poor]
- **Pattern Adherence**: [High/Medium/Low]
- **Customizations**: [List any deviations or customizations]

### Technology Stack Assessment
**Languages**: {', '.join(insights.primary_languages)}
**Frameworks**: {', '.join(insights.frameworks) if insights.frameworks else 'None'}
- **Code Quality**: [Assessment of language-specific code quality]
- **Framework Usage**: [How well frameworks are utilized]
- **Integration**: [How well different technologies work together]

### Structural Analysis
**Complexity Metrics**:
- Overall Complexity: {insights.complexity_metrics['overall_complexity']:.2f}
- Documentation Coverage: {insights.documentation_coverage:.1%}

**Strengths**:
- [List architectural strengths based on pattern analysis]

**Improvement Areas**:
- [List specific improvements based on detected patterns and complexity]

### Recommendations
**Immediate Actions**:
1. [Specific recommendation based on pattern analysis]
2. [Technology-specific improvement]

**Long-term Improvements**:
1. [Strategic architectural enhancement]
2. [Pattern evolution recommendation]
```

## Context Variables
- **CODEBASE_PATH**: {{CODEBASE_PATH}}
- **ANALYSIS_FOCUS**: {{ANALYSIS_FOCUS}}
- **TARGET_AUDIENCE**: {{TARGET_AUDIENCE}}

---
**Codebase to analyze:**
"""
        
        return PromptTemplate(
            name=f"architecture_analysis_{insights.architecture_type.lower()}",
            template_type="architecture_analysis",
            content=template_content,
            variables=["CODEBASE_PATH", "ANALYSIS_FOCUS", "TARGET_AUDIENCE"],
            use_cases=[
                "Codebase architecture review",
                "Technical debt assessment",
                "Architecture migration planning"
            ],
            specializations={
                "pattern_focus": primary_pattern.name if primary_pattern else "General",
                "technology_stack": ', '.join(insights.primary_languages),
                "complexity_level": self._get_complexity_level(insights.complexity_metrics['overall_complexity'])
            },
            metadata={
                "generated_from": "codebase_analysis",
                "confidence": primary_pattern.confidence if primary_pattern else 0.5,
                "insights_used": len(insights.patterns),
                "generation_timestamp": datetime.now().isoformat()
            }
        )
    
    async def _generate_bug_fixing_template(self) -> PromptTemplate:
        """Generate a bug fixing template based on codebase insights."""
        insights = self.codebase_insights
        
        # Build technology-specific debugging approaches
        debug_strategies = self._build_debug_strategies(insights.primary_languages, insights.frameworks)
        
        # Build pattern-specific debugging guidance
        pattern_debug_guidance = self._build_pattern_debug_guidance(insights.patterns)
        
        template_content = f"""# Context-Aware Bug Fixing Assistant

You are an expert debugger with deep knowledge of **{', '.join(insights.primary_languages)}** and **{', '.join(insights.frameworks) if insights.frameworks else 'the frameworks'}** used in this codebase.

## Codebase Context
- **Architecture**: {insights.architecture_type}
- **Primary Language**: {', '.join(insights.primary_languages)}
- **Frameworks**: {', '.join(insights.frameworks) if insights.frameworks else 'None detected'}
- **Complexity**: {self._get_complexity_level(insights.complexity_metrics['overall_complexity'])}
- **Testing Patterns**: {', '.join(insights.testing_patterns) if insights.testing_patterns else 'None detected'}

## Technology-Specific Debugging Strategies
{debug_strategies}

## Pattern-Specific Debugging Guidance
{pattern_debug_guidance}

## Debugging Protocol

### Phase 1: Context-Aware Analysis
1. **Understand the codebase architecture** ({insights.architecture_type})
2. **Identify the component layer** where the bug occurs
3. **Consider framework-specific behaviors** ({', '.join(insights.frameworks) if insights.frameworks else 'general patterns'})
4. **Check for pattern-specific anti-patterns**

### Phase 2: Systematic Investigation
1. **Analyze error symptoms** in context of {', '.join(insights.primary_languages)} specifics
2. **Trace execution flow** through architectural layers
3. **Examine component interactions** and dependencies
4. **Review framework-specific configurations** and setup

### Phase 3: Solution Development
1. **Apply technology best practices** for {', '.join(insights.primary_languages)}
2. **Follow architectural patterns** ({insights.architecture_type})
3. **Ensure framework compatibility** 
4. **Validate with existing test patterns**

## Output Format

```markdown
## Bug Analysis Report

### Problem Classification
- **Error Type**: [Runtime/Logic/Configuration/Integration]
- **Component Layer**: [Presentation/Business/Data/Infrastructure]
- **Severity**: [Critical/High/Medium/Low]

### Context Analysis
- **Architecture Impact**: [How this affects the {insights.architecture_type} pattern]
- **Framework Considerations**: [Relevant to {', '.join(insights.frameworks) if insights.frameworks else 'current stack'}]
- **Technology Specifics**: [Language-specific considerations for {', '.join(insights.primary_languages)}]

### Root Cause Analysis
- **Primary Cause**: [Detailed explanation]
- **Contributing Factors**: [Secondary issues]
- **Pattern Violations**: [Any architectural pattern violations]

### Solution Implementation
**Immediate Fix**:
```{insights.primary_languages[0].lower() if insights.primary_languages else 'code'}
// Context-aware fix implementation
```

**Testing Strategy**:
- [How to test this fix given the existing testing patterns]
- [Framework-specific testing approaches]

**Prevention Measures**:
- [How to prevent similar issues in this architecture]
- [Pattern-specific best practices]
```

## Variables
- **BUG_DESCRIPTION**: {{BUG_DESCRIPTION}}
- **ERROR_MESSAGE**: {{ERROR_MESSAGE}}
- **COMPONENT**: {{COMPONENT}}

---
**Bug to analyze:**
"""
        
        return PromptTemplate(
            name=f"bug_fixing_{insights.primary_languages[0].lower() if insights.primary_languages else 'general'}",
            template_type="bug_fixing",
            content=template_content,
            variables=["BUG_DESCRIPTION", "ERROR_MESSAGE", "COMPONENT"],
            use_cases=[
                "Runtime error debugging",
                "Logic error analysis",
                "Framework-specific issue resolution"
            ],
            specializations={
                "primary_language": insights.primary_languages[0] if insights.primary_languages else "Unknown",
                "framework_focus": insights.frameworks[0] if insights.frameworks else "General",
                "architecture_pattern": insights.architecture_type
            },
            metadata={
                "generated_from": "codebase_analysis",
                "debug_strategies_count": len(insights.primary_languages) + len(insights.frameworks),
                "testing_patterns": len(insights.testing_patterns),
                "generation_timestamp": datetime.now().isoformat()
            }
        )
    
    async def _generate_code_generation_template(self) -> PromptTemplate:
        """Generate a code generation template based on codebase insights."""
        insights = self.codebase_insights
        
        # Build language-specific generation guidelines
        generation_guidelines = self._build_generation_guidelines(insights.primary_languages, insights.frameworks)
        
        # Build pattern-specific code structure guidance
        structure_guidance = self._build_structure_guidance(insights.patterns)
        
        template_content = f"""# Context-Aware Code Generation Assistant

You are an expert developer specializing in **{', '.join(insights.primary_languages)}** with deep knowledge of **{', '.join(insights.frameworks) if insights.frameworks else 'the architectural patterns'}** used in this codebase.

## Codebase Context
- **Architecture**: {insights.architecture_type}
- **Primary Language**: {', '.join(insights.primary_languages)}
- **Frameworks**: {', '.join(insights.frameworks) if insights.frameworks else 'None detected'}
- **Patterns**: {[p.name for p in insights.patterns] if insights.patterns else 'None detected'}
- **Complexity**: {self._get_complexity_level(insights.complexity_metrics['overall_complexity'])}

## Language & Framework Guidelines
{generation_guidelines}

## Architecture-Specific Structure Guidelines
{structure_guidance}

## Code Generation Protocol

### Phase 1: Architecture Integration Analysis
1. **Identify target layer** in {insights.architecture_type} architecture
2. **Determine component relationships** and dependencies
3. **Plan integration points** with existing codebase
4. **Consider framework conventions** and patterns

### Phase 2: Implementation Planning
1. **Follow established patterns** from codebase analysis
2. **Apply language best practices** for {', '.join(insights.primary_languages)}
3. **Integrate with existing structure** and conventions
4. **Plan testing approach** based on detected patterns

### Phase 3: Code Generation
1. **Generate implementation** following architectural patterns
2. **Add appropriate documentation** (current coverage: {insights.documentation_coverage:.1%})
3. **Include test scaffolding** if testing patterns exist
4. **Ensure framework compatibility** and conventions

## Output Format

```markdown
## Code Generation Plan

### Architecture Integration
- **Target Component**: [Which architectural layer/component]
- **Integration Points**: [How it connects to existing code]
- **Dependencies**: [Required dependencies and imports]

### Implementation Strategy
- **Pattern Compliance**: [How it follows {insights.architecture_type}]
- **Framework Integration**: [How it uses {', '.join(insights.frameworks) if insights.frameworks else 'existing patterns'}]
- **Testing Approach**: [How to test in this codebase context]

### Generated Code

```{insights.primary_languages[0].lower() if insights.primary_languages else 'code'}
# Context-aware implementation
# Follows {insights.architecture_type} pattern
# Integrates with {', '.join(insights.frameworks) if insights.frameworks else 'existing structure'}

// Implementation here
```

### Integration Instructions
1. **File Placement**: [Where to place the generated code]
2. **Dependencies**: [What needs to be imported/installed]
3. **Configuration**: [Any framework-specific configuration needed]
4. **Testing**: [How to test the generated code]

### Next Steps
- [How to extend this implementation]
- [Integration with existing components]
- [Framework-specific considerations]
```

## Variables
- **FEATURE_DESCRIPTION**: {{FEATURE_DESCRIPTION}}
- **COMPONENT_TYPE**: {{COMPONENT_TYPE}}
- **INTEGRATION_REQUIREMENTS**: {{INTEGRATION_REQUIREMENTS}}

---
**Feature to implement:**
"""
        
        return PromptTemplate(
            name=f"code_generation_{insights.architecture_type.lower().replace(' ', '_')}",
            template_type="code_generation",
            content=template_content,
            variables=["FEATURE_DESCRIPTION", "COMPONENT_TYPE", "INTEGRATION_REQUIREMENTS"],
            use_cases=[
                "New feature implementation",
                "Component scaffolding",
                "Pattern-compliant code generation"
            ],
            specializations={
                "architecture_pattern": insights.architecture_type,
                "primary_framework": insights.frameworks[0] if insights.frameworks else "None",
                "language_focus": ', '.join(insights.primary_languages)
            },
            metadata={
                "generated_from": "codebase_analysis",
                "pattern_count": len(insights.patterns),
                "framework_count": len(insights.frameworks),
                "generation_timestamp": datetime.now().isoformat()
            }
        )
    
    async def _generate_refactoring_template(self) -> PromptTemplate:
        """Generate a refactoring template based on codebase insights."""
        insights = self.codebase_insights
        
        # Build refactoring strategies based on patterns and complexity
        refactoring_strategies = self._build_refactoring_strategies(insights)
        
        template_content = f"""# Context-Aware Refactoring Assistant

You are an expert refactoring specialist with deep knowledge of **{insights.architecture_type}** architecture and **{', '.join(insights.primary_languages)}** optimization techniques.

## Codebase Context
- **Architecture**: {insights.architecture_type}
- **Complexity Level**: {self._get_complexity_level(insights.complexity_metrics['overall_complexity'])} (Score: {insights.complexity_metrics['overall_complexity']:.2f})
- **Patterns**: {[p.name for p in insights.patterns] if insights.patterns else 'General patterns'}
- **Languages**: {', '.join(insights.primary_languages)}
- **Frameworks**: {', '.join(insights.frameworks) if insights.frameworks else 'None detected'}

## Refactoring Strategies
{refactoring_strategies}

## Refactoring Protocol

### Phase 1: Architecture-Aware Analysis
1. **Assess current implementation** against {insights.architecture_type} principles
2. **Identify pattern violations** or anti-patterns
3. **Evaluate complexity impact** (current level: {self._get_complexity_level(insights.complexity_metrics['overall_complexity'])})
4. **Consider framework constraints** and best practices

### Phase 2: Refactoring Planning
1. **Prioritize improvements** based on architectural impact
2. **Plan incremental changes** to maintain stability
3. **Identify testing requirements** for validation
4. **Consider integration effects** on existing components

### Phase 3: Implementation Strategy
1. **Apply pattern-specific improvements**
2. **Optimize for {', '.join(insights.primary_languages)} best practices**
3. **Maintain framework compatibility**
4. **Preserve existing functionality** and interfaces

## Output Format

```markdown
## Refactoring Analysis

### Current State Assessment
- **Architecture Compliance**: [How well it follows {insights.architecture_type}]
- **Pattern Adherence**: [Assessment against detected patterns]
- **Complexity Analysis**: [Impact on overall complexity: {insights.complexity_metrics['overall_complexity']:.2f}]
- **Framework Integration**: [How it aligns with {', '.join(insights.frameworks) if insights.frameworks else 'current structure'}]

### Refactoring Opportunities
**High Priority**:
1. [Architecture-specific improvement]
2. [Pattern-compliance enhancement]

**Medium Priority**:
1. [Code quality improvement]
2. [Framework optimization]

**Low Priority**:
1. [Style and convention improvements]

### Implementation Plan

**Step 1: Architecture Alignment**
```{insights.primary_languages[0].lower() if insights.primary_languages else 'code'}
// Refactored implementation
// Follows {insights.architecture_type} pattern
// Improves compliance with detected patterns
```

**Step 2: Testing Strategy**
- [How to test the refactored code]
- [Regression testing approach]
- [Integration testing considerations]

**Step 3: Migration Plan**
- [How to safely deploy the refactoring]
- [Rollback strategy]
- [Monitoring approach]

### Risk Assessment
- **Breaking Changes**: [Potential impacts]
- **Framework Compatibility**: [Compatibility considerations]
- **Performance Impact**: [Expected performance changes]

### Success Metrics
- [How to measure refactoring success]
- [Architecture quality improvements]
- [Complexity reduction targets]
```

## Variables
- **CODE_TO_REFACTOR**: {{CODE_TO_REFACTOR}}
- **REFACTORING_GOALS**: {{REFACTORING_GOALS}}
- **CONSTRAINTS**: {{CONSTRAINTS}}

---
**Code to refactor:**
"""
        
        return PromptTemplate(
            name=f"refactoring_{insights.architecture_type.lower().replace(' ', '_')}",
            template_type="refactoring",
            content=template_content,
            variables=["CODE_TO_REFACTOR", "REFACTORING_GOALS", "CONSTRAINTS"],
            use_cases=[
                "Legacy code modernization",
                "Architecture compliance improvement",
                "Performance optimization"
            ],
            specializations={
                "architecture_focus": insights.architecture_type,
                "complexity_level": self._get_complexity_level(insights.complexity_metrics['overall_complexity']),
                "pattern_focus": ', '.join([p.name for p in insights.patterns])
            },
            metadata={
                "generated_from": "codebase_analysis",
                "complexity_score": insights.complexity_metrics['overall_complexity'],
                "patterns_considered": len(insights.patterns),
                "generation_timestamp": datetime.now().isoformat()
            }
        )
    
    async def _generate_testing_template(self) -> PromptTemplate:
        """Generate a testing template based on codebase insights."""
        insights = self.codebase_insights
        
        # Build testing strategies based on detected patterns and frameworks
        testing_strategies = self._build_testing_strategies(insights)
        
        template_content = f"""# Context-Aware Testing Assistant

You are an expert testing engineer with deep knowledge of **{', '.join(insights.primary_languages)}** testing frameworks and **{insights.architecture_type}** testing patterns.

## Codebase Testing Context
- **Architecture**: {insights.architecture_type}
- **Primary Languages**: {', '.join(insights.primary_languages)}
- **Frameworks**: {', '.join(insights.frameworks) if insights.frameworks else 'None detected'}
- **Existing Test Patterns**: {', '.join(insights.testing_patterns) if insights.testing_patterns else 'None detected'}
- **Complexity**: {self._get_complexity_level(insights.complexity_metrics['overall_complexity'])}

## Architecture-Specific Testing Strategies
{testing_strategies}

## Testing Protocol

### Phase 1: Test Strategy Planning
1. **Analyze component architecture** in {insights.architecture_type} context
2. **Identify testing layers** and boundaries
3. **Plan test types** based on complexity level
4. **Consider framework-specific testing** approaches

### Phase 2: Test Design
1. **Design unit tests** for individual components
2. **Plan integration tests** for component interactions
3. **Define end-to-end tests** for user workflows
4. **Include performance tests** if complexity warrants

### Phase 3: Test Implementation
1. **Follow language-specific** testing conventions for {', '.join(insights.primary_languages)}
2. **Use appropriate frameworks** and tools
3. **Implement pattern-specific** test structures
4. **Include mocking strategies** for dependencies

## Output Format

```markdown
## Test Strategy & Implementation

### Test Architecture
- **Testing Layers**: [Unit/Integration/E2E strategy for {insights.architecture_type}]
- **Test Types**: [Based on {self._get_complexity_level(insights.complexity_metrics['overall_complexity'])} complexity]
- **Framework Tools**: [Testing tools for {', '.join(insights.frameworks) if insights.frameworks else 'current stack'}]

### Test Categories

**Unit Tests**
```{insights.primary_languages[0].lower() if insights.primary_languages else 'code'}
// Unit test implementation
// Following {insights.architecture_type} testing patterns
// Using appropriate testing framework for {', '.join(insights.primary_languages)}
```

**Integration Tests**
```{insights.primary_languages[0].lower() if insights.primary_languages else 'code'}
// Integration test implementation
// Testing component interactions
// Framework-specific integration testing
```

**End-to-End Tests**
```{insights.primary_languages[0].lower() if insights.primary_languages else 'code'}
// E2E test implementation
// Full workflow testing
// Architecture-aware test scenarios
```

### Test Data & Mocking
- **Test Data Strategy**: [How to manage test data]
- **Mocking Approach**: [What and how to mock]
- **Environment Setup**: [Test environment configuration]

### Quality Metrics
- **Coverage Targets**: [Based on codebase complexity]
- **Performance Thresholds**: [Expected performance criteria]
- **Quality Gates**: [When tests should pass/fail]

### Execution Strategy
- **Test Runner**: [Recommended test execution approach]
- **CI/CD Integration**: [How to integrate with deployment pipeline]
- **Reporting**: [Test result reporting and analysis]
```

## Variables
- **COMPONENT_TO_TEST**: {{COMPONENT_TO_TEST}}
- **TEST_SCENARIOS**: {{TEST_SCENARIOS}}
- **TESTING_GOALS**: {{TESTING_GOALS}}

---
**Component/feature to test:**
"""
        
        return PromptTemplate(
            name=f"testing_{insights.primary_languages[0].lower() if insights.primary_languages else 'general'}",
            template_type="testing",
            content=template_content,
            variables=["COMPONENT_TO_TEST", "TEST_SCENARIOS", "TESTING_GOALS"],
            use_cases=[
                "Test suite development",
                "Legacy code test coverage",
                "Framework-specific testing"
            ],
            specializations={
                "testing_frameworks": ', '.join(insights.testing_patterns) if insights.testing_patterns else "General",
                "architecture_pattern": insights.architecture_type,
                "complexity_level": self._get_complexity_level(insights.complexity_metrics['overall_complexity'])
            },
            metadata={
                "generated_from": "codebase_analysis",
                "existing_test_patterns": len(insights.testing_patterns),
                "complexity_informed": True,
                "generation_timestamp": datetime.now().isoformat()
            }
        )
    
    async def _generate_documentation_template(self) -> PromptTemplate:
        """Generate a documentation template based on codebase insights."""
        insights = self.codebase_insights
        
        # Build documentation strategies based on architecture and complexity
        doc_strategies = self._build_documentation_strategies(insights)
        
        template_content = f"""# Context-Aware Documentation Assistant

You are an expert technical writer with deep understanding of **{insights.architecture_type}** architecture and **{', '.join(insights.primary_languages)}** documentation standards.

## Codebase Documentation Context
- **Architecture**: {insights.architecture_type}
- **Languages**: {', '.join(insights.primary_languages)}
- **Frameworks**: {', '.join(insights.frameworks) if insights.frameworks else 'None detected'}
- **Current Coverage**: {insights.documentation_coverage:.1%}
- **Complexity**: {self._get_complexity_level(insights.complexity_metrics['overall_complexity'])}
- **Patterns**: {[p.name for p in insights.patterns] if insights.patterns else 'General patterns'}

## Documentation Strategies
{doc_strategies}

## Documentation Protocol

### Phase 1: Architecture-Aware Documentation Planning
1. **Map documentation** to {insights.architecture_type} layers
2. **Identify key components** requiring documentation
3. **Plan documentation types** based on complexity
4. **Consider framework-specific** documentation needs

### Phase 2: Content Strategy
1. **Document architectural decisions** and patterns
2. **Explain component interactions** and dependencies
3. **Provide usage examples** and best practices
4. **Include troubleshooting guides** for common issues

### Phase 3: Implementation Guidelines
1. **Follow language-specific** documentation conventions
2. **Use appropriate documentation** formats and tools
3. **Include code examples** and diagrams
4. **Maintain consistency** with existing documentation

## Output Format

```markdown
## Documentation Plan & Content

### Documentation Architecture
- **Documentation Types**: [API/User/Developer/Architecture docs]
- **Target Audiences**: [Developers/Users/Maintainers]
- **Coverage Strategy**: [Current: {insights.documentation_coverage:.1%}, Target: ____%]

### Architecture Documentation

#### System Overview
**Architecture Pattern**: {insights.architecture_type}
- **Components**: [Key architectural components]
- **Interactions**: [How components communicate]
- **Data Flow**: [How data moves through the system]

#### Technical Stack
**Languages**: {', '.join(insights.primary_languages)}
**Frameworks**: {', '.join(insights.frameworks) if insights.frameworks else 'None'}
**Patterns**: {[p.name for p in insights.patterns] if insights.patterns else 'None'}

### Component Documentation

#### [Component Name]
**Purpose**: [What this component does]
**Architecture Layer**: [Which layer in {insights.architecture_type}]
**Dependencies**: [What it depends on]
**Interfaces**: [How to interact with it]

```{insights.primary_languages[0].lower() if insights.primary_languages else 'code'}
// Usage example
// Following {insights.architecture_type} patterns
// Framework-specific implementation
```

### API Documentation
[If applicable - API documentation following framework conventions]

### Developer Guide
**Setup Instructions**: [How to set up development environment]
**Coding Standards**: [Language and framework-specific standards]
**Testing Guidelines**: [How to test in this architecture]
**Deployment Process**: [How to deploy changes]

### Troubleshooting
**Common Issues**: [Architecture-specific common problems]
**Debug Strategies**: [How to debug in this stack]
**Performance Considerations**: [Performance guidelines for this complexity level]
```

## Variables
- **COMPONENT_TO_DOCUMENT**: {{COMPONENT_TO_DOCUMENT}}
- **DOCUMENTATION_TYPE**: {{DOCUMENTATION_TYPE}}
- **TARGET_AUDIENCE**: {{TARGET_AUDIENCE}}

---
**Component/system to document:**
"""
        
        return PromptTemplate(
            name=f"documentation_{insights.architecture_type.lower().replace(' ', '_')}",
            template_type="documentation",
            content=template_content,
            variables=["COMPONENT_TO_DOCUMENT", "DOCUMENTATION_TYPE", "TARGET_AUDIENCE"],
            use_cases=[
                "API documentation",
                "Architecture documentation",
                "Developer onboarding guides"
            ],
            specializations={
                "architecture_focus": insights.architecture_type,
                "language_conventions": ', '.join(insights.primary_languages),
                "current_coverage": f"{insights.documentation_coverage:.1%}"
            },
            metadata={
                "generated_from": "codebase_analysis",
                "current_coverage": insights.documentation_coverage,
                "architecture_informed": True,
                "generation_timestamp": datetime.now().isoformat()
            }
        )
    
    # Helper methods for template generation
    
    def _get_complexity_level(self, score: float) -> str:
        """Convert complexity score to human-readable level."""
        thresholds = self.config["analysis"]["complexity_thresholds"]
        if score < thresholds["low"]:
            return "Low"
        elif score < thresholds["medium"]:
            return "Medium"
        elif score < thresholds["high"]:
            return "High"
        else:
            return "Very High"
    
    def _build_pattern_specific_instructions(self, patterns: List[ArchitecturalPattern]) -> str:
        """Build instructions specific to detected architectural patterns."""
        if not patterns:
            return "- Apply general architectural analysis principles\n- Focus on code organization and structure"
        
        instructions = []
        for pattern in patterns:
            instructions.append(f"""
**{pattern.name} Pattern Analysis**:
- {pattern.description}
- Key implications: {', '.join(pattern.implications)}
- Look for: {', '.join(pattern.evidence) if pattern.evidence else 'standard pattern implementations'}
""")
        
        return '\n'.join(instructions)
    
    def _build_technology_guidance(self, languages: List[str], frameworks: List[str]) -> str:
        """Build technology-specific guidance."""
        guidance = []
        
        for lang in languages:
            lang_guidance = {
                'Python': "- Follow PEP 8 standards and Python idioms\n- Consider asyncio patterns and context managers\n- Analyze package structure and imports",
                'JavaScript': "- Follow ESLint standards and modern ES6+ patterns\n- Consider async/await and promise patterns\n- Analyze module structure and dependencies",
                'TypeScript': "- Analyze type definitions and interfaces\n- Consider generic patterns and type safety\n- Evaluate module and namespace organization",
                'Java': "- Follow Java coding conventions and design patterns\n- Analyze package structure and access modifiers\n- Consider inheritance and interface usage",
                'C++': "- Analyze header/implementation separation\n- Consider RAII and modern C++ patterns\n- Evaluate memory management patterns"
            }
            
            guidance.append(lang_guidance.get(lang, f"- Apply {lang} best practices and conventions"))
        
        for framework in frameworks:
            framework_guidance = {
                'Django': "- Analyze models, views, templates separation\n- Consider middleware and URL routing patterns",
                'Flask': "- Analyze route organization and blueprint usage\n- Consider application factory patterns",
                'React': "- Analyze component hierarchy and state management\n- Consider hooks and context patterns",
                'Vue': "- Analyze component structure and composition API\n- Consider store patterns and routing",
                'Express': "- Analyze middleware chain and route organization\n- Consider error handling patterns"
            }
            
            guidance.append(framework_guidance.get(framework, f"- Apply {framework} best practices"))
        
        return '\n'.join(guidance)
    
    def _build_debug_strategies(self, languages: List[str], frameworks: List[str]) -> str:
        """Build debugging strategies specific to technologies."""
        strategies = []
        
        for lang in languages:
            lang_strategies = {
                'Python': """
**Python Debugging Strategies**:
- Use pdb/ipdb for interactive debugging
- Leverage logging with appropriate levels
- Check for common Python gotchas (mutable defaults, late binding)
- Analyze stack traces and exception chains
""",
                'JavaScript': """
**JavaScript Debugging Strategies**:
- Use browser DevTools and console debugging
- Check for async/await and promise-related issues
- Analyze scope and closure behavior
- Consider timing and event-related bugs
""",
                'TypeScript': """
**TypeScript Debugging Strategies**:
- Check type errors and compilation issues
- Use TypeScript-aware debugging tools
- Analyze type inference and generic constraints
- Consider type assertion and narrowing issues
"""
            }
            strategies.append(lang_strategies.get(lang, f"Apply {lang} debugging best practices"))
        
        return '\n'.join(strategies)
    
    def _build_pattern_debug_guidance(self, patterns: List[ArchitecturalPattern]) -> str:
        """Build debugging guidance specific to architectural patterns."""
        if not patterns:
            return "Apply general debugging principles and component isolation"
        
        guidance = []
        for pattern in patterns:
            pattern_guidance = {
                'MVC': "- Debug by isolating Model, View, and Controller layers\n- Check data flow between components\n- Verify controller routing and view rendering",
                'Microservices': "- Debug service-to-service communication\n- Check API contracts and data serialization\n- Analyze distributed tracing and logging",
                'Layered Architecture': "- Debug layer by layer from top to bottom\n- Check data transformation between layers\n- Verify layer boundaries and dependencies"
            }
            
            guidance.append(f"**{pattern.name} Debugging**:\n{pattern_guidance.get(pattern.name, f'Apply {pattern.name} specific debugging approaches')}")
        
        return '\n'.join(guidance)
    
    def _build_generation_guidelines(self, languages: List[str], frameworks: List[str]) -> str:
        """Build code generation guidelines for specific technologies."""
        guidelines = []
        
        for lang in languages:
            lang_guidelines = {
                'Python': """
**Python Code Generation Guidelines**:
- Follow PEP 8 formatting and naming conventions
- Use type hints for better code clarity
- Implement proper error handling with specific exceptions
- Include docstrings following Google or NumPy style
- Use context managers and proper resource cleanup
""",
                'JavaScript': """
**JavaScript Code Generation Guidelines**:
- Use modern ES6+ syntax and features
- Implement proper error handling with try/catch
- Follow consistent naming conventions (camelCase)
- Include JSDoc comments for documentation
- Use async/await for asynchronous operations
""",
                'TypeScript': """
**TypeScript Code Generation Guidelines**:
- Define proper interfaces and types
- Use generic types where appropriate
- Implement strict type checking
- Include comprehensive type documentation
- Follow TypeScript best practices for null safety
"""
            }
            guidelines.append(lang_guidelines.get(lang, f"Follow {lang} best practices and conventions"))
        
        return '\n'.join(guidelines)
    
    def _build_structure_guidance(self, patterns: List[ArchitecturalPattern]) -> str:
        """Build structure guidance based on architectural patterns."""
        if not patterns:
            return "Follow general software engineering principles for code organization"
        
        guidance = []
        for pattern in patterns:
            pattern_guidance = {
                'MVC': """
**MVC Structure Guidelines**:
- Place business logic in Models
- Keep Views focused on presentation
- Use Controllers for request/response handling
- Maintain clear separation of concerns
""",
                'Microservices': """
**Microservices Structure Guidelines**:
- Design for service independence
- Implement proper API contracts
- Use appropriate data persistence per service
- Include health checks and monitoring
""",
                'Layered Architecture': """
**Layered Architecture Guidelines**:
- Respect layer boundaries and dependencies
- Keep layer interfaces clean and minimal
- Implement proper abstraction at each layer
- Avoid layer violations and shortcuts
"""
            }
            
            guidance.append(pattern_guidance.get(pattern.name, f"Follow {pattern.name} structural principles"))
        
        return '\n'.join(guidance)
    
    def _build_refactoring_strategies(self, insights: CodebaseInsight) -> str:
        """Build refactoring strategies based on codebase insights."""
        strategies = []
        
        complexity_level = self._get_complexity_level(insights.complexity_metrics['overall_complexity'])
        
        # Complexity-based strategies
        complexity_strategies = {
            'Low': "- Focus on code clarity and maintainability\n- Apply simple refactoring patterns\n- Improve documentation and naming",
            'Medium': "- Extract methods and classes for better organization\n- Implement design patterns where appropriate\n- Improve error handling and validation",
            'High': "- Break down large components into smaller ones\n- Apply SOLID principles more rigorously\n- Consider architectural pattern improvements",
            'Very High': "- Consider major architectural refactoring\n- Implement comprehensive testing before changes\n- Plan incremental refactoring approach"
        }
        
        strategies.append(f"**Complexity-Based Strategy ({complexity_level})**:\n{complexity_strategies.get(complexity_level, 'Apply general refactoring principles')}")
        
        # Pattern-based strategies
        for pattern in insights.patterns:
            pattern_strategies = {
                'MVC': "- Improve separation between Model, View, and Controller\n- Extract business logic from controllers\n- Simplify view logic and templates",
                'Microservices': "- Improve service boundaries and contracts\n- Reduce coupling between services\n- Optimize data flow and communication",
                'Layered Architecture': "- Strengthen layer boundaries\n- Reduce dependencies between layers\n- Improve abstraction levels"
            }
            
            strategy = pattern_strategies.get(pattern.name, f"Apply {pattern.name} specific refactoring approaches")
            strategies.append(f"**{pattern.name} Refactoring**:\n{strategy}")
        
        return '\n'.join(strategies)
    
    def _build_testing_strategies(self, insights: CodebaseInsight) -> str:
        """Build testing strategies based on codebase insights."""
        strategies = []
        
        # Architecture-based testing strategies
        arch_strategies = {
            'MVC': """
**MVC Testing Strategy**:
- Unit test Models independently with mock data
- Test Controllers with mock services and views  
- Test Views with mock data and user interactions
- Integration test the full MVC flow
""",
            'Microservices': """
**Microservices Testing Strategy**:
- Unit test each service in isolation
- Integration test service-to-service communication
- Contract testing for API agreements
- End-to-end testing for complete workflows
""",
            'Layered Architecture': """
**Layered Architecture Testing Strategy**:
- Test each layer independently
- Mock dependencies between layers
- Integration test layer interactions
- Validate data transformation between layers
"""
        }
        
        strategies.append(arch_strategies.get(insights.architecture_type, "Apply general testing strategies for the architecture"))
        
        # Language-specific testing approaches
        for lang in insights.primary_languages:
            lang_strategies = {
                'Python': "- Use pytest or unittest framework\n- Implement fixtures for test data\n- Use mock/patch for dependencies\n- Include property-based testing with Hypothesis",
                'JavaScript': "- Use Jest or Mocha testing frameworks\n- Implement proper mocking with sinon or jest.mock\n- Include DOM testing with Testing Library\n- Use snapshot testing for UI components",
                'TypeScript': "- Use Jest with TypeScript support\n- Include type-safe mocking strategies\n- Test type definitions and interfaces\n- Use ts-node for test execution"
            }
            
            strategies.append(f"**{lang} Testing Approach**:\n{lang_strategies.get(lang, f'Use {lang} testing best practices')}")
        
        return '\n'.join(strategies)
    
    def _build_documentation_strategies(self, insights: CodebaseInsight) -> str:
        """Build documentation strategies based on codebase insights."""
        strategies = []
        
        # Coverage-based strategy
        coverage = insights.documentation_coverage
        if coverage < 0.3:
            strategies.append("""
**Documentation Coverage Strategy (Low Coverage)**:
- Prioritize high-level architecture documentation
- Document public APIs and interfaces first
- Create quick-start guides for developers
- Focus on critical business logic documentation
""")
        elif coverage < 0.7:
            strategies.append("""
**Documentation Coverage Strategy (Medium Coverage)**:
- Fill gaps in existing documentation
- Improve consistency across documentation
- Add more detailed examples and use cases
- Include troubleshooting and FAQ sections
""")
        else:
            strategies.append("""
**Documentation Coverage Strategy (Good Coverage)**:
- Maintain and update existing documentation
- Focus on advanced topics and edge cases
- Improve discoverability and organization
- Add interactive examples and tutorials
""")
        
        # Architecture-specific documentation
        arch_strategies = {
            'MVC': "- Document the Model-View-Controller separation\n- Explain data flow and request handling\n- Include component interaction diagrams",
            'Microservices': "- Document service architecture and boundaries\n- Explain inter-service communication patterns\n- Include deployment and scaling guidelines",
            'Layered Architecture': "- Document layer responsibilities and boundaries\n- Explain data transformation between layers\n- Include architectural decision rationale"
        }
        
        strategies.append(f"**Architecture Documentation**:\n{arch_strategies.get(insights.architecture_type, 'Document architectural decisions and patterns')}")
        
        return '\n'.join(strategies)
    
    async def save_generated_templates(self, output_dir: Optional[str] = None) -> List[str]:
        """Save generated templates to the file system."""
        if not self.generated_templates:
            raise ValueError("No templates have been generated yet")
        
        if output_dir is None:
            output_dir = self.cognee_templates_dir / "generated"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        
        for template in self.generated_templates:
            # Create template file
            template_filename = f"{template.name}.md"
            template_path = output_path / template_filename
            
            with open(template_path, 'w') as f:
                f.write(template.content)
            
            # Create metadata file
            metadata_filename = f"{template.name}_metadata.json"
            metadata_path = output_path / metadata_filename
            
            metadata = {
                "template": asdict(template),
                "generation_info": {
                    "codebase_insights": asdict(self.codebase_insights) if self.codebase_insights else None,
                    "generation_timestamp": datetime.now().isoformat(),
                    "generator_config": self.config
                }
            }
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            saved_files.extend([str(template_path), str(metadata_path)])
            self.logger.info(f"Saved template: {template_path}")
        
        # Create index file
        index_path = output_path / "index.json"
        index_data = {
            "generated_templates": [
                {
                    "name": template.name,
                    "type": template.template_type,
                    "file": f"{template.name}.md",
                    "metadata_file": f"{template.name}_metadata.json",
                    "specializations": template.specializations,
                    "use_cases": template.use_cases
                }
                for template in self.generated_templates
            ],
            "generation_summary": {
                "total_templates": len(self.generated_templates),
                "codebase_analyzed": str(self.knowledge_data.get("codebase_analysis", {}).get("repo_path", "Unknown")),
                "generation_timestamp": datetime.now().isoformat(),
                "architecture_type": self.codebase_insights.architecture_type if self.codebase_insights else "Unknown"
            }
        }
        
        with open(index_path, 'w') as f:
            json.dump(index_data, f, indent=2)
        
        saved_files.append(str(index_path))
        
        self.logger.info(f"Generated {len(self.generated_templates)} templates saved to: {output_path}")
        return saved_files
    
    async def optimize_templates(self, feedback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Optimize generated templates based on usage feedback and performance data."""
        if not self.generated_templates:
            raise ValueError("No templates available for optimization")
        
        optimization_results = {
            "optimized_templates": [],
            "optimization_suggestions": [],
            "performance_improvements": {},
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info("Starting template optimization process")
        
        try:
            # Analyze template usage patterns
            usage_analysis = await self._analyze_template_usage(feedback_data)
            
            # Generate optimization suggestions
            suggestions = await self._generate_optimization_suggestions(usage_analysis)
            optimization_results["optimization_suggestions"] = suggestions
            
            # Apply automatic optimizations
            optimized_templates = await self._apply_automatic_optimizations()
            optimization_results["optimized_templates"] = optimized_templates
            
            # Calculate performance improvements
            performance_improvements = await self._calculate_performance_improvements(usage_analysis)
            optimization_results["performance_improvements"] = performance_improvements
            
            self.optimization_suggestions = suggestions
            
            self.logger.info(f"Optimization completed: {len(optimized_templates)} templates optimized")
            
        except Exception as e:
            self.logger.error(f"Template optimization failed: {e}")
            optimization_results["error"] = str(e)
        
        return optimization_results
    
    async def _analyze_template_usage(self, feedback_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how templates are being used and their effectiveness."""
        usage_analysis = {
            "template_effectiveness": {},
            "common_patterns": [],
            "performance_metrics": {},
            "user_feedback": {}
        }
        
        # Analyze each template
        for template in self.generated_templates:
            effectiveness = {
                "confidence_score": template.metadata.get("confidence", 0.5),
                "specialization_coverage": len(template.specializations),
                "use_case_diversity": len(template.use_cases),
                "complexity_alignment": self._assess_complexity_alignment(template)
            }
            
            usage_analysis["template_effectiveness"][template.name] = effectiveness
        
        # Incorporate feedback data if provided
        if feedback_data:
            usage_analysis["user_feedback"] = feedback_data
        
        return usage_analysis
    
    def _assess_complexity_alignment(self, template: PromptTemplate) -> float:
        """Assess how well a template aligns with codebase complexity."""
        if not self.codebase_insights:
            return 0.5
        
        template_complexity = template.metadata.get("complexity_score", 0.5)
        codebase_complexity = self.codebase_insights.complexity_metrics.get("overall_complexity", 0.5)
        
        # Calculate alignment score (closer complexities = better alignment)
        alignment = 1.0 - abs(template_complexity - codebase_complexity)
        return max(0.0, alignment)
    
    async def _generate_optimization_suggestions(self, usage_analysis: Dict[str, Any]) -> List[str]:
        """Generate specific optimization suggestions based on usage analysis."""
        suggestions = []
        
        # Analyze template effectiveness
        for template_name, effectiveness in usage_analysis["template_effectiveness"].items():
            confidence = effectiveness["confidence_score"]
            complexity_alignment = effectiveness["complexity_alignment"]
            
            if confidence < 0.6:
                suggestions.append(f"Template '{template_name}': Improve confidence by adding more specific examples and constraints")
            
            if complexity_alignment < 0.7:
                suggestions.append(f"Template '{template_name}': Better align with codebase complexity level")
            
            if effectiveness["use_case_diversity"] < 2:
                suggestions.append(f"Template '{template_name}': Expand use cases to cover more scenarios")
        
        # Add general optimization suggestions
        if self.codebase_insights:
            patterns_count = len(self.codebase_insights.patterns)
            if patterns_count > 3:
                suggestions.append("Consider creating more specialized templates for detected architectural patterns")
            
            if self.codebase_insights.documentation_coverage < 0.5:
                suggestions.append("Focus on documentation templates to improve codebase documentation coverage")
        
        return suggestions
    
    async def _apply_automatic_optimizations(self) -> List[str]:
        """Apply automatic optimizations to templates where possible."""
        optimized_templates = []
        
        for template in self.generated_templates:
            optimized = False
            
            # Optimize variable usage
            if len(template.variables) < 2:
                # Add common variables if missing
                common_vars = ["CONTEXT", "FOCUS", "TARGET_AUDIENCE"]
                for var in common_vars:
                    if var not in template.variables:
                        template.variables.append(var)
                        optimized = True
            
            # Optimize specializations based on codebase insights
            if self.codebase_insights and len(template.specializations) < 3:
                if "complexity_level" not in template.specializations:
                    complexity = self._get_complexity_level(self.codebase_insights.complexity_metrics['overall_complexity'])
                    template.specializations["complexity_level"] = complexity
                    optimized = True
            
            if optimized:
                optimized_templates.append(template.name)
        
        return optimized_templates
    
    async def _calculate_performance_improvements(self, usage_analysis: Dict[str, Any]) -> Dict[str, float]:
        """Calculate expected performance improvements from optimizations."""
        improvements = {
            "accuracy_improvement": 0.0,
            "efficiency_improvement": 0.0,
            "specialization_improvement": 0.0
        }
        
        # Calculate improvements based on optimization applied
        total_templates = len(self.generated_templates)
        if total_templates == 0:
            return improvements
        
        # Accuracy improvement based on confidence scores
        total_confidence = sum(
            template.metadata.get("confidence", 0.5) 
            for template in self.generated_templates
        )
        avg_confidence = total_confidence / total_templates
        improvements["accuracy_improvement"] = min(0.2, (1.0 - avg_confidence) * 0.5)
        
        # Efficiency improvement based on specialization coverage
        total_specializations = sum(
            len(template.specializations) 
            for template in self.generated_templates
        )
        avg_specializations = total_specializations / total_templates
        improvements["efficiency_improvement"] = min(0.15, avg_specializations * 0.05)
        
        # Specialization improvement based on codebase insights utilization
        if self.codebase_insights:
            insights_utilization = min(1.0, len(self.codebase_insights.patterns) * 0.2)
            improvements["specialization_improvement"] = insights_utilization * 0.1
        
        return improvements


# Async wrapper functions for CLI usage

async def analyze_and_generate_prompts(repo_path: str, prompt_types: Optional[List[str]] = None,
                                     config_path: Optional[str] = None,
                                     output_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Main function to analyze codebase and generate intelligent prompts.
    """
    generator = PromptIntelligenceGenerator(config_path)
    
    try:
        # Step 1: Analyze codebase
        print(f"🔍 Analyzing codebase: {repo_path}")
        insights = await generator.analyze_codebase(repo_path)
        
        print(f"✅ Analysis complete:")
        print(f"   - Architecture: {insights.architecture_type}")
        print(f"   - Languages: {', '.join(insights.primary_languages)}")
        print(f"   - Frameworks: {', '.join(insights.frameworks) if insights.frameworks else 'None'}")
        print(f"   - Patterns: {[p.name for p in insights.patterns]}")
        print(f"   - Complexity: {generator._get_complexity_level(insights.complexity_metrics['overall_complexity'])}")
        
        # Step 2: Generate prompts
        print(f"\n🛠️ Generating context-aware prompts...")
        templates = await generator.generate_context_aware_prompts(prompt_types)
        
        print(f"✅ Generated {len(templates)} templates:")
        for template in templates:
            print(f"   - {template.name} ({template.template_type})")
        
        # Step 3: Save templates
        print(f"\n💾 Saving templates...")
        saved_files = await generator.save_generated_templates(output_dir)
        
        print(f"✅ Templates saved to: {Path(saved_files[0]).parent}")
        
        # Step 4: Return results
        return {
            "codebase_insights": insights,
            "generated_templates": templates,
            "saved_files": saved_files,
            "cognee_data": generator.prepare_cognee_data(),
            "search_queries": generator.prepare_search_queries()
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


async def optimize_existing_templates(template_dir: str, feedback_data: Optional[Dict[str, Any]] = None,
                                    config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Optimize existing templates based on feedback and usage patterns.
    """
    generator = PromptIntelligenceGenerator(config_path)
    
    try:
        # Load existing templates
        print(f"📂 Loading templates from: {template_dir}")
        # Implementation would load existing templates
        
        # Optimize templates
        print(f"⚡ Optimizing templates...")
        optimization_results = await generator.optimize_templates(feedback_data)
        
        print(f"✅ Optimization complete:")
        print(f"   - Optimized templates: {len(optimization_results['optimized_templates'])}")
        print(f"   - Suggestions: {len(optimization_results['optimization_suggestions'])}")
        
        return optimization_results
        
    except Exception as e:
        print(f"❌ Optimization error: {e}")
        raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate intelligent, context-aware prompts from codebase analysis")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze and generate command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze codebase and generate prompts")
    analyze_parser.add_argument("repo_path", help="Path to repository to analyze")
    analyze_parser.add_argument("--types", nargs="+", 
                               choices=["architecture_analysis", "bug_fixing", "code_generation", 
                                       "refactoring", "testing", "documentation"],
                               help="Types of prompts to generate")
    analyze_parser.add_argument("--config", help="Path to configuration file")
    analyze_parser.add_argument("--output", help="Output directory for generated templates")
    
    # Optimize command  
    optimize_parser = subparsers.add_parser("optimize", help="Optimize existing templates")
    optimize_parser.add_argument("template_dir", help="Directory containing templates to optimize")
    optimize_parser.add_argument("--feedback", help="Path to feedback data JSON file")
    optimize_parser.add_argument("--config", help="Path to configuration file")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        try:
            results = asyncio.run(analyze_and_generate_prompts(
                repo_path=args.repo_path,
                prompt_types=args.types,
                config_path=args.config,
                output_dir=args.output
            ))
            
            print(f"\n🎉 Success! Generated {len(results['generated_templates'])} intelligent prompt templates")
            sys.exit(0)
            
        except Exception as e:
            print(f"\n❌ Failed: {e}")
            sys.exit(1)
    
    elif args.command == "optimize":
        try:
            feedback_data = None
            if args.feedback and Path(args.feedback).exists():
                with open(args.feedback, 'r') as f:
                    feedback_data = json.load(f)
            
            results = asyncio.run(optimize_existing_templates(
                template_dir=args.template_dir,
                feedback_data=feedback_data,
                config_path=args.config
            ))
            
            print(f"\n🎉 Optimization complete!")
            sys.exit(0)
            
        except Exception as e:
            print(f"\n❌ Optimization failed: {e}")
            sys.exit(1)
    
    else:
        parser.print_help()
        sys.exit(1)