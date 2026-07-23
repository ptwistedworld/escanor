# Escanor C2 Frameworks Module Package
"""
C2 Framework integration modules for Escanor.
Provides interfaces to popular C2 frameworks including Empire, PoshC2, and Koadic.
"""

from .empire_c2 import EmpireC2Module
from .poshc2 import PoshC2Module
from .koadic import KoadicModule

__all__ = [
    "EmpireC2Module",
    "PoshC2Module", 
    "KoadicModule"
]
