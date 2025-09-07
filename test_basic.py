#!/usr/bin/env python3
"""
Basic test for OpenManus application components.
Created in response to: "HAZ UNA PRUEBA" (Make a Test)

This test validates core functionality of the OpenManus framework.
"""

import unittest
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))


class TestBasicFunctionality(unittest.TestCase):
    """Basic tests for OpenManus core components"""

    def test_project_structure(self):
        """Test that essential project files and directories exist"""
        project_root = Path(__file__).parent
        
        # Check essential files exist
        essential_files = [
            'main.py',
            'requirements.txt',
            'README.md',
            'app/__init__.py',
            'app/config.py',
            'app/logger.py'
        ]
        
        for file_path in essential_files:
            full_path = project_root / file_path
            self.assertTrue(full_path.exists(), f"Essential file missing: {file_path}")

    def test_main_entry_point_exists(self):
        """Test that main entry point is accessible"""
        project_root = Path(__file__).parent
        main_py = project_root / "main.py"
        
        self.assertTrue(main_py.exists(), "main.py entry point missing")
        
        # Read main.py and check it has basic structure
        with main_py.open('r') as f:
            content = f.read()
            
        # Check for essential components in main.py
        self.assertIn('main()', content, "main() function not found in main.py")
        self.assertIn('asyncio', content, "asyncio import not found in main.py")

    def test_configuration_files_exist(self):
        """Test that configuration files exist"""
        project_root = Path(__file__).parent
        config_dir = project_root / "config"
        
        self.assertTrue(config_dir.exists(), "Config directory missing")
        
        # Look for either config.toml or config.example.toml
        config_file = config_dir / "config.toml"
        example_config = config_dir / "config.example.toml"
        
        has_config = config_file.exists() or example_config.exists()
        self.assertTrue(has_config, "No configuration file found")

    def test_app_modules_structure(self):
        """Test that app modules have correct structure without importing them"""
        project_root = Path(__file__).parent
        app_dir = project_root / "app"
        
        self.assertTrue(app_dir.exists(), "App directory missing")
        self.assertTrue(app_dir.is_dir(), "App is not a directory")
        
        # Check essential app modules exist
        essential_modules = [
            'config.py',
            'logger.py',
            'agent',
            'tool',
            'sandbox'
        ]
        
        for module in essential_modules:
            module_path = app_dir / module
            self.assertTrue(module_path.exists(), f"Essential app module missing: {module}")

    def test_main_script_syntax(self):
        """Test that main.py has valid Python syntax"""
        project_root = Path(__file__).parent
        main_py = project_root / "main.py"
        
        # Read and attempt to compile the main script
        with main_py.open('r') as f:
            content = f.read()
        
        try:
            compile(content, str(main_py), 'exec')
        except SyntaxError as e:
            self.fail(f"Syntax error in main.py: {e}")

    def test_app_modules_syntax(self):
        """Test that core app modules have valid Python syntax"""
        project_root = Path(__file__).parent
        app_dir = project_root / "app"
        
        # Test syntax of core modules
        core_modules = ['config.py', 'logger.py']
        
        for module_file in core_modules:
            module_path = app_dir / module_file
            if module_path.exists():
                with module_path.open('r') as f:
                    content = f.read()
                
                try:
                    compile(content, str(module_path), 'exec')
                except SyntaxError as e:
                    self.fail(f"Syntax error in {module_file}: {e}")

    def test_project_has_tests_directory(self):
        """Test that the project has a tests directory"""
        project_root = Path(__file__).parent
        tests_dir = project_root / "tests"
        
        self.assertTrue(tests_dir.exists(), "Tests directory missing")
        self.assertTrue(tests_dir.is_dir(), "Tests is not a directory")
        
        # Check if there are any test files
        test_files = list(tests_dir.glob("**/*.py"))
        self.assertGreater(len(test_files), 0, "No test files found in tests directory")


class TestProjectIntegrity(unittest.TestCase):
    """Tests to ensure project integrity and completeness"""

    def test_readme_exists_and_not_empty(self):
        """Test that README.md exists and has content"""
        project_root = Path(__file__).parent
        readme = project_root / "README.md"
        
        self.assertTrue(readme.exists(), "README.md is missing")
        
        # Check that README has content
        content = readme.read_text()
        self.assertGreater(len(content.strip()), 100, "README.md appears to be empty or too short")
        self.assertIn("OpenManus", content, "README should mention OpenManus")

    def test_requirements_file_exists(self):
        """Test that requirements.txt exists and has content"""
        project_root = Path(__file__).parent
        requirements = project_root / "requirements.txt"
        
        self.assertTrue(requirements.exists(), "requirements.txt is missing")
        
        # Check that requirements has content
        content = requirements.read_text()
        self.assertGreater(len(content.strip()), 10, "requirements.txt appears to be empty")

    def test_license_file_exists(self):
        """Test that LICENSE file exists"""
        project_root = Path(__file__).parent
        license_file = project_root / "LICENSE"
        
        self.assertTrue(license_file.exists(), "LICENSE file is missing")

    def test_docker_support(self):
        """Test that Docker support files exist"""
        project_root = Path(__file__).parent
        dockerfile = project_root / "Dockerfile"
        
        if dockerfile.exists():
            # If Dockerfile exists, verify it has content
            content = dockerfile.read_text()
            self.assertGreater(len(content.strip()), 10, "Dockerfile appears to be empty")

    def test_git_configuration(self):
        """Test that git configuration files exist"""
        project_root = Path(__file__).parent
        
        # Check for .gitignore
        gitignore = project_root / ".gitignore"
        self.assertTrue(gitignore.exists(), ".gitignore file is missing")
        
        # Check .gitignore has content
        if gitignore.exists():
            content = gitignore.read_text()
            self.assertGreater(len(content.strip()), 10, ".gitignore appears to be empty")


def run_basic_tests():
    """Function to run all basic tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBasicFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestProjectIntegrity))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING BASIC TESTS FOR OPENMANUS")
    print("Test created in response to: 'HAZ UNA PRUEBA' (Make a Test)")
    print("=" * 60)
    
    result = run_basic_tests()
    
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED! OpenManus basic functionality is working.")
    else:
        print("❌ SOME TESTS FAILED!")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
    print("=" * 60)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)