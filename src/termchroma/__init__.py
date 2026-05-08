"""
🎨 TermChroma - Lightweight Terminal Color Theme Intelligent Generation & Management Engine
轻量级终端颜色主题智能生成与管理引擎

A zero-dependency CLI tool for extracting, generating, and managing terminal color themes.
"""

__version__ = "1.0.0"
__author__ = "Lobster Agent"
__license__ = "MIT"

from termchroma.core import ColorExtractor, ThemeGenerator, ThemeManager
from termchroma.models import Color, Theme

__all__ = [
    "ColorExtractor",
    "ThemeGenerator", 
    "ThemeManager",
    "Color",
    "Theme",
    "__version__",
]
