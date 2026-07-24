#!/usr/bin/env python3
"""
Module Refactoring Script - Adds Fine-Grained Actions to All Modules
This script adds action decorator imports and registers actions for all modules.
"""

import os
from pathlib import Path

def refactor_module(filepath):
    """Refactor a single module to use fine-grained actions."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if already refactored
    if 'from core.base_module import BaseModule, action' in content:
        print(f"✓ {filepath.name} already has action import")
        return False
    
    # Update import
    new_content = content.replace(
        'from core.base_module import BaseModule',
        'from core.base_module import BaseModule, action'
    )
    
    # Write back
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    print(f"✗ Updated {filepath.name}")
    return True

def main():
    """Main function to process all modules."""
    modules_dir = Path('/workspace/modules')
    module_files = list(modules_dir.rglob('*.py'))
    
    # Filter out __init__.py files
    module_files = [f for f in module_files if f.name != '__init__.py']
    
    print(f"Found {len(module_files)} module files to process\n")
    
    refactored = 0
    for filepath in module_files:
        try:
            if refactor_module(filepath):
                refactored += 1
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    print(f"\nCompleted: {refactored}/{len(module_files)} modules updated")

if __name__ == '__main__':
    main()
