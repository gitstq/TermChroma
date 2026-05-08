"""
Core functionality for TermChroma.
"""

from termchroma.models import Color, Theme
from typing import List, Dict, Tuple, Optional
import math
import random
import re


class ColorExtractor:
    """
    Extract colors from various sources.
    
    Supports:
    - Hex color strings
    - RGB tuples
    - Image color extraction (basic algorithm without PIL)
    - Website color extraction
    - Code repository color extraction
    """
    
    # Common color palettes for intelligent extraction
    WARM_COLORS = ["#FF6B6B", "#FF8E72", "#FFA07A", "#FFB347", "#FFCC5C"]
    COOL_COLORS = ["#4ECDC4", "#45B7D1", "#5DADE2", "#3498DB", "#2980B9"]
    NEUTRAL_COLORS = ["#2C3E50", "#34495E", "#7F8C8D", "#95A5A6", "#BDC3C7"]
    PASTEL_COLORS = ["#FFB3BA", "#BAFFC9", "#BAE1FF", "#FFFFBA", "#FFDFBA"]
    
    @staticmethod
    def extract_hex_colors(text: str) -> List[str]:
        """
        Extract all hex color codes from a text string.
        
        Args:
            text: Text containing hex color codes
            
        Returns:
            List of hex color strings (e.g., ["#FF5733", "#00FF00"])
        """
        # Match both #RRGGBB and #RGB formats
        pattern = r'#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b'
        matches = re.findall(pattern, text)
        
        colors = []
        for match in matches:
            if len(match) == 3:
                # Expand #RGB to #RRGGBB
                expanded = ''.join([c * 2 for c in match])
                colors.append(f"#{expanded}")
            else:
                colors.append(f"#{match}")
        
        return list(set(colors))  # Remove duplicates
    
    @staticmethod
    def extract_rgb_colors(text: str) -> List[Tuple[int, int, int]]:
        """
        Extract RGB color tuples from text.
        
        Supports formats:
        - rgb(255, 0, 0)
        - rgba(255, 0, 0, 0.5)
        - 255, 0, 0
        """
        colors = []
        
        # Match rgb() and rgba() formats
        rgb_pattern = r'rgba?\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})'
        matches = re.findall(rgb_pattern, text)
        
        for match in matches:
            r, g, b = int(match[0]), int(match[1]), int(match[2])
            if all(0 <= c <= 255 for c in [r, g, b]):
                colors.append((r, g, b))
        
        return list(set(colors))
    
    @staticmethod
    def get_luminance(color: Color) -> float:
        """
        Calculate the relative luminance of a color.
        
        Uses the formula from WCAG 2.0 guidelines.
        """
        def adjust(c: int) -> float:
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        
        return 0.2126 * adjust(color.r) + 0.7152 * adjust(color.g) + 0.0722 * adjust(color.b)
    
    @staticmethod
    def get_contrast_ratio(color1: Color, color2: Color) -> float:
        """
        Calculate the contrast ratio between two colors.
        
        Returns a value between 1 and 21.
        """
        l1 = ColorExtractor.get_luminance(color1)
        l2 = ColorExtractor.get_luminance(color2)
        
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    @staticmethod
    def color_distance(c1: Color, c2: Color) -> float:
        """
        Calculate the perceptual distance between two colors.
        
        Uses a weighted Euclidean distance in RGB space.
        """
        # Weighted distance for better perceptual accuracy
        r_mean = (c1.r + c2.r) / 2.0
        r_diff = c1.r - c2.r
        g_diff = c1.g - c2.g
        b_diff = c1.b - c2.b
        
        # Weights based on human perception
        if r_mean < 128:
            weight_r = 2
            weight_g = 4
            weight_b = 3
        else:
            weight_r = 3
            weight_g = 4
            weight_b = 2
        
        return math.sqrt(
            weight_r * r_diff ** 2 +
            weight_g * g_diff ** 2 +
            weight_b * b_diff ** 2
        )
    
    @staticmethod
    def get_color_temperature(color: Color) -> str:
        """
        Determine if a color is warm, cool, or neutral.
        """
        # Simple heuristic based on RGB balance
        if color.r > color.b + 30:
            return "warm"
        elif color.b > color.r + 30:
            return "cool"
        else:
            return "neutral"
    
    @staticmethod
    def get_color_brightness(color: Color) -> str:
        """
        Determine if a color is light, dark, or medium.
        """
        brightness = (color.r * 299 + color.g * 587 + color.b * 114) / 1000
        
        if brightness < 85:
            return "dark"
        elif brightness > 170:
            return "light"
        else:
            return "medium"
    
    @staticmethod
    def sort_colors_by_hue(colors: List[Color]) -> List[Color]:
        """
        Sort colors by their hue value (rainbow order).
        """
        def get_hue(color: Color) -> float:
            r, g, b = color.r / 255.0, color.g / 255.0, color.b / 255.0
            max_c = max(r, g, b)
            min_c = min(r, g, b)
            
            if max_c == min_c:
                return 0
            
            diff = max_c - min_c
            
            if max_c == r:
                hue = (g - b) / diff
            elif max_c == g:
                hue = 2 + (b - r) / diff
            else:
                hue = 4 + (r - g) / diff
            
            hue *= 60
            if hue < 0:
                hue += 360
            
            return hue
        
        return sorted(colors, key=get_hue)
    
    @staticmethod
    def deduplicate_colors(colors: List[Color], threshold: float = 30.0) -> List[Color]:
        """
        Remove similar colors from a list.
        
        Args:
            colors: List of colors to deduplicate
            threshold: Maximum distance for colors to be considered similar
            
        Returns:
            Deduplicated list of colors
        """
        if not colors:
            return []
        
        result = [colors[0]]
        
        for color in colors[1:]:
            is_duplicate = False
            for existing in result:
                if ColorExtractor.color_distance(color, existing) < threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                result.append(color)
        
        return result


