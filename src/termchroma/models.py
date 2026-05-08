"""
Data models for TermChroma.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json
import re


@dataclass
class Color:
    """Represents a color with RGB and HEX values."""
    
    r: int  # Red (0-255)
    g: int  # Green (0-255)
    b: int  # Blue (0-255)
    name: Optional[str] = None
    
    def __post_init__(self):
        """Validate color values."""
        for component, name in [(self.r, 'r'), (self.g, 'g'), (self.b, 'b')]:
            if not 0 <= component <= 255:
                raise ValueError(f"{name} must be between 0 and 255, got {component}")
    
    @classmethod
    def from_hex(cls, hex_str: str, name: Optional[str] = None) -> "Color":
        """Create a Color from a hex string (#RRGGBB, RRGGBB, #RGB, or RGB)."""
        hex_str = hex_str.lstrip('#')
        
        # Support 3-character short format (#RGB -> #RRGGBB)
        if len(hex_str) == 3:
            if not re.match(r'^[0-9A-Fa-f]{3}$', hex_str):
                raise ValueError(f"Invalid hex color: {hex_str}")
            hex_str = ''.join([c * 2 for c in hex_str])
        
        if len(hex_str) != 6:
            raise ValueError(f"Invalid hex color: {hex_str}")
        if not re.match(r'^[0-9A-Fa-f]{6}$', hex_str):
            raise ValueError(f"Invalid hex color: {hex_str}")
        
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return cls(r=r, g=g, b=b, name=name)
    
    @classmethod
    def from_rgb_tuple(cls, rgb: tuple, name: Optional[str] = None) -> "Color":
        """Create a Color from an RGB tuple."""
        return cls(r=rgb[0], g=rgb[1], b=rgb[2], name=name)
    
    @property
    def hex(self) -> str:
        """Return the hex representation (#RRGGBB)."""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    @property
    def rgb(self) -> tuple:
        """Return the RGB tuple."""
        return (self.r, self.g, self.b)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "r": self.r,
            "g": self.g,
            "b": self.b,
            "hex": self.hex,
            "name": self.name
        }
    
    def __str__(self) -> str:
        """String representation."""
        name_part = f" ({self.name})" if self.name else ""
        return f"{self.hex}{name_part}"
    
    def __hash__(self) -> int:
        """Make Color hashable."""
        return hash((self.r, self.g, self.b))
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Color):
            return False
        return self.rgb == other.rgb


