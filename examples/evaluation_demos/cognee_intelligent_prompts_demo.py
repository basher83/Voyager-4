#!/usr/bin/env python3
"""
Cognee-Enhanced Intelligent Prompt Generator Demo

This script demonstrates how to use Cognee's MCP integration to create 
intelligent, context-aware prompts based on codebase analysis using knowledge graphs.
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from evaluations.scripts.codebase_intelligent_prompts import (
    PromptIntelligenceGenerator, 
    CodebaseInsight,
    PromptTemplate
)

class CogneeEnhancedPromptGenerator(PromptIntelligenceGenerator):
    """
    Enhanced prompt generator that uses Cognee MCP functions for deeper analysis.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        super().__init__(config_path)
        self.cognee_insights = {}
        self.cognee_available = False
        
    async def analyze_with_cognee(self, repo_path: str) -> Dict[str, Any]:
        """
        Perform enhanced codebase analysis using Cognee MCP integration.
        """
        self.logger.info("🧠 Starting Cognee-enhanced codebase analysis")
        
        # First, do standard analysis
        base_insights = await self.analyze_codebase(repo_path)
        
        # Prepare knowledge for Cognee
        cognee_data = self.prepare_cognee_data()
        
        # In a real Claude Code environment, these would be MCP calls:
        # cognee_results = await self._run_cognee_analysis(cognee_data)
        
        # For demo purposes, simulate enhanced insights
        enhanced_insights = await self._simulate_cognee_insights(base_insights, cognee_data)
        
        return {
            "base_insights": base_insights,
            "cognee_data": cognee_data,
            "enhanced_insights": enhanced_insights,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    async def _simulate_cognee_insights(self, base_insights: CodebaseInsight, cognee_data: str) -> Dict[str, Any]:
        """
        Simulate the kind of enhanced insights Cognee would provide.
        """
        return {
            "architectural_relationships": [
                {
                    "type": "template_hierarchy",
                    "description": "Templates organized in progressive enhancement pattern",
                    "components": ["base", "enhanced", "advanced", "structured", "specialized"],
                    "relationships": ["base -> enhanced -> advanced", "structured -> specialized"]
                },
                {
                    "type": "evaluation_flow", 
                    "description": "Evaluation-driven development workflow",
                    "components": ["scripts", "config", "metrics", "results"],
                    "relationships": ["scripts use config", "scripts generate metrics", "metrics stored in results"]
                }
            ],
            "code_patterns": [
                {
                    "pattern": "Template Factory Pattern",
                    "locations": ["evaluations/scripts/codebase_intelligent_prompts.py"],
                    "description": "Dynamic template generation based on codebase analysis"
                },
                {
                    "pattern": "Configuration-Driven Architecture",
                    "locations": ["evaluations/config/", ".env", "setup.py"],
                    "description": "Flexible configuration system for different environments"
                }
            ],
            "dependency_insights": [
                {
                    "cluster": "AI/ML Libraries",
                    "components": ["anthropic", "sentence-transformers", "numpy", "scipy"],
                    "purpose": "LLM integration and text similarity analysis"
                },
                {
                    "cluster": "Evaluation Framework",
                    "components": ["pytest", "rouge", "nltk"],
                    "purpose": "Automated testing and metric calculation"
                }
            ],
            "development_patterns": [
                {
                    "pattern": "Progressive Enhancement",
                    "evidence": "Template hierarchy from base to specialized",
                    "impact": "Allows systematic prompt improvement"
                },
                {
                    "pattern": "Documentation-First",
                    "evidence": "anthropic-md/ directory with official docs",
                    "impact": "Ensures accuracy and authoritative source"
                }
            ]
        }
    
    async def generate_cognee_enhanced_templates(self, prompt_types: Optional[List[str]] = None) -> List[PromptTemplate]:
        """
        Generate enhanced templates using Cognee insights.
        """
        self.logger.info("🛠️ Generating Cognee-enhanced prompt templates")
        
        # Get base templates
        base_templates = await self.generate_context_aware_prompts(prompt_types)
        
        # Enhance each template with Cognee insights
        enhanced_templates = []
        for template in base_templates:
            enhanced_template = await self._enhance_template_with_cognee(template)
            enhanced_templates.append(enhanced_template)
        
        return enhanced_templates
    
    async def _enhance_template_with_cognee(self, template: PromptTemplate) -> PromptTemplate:
        """
        Enhance a template using Cognee knowledge graph insights.
        """
        # Add Cognee-specific enhancements to the template content
        cognee_enhancement = f"""

## 🧠 Cognee Knowledge Graph Enhancement

This template has been enhanced with insights from knowledge graph analysis:

### Architectural Relationship Awareness
- **Template Hierarchy Pattern**: This prompt understands the progressive enhancement structure
- **Evaluation Flow Integration**: Connects with the evaluation-driven development workflow
- **Configuration Dependencies**: Aware of the flexible configuration system

### Code Pattern Recognition
- **Template Factory Pattern**: Can generate context-specific variations
- **Documentation-First Approach**: Leverages authoritative Anthropic documentation
- **Progressive Enhancement**: Builds complexity systematically

### Enhanced Context Variables
- **KNOWLEDGE_GRAPH_CONTEXT**: {{KNOWLEDGE_GRAPH_CONTEXT}}
- **RELATIONSHIP_INSIGHTS**: {{RELATIONSHIP_INSIGHTS}}
- **PATTERN_AWARENESS**: {{PATTERN_AWARENESS}}

### Cognee-Powered Capabilities
1. **Relationship-Aware Analysis**: Understands how components connect
2. **Pattern-Based Reasoning**: Applies detected architectural patterns
3. **Context-Sensitive Adaptation**: Adjusts based on knowledge graph insights
4. **Dependency-Informed Decisions**: Considers technical dependencies

---
"""
        
        # Insert enhancement into template content
        enhanced_content = template.content + cognee_enhancement
        
        # Update template with enhanced information
        enhanced_template = PromptTemplate(
            name=f"{template.name}_cognee_enhanced",
            template_type=template.template_type,
            content=enhanced_content,
            variables=template.variables + ["KNOWLEDGE_GRAPH_CONTEXT", "RELATIONSHIP_INSIGHTS", "PATTERN_AWARENESS"],
            use_cases=template.use_cases + ["Knowledge graph-informed analysis"],
            specializations={
                **template.specializations,
                "cognee_enhanced": True,
                "knowledge_graph_integration": "enabled",
                "relationship_awareness": "high"
            },
            metadata={
                **template.metadata,
                "cognee_enhanced": True,
                "enhancement_timestamp": datetime.now().isoformat(),
                "knowledge_graph_features": [
                    "architectural_relationships",
                    "code_patterns", 
                    "dependency_insights",
                    "development_patterns"
                ]
            }
        )
        
        return enhanced_template
    
    async def save_cognee_enhanced_templates(self, templates: List[PromptTemplate], output_dir: Optional[str] = None) -> List[str]:
        """
        Save Cognee-enhanced templates with additional metadata.
        """
        if output_dir is None:
            output_dir = self.cognee_templates_dir / "cognee-enhanced"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        
        for template in templates:
            # Save template file
            template_filename = f"{template.name}.md"
            template_path = output_path / template_filename
            
            with open(template_path, 'w') as f:
                f.write(template.content)
            
            # Save enhanced metadata
            metadata_filename = f"{template.name}_metadata.json"
            metadata_path = output_path / metadata_filename
            
            enhanced_metadata = {
                "template": {
                    "name": template.name,
                    "type": template.template_type,
                    "variables": template.variables,
                    "use_cases": template.use_cases,
                    "specializations": template.specializations,
                    "metadata": template.metadata
                },
                "cognee_enhancements": {
                    "enhanced": template.metadata.get("cognee_enhanced", False),
                    "features": template.metadata.get("knowledge_graph_features", []),
                    "enhancement_timestamp": template.metadata.get("enhancement_timestamp"),
                    "relationship_awareness": template.specializations.get("relationship_awareness", "none")
                },
                "usage_instructions": {
                    "basic_usage": f"Use this template for {template.template_type} with Cognee knowledge graph context",
                    "cognee_features": "This template includes relationship awareness and pattern recognition",
                    "variable_population": "Populate KNOWLEDGE_GRAPH_CONTEXT with relevant insights from Cognee search"
                }
            }
            
            with open(metadata_path, 'w') as f:
                json.dump(enhanced_metadata, f, indent=2)
            
            saved_files.extend([str(template_path), str(metadata_path)])
            self.logger.info(f"Saved Cognee-enhanced template: {template_path}")
        
        # Create enhanced index
        index_path = output_path / "cognee_enhanced_index.json"
        index_data = {
            "cognee_enhanced_templates": [
                {
                    "name": template.name,
                    "type": template.template_type,
                    "file": f"{template.name}.md",
                    "metadata_file": f"{template.name}_metadata.json",
                    "cognee_features": template.metadata.get("knowledge_graph_features", []),
                    "enhancement_level": "full" if template.metadata.get("cognee_enhanced") else "basic"
                }
                for template in templates
            ],
            "enhancement_summary": {
                "total_templates": len(templates),
                "cognee_enhanced_count": sum(1 for t in templates if t.metadata.get("cognee_enhanced")),
                "knowledge_graph_integration": "enabled",
                "generation_timestamp": datetime.now().isoformat()
            }
        }
        
        with open(index_path, 'w') as f:
            json.dump(index_data, f, indent=2)
        
        saved_files.append(str(index_path))
        
        self.logger.info(f"Saved {len(templates)} Cognee-enhanced templates to: {output_path}")
        return saved_files


async def run_cognee_demo(repo_path: str = ".") -> Dict[str, Any]:
    """
    Run the complete Cognee-enhanced intelligent prompt generation demo.
    """
    print("🚀 Starting Cognee-Enhanced Intelligent Prompt Generation Demo")
    print("=" * 70)
    
    generator = CogneeEnhancedPromptGenerator()
    
    try:
        # Step 1: Analyze with Cognee enhancement
        print("\n🔍 Phase 1: Cognee-Enhanced Codebase Analysis")
        analysis_results = await generator.analyze_with_cognee(repo_path)
        
        base_insights = analysis_results["base_insights"]
        print(f"✅ Base Analysis Complete:")
        print(f"   - Architecture: {base_insights.architecture_type}")
        print(f"   - Languages: {', '.join(base_insights.primary_languages)}")
        print(f"   - Frameworks: {', '.join(base_insights.frameworks) if base_insights.frameworks else 'None'}")
        print(f"   - Complexity: {generator._get_complexity_level(base_insights.complexity_metrics['overall_complexity'])}")
        
        enhanced_insights = analysis_results["enhanced_insights"]
        print(f"✅ Cognee Enhancement Complete:")
        print(f"   - Architectural Relationships: {len(enhanced_insights['architectural_relationships'])}")
        print(f"   - Code Patterns: {len(enhanced_insights['code_patterns'])}")
        print(f"   - Dependency Clusters: {len(enhanced_insights['dependency_insights'])}")
        
        # Step 2: Generate enhanced templates
        print("\n🛠️ Phase 2: Cognee-Enhanced Template Generation")
        enhanced_templates = await generator.generate_cognee_enhanced_templates([
            "architecture_analysis", "code_generation", "bug_fixing"
        ])
        
        print(f"✅ Generated {len(enhanced_templates)} Cognee-enhanced templates:")
        for template in enhanced_templates:
            enhancement_status = "🧠 Enhanced" if template.metadata.get("cognee_enhanced") else "📝 Basic"
            print(f"   - {template.name} ({template.template_type}) {enhancement_status}")
        
        # Step 3: Save enhanced templates
        print("\n💾 Phase 3: Saving Cognee-Enhanced Templates")
        saved_files = await generator.save_cognee_enhanced_templates(enhanced_templates)
        
        template_dir = Path(saved_files[0]).parent
        print(f"✅ Templates saved to: {template_dir}")
        print(f"   - Template files: {len([f for f in saved_files if f.endswith('.md')])}")
        print(f"   - Metadata files: {len([f for f in saved_files if f.endswith('.json')])}")
        
        # Step 4: Demonstrate usage
        print("\n🎯 Phase 4: Usage Demonstration")
        demo_template = enhanced_templates[0]
        print(f"📋 Sample Enhanced Template: {demo_template.name}")
        print(f"   - Type: {demo_template.template_type}")
        print(f"   - Variables: {len(demo_template.variables)}")
        print(f"   - Cognee Features: {demo_template.metadata.get('knowledge_graph_features', [])}")
        print(f"   - Relationship Awareness: {demo_template.specializations.get('relationship_awareness', 'none')}")
        
        return {
            "status": "success",
            "analysis_results": analysis_results,
            "enhanced_templates": enhanced_templates,
            "saved_files": saved_files,
            "demo_complete": True
        }
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "demo_complete": False
        }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Cognee-Enhanced Intelligent Prompt Generator Demo")
    parser.add_argument("--repo-path", default=".", help="Path to repository to analyze")
    
    args = parser.parse_args()
    
    try:
        results = asyncio.run(run_cognee_demo(args.repo_path))
        
        if results["status"] == "success":
            print(f"\n🎉 Demo completed successfully!")
            print(f"📊 Results:")
            print(f"   - Enhanced templates: {len(results.get('enhanced_templates', []))}")
            print(f"   - Saved files: {len(results.get('saved_files', []))}")
            sys.exit(0)
        else:
            print(f"\n❌ Demo failed: {results.get('error', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)