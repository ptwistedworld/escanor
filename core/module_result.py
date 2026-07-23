"""
Module Result Class
Represents the result of a module execution
"""

from typing import Any, Dict, Optional


class ModuleResult:
    """Container for module execution results"""
    
    def __init__(self, success: bool = False, data: Optional[Dict[str, Any]] = None, 
                 error: Optional[str] = None):
        self.success = success
        self.data = data or {}
        self.error = error
    
    def __bool__(self) -> bool:
        return self.success
    
    def __repr__(self) -> str:
        if self.success:
            return f"ModuleResult(success=True, data={self.data})"
        return f"ModuleResult(success=False, error='{self.error}')"
