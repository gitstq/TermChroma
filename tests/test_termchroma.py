"""
Tests for TermChroma.
"""

import pytest
from termchroma.models import Color, Theme
from termchroma.core import ColorExtractor, ThemeGenerator, ThemeManager


class TestColor:
    """Tests for the Color class."""
    
    def test_color_creation(self):
        """Test creating a color."""
        color = Color(255, 128, 0, "orange")
        assert color.r == 255
        assert color.g == 128
        assert color.b == 0
        assert color.name == "orange"
    
    def test_color_from_hex(self):
        """Test creating a color from hex string."""
        color = Color.from_hex("#FF8000", "orange")
        assert color.r == 255
        assert color.g == 128
        assert color.b == 0
        assert color.hex == "#ff8000"
    
    def test_color_from_hex_short(self):
        """Test creating a color from short hex string."""
        color = Color.from_hex("#F80")
        assert color.r == 255
        assert color.g == 136
        assert color.b == 0
    
    def test_color_invalid_hex(self):
        """Test that invalid hex raises error."""
        with pytest.raises(ValueError):
            Color.from_hex("invalid")
        
        with pytest.raises(ValueError):
            Color.from_hex("#GGGGGG")
    
    def test_color_invalid_rgb(self):
        """Test that invalid RGB raises error."""
        with pytest.raises(ValueError):
            Color(300, 0, 0)
        
        with pytest.raises(ValueError):
            Color(-1, 0, 0)
    
    def test_color_hex_property(self):
        """Test hex property."""
        color = Color(255, 0, 128)
        assert color.hex == "#ff0080"
    
    def test_color_rgb_property(self):
        """Test rgb property."""
        color = Color(255, 128, 0)
        assert color.rgb == (255, 128, 0)
    
    def test_color_equality(self):
        """Test color equality."""
        c1 = Color(255, 128, 0)
        c2 = Color(255, 128, 0)
        c3 = Color(255, 128, 1)
        
        assert c1 == c2
        assert c1 != c3
    
    def test_color_hash(self):
        """Test color hashability."""
        c1 = Color(255, 128, 0)
        c2 = Color(255, 128, 0)
        
        assert hash(c1) == hash(c2)
        assert len({c1, c2}) == 1


class TestTheme:
    """Tests for the Theme class."""
    
    def test_theme_creation(self):
        """Test creating a theme."""
        theme = Theme(
            name="Test Theme",
            author="Test Author",
            description="A test theme"
        )
        
        assert theme.name == "Test Theme"
        assert theme.author == "Test Author"
        assert theme.description == "A test theme"
    
    def test_theme_default_colors(self):
        """Test that theme has default colors."""
        theme = Theme(name="Test")
        
        assert theme.black is not None
        assert theme.red is not None
        assert theme.background is not None
        assert theme.foreground is not None
    
    def test_theme_get_colors(self):
        """Test getting all colors."""
        theme = Theme(name="Test")
        colors = theme.get_colors()
        
        assert "black" in colors
        assert "red" in colors
        assert "background" in colors
        assert len(colors) == 21
    
    def test_theme_get_ansi_colors(self):
        """Test getting ANSI colors."""
        theme = Theme(name="Test")
        ansi = theme.get_ansi_colors()
        
        assert len(ansi) == 16
    
    def test_theme_to_dict(self):
        """Test converting theme to dict."""
        theme = Theme(name="Test", author="Author")
        data = theme.to_dict()
        
        assert data["name"] == "Test"
        assert data["author"] == "Author"
        assert "colors" in data
    
    def test_theme_to_json(self):
        """Test converting theme to JSON."""
        theme = Theme(name="Test")
        json_str = theme.to_json()
        
        assert '"name": "Test"' in json_str
        assert '"colors"' in json_str
    
    def test_theme_from_dict(self):
        """Test creating theme from dict."""
        data = {
            "name": "Test",
            "author": "Author",
            "colors": {
                "black": {"hex": "#000000"},
                "red": {"hex": "#ff0000"},
                "background": {"hex": "#1a1a1a"},
                "foreground": {"hex": "#ffffff"},
            }
        }
        
        theme = Theme.from_dict(data)
        
        assert theme.name == "Test"
        assert theme.author == "Author"
        assert theme.black.hex == "#000000"
        assert theme.red.hex == "#ff0000"


