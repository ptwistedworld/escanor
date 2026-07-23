#!/usr/bin/env python3
"""
Base Module Class
All modules must inherit from this base class
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime


class BaseModule(ABC):
    """Abstract base class for all Escanor modules"""
    
    def __init__(self):
        self.name = ""
        self.category = ""
        self.description = ""
        self.author = ""
        self.version = "1.0.0"
        self.options: Dict[str, Any] = {}
        self.required_options: List[str] = []
        self.results: Optional[Dict] = None
        self.created_at = datetime.now()
    
    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """
        Execute the module's main functionality
        Returns: Dictionary containing results
        """
        pass
    
    def validate_options(self) -> bool:
        """Validate that all required options are set"""
        for option in self.required_options:
            if option not in self.options or not self.options[option]:
                print(f"[!] Missing required option: {option}")
                return False
        return True
    
    def set_option(self, key: str, value: Any) -> None:
        """Set a module option"""
        self.options[key] = value
    
    def get_option(self, key: str) -> Any:
        """Get a module option value"""
        return self.options.get(key)
    
    def show_options(self) -> None:
        """Display all module options"""
        print(f"\n{'Option':<20} {'Value':<30} {'Required':<10} {'Description':<40}")
        print("-" * 100)
        
        # Get descriptions from module if available
        descriptions = getattr(self, 'option_descriptions', {})
        
        for key in self.options.keys():
            value = str(self.options[key]) if self.options[key] else ""
            required = "Yes" if key in self.required_options else "No"
            desc = descriptions.get(key, "")
            print(f"{key:<20} {value:<30} {required:<10} {desc:<40}")
    
    def info(self) -> Dict[str, str]:
        """Return module information"""
        return {
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "author": self.author,
            "version": self.version
        }
    
    def log(self, message: str, level: str = "INFO") -> None:
        """Log module activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
