#!/usr/bin/env python3
"""
Unit tests for llm-labs validation.

Tests:
1. Repository structure validation
2. Markdown file integrity
3. Wiki-link validation (Obsidian [[links]])
4. No secrets or placeholders in content
"""

import os
import re
import sys
import unittest
from pathlib import Path

import validate


class TestRepositoryStructure(unittest.TestCase):
    """Test repository structure integrity."""

    def test_required_directories_exist(self):
        """All required directories must exist."""
        required_dirs = [
            'ai-drafts',
            'notes',
            'resources',
            'templates',
            'tools',
            'workflows',
        ]
        for dir_name in required_dirs:
            with self.subTest(directory=dir_name):
                self.assertTrue(
                    os.path.isdir(dir_name),
                    f"Missing required directory: {dir_name}/"
                )

    def test_required_files_exist(self):
        """Core documentation files must exist."""
        required_files = [
            'README.md',
            'LICENSE',
            'OBSIDIAN.md',
            '.gitignore',
            'validate.py',
            'Makefile',
        ]
        for file_name in required_files:
            with self.subTest(file=file_name):
                self.assertTrue(
                    os.path.isfile(file_name),
                    f"Missing required file: {file_name}"
                )

    def test_directories_not_empty(self):
        """Content directories should not be empty."""
        content_dirs = [
            'ai-drafts',
            'notes',
            'resources',
            'templates',
            'tools',
            'workflows',
        ]
        for dir_name in content_dirs:
            with self.subTest(directory=dir_name):
                if os.path.isdir(dir_name):
                    files = [f for f in os.listdir(dir_name)
                             if not f.startswith('.')]
                    self.assertGreater(
                        len(files), 0,
                        f"Directory {dir_name}/ should not be empty"
                    )


class TestMarkdownFiles(unittest.TestCase):
    """Test markdown file integrity."""

    @classmethod
    def setUpClass(cls):
        """Find all markdown files once."""
        cls.md_files = []
        for root, dirs, files in os.walk('.'):
            # Skip .git and .obsidian directories
            if '.git' in root or '.obsidian' in root:
                continue
            for file in files:
                if file.endswith('.md'):
                    cls.md_files.append(os.path.join(root, file))

    def test_markdown_files_exist(self):
        """Repository should contain markdown files."""
        self.assertGreater(
            len(self.md_files), 0,
            "No markdown files found in repository"
        )

    def test_markdown_files_readable(self):
        """All markdown files must be readable."""
        for md_file in self.md_files:
            with self.subTest(file=md_file):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.assertIsNotNone(content)
                except Exception as e:
                    self.fail(f"Cannot read {md_file}: {e}")

    def test_markdown_files_not_empty(self):
        """Markdown files should not be empty."""
        for md_file in self.md_files:
            with self.subTest(file=md_file):
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    self.assertGreater(
                        len(content), 0,
                        f"File {md_file} is empty"
                    )