class TestColorExtractor:
    """Tests for the ColorExtractor class."""
    
    def test_extract_hex_colors(self):
        """Test extracting hex colors from text."""
        text = "Colors: #FF5733 #00FF00 #0000FF"
        colors = ColorExtractor.extract_hex_colors(text)
        
        assert len(colors) == 3
        # Colors are case-preserved from input
        colors_lower = [c.lower() for c in colors]
        assert "#ff5733" in colors_lower
        assert "#00ff00" in colors_lower
        assert "#0000ff" in colors_lower
    
    def test_extract_hex_colors_short(self):
        """Test extracting short hex colors."""
        text = "Color: #F80"
        colors = ColorExtractor.extract_hex_colors(text)
        
        assert len(colors) == 1
        assert colors[0].lower() == "#ff8800"
    
    def test_extract_rgb_colors(self):
        """Test extracting RGB colors."""
        text = "rgb(255, 0, 128) and rgba(100, 200, 50, 0.5)"
        colors = ColorExtractor.extract_rgb_colors(text)
        
        assert len(colors) == 2
        assert (255, 0, 128) in colors
        assert (100, 200, 50) in colors
    
    def test_get_luminance(self):
        """Test luminance calculation."""
        white = Color(255, 255, 255)
        black = Color(0, 0, 0)
        
        assert ColorExtractor.get_luminance(white) > ColorExtractor.get_luminance(black)
    
    def test_get_contrast_ratio(self):
        """Test contrast ratio calculation."""
        white = Color(255, 255, 255)
        black = Color(0, 0, 0)
        
        ratio = ColorExtractor.get_contrast_ratio(white, black)
        assert ratio == 21.0  # Maximum contrast
    
    def test_color_distance(self):
        """Test color distance calculation."""
        c1 = Color(0, 0, 0)
        c2 = Color(255, 255, 255)
        c3 = Color(0, 0, 1)
        
        assert ColorExtractor.color_distance(c1, c2) > ColorExtractor.color_distance(c1, c3)
    
    def test_get_color_temperature(self):
        """Test color temperature detection."""
        warm = Color(255, 100, 50)
        cool = Color(50, 100, 255)
        neutral = Color(128, 128, 128)
        
        assert ColorExtractor.get_color_temperature(warm) == "warm"
        assert ColorExtractor.get_color_temperature(cool) == "cool"
        assert ColorExtractor.get_color_temperature(neutral) == "neutral"
    
    def test_deduplicate_colors(self):
        """Test color deduplication."""
        colors = [
            Color(0, 0, 0),
            Color(1, 1, 1),  # Very similar to black
            Color(255, 0, 0),
            Color(254, 0, 0),  # Very similar to red
        ]
        
        deduped = ColorExtractor.deduplicate_colors(colors, threshold=10.0)
        assert len(deduped) < len(colors)


class TestThemeGenerator:
    """Tests for the ThemeGenerator class."""
    
    def test_lighten_color(self):
        """Test lightening a color."""
        color = Color(100, 100, 100)
        lightened = ThemeGenerator.lighten_color(color, 0.5)
        
        assert lightened.r > color.r
        assert lightened.g > color.g
        assert lightened.b > color.b
    
    def test_darken_color(self):
        """Test darkening a color."""
        color = Color(200, 200, 200)
        darkened = ThemeGenerator.darken_color(color, 0.5)
        
        assert darkened.r < color.r
        assert darkened.g < color.g
        assert darkened.b < color.b
    
    def test_get_complementary_color(self):
        """Test getting complementary color."""
        color = Color(255, 0, 0)
        complement = ThemeGenerator.get_complementary_color(color)
        
        assert complement.r == 0
        assert complement.g == 255
        assert complement.b == 255
    
    def test_generate_theme_from_base_color(self):
        """Test generating a theme from base color."""
        base = Color.from_hex("#FF5733")
        theme = ThemeGenerator.generate_theme_from_base_color(
            base_color=base,
            name="Test Theme",
            author="Test"
        )
        
        assert theme.name == "Test Theme"
        assert theme.author == "Test"
        assert theme.black is not None
        assert theme.background is not None
        assert theme.foreground is not None
    
    def test_generate_light_theme(self):
        """Test generating a light theme."""
        base = Color.from_hex("#FF5733")
        theme = ThemeGenerator.generate_theme_from_base_color(
            base_color=base,
            name="Light Theme",
            style="light"
        )
        
        # Light theme should have light background
        bg_brightness = (theme.background.r + theme.background.g + theme.background.b) / 3
        assert bg_brightness > 128


class TestThemeManager:
    """Tests for the ThemeManager class."""
    
    def test_builtin_themes_loaded(self):
        """Test that built-in themes are loaded."""
        manager = ThemeManager()
        
        assert "dracula" in manager.list_themes()
        assert "nord" in manager.list_themes()
        assert "gruvbox" in manager.list_themes()
    
    def test_get_theme(self):
        """Test getting a theme."""
        manager = ThemeManager()
        theme = manager.get_theme("dracula")
        
        assert theme is not None
        assert theme.name == "Dracula"
    
    def test_get_nonexistent_theme(self):
        """Test getting a non-existent theme."""
        manager = ThemeManager()
        theme = manager.get_theme("nonexistent")
        
        assert theme is None
    
    def test_add_theme(self):
        """Test adding a theme."""
        manager = ThemeManager()
        theme = Theme(name="Custom Theme", author="Test")
        
        manager.add_theme(theme)
        
        assert "custom-theme" in manager.list_themes()
    
    def test_export_to_alacritty(self):
        """Test exporting to Alacritty format."""
        manager = ThemeManager()
        theme = manager.get_theme("dracula")
        
        output = manager.export_to_alacritty(theme)
        
        assert "colors:" in output
        assert "primary:" in output
        assert "normal:" in output
        assert "bright:" in output
    
    def test_export_to_kitty(self):
        """Test exporting to Kitty format."""
        manager = ThemeManager()
        theme = manager.get_theme("dracula")
        
        output = manager.export_to_kitty(theme)
        
        assert "foreground" in output
        assert "background" in output
        assert "color0" in output
    
    def test_export_to_windows_terminal(self):
        """Test exporting to Windows Terminal format."""
        manager = ThemeManager()
        theme = manager.get_theme("dracula")
        
        output = manager.export_to_windows_terminal(theme)
        
        assert '"name"' in output
        assert '"foreground"' in output
        assert '"background"' in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
