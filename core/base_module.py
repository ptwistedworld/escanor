#!/usr/bin/env python3
"""
Base Module Class
All modules must inherit from this base class

Supports fine-grained actions for precise control over module behavior.
Each module can expose multiple actions that can be selected and executed independently.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class ActionDefinition:
    """Defines a single action within a module"""
    name: str
    description: str
    method_name: str  # The method to call on the module
    required_options: List[str] = field(default_factory=list)
    optional_options: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for display/serialization"""
        return {
            "name": self.name,
            "description": self.description,
            "required_options": self.required_options,
            "optional_options": self.optional_options,
            "tags": self.tags
        }


class BaseModule(ABC):
    """Abstract base class for all Escanor modules
    
    Modules can expose multiple fine-grained actions for precise control.
    Actions are registered using the @action decorator or register_action method.
    """
    
    def __init__(self):
        self.name = ""
        self.display_name = ""  # Human-readable name
        self.category = ""
        self.description = ""
        self.author = ""
        self.version = "1.0.0"
        self.options: Dict[str, Any] = {}
        self.required_options: List[str] = []
        self.results: Optional[Dict] = None
        self.created_at = datetime.now()
        self._actions: Dict[str, ActionDefinition] = {}
        self._current_action: Optional[str] = None
        
        # Register default 'run' action if module has run() method
        if hasattr(self, 'run') and callable(getattr(self, 'run')):
            self.register_action(
                name="run",
                description="Execute the module's primary function",
                method_name="run"
            )
    
    def action(self, name: str, description: str, 
               required_options: List[str] = None,
               optional_options: List[str] = None,
               tags: List[str] = None):
        """
        Decorator to register a module action
        
        Usage:
            @action(name="scan", description="Perform network scan", 
                   required_options=["TARGET"], tags=["recon", "network"])
            def scan_ports(self):
                ...
        """
        def decorator(func):
            self.register_action(
                name=name,
                description=description,
                method_name=func.__name__,
                required_options=required_options or [],
                optional_options=optional_options or [],
                tags=tags or []
            )
            return func
        return decorator
    
    def register_action(self, name: str, description: str, method_name: str,
                       required_options: List[str] = None,
                       optional_options: List[str] = None,
                       tags: List[str] = None) -> None:
        """
        Programmatically register an action
        
        Args:
            name: Short name for the action (used in commands)
            description: Human-readable description
            method_name: Name of the method to call on this module
            required_options: List of option names required for this action
            optional_options: List of option names used by this action
            tags: Tags for categorizing/searching actions
        """
        self._actions[name] = ActionDefinition(
            name=name,
            description=description,
            method_name=method_name,
            required_options=required_options or [],
            optional_options=optional_options or [],
            tags=tags or []
        )
    
    def list_actions(self) -> Dict[str, ActionDefinition]:
        """Return all registered actions"""
        return self._actions.copy()
    
    def get_action(self, action_name: str) -> Optional[ActionDefinition]:
        """Get a specific action by name"""
        return self._actions.get(action_name.lower())
    
    def set_action(self, action_name: str) -> bool:
        """
        Set the current action to execute
        
        Returns True if action exists, False otherwise
        """
        action = self.get_action(action_name)
        if action:
            self._current_action = action_name
            return True
        return False
    
    def get_current_action(self) -> Optional[str]:
        """Get the currently selected action"""
        return self._current_action
    
    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """
        Execute the module's main functionality
        This is the default action if no specific action is selected
        
        Returns: Dictionary containing results
        """
        pass
    
    def execute_action(self, action_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a specific action or the currently selected action
        
        Args:
            action_name: Name of action to execute (uses current if None)
            
        Returns: Dictionary containing results
        """
        action_to_run = action_name or self._current_action
        
        if not action_to_run:
            # No action specified, run default
            return self.run()
        
        action = self.get_action(action_to_run)
        if not action:
            raise ValueError(f"Action '{action_to_run}' not found in module '{self.name}'")
        
        # Validate action-specific required options
        for opt in action.required_options:
            if opt not in self.options or not self.options[opt]:
                raise ValueError(f"Action '{action_to_run}' requires option '{opt}'")
        
        # Get the method and execute it
        method = getattr(self, action.method_name, None)
        if not method or not callable(method):
            raise ValueError(f"Method '{action.method_name}' not found in module '{self.name}'")
        
        return method()
    
    def validate_options(self) -> bool:
        """Validate that all required options are set"""
        # If an action is selected, validate action-specific options
        if self._current_action:
            action = self.get_action(self._current_action)
            if action:
                for option in action.required_options:
                    if option not in self.options or not self.options[option]:
                        print(f"[!] Missing required option for action '{self._current_action}': {option}")
                        return False
                return True
        
        # Otherwise validate module-level required options
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
    
    def show_actions(self) -> None:
        """Display all available actions in the module"""
        if not self._actions:
            print("\n[!] No actions defined in this module")
            return
        
        print(f"\n{'='*80}")
        print(f"ACTIONS AVAILABLE IN MODULE: {self.name}")
        print(f"{'='*80}")
        print(f"\n{'Action':<20} {'Description':<45} {'Tags'}")
        print("-" * 80)
        
        current = self._current_action or "none"
        for action_name, action_def in self._actions.items():
            marker = ">>>" if action_name == current else "   "
            tags_str = ", ".join(action_def.tags) if action_def.tags else "-"
            print(f"{marker} {action_name:<18} {action_def.description:<45} {tags_str}")
        
        print(f"\nCurrent action: {current}")
        print(f"\nUse 'action <name>' to select an action before running")
        print(f"{'='*80}\n")
    
    def info(self) -> Dict[str, Any]:
        """Return module information including actions"""
        info = {
            "name": self.name,
            "display_name": self.display_name or self.name,
            "category": self.category,
            "description": self.description,
            "author": self.author,
            "version": self.version,
            "actions_count": len(self._actions)
        }
        
        # Include action names if available
        if self._actions:
            info["actions"] = list(self._actions.keys())
        
        return info
    
    def log(self, message: str, level: str = "INFO") -> None:
        """Log module activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        action_prefix = f"[{self._current_action}] " if self._current_action else ""
        print(f"[{timestamp}] [{level}] {action_prefix}{message}")
    
    def log_error(self, message: str) -> None:
        """Convenience method for logging errors"""
        self.log(message, "ERROR")
    
    def log_success(self, message: str) -> None:
        """Convenience method for logging success"""
        self.log(message, "SUCCESS")
    
    def log_info(self, message: str) -> None:
        """Convenience method for logging info"""
        self.log(message, "INFO")
