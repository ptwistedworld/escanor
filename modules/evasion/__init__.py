# Escanor Evasion Module Package
"""
EDR/AV evasion modules for Escanor.
Provides interfaces to evasion frameworks including EDRSilencer.
"""

from .edrsilencer import EDRSilencerModule

__all__ = [
    "EDRSilencerModule"
]
