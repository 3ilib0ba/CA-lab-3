"""
Translator module
"""

from .preprocessing import minify_text
from .translator import parse_code

__all__ = ('minify_text', 'parse_code')