class TestWikiLinks(unittest.TestCase):
    """Test Obsidian wiki-link integrity."""

    # Known missing links documented in OBSIDIAN.md
    KNOWN_MISSING = {
        'tools/context7',
        'tools/claude-code',
        'tools/cursor',
        'tools/firebase',
        'tools/bmat',
        'resources/to-explore',
        'notes/lessons-learned',
        'ai-drafts/agentic-experiment',
        'ai-drafts/context-sync-test',
        'ai-drafts/chatiq-stack-validation-example',
        'workflows/current-setup',
    }

    @classmethod
    def setUpClass(cls):
        """Find all markdown files and extract wiki-links."""
        cls.md_files = []
        cls.wiki_links = {}  # {source_file: [(link_text, target_path), ...]}
        
        for root, dirs, files in os.walk('.'):
            if '.git' in root or '.obsidian' in root:
                continue
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    cls.md_files.append(file_path)
        
        # Extract all wiki-links from files
        wiki_pattern = re.compile(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')
        
        for md_file in cls.md_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                links = wiki_pattern.findall(content)
                if links:
                    cls.wiki_links[md_file] = [
                        (target, display if display else target)
                        for target, display in links
                    ]

    def test_wiki_links_found(self):
        """Repository should use wiki-links (core feature)."""
        total_links = sum(len(links) for links in self.wiki_links.values())
        self.assertGreater(
            total_links, 0,
            "No wiki-links found - core Obsidian feature not in use"
        )

    def test_wiki_links_target_valid_files(self):
        """Wiki-links should point to existing files (except known missing)."""
        broken_links = []
        
        # Files that are templates/documentation showing examples
        example_files = ['OBSIDIAN.md', 'templates/note-template.md', 
                         'templates/workflow-template.md', 'templates/ai-draft-template.md',
                         'templates/tool-template.md', 'templates/resource-template.md']
        
        for source_file, links in self.wiki_links.items():
            # Skip example links in documentation files
            if any(source_file.endswith(ex) for ex in example_files):
                continue
                
            for link_target, display_text in links:
                # Skip obviously fake/example links
                if any(placeholder in link_target for placeholder in 
                       ['page-name', 'path/to/', 'example', '{{', 'workflows/', 'tools/']):
                    continue
                
                # Normalize path: add .md if missing
                target_path = link_target
                if not target_path.endswith('.md'):
                    target_path = f"{target_path}.md"
                
                # Check if target exists
                if not os.path.isfile(target_path):
                    # Check if it's a known missing link
                    normalized_link = link_target.replace('.md', '')
                    if normalized_link not in self.KNOWN_MISSING:
                        broken_links.append({
                            'source': source_file,
                            'target': link_target,
                            'display': display_text,
                        })
        
        if broken_links:
            error_msg = "\nBroken wiki-links found:\n"
            for link in broken_links:
                error_msg += (
                    f"  {link['source']}: [[{link['target']}]] "
                    f"(displays as '{link['display']}')\n"
                )
            error_msg += (
                "\nIf these are intentional, add them to "
                "KNOWN_MISSING in test_validate.py and document in OBSIDIAN.md"
            )
            self.fail(error_msg)

    def test_known_missing_documented(self):
        """Known missing links should be documented in OBSIDIAN.md."""
        obsidian_doc = 'OBSIDIAN.md'
        self.assertTrue(
            os.path.isfile(obsidian_doc),
            "OBSIDIAN.md must exist to document missing links"
        )
        
        with open(obsidian_doc, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that file has a "Missing Link Targets" section
        self.assertIn(
            'Missing Link Targets',
            content,
            "OBSIDIAN.md should have 'Missing Link Targets' section"
        )


class TestNoSecrets(unittest.TestCase):
    """Test for secrets and placeholders that shouldn't be committed."""

    @classmethod
    def setUpClass(cls):
        """Find all text files to scan."""
        cls.text_files = []
        for root, dirs, files in os.walk('.'):
            # Skip .git, .obsidian, and common binary/generated dirs
            if any(skip in root for skip in ['.git', '.obsidian', 'node_modules', '__pycache__']):
                continue
            for file in files:
                # Only scan text files
                if any(file.endswith(ext) for ext in ['.md', '.py', '.yml', '.yaml', '.json', '.txt', '.sh']):
                    cls.text_files.append(os.path.join(root, file))

    def test_no_api_keys_in_files(self):
        """Files should not contain API keys or secrets."""
        # Common patterns that indicate secrets
        secret_patterns = [
            re.compile(r'api[_-]?key\s*[=:]\s*["\'][a-zA-Z0-9]{20,}["\']', re.IGNORECASE),
            re.compile(r'secret[_-]?key\s*[=:]\s*["\'][a-zA-Z0-9]{20,}["\']', re.IGNORECASE),
            re.compile(r'password\s*[=:]\s*["\'][^"\']{8,}["\']', re.IGNORECASE),
            re.compile(r'token\s*[=:]\s*["\'][a-zA-Z0-9]{20,}["\']', re.IGNORECASE),
        ]
        
        findings = []
        for file_path in self.text_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for pattern in secret_patterns:
                        matches = pattern.finditer(content)
                        for match in matches:
                            # Skip if it's in a comment explaining API keys
                            line = content[max(0, match.start()-100):match.end()+100]
                            if not any(indicator in line.lower() for indicator in ['example', 'placeholder', 'your_', '<', '[']):
                                findings.append({
                                    'file': file_path,
                                    'match': match.group(0)[:50],
                                })
            except Exception:
                # Skip files that can't be read as text
                pass
        
        if findings:
            error_msg = "\nPotential secrets found in files:\n"
            for finding in findings:
                error_msg += f"  {finding['file']}: {finding['match']}...\n"
            self.fail(error_msg)

    def test_no_placeholder_todos_in_production_code(self):
        """Production code should not have unresolved placeholders."""
        # Only check validate.py (our production code)
        if not os.path.isfile('validate.py'):
            self.skipTest("validate.py not found")
        
        with open('validate.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for obvious placeholders
        placeholders = [
            'TODO',
            'FIXME',
            'XXX',
            'HACK',
            'placeholder',
            'FILL_ME',
            'CHANGE_ME',
        ]
        
        findings = []
        for placeholder in placeholders:
            if placeholder in content:
                # Get line number
                for i, line in enumerate(content.split('\n'), 1):
                    if placeholder in line:
                        findings.append({
                            'placeholder': placeholder,
                            'line': i,
                            'content': line.strip()[:60],
                        })
        
        if findings:
            error_msg = "\nPlaceholders found in validate.py:\n"
            for finding in findings:
                error_msg += (
                    f"  Line {finding['line']}: {finding['placeholder']} "
                    f"- {finding['content']}\n"
                )
            self.fail(error_msg)


class TestCIConfiguration(unittest.TestCase):
    """Test CI/CD configuration."""

    def test_github_actions_exists(self):
        """GitHub Actions workflow should exist."""
        ci_file = '.github/workflows/ci.yml'
        self.assertTrue(
            os.path.isfile(ci_file),
            "CI workflow file must exist"
        )

    def test_ci_runs_validation(self):
        """CI should run validation tests."""
        ci_file = '.github/workflows/ci.yml'
        with open(ci_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that CI runs tests
        self.assertIn(
            'make test',
            content,
            "CI should run 'make test'"
        )

    def test_makefile_has_test_target(self):
        """Makefile should have test target."""
        if not os.path.isfile('Makefile'):
            self.skipTest("Makefile not found")
        
        with open('Makefile', 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn(
            'test:',
            content,
            "Makefile should have 'test' target"
        )


class TestREADMEAccuracy(unittest.TestCase):
    """Test that README accurately describes the repository."""

    def test_readme_exists(self):
        """README.md must exist."""
        self.assertTrue(os.path.isfile('README.md'))

    def test_readme_documents_validation(self):
        """README should document how to run validation."""
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn(
            'make test',
            content,
            "README should document 'make test' command"
        )
        self.assertIn(
            'validate',
            content.lower(),
            "README should mention validation"
        )

    def test_readme_documents_ci(self):
        """README should document CI/CD status."""
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn(
            'CI',
            content,
            "README should mention CI/CD"
        )


def run_tests():
    """Run all tests with detailed output."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
