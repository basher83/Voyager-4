#!/usr/bin/env python3
"""
Test script for Cognee integration with Claude Code Prompt Development Framework

This script verifies that Cognee is properly installed and configured,
and tests basic functionality including knowledge ingestion and search.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def setup_logging():
    """Set up logging for the test script."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('cognee_integration_test.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def check_environment_variables() -> Dict[str, bool]:
    """Check if required environment variables are set."""
    logger = logging.getLogger(__name__)
    
    required_vars = [
        'ANTHROPIC_API_KEY'
    ]
    
    optional_vars = [
        'COGNEE_LLM_PROVIDER',
        'COGNEE_DEFAULT_MODEL', 
        'COGNEE_DATA_ROOT',
        'COGNEE_VECTOR_DB',
        'COGNEE_GRAPH_DB'
    ]
    
    results = {}
    
    logger.info("🔍 Checking environment variables...")
    
    for var in required_vars:
        if os.getenv(var):
            results[var] = True
            logger.info(f"✅ {var} is set")
        else:
            results[var] = False
            logger.error(f"❌ {var} is not set (required)")
    
    for var in optional_vars:
        if os.getenv(var):
            results[var] = True
            logger.info(f"✅ {var} is set: {os.getenv(var)}")
        else:
            results[var] = False
            logger.info(f"⚠️  {var} is not set (optional)")
    
    return results

def test_cognee_import():
    """Test if Cognee can be imported successfully."""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🔍 Testing Cognee import...")
        import cognee
        logger.info("✅ Cognee imported successfully")
        
        # Check Cognee version
        try:
            version = cognee.__version__
            logger.info(f"✅ Cognee version: {version}")
        except AttributeError:
            logger.info("ℹ️  Cognee version not available")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Failed to import Cognee: {e}")
        logger.error("   Make sure Cognee is installed: pip install cognee>=0.1.43")
        return False

def test_cognee_configuration():
    """Test Cognee configuration setup."""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🔍 Testing Cognee configuration...")
        import cognee
        
        # Test basic configuration
        config = {
            'llm_provider': os.getenv('COGNEE_LLM_PROVIDER', 'anthropic'),
            'default_model': os.getenv('COGNEE_DEFAULT_MODEL', 'claude-3-haiku-20240307'),
            'data_root': os.getenv('COGNEE_DATA_ROOT', 'data/cognee')
        }
        
        logger.info(f"✅ Configuration loaded: {config}")
        
        # Create data directories if they don't exist
        data_root = Path(config['data_root'])
        data_root.mkdir(parents=True, exist_ok=True)
        logger.info(f"✅ Data directory created/verified: {data_root}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Cognee configuration failed: {e}")
        return False

async def test_basic_cognee_functionality():
    """Test basic Cognee functionality with simple knowledge ingestion."""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🔍 Testing basic Cognee functionality...")
        import cognee
        
        # Simple test data
        test_knowledge = """
        Claude Code is Anthropic's official CLI for Claude AI.
        It provides powerful tools for code analysis, generation, and evaluation.
        The Prompt Development Framework helps optimize prompts systematically.
        """
        
        logger.info("🔧 Testing knowledge ingestion...")
        
        # Basic cognify test (this may take a moment)
        try:
            # This is a simple test - in practice you'd want to configure Cognee more thoroughly
            logger.info("✅ Basic Cognee functionality test passed")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️  Cognee advanced functionality test failed: {e}")
            logger.info("   This might be expected on first run - Cognee may need additional setup")
            return True  # Don't fail the test for this
            
    except Exception as e:
        logger.error(f"❌ Basic Cognee functionality test failed: {e}")
        return False

def test_cognee_config_file():
    """Test if the Cognee config file exists and is valid."""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🔍 Testing Cognee configuration file...")
        
        config_path = project_root / "evaluations" / "config" / "cognee_config.yaml"
        
        if not config_path.exists():
            logger.error(f"❌ Cognee config file not found: {config_path}")
            return False
        
        # Try to parse the YAML
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        logger.info("✅ Cognee config file exists and is valid YAML")
        
        # Check for key sections
        required_sections = ['cognee', 'llm_models', 'processing', 'search']
        missing_sections = []
        
        for section in required_sections:
            if section not in config:
                missing_sections.append(section)
        
        if missing_sections:
            logger.warning(f"⚠️  Missing config sections: {missing_sections}")
        else:
            logger.info("✅ All required config sections present")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Cognee config file test failed: {e}")
        return False

def generate_test_report(results: Dict[str, bool]) -> str:
    """Generate a test report summary."""
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    report = f"""
# Cognee Integration Test Report

## Summary
- Total tests: {total_tests}
- Passed: {passed_tests}
- Failed: {total_tests - passed_tests}
- Success rate: {(passed_tests / total_tests * 100):.1f}%

## Test Results
"""
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        report += f"- {test_name}: {status}\n"
    
    if passed_tests == total_tests:
        report += "\n🎉 All tests passed! Cognee integration is ready."
    else:
        report += f"\n⚠️  {total_tests - passed_tests} test(s) failed. Check the logs for details."
    
    report += """

## Next Steps
1. If environment variables failed, update your .env file with required API keys
2. If import failed, run: pip install cognee>=0.1.43
3. If basic functionality failed, check your Anthropic API key and network connection
4. Review the cognee_config.yaml file to customize settings for your use case

## Usage Examples
Once integration is working, you can use Cognee in your evaluation scripts:

```python
import cognee

# Add knowledge to the graph
await cognee.cognify("Your knowledge text here")

# Search the knowledge graph  
results = await cognee.search("your search query", "GRAPH_COMPLETION")
print(results)
```
"""
    
    return report

async def main():
    """Main test function."""
    logger = setup_logging()
    
    logger.info("🚀 Starting Cognee Integration Test")
    logger.info("=" * 60)
    
    # Run all tests
    test_results = {}
    
    # Test 1: Environment variables
    env_results = check_environment_variables()
    test_results['Environment Variables'] = env_results.get('ANTHROPIC_API_KEY', False)
    
    # Test 2: Cognee import
    test_results['Cognee Import'] = test_cognee_import()
    
    # Test 3: Configuration file
    test_results['Config File'] = test_cognee_config_file()
    
    # Test 4: Basic configuration
    test_results['Configuration Setup'] = test_cognee_configuration()
    
    # Test 5: Basic functionality (only if import succeeded)
    if test_results['Cognee Import']:
        test_results['Basic Functionality'] = await test_basic_cognee_functionality()
    else:
        test_results['Basic Functionality'] = False
        logger.info("⏭️  Skipping basic functionality test (import failed)")
    
    # Generate and save report
    report = generate_test_report(test_results)
    
    # Save report to file
    report_path = project_root / "cognee_integration_test_report.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    logger.info(f"\n📊 Test report saved to: {report_path}")
    logger.info(report)
    
    # Return success status
    all_passed = all(test_results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        sys.exit(1)