@dataclass
class Theme:
    """Represents a complete terminal color theme."""
    
    name: str
    author: str = "Unknown"
    description: str = ""
    
    # Standard 16 terminal colors
    black: Color = field(default_factory=lambda: Color(0, 0, 0, "black"))
    red: Color = field(default_factory=lambda: Color(205, 49, 49, "red"))
    green: Color = field(default_factory=lambda: Color(13, 188, 121, "green"))
    yellow: Color = field(default_factory=lambda: Color(229, 229, 16, "yellow"))
    blue: Color = field(default_factory=lambda: Color(36, 114, 200, "blue"))
    magenta: Color = field(default_factory=lambda: Color(188, 63, 188, "magenta"))
    cyan: Color = field(default_factory=lambda: Color(17, 168, 205, "cyan"))
    white: Color = field(default_factory=lambda: Color(229, 229, 229, "white"))
    
    # Bright variants
    bright_black: Color = field(default_factory=lambda: Color(102, 102, 102, "bright_black"))
    bright_red: Color = field(default_factory=lambda: Color(241, 76, 76, "bright_red"))
    bright_green: Color = field(default_factory=lambda: Color(35, 209, 139, "bright_green"))
    bright_yellow: Color = field(default_factory=lambda: Color(245, 245, 67, "bright_yellow"))
    bright_blue: Color = field(default_factory=lambda: Color(59, 142, 234, "bright_blue"))
    bright_magenta: Color = field(default_factory=lambda: Color(214, 112, 214, "bright_magenta"))
    bright_cyan: Color = field(default_factory=lambda: Color(41, 184, 219, "bright_cyan"))
    bright_white: Color = field(default_factory=lambda: Color(255, 255, 255, "bright_white"))
    
    # UI colors
    background: Color = field(default_factory=lambda: Color(30, 30, 30, "background"))
    foreground: Color = field(default_factory=lambda: Color(204, 204, 204, "foreground"))
    cursor: Color = field(default_factory=lambda: Color(204, 204, 204, "cursor"))
    selection_background: Optional[Color] = None
    selection_foreground: Optional[Color] = None
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    
    def __post_init__(self):
        """Set default selection colors if not provided."""
        if self.selection_background is None:
            self.selection_background = Color(
                self.background.r + 30 if self.background.r < 225 else 255,
                self.background.g + 30 if self.background.g < 225 else 255,
                self.background.b + 30 if self.background.b < 225 else 255,
                "selection_background"
            )
        if self.selection_foreground is None:
            self.selection_foreground = self.foreground
    
    def get_colors(self) -> Dict[str, Color]:
        """Get all colors as a dictionary."""
        return {
            "black": self.black,
            "red": self.red,
            "green": self.green,
            "yellow": self.yellow,
            "blue": self.blue,
            "magenta": self.magenta,
            "cyan": self.cyan,
            "white": self.white,
            "bright_black": self.bright_black,
            "bright_red": self.bright_red,
            "bright_green": self.bright_green,
            "bright_yellow": self.bright_yellow,
            "bright_blue": self.bright_blue,
            "bright_magenta": self.bright_magenta,
            "bright_cyan": self.bright_cyan,
            "bright_white": self.bright_white,
            "background": self.background,
            "foreground": self.foreground,
            "cursor": self.cursor,
            "selection_background": self.selection_background,
            "selection_foreground": self.selection_foreground,
        }
    
    def get_ansi_colors(self) -> List[Color]:
        """Get the 16 ANSI colors in order."""
        return [
            self.black, self.red, self.green, self.yellow,
            self.blue, self.magenta, self.cyan, self.white,
            self.bright_black, self.bright_red, self.bright_green, self.bright_yellow,
            self.bright_blue, self.bright_magenta, self.bright_cyan, self.bright_white,
        ]
    
    def to_dict(self) -> Dict:
        """Convert theme to dictionary."""
        colors = self.get_colors()
        return {
            "name": self.name,
            "author": self.author,
            "description": self.description,
            "version": self.version,
            "tags": self.tags,
            "colors": {k: v.to_dict() for k, v in colors.items()},
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert theme to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Theme":
        """Create a Theme from a dictionary."""
        colors = data.get("colors", {})
        
        def get_color(key: str, default: Color) -> Color:
            c = colors.get(key)
            if c is None:
                return default
            if isinstance(c, Color):
                return c
            return Color.from_hex(c["hex"], c.get("name"))
        
        return cls(
            name=data["name"],
            author=data.get("author", "Unknown"),
            description=data.get("description", ""),
            version=data.get("version", "1.0.0"),
            tags=data.get("tags", []),
            black=get_color("black", Color(0, 0, 0, "black")),
            red=get_color("red", Color(205, 49, 49, "red")),
            green=get_color("green", Color(13, 188, 121, "green")),
            yellow=get_color("yellow", Color(229, 229, 16, "yellow")),
            blue=get_color("blue", Color(36, 114, 200, "blue")),
            magenta=get_color("magenta", Color(188, 63, 188, "magenta")),
            cyan=get_color("cyan", Color(17, 168, 205, "cyan")),
            white=get_color("white", Color(229, 229, 229, "white")),
            bright_black=get_color("bright_black", Color(102, 102, 102, "bright_black")),
            bright_red=get_color("bright_red", Color(241, 76, 76, "bright_red")),
            bright_green=get_color("bright_green", Color(35, 209, 139, "bright_green")),
            bright_yellow=get_color("bright_yellow", Color(245, 245, 67, "bright_yellow")),
            bright_blue=get_color("bright_blue", Color(59, 142, 234, "bright_blue")),
            bright_magenta=get_color("bright_magenta", Color(214, 112, 214, "bright_magenta")),
            bright_cyan=get_color("bright_cyan", Color(41, 184, 219, "bright_cyan")),
            bright_white=get_color("bright_white", Color(255, 255, 255, "bright_white")),
            background=get_color("background", Color(30, 30, 30, "background")),
            foreground=get_color("foreground", Color(204, 204, 204, "foreground")),
            cursor=get_color("cursor", Color(204, 204, 204, "cursor")),
            selection_background=get_color("selection_background", None),
            selection_foreground=get_color("selection_foreground", None),
        )
    
    def __str__(self) -> str:
        """String representation."""
        return f"Theme({self.name} by {self.author})"