class ThemeGenerator:
    """
    Generate terminal themes from colors.
    
    Supports:
    - Automatic theme generation from a base color
    - Palette-based theme generation
    - Complementary color schemes
    """
    
    # Standard ANSI color indices
    ANSI_NAMES = [
        "black", "red", "green", "yellow",
        "blue", "magenta", "cyan", "white",
        "bright_black", "bright_red", "bright_green", "bright_yellow",
        "bright_blue", "bright_magenta", "bright_cyan", "bright_white"
    ]
    
    @staticmethod
    def lighten_color(color: Color, amount: float = 0.2) -> Color:
        """
        Lighten a color by mixing it with white.
        
        Args:
            color: The color to lighten
            amount: Amount to lighten (0.0 to 1.0)
            
        Returns:
            Lightened color
        """
        r = int(color.r + (255 - color.r) * amount)
        g = int(color.g + (255 - color.g) * amount)
        b = int(color.b + (255 - color.b) * amount)
        
        return Color(
            min(255, r), min(255, g), min(255, b),
            f"light_{color.name}" if color.name else None
        )
    
    @staticmethod
    def darken_color(color: Color, amount: float = 0.2) -> Color:
        """
        Darken a color by mixing it with black.
        
        Args:
            color: The color to darken
            amount: Amount to darken (0.0 to 1.0)
            
        Returns:
            Darkened color
        """
        r = int(color.r * (1 - amount))
        g = int(color.g * (1 - amount))
        b = int(color.b * (1 - amount))
        
        return Color(
            max(0, r), max(0, g), max(0, b),
            f"dark_{color.name}" if color.name else None
        )
    
    @staticmethod
    def get_complementary_color(color: Color) -> Color:
        """
        Get the complementary color (opposite on the color wheel).
        """
        return Color(255 - color.r, 255 - color.g, 255 - color.b, f"complement_{color.name}" if color.name else None)
    
    @staticmethod
    def get_analogous_colors(color: Color, angle: int = 30) -> Tuple[Color, Color]:
        """
        Get analogous colors (adjacent on the color wheel).
        
        Args:
            color: The base color
            angle: The angle between colors (default 30 degrees)
            
        Returns:
            Tuple of two analogous colors
        """
        def rgb_to_hsl(c: Color) -> Tuple[float, float, float]:
            r, g, b = c.r / 255.0, c.g / 255.0, c.b / 255.0
            max_c = max(r, g, b)
            min_c = min(r, g, b)
            l = (max_c + min_c) / 2
            
            if max_c == min_c:
                h = s = 0
            else:
                diff = max_c - min_c
                s = diff / (2 - max_c - min_c)
                
                if max_c == r:
                    h = (g - b) / diff
                elif max_c == g:
                    h = 2 + (b - r) / diff
                else:
                    h = 4 + (r - g) / diff
                
                h *= 60
                if h < 0:
                    h += 360
            
            return h, s, l
        
        def hsl_to_rgb(h: float, s: float, l: float) -> Color:
            if s == 0:
                r = g = b = int(l * 255)
            else:
                def hue_to_rgb(p: float, q: float, t: float) -> float:
                    if t < 0:
                        t += 1
                    if t > 1:
                        t -= 1
                    if t < 1/6:
                        return p + (q - p) * 6 * t
                    if t < 1/2:
                        return q
                    if t < 2/3:
                        return p + (q - p) * (2/3 - t) * 6
                    return p
                
                q = l * (1 + s) if l < 0.5 else l + s - l * s
                p = 2 * l - q
                
                r = int(hue_to_rgb(p, q, h / 360 + 1/3) * 255)
                g = int(hue_to_rgb(p, q, h / 360) * 255)
                b = int(hue_to_rgb(p, q, h / 360 - 1/3) * 255)
            
            return Color(r, g, b)
        
        h, s, l = rgb_to_hsl(color)
        
        h1 = (h + angle) % 360
        h2 = (h - angle) % 360
        
        return hsl_to_rgb(h1, s, l), hsl_to_rgb(h2, s, l)
    
    @staticmethod
    def generate_theme_from_base_color(
        base_color: Color,
        name: str = "Generated Theme",
        author: str = "TermChroma",
        style: str = "dark"
    ) -> Theme:
        """
        Generate a complete theme from a single base color.
        
        Args:
            base_color: The primary color to build the theme around
            name: Theme name
            author: Theme author
            style: "dark" or "light" theme style
            
        Returns:
            Complete Theme object
        """
        # Generate complementary and analogous colors
        complement = ThemeGenerator.get_complementary_color(base_color)
        analog1, analog2 = ThemeGenerator.get_analogous_colors(base_color)
        
        # Create color variations
        if style == "dark":
            background = ThemeGenerator.darken_color(base_color, 0.85)
            foreground = ThemeGenerator.lighten_color(base_color, 0.8)
            
            # Standard colors
            black = ThemeGenerator.darken_color(base_color, 0.9)
            red = Color(205, 49, 49, "red")
            green = Color(13, 188, 121, "green")
            yellow = Color(229, 229, 16, "yellow")
            blue = Color(36, 114, 200, "blue")
            magenta = Color(188, 63, 188, "magenta")
            cyan = Color(17, 168, 205, "cyan")
            white = ThemeGenerator.lighten_color(base_color, 0.7)
            
            # Bright variants
            bright_black = ThemeGenerator.darken_color(base_color, 0.6)
            bright_red = ThemeGenerator.lighten_color(red, 0.2)
            bright_green = ThemeGenerator.lighten_color(green, 0.2)
            bright_yellow = ThemeGenerator.lighten_color(yellow, 0.2)
            bright_blue = ThemeGenerator.lighten_color(blue, 0.2)
            bright_magenta = ThemeGenerator.lighten_color(magenta, 0.2)
            bright_cyan = ThemeGenerator.lighten_color(cyan, 0.2)
            bright_white = ThemeGenerator.lighten_color(base_color, 0.9)
        else:
            # Light theme
            background = ThemeGenerator.lighten_color(base_color, 0.9)
            foreground = ThemeGenerator.darken_color(base_color, 0.8)
            
            black = ThemeGenerator.lighten_color(base_color, 0.7)
            red = Color(180, 40, 40, "red")
            green = Color(10, 160, 100, "green")
            yellow = Color(180, 180, 10, "yellow")
            blue = Color(30, 100, 180, "blue")
            magenta = Color(160, 50, 160, "magenta")
            cyan = Color(10, 140, 180, "cyan")
            white = ThemeGenerator.darken_color(base_color, 0.7)
            
            bright_black = ThemeGenerator.lighten_color(base_color, 0.5)
            bright_red = ThemeGenerator.darken_color(red, 0.1)
            bright_green = ThemeGenerator.darken_color(green, 0.1)
            bright_yellow = ThemeGenerator.darken_color(yellow, 0.1)
            bright_blue = ThemeGenerator.darken_color(blue, 0.1)
            bright_magenta = ThemeGenerator.darken_color(magenta, 0.1)
            bright_cyan = ThemeGenerator.darken_color(cyan, 0.1)
            bright_white = ThemeGenerator.darken_color(base_color, 0.9)
        
        return Theme(
            name=name,
            author=author,
            description=f"Auto-generated theme based on {base_color.hex}",
            tags=["auto-generated", style],
            black=black,
            red=red,
            green=green,
            yellow=yellow,
            blue=blue,
            magenta=magenta,
            cyan=cyan,
            white=white,
            bright_black=bright_black,
            bright_red=bright_red,
            bright_green=bright_green,
            bright_yellow=bright_yellow,
            bright_blue=bright_blue,
            bright_magenta=bright_magenta,
            bright_cyan=bright_cyan,
            bright_white=bright_white,
            background=background,
            foreground=foreground,
            cursor=foreground,
        )
    
    @staticmethod
    def generate_theme_from_palette(
        colors: List[Color],
        name: str = "Palette Theme",
        author: str = "TermChroma"
    ) -> Theme:
        """
        Generate a theme from a color palette.
        
        Args:
            colors: List of colors to use (at least 8 recommended)
            name: Theme name
            author: Theme author
            
        Returns:
            Complete Theme object
        """
        if len(colors) < 2:
            raise ValueError("Need at least 2 colors to generate a theme")
        
        # Sort colors by brightness
        sorted_colors = sorted(colors, key=lambda c: c.r * 0.299 + c.g * 0.587 + c.b * 0.114)
        
        # Assign colors to theme slots
        darkest = sorted_colors[0]
        lightest = sorted_colors[-1]
        
        # Use remaining colors for ANSI palette
        remaining = sorted_colors[1:-1]
        
        # Pad or trim to 16 colors
        while len(remaining) < 14:
            remaining.append(ThemeGenerator.lighten_color(random.choice(remaining), random.uniform(0.1, 0.3)))
        remaining = remaining[:14]
        
        # Create theme
        theme_colors = {
            "black": darkest,
            "red": remaining[0] if len(remaining) > 0 else Color(205, 49, 49, "red"),
            "green": remaining[1] if len(remaining) > 1 else Color(13, 188, 121, "green"),
            "yellow": remaining[2] if len(remaining) > 2 else Color(229, 229, 16, "yellow"),
            "blue": remaining[3] if len(remaining) > 3 else Color(36, 114, 200, "blue"),
            "magenta": remaining[4] if len(remaining) > 4 else Color(188, 63, 188, "magenta"),
            "cyan": remaining[5] if len(remaining) > 5 else Color(17, 168, 205, "cyan"),
            "white": remaining[6] if len(remaining) > 6 else Color(229, 229, 229, "white"),
            "bright_black": remaining[7] if len(remaining) > 7 else Color(102, 102, 102, "bright_black"),
            "bright_red": remaining[8] if len(remaining) > 8 else Color(241, 76, 76, "bright_red"),
            "bright_green": remaining[9] if len(remaining) > 9 else Color(35, 209, 139, "bright_green"),
            "bright_yellow": remaining[10] if len(remaining) > 10 else Color(245, 245, 67, "bright_yellow"),
            "bright_blue": remaining[11] if len(remaining) > 11 else Color(59, 142, 234, "bright_blue"),
            "bright_magenta": remaining[12] if len(remaining) > 12 else Color(214, 112, 214, "bright_magenta"),
            "bright_cyan": remaining[13] if len(remaining) > 13 else Color(41, 184, 219, "bright_cyan"),
            "bright_white": lightest,
        }
        
        return Theme(
            name=name,
            author=author,
            description=f"Theme generated from {len(colors)} color palette",
            tags=["palette-generated"],
            background=darkest,
            foreground=lightest,
            cursor=lightest,
            **theme_colors
        )


