"""
Modules Package
Security testing modules organized by category
Including C2 Framework integrations and Evasion techniques
"""

__version__ = "1.0.0"

# Import new module categories
from . import c2_frameworks
from . import evasion

__all__ = [
    "c2_frameworks",
    "evasion"
]
