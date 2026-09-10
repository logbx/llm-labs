#!/usr/bin/env python3
"""
Validation script for llm-labs repository.

Checks:
1. Directory structure is intact
2. Key files exist
3. No empty directories (except .obsidian)
4. Markdown files are readable
"""

import os
import sys
from pathlib import Path

def validate_structure():
    """Validate directory structure."""
    required_dirs = [
        'ai-drafts',
        'notes',
        'resources',
        'templates',
        'tools',
        'workflows',
    ]
    
    required_files = [
        'README.md',
        'LICENSE',
        'OBSIDIAN.md',
        '.gitignore',
    ]
    
    errors = []
    warnings = []
    
    # Check required directories
    for dir_name in required_dirs:
        if not os.path.isdir(dir_name):
            errors.append(f"Missing required directory: {dir_name}/")
    
    # Check required files
    for file_name in required_files:
        if not os.path.isfile(file_name):
            errors.append(f"Missing required file: {file_name}")
    
    # Check that directories have content (except .obsidian)
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            files = [f for f in os.listdir(dir_name) if not f.startswith('.')]
            if not files:
                warnings.append(f"Directory {dir_name}/ is empty")
    
    return errors, warnings

def validate_markdown():
    """Validate markdown files are readable."""
    errors = []
    warnings = []
    
    md_files = []
    for root, dirs, files in os.walk('.'):
        # Skip .git and .obsidian directories
        if '.git' in root or '.obsidian' in root:
            continue
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    if not md_files:
        errors.append("No markdown files found")
        return errors, warnings
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content.strip()) == 0:
                    warnings.append(f"File {md_file} is empty")
        except Exception as e:
            errors.append(f"Cannot read {md_file}: {e}")
    
    return errors, warnings

def main():
    """Run all validations."""
    print("🔍 Validating llm-labs repository...\n")
    
    all_errors = []
    all_warnings = []
    
    # Validate structure
    print("Checking directory structure...")
    errors, warnings = validate_structure()
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Validate markdown
    print("Checking markdown files...")
    errors, warnings = validate_markdown()
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Report results
    print("\n" + "="*60)
    
    if all_errors:
        print(f"\n❌ {len(all_errors)} ERROR(S) FOUND:\n")
        for error in all_errors:
            print(f"  • {error}")
    
    if all_warnings:
        print(f"\n⚠️  {len(all_warnings)} WARNING(S):\n")
        for warning in all_warnings:
            print(f"  • {warning}")
    
    if not all_errors and not all_warnings:
        print("\n✅ All validation checks passed!")
    elif not all_errors:
        print("\n✅ All critical checks passed (warnings can be ignored)")
    
    print("\n" + "="*60)
    
    # Exit with error code if there are errors
    sys.exit(1 if all_errors else 0)

if __name__ == '__main__':
    main()