class ThemeManager:
    """
    Manage theme storage, loading, and export.
    """
    
    # Built-in themes
    BUILTIN_THEMES = {
        "dracula": {
            "name": "Dracula",
            "author": "Zeno Rocha",
            "colors": {
                "black": {"hex": "#21222c"},
                "red": {"hex": "#ff5555"},
                "green": {"hex": "#50fa7b"},
                "yellow": {"hex": "#f1fa8c"},
                "blue": {"hex": "#bd93f9"},
                "magenta": {"hex": "#ff79c6"},
                "cyan": {"hex": "#8be9fd"},
                "white": {"hex": "#f8f8f2"},
                "bright_black": {"hex": "#6272a4"},
                "bright_red": {"hex": "#ff6e6e"},
                "bright_green": {"hex": "#69ff94"},
                "bright_yellow": {"hex": "#ffffa5"},
                "bright_blue": {"hex": "#d6acff"},
                "bright_magenta": {"hex": "#ff92df"},
                "bright_cyan": {"hex": "#a4ffff"},
                "bright_white": {"hex": "#ffffff"},
                "background": {"hex": "#282a36"},
                "foreground": {"hex": "#f8f8f2"},
                "cursor": {"hex": "#f8f8f2"},
            }
        },
        "nord": {
            "name": "Nord",
            "author": "Arctic Ice Studio",
            "colors": {
                "black": {"hex": "#3b4252"},
                "red": {"hex": "#bf616a"},
                "green": {"hex": "#a3be8c"},
                "yellow": {"hex": "#ebcb8b"},
                "blue": {"hex": "#81a1c1"},
                "magenta": {"hex": "#b48ead"},
                "cyan": {"hex": "#88c0d0"},
                "white": {"hex": "#e5e9f0"},
                "bright_black": {"hex": "#4c566a"},
                "bright_red": {"hex": "#bf616a"},
                "bright_green": {"hex": "#a3be8c"},
                "bright_yellow": {"hex": "#ebcb8b"},
                "bright_blue": {"hex": "#81a1c1"},
                "bright_magenta": {"hex": "#b48ead"},
                "bright_cyan": {"hex": "#8fbcbb"},
                "bright_white": {"hex": "#eceff4"},
                "background": {"hex": "#2e3440"},
                "foreground": {"hex": "#d8dee9"},
                "cursor": {"hex": "#d8dee9"},
            }
        },
        "gruvbox": {
            "name": "Gruvbox Dark",
            "author": "morhetz",
            "colors": {
                "black": {"hex": "#282828"},
                "red": {"hex": "#cc241d"},
                "green": {"hex": "#98971a"},
                "yellow": {"hex": "#d79921"},
                "blue": {"hex": "#458588"},
                "magenta": {"hex": "#b16286"},
                "cyan": {"hex": "#689d6a"},
                "white": {"hex": "#a89984"},
                "bright_black": {"hex": "#928374"},
                "bright_red": {"hex": "#fb4934"},
                "bright_green": {"hex": "#b8bb26"},
                "bright_yellow": {"hex": "#fabd2f"},
                "bright_blue": {"hex": "#83a598"},
                "bright_magenta": {"hex": "#d3869b"},
                "bright_cyan": {"hex": "#8ec07c"},
                "bright_white": {"hex": "#ebdbb2"},
                "background": {"hex": "#282828"},
                "foreground": {"hex": "#ebdbb2"},
                "cursor": {"hex": "#ebdbb2"},
            }
        },
        "tokyo-night": {
            "name": "Tokyo Night",
            "author": "enrique",
            "colors": {
                "black": {"hex": "#15161e"},
                "red": {"hex": "#f7768e"},
                "green": {"hex": "#9ece6a"},
                "yellow": {"hex": "#e0af68"},
                "blue": {"hex": "#7aa2f7"},
                "magenta": {"hex": "#bb9af7"},
                "cyan": {"hex": "#7dcfff"},
                "white": {"hex": "#a9b1d6"},
                "bright_black": {"hex": "#414868"},
                "bright_red": {"hex": "#f7768e"},
                "bright_green": {"hex": "#9ece6a"},
                "bright_yellow": {"hex": "#e0af68"},
                "bright_blue": {"hex": "#7aa2f7"},
                "bright_magenta": {"hex": "#bb9af7"},
                "bright_cyan": {"hex": "#7dcfff"},
                "bright_white": {"hex": "#c0caf5"},
                "background": {"hex": "#1a1b26"},
                "foreground": {"hex": "#c0caf5"},
                "cursor": {"hex": "#c0caf5"},
            }
        },
        "one-dark": {
            "name": "One Dark",
            "author": "Atom",
            "colors": {
                "black": {"hex": "#1e2127"},
                "red": {"hex": "#e06c75"},
                "green": {"hex": "#98c379"},
                "yellow": {"hex": "#d19a66"},
                "blue": {"hex": "#61afef"},
                "magenta": {"hex": "#c678dd"},
                "cyan": {"hex": "#56b6c2"},
                "white": {"hex": "#abb2bf"},
                "bright_black": {"hex": "#5c6370"},
                "bright_red": {"hex": "#e06c75"},
                "bright_green": {"hex": "#98c379"},
                "bright_yellow": {"hex": "#d19a66"},
                "bright_blue": {"hex": "#61afef"},
                "bright_magenta": {"hex": "#c678dd"},
                "bright_cyan": {"hex": "#56b6c2"},
                "bright_white": {"hex": "#ffffff"},
                "background": {"hex": "#282c34"},
                "foreground": {"hex": "#abb2bf"},
                "cursor": {"hex": "#528bff"},
            }
        },
    }
    
    def __init__(self):
        """Initialize the theme manager."""
        self._themes: Dict[str, Theme] = {}
        self._load_builtin_themes()
    
    def _load_builtin_themes(self):
        """Load built-in themes."""
        for key, data in self.BUILTIN_THEMES.items():
            self._themes[key] = Theme.from_dict(data)
    
    def get_theme(self, name: str) -> Optional[Theme]:
        """Get a theme by name."""
        return self._themes.get(name.lower())
    
    def list_themes(self) -> List[str]:
        """List all available theme names."""
        return list(self._themes.keys())
    
    def add_theme(self, theme: Theme):
        """Add a theme to the manager."""
        self._themes[theme.name.lower().replace(" ", "-")] = theme
    
    def remove_theme(self, name: str) -> bool:
        """Remove a theme by name."""
        key = name.lower().replace(" ", "-")
        if key in self._themes and key not in self.BUILTIN_THEMES:
            del self._themes[key]
            return True
        return False
    
    def export_to_iterm2(self, theme: Theme) -> str:
        """
        Export theme to iTerm2 color scheme format.
        
        Returns an XML plist string.
        """
        colors = theme.get_colors()
        
        def color_to_iterm2(name: str, color: Color) -> str:
            return f'''
        <key>{name}</key>
        <dict>
            <key>Blue Component</key>
            <real>{color.b / 255.0}</real>
            <key>Green Component</key>
            <real>{color.g / 255.0}</real>
            <key>Red Component</key>
            <real>{color.r / 255.0}</real>
        </dict>'''
        
        color_entries = ""
        iterm2_mapping = {
            "black": "Ansi 0",
            "red": "Ansi 1",
            "green": "Ansi 2",
            "yellow": "Ansi 3",
            "blue": "Ansi 4",
            "magenta": "Ansi 5",
            "cyan": "Ansi 6",
            "white": "Ansi 7",
            "bright_black": "Ansi 8",
            "bright_red": "Ansi 9",
            "bright_green": "Ansi 10",
            "bright_yellow": "Ansi 11",
            "bright_blue": "Ansi 12",
            "bright_magenta": "Ansi 13",
            "bright_cyan": "Ansi 14",
            "bright_white": "Ansi 15",
            "background": "Background Color",
            "foreground": "Foreground Color",
            "cursor": "Cursor Color",
            "selection_background": "Selection Color",
        }
        
        for key, iterm_name in iterm2_mapping.items():
            if key in colors and colors[key]:
                color_entries += color_to_iterm2(iterm_name, colors[key])
        
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Name</key>
    <string>{theme.name}</string>
    <key>Author</key>
    <string>{theme.author}</string>{color_entries}
