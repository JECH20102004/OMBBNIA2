#!/usr/bin/env python3
"""
Basic integration test for OpenManus application.
Created in response to: "HAZ UNA PRUEBA" (Make a Test)

This test validates the overall project structure and basic integrity
of the OpenManus framework without requiring external dependencies.
"""

import unittest
import sys
import os
from pathlib import Path

# Add the parent directories to the Python path to import from app
current_dir = Path(__file__).parent
project_root = current_dir.parent  # Go up one level from tests/ to project root
sys.path.insert(0, str(project_root))


class TestProjectStructure(unittest.TestCase):
    """Test the basic project structure and file integrity"""

    def setUp(self):
        """Set up test fixtures"""
        self.project_root = project_root

    def test_essential_files_exist(self):
        """Test that all essential project files exist"""
        essential_files = [
            'main.py',
            'requirements.txt', 
            'README.md',
            'LICENSE',
            'app/__init__.py',
            'app/config.py',
            'app/logger.py',
            'tests/sandbox'
        ]
        
        for file_path in essential_files:
            full_path = self.project_root / file_path
            self.assertTrue(full_path.exists(), f"Essential file/directory missing: {file_path}")

    def test_main_script_structure(self):
        """Test that main.py has the expected structure"""
        main_py = self.project_root / "main.py"
        content = main_py.read_text()
        
        # Check for key components
        self.assertIn('async def main()', content, "main() function should be async")
        self.assertIn('asyncio', content, "Should import asyncio")
        self.assertIn('Manus', content, "Should reference Manus agent")

    def test_app_module_structure(self):
        """Test that app module has expected structure"""
        app_dir = self.project_root / "app"
        
        # Check subdirectories exist
        expected_subdirs = ['agent', 'tool', 'sandbox', 'prompt']
        for subdir in expected_subdirs:
            subdir_path = app_dir / subdir
            self.assertTrue(subdir_path.exists(), f"App subdirectory missing: {subdir}")

    def test_config_files_exist(self):
        """Test that configuration files exist"""
        config_dir = self.project_root / "config"
        self.assertTrue(config_dir.exists(), "Config directory should exist")
        
        # Should have either config.toml or config.example.toml
        config_file = config_dir / "config.toml"
        example_config = config_dir / "config.example.toml"
        
        has_config = config_file.exists() or example_config.exists()
        self.assertTrue(has_config, "Should have configuration file")

    def test_python_syntax_validity(self):
        """Test that core Python files have valid syntax"""
        python_files = [
            'main.py',
            'run_flow.py',
            'run_mcp.py',
            'app/config.py',
            'app/logger.py'
        ]
        
        for file_path in python_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                with full_path.open('r') as f:
                    content = f.read()
                
                try:
                    compile(content, str(full_path), 'exec')
                except SyntaxError as e:
                    self.fail(f"Syntax error in {file_path}: {e}")


class TestDocumentation(unittest.TestCase):
    """Test documentation completeness"""

    def setUp(self):
        """Set up test fixtures"""
        self.project_root = project_root

    def test_readme_content(self):
        """Test README.md has appropriate content"""
        readme = self.project_root / "README.md"
        content = readme.read_text()
        
        # Check for key sections
        self.assertIn("OpenManus", content, "README should mention OpenManus")
        self.assertIn("Installation", content, "README should have installation instructions")
        self.assertIn("Quick Start", content, "README should have quick start guide")

    def test_requirements_valid(self):
        """Test that requirements.txt is valid"""
        requirements = self.project_root / "requirements.txt"
        content = requirements.read_text()
        
        # Should contain essential packages
        essential_packages = ['pydantic', 'loguru', 'openai', 'fastapi']
        for package in essential_packages:
            self.assertIn(package, content, f"Requirements should include {package}")


class TestProjectIntegrity(unittest.TestCase):
    """Test overall project integrity"""

    def setUp(self):
        """Set up test fixtures"""
        self.project_root = project_root

    def test_git_configuration(self):
        """Test git configuration files"""
        gitignore = self.project_root / ".gitignore"
        self.assertTrue(gitignore.exists(), ".gitignore should exist")
        
        gitignore_content = gitignore.read_text()
        # Should ignore common files (checking for similar patterns)
        expected_patterns = ['__pycache__', '*.py[cod]', '.env']
        for pattern in expected_patterns:
            self.assertIn(pattern, gitignore_content, f"Should ignore {pattern}")

    def test_license_exists(self):
        """Test that license file exists"""
        license_file = self.project_root / "LICENSE"
        self.assertTrue(license_file.exists(), "LICENSE file should exist")

    def test_docker_support(self):
        """Test Docker configuration if present"""
        dockerfile = self.project_root / "Dockerfile"
        if dockerfile.exists():
            content = dockerfile.read_text()
            self.assertIn("python", content.lower(), "Dockerfile should use Python")


if __name__ == "__main__":
    unittest.main(verbosity=2)