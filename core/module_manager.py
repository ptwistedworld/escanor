#!/usr/bin/env python3
"""
Module Manager
Handles loading, listing, and executing modules
"""

import os
import sys
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional
from core.base_module import BaseModule


class ModuleManager:
    """Manages all framework modules"""

    def __init__(self):
        self.modules: Dict[str, BaseModule] = {}
        self.categories: Dict[str, List[str]] = {}
        self.module_path = Path(__file__).parent.parent / "modules"
        self.load_all_modules()

    def load_all_modules(self) -> None:
        """Load all modules from the modules directory"""
        if not self.module_path.exists():
            print(f"[!] Modules directory not found: {self.module_path}")
            return

        for category_dir in self.module_path.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('_'):
                category = category_dir.name
                
                # Check for subdirectories (like privesc under exploitation)
                for subdir in category_dir.iterdir():
                    if subdir.is_dir() and not subdir.name.startswith('_'):
                        subcategory = f"{category}/{subdir.name}"
                        self.categories[subcategory] = []
                        
                        for module_file in subdir.glob("*.py"):
                            if module_file.name.startswith('_') or module_file.name == '__init__.py':
                                continue
                            try:
                                self.load_module(module_file, subcategory)
                            except Exception as e:
                                print(f"[!] Error loading module {module_file}: {e}")
                
                # Also check for modules directly in the category directory
                self.categories[category] = []
                for module_file in category_dir.glob("*.py"):
                    if module_file.name.startswith('_') or module_file.name == '__init__.py':
                        continue
                    try:
                        self.load_module(module_file, category)
                    except Exception as e:
                        print(f"[!] Error loading module {module_file}: {e}")

    def load_module(self, module_path: Path, category: str) -> None:
        """Load a single module from file"""
        spec = importlib.util.spec_from_file_location(
            module_path.stem,
            module_path
        )

        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load spec for {module_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_path.stem] = module
        spec.loader.exec_module(module)

        # Find the module class (should inherit from BaseModule)
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and
                issubclass(attr, BaseModule) and
                attr is not BaseModule and
                not attr_name.startswith('_')):

                instance = attr()
                # Use the module's name attribute if available, otherwise use class name
                module_key = f"{category}/{instance.name if hasattr(instance, 'name') else attr_name}"
                self.modules[module_key] = instance
                self.categories[category].append(instance.name if hasattr(instance, 'name') else attr_name)
                break

    def get_module(self, module_name: str) -> Optional[BaseModule]:
        """Get a module by name"""
        # Try exact match first
        if module_name in self.modules:
            return self.modules[module_name]

        # Try case-insensitive match
        for key, module in self.modules.items():
            if key.lower() == module_name.lower():
                return module

        # Try finding by short name (case-insensitive) - check both class name and filename
        for key, module in self.modules.items():
            # Check if ends with /module_name (category/module format)
            if key.lower().endswith(f"/{module_name.lower()}"):
                return module
            # Also check the module's internal name attribute
            if hasattr(module, 'name') and module.name.lower() == module_name.lower():
                return module

        return None

    def list_modules(self) -> Dict[str, List[str]]:
        """List all available modules organized by category"""
        return self.categories

    def run_module(self, module_name: str, options: Optional[Dict] = None,
                   verbose: bool = False) -> Optional[Dict[str, Any]]:
        """Run a specific module with optional parameters"""
        module = self.get_module(module_name)

        if not module:
            print(f"[!] Module not found: {module_name}")
            return None

        if verbose:
            print(f"\n[*] Loading module: {module.name}")
            print(f"    Category: {module.category}")
            print(f"    Description: {module.description}")

        # Set options if provided
        if options:
            for key, value in options.items():
                module.set_option(key, value)

        # Validate and run
        if module.validate_options():
            if verbose:
                print(f"\n[*] Executing {module.name}...")

            try:
                results = module.run()
                module.results = results

                if verbose and results:
                    print(f"\n[+] Module completed successfully")
                    print(f"    Results: {results}")

                return results
            except Exception as e:
                print(f"[!] Module execution failed: {e}")
                return None
        else:
            print(f"[!] Module validation failed")
            return None

    def reload_modules(self) -> None:
        """Reload all modules (useful after adding new ones)"""
        self.modules.clear()
        self.categories.clear()
        self.load_all_modules()
        print("[+] Modules reloaded successfully")