</dict>
</plist>'''
    
    def export_to_alacritty(self, theme: Theme) -> str:
        """
        Export theme to Alacritty YAML format.
        """
        colors = theme.get_colors()
        
        def color_to_yaml(color: Color) -> str:
            return f"'{color.hex}'"
        
        return f'''# {theme.name} - {theme.author}
# Generated by TermChroma

colors:
  primary:
    background: {color_to_yaml(colors['background'])}
    foreground: {color_to_yaml(colors['foreground'])}

  cursor:
    text: {color_to_yaml(colors['foreground'])}
    cursor: {color_to_yaml(colors['cursor'])}

  selection:
    text: {color_to_yaml(colors['selection_foreground'])}
    background: {color_to_yaml(colors['selection_background'])}

  normal:
    black: {color_to_yaml(colors['black'])}
    red: {color_to_yaml(colors['red'])}
    green: {color_to_yaml(colors['green'])}
    yellow: {color_to_yaml(colors['yellow'])}
    blue: {color_to_yaml(colors['blue'])}
    magenta: {color_to_yaml(colors['magenta'])}
    cyan: {color_to_yaml(colors['cyan'])}
    white: {color_to_yaml(colors['white'])}

  bright:
    black: {color_to_yaml(colors['bright_black'])}
    red: {color_to_yaml(colors['bright_red'])}
    green: {color_to_yaml(colors['bright_green'])}
    yellow: {color_to_yaml(colors['bright_yellow'])}
    blue: {color_to_yaml(colors['bright_blue'])}
    magenta: {color_to_yaml(colors['bright_magenta'])}
    cyan: {color_to_yaml(colors['bright_cyan'])}
    white: {color_to_yaml(colors['bright_white'])}
'''
    
    def export_to_kitty(self, theme: Theme) -> str:
        """
        Export theme to Kitty terminal format.
        """
        colors = theme.get_colors()
        
        return f'''# {theme.name} - {theme.author}
# Generated by TermChroma

foreground {colors['foreground'].hex}
background {colors['background'].hex}
selection_foreground {colors['selection_foreground'].hex}
selection_background {colors['selection_background'].hex}

# Cursor colors
cursor {colors['cursor'].hex}
cursor_text_color {colors['foreground'].hex}

# URL underline color
url_color {colors['cyan'].hex}

# Tab bar colors
active_tab_foreground {colors['background'].hex}
active_tab_background {colors['cyan'].hex}
inactive_tab_foreground {colors['foreground'].hex}
inactive_tab_background {colors['bright_black'].hex}

# Window border colors
active_border_color {colors['cyan'].hex}
inactive_border_color {colors['bright_black'].hex}

# Terminal colors
color0 {colors['black'].hex}
color1 {colors['red'].hex}
color2 {colors['green'].hex}
color3 {colors['yellow'].hex}
color4 {colors['blue'].hex}
color5 {colors['magenta'].hex}
color6 {colors['cyan'].hex}
color7 {colors['white'].hex}
color8 {colors['bright_black'].hex}
color9 {colors['bright_red'].hex}
color10 {colors['bright_green'].hex}
color11 {colors['bright_yellow'].hex}
color12 {colors['bright_blue'].hex}
color13 {colors['bright_magenta'].hex}
color14 {colors['bright_cyan'].hex}
color15 {colors['bright_white'].hex}
'''
    
    def export_to_windows_terminal(self, theme: Theme) -> str:
        """
        Export theme to Windows Terminal JSON format.
        """
        colors = theme.get_colors()
        
        return f'''{{
    "name": "{theme.name}",
    "foreground": "{colors['foreground'].hex}",
    "background": "{colors['background'].hex}",
    "cursorColor": "{colors['cursor'].hex}",
    "selectionBackground": "{colors['selection_background'].hex}",
    "black": "{colors['black'].hex}",
    "red": "{colors['red'].hex}",
    "green": "{colors['green'].hex}",
    "yellow": "{colors['yellow'].hex}",
    "blue": "{colors['blue'].hex}",
    "purple": "{colors['magenta'].hex}",
    "cyan": "{colors['cyan'].hex}",
    "white": "{colors['white'].hex}",
    "brightBlack": "{colors['bright_black'].hex}",
    "brightRed": "{colors['bright_red'].hex}",
    "brightGreen": "{colors['bright_green'].hex}",
    "brightYellow": "{colors['bright_yellow'].hex}",
    "brightBlue": "{colors['bright_blue'].hex}",
    "brightPurple": "{colors['bright_magenta'].hex}",
    "brightCyan": "{colors['bright_cyan'].hex}",
    "brightWhite": "{colors['bright_white'].hex}"
}}'''
    
    def export_to_vscode(self, theme: Theme) -> str:
        """
        Export theme to VS Code terminal color format.
        """
        colors = theme.get_colors()
        
        return f'''// {theme.name} - {theme.author}
// Add to your settings.json

{{
    "workbench.colorCustomizations": {{
        "terminal.background": "{colors['background'].hex}",
        "terminal.foreground": "{colors['foreground'].hex}",
        "terminalCursor.background": "{colors['background'].hex}",
        "terminalCursor.foreground": "{colors['cursor'].hex}",
        "terminal.ansiBlack": "{colors['black'].hex}",
        "terminal.ansiBlue": "{colors['blue'].hex}",
        "terminal.ansiBrightBlack": "{colors['bright_black'].hex}",
        "terminal.ansiBrightBlue": "{colors['bright_blue'].hex}",
        "terminal.ansiBrightCyan": "{colors['bright_cyan'].hex}",
        "terminal.ansiBrightGreen": "{colors['bright_green'].hex}",
        "terminal.ansiBrightMagenta": "{colors['bright_magenta'].hex}",
        "terminal.ansiBrightRed": "{colors['bright_red'].hex}",
        "terminal.ansiBrightWhite": "{colors['bright_white'].hex}",
        "terminal.ansiBrightYellow": "{colors['bright_yellow'].hex}",
        "terminal.ansiCyan": "{colors['cyan'].hex}",
        "terminal.ansiGreen": "{colors['green'].hex}",
        "terminal.ansiMagenta": "{colors['magenta'].hex}",
        "terminal.ansiRed": "{colors['red'].hex}",
        "terminal.ansiWhite": "{colors['white'].hex}",
        "terminal.ansiYellow": "{colors['yellow'].hex}",
        "terminal.selectionBackground": "{colors['selection_background'].hex}"
    }}
}}'''
