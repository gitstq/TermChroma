"""
Terminal User Interface for TermChroma.
"""

import sys
from typing import Optional, List, Dict
from termchroma.core import ThemeManager, ColorExtractor, ThemeGenerator
from termchroma.models import Color, Theme


class TUI:
    """
    Simple Terminal User Interface for TermChroma.
    
    Provides an interactive menu-driven interface without external dependencies.
    """
    
    # ANSI escape codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    
    # Colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    def __init__(self, manager: ThemeManager):
        """Initialize TUI with a theme manager."""
        self.manager = manager
        self.running = True
        self.current_theme: Optional[Theme] = None
    
    def clear_screen(self):
        """Clear the terminal screen."""
        print("\033[2J\033[H", end="")
    
    def print_header(self):
        """Print the application header."""
        self.clear_screen()
        print(f"""
{self.CYAN}{self.BOLD}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🎨 TermChroma - Terminal Color Theme Engine v1.0.0            ║
║   轻量级终端颜色主题智能生成与管理引擎                              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{self.RESET}
""")
    
    def print_menu(self):
        """Print the main menu."""
        print(f"""
{self.BOLD}Main Menu:{self.RESET}

  {self.GREEN}1.{self.RESET} 📋 List Themes
  {self.GREEN}2.{self.RESET} 🔍 Preview Theme
  {self.GREEN}3.{self.RESET} 🎨 Generate Theme
  {self.GREEN}4.{self.RESET} 📤 Export Theme
  {self.GREEN}5.{self.RESET} 🔎 Extract Colors
  {self.GREEN}6.{self.RESET} ℹ️  Theme Info
  {self.YELLOW}0.{self.RESET} 🚪 Exit

""")
    
    def print_color_block(self, color: Color, width: int = 4) -> str:
        """Create a colored block string."""
        return f"\033[48;2;{color.r};{color.g};{color.b}m{' ' * width}\033[0m"
    
    def input_with_prompt(self, prompt: str, default: str = "") -> str:
        """Get user input with a prompt."""
        default_hint = f" [{default}]" if default else ""
        try:
            value = input(f"{self.CYAN}{prompt}{default_hint}: {self.RESET}").strip()
            return value if value else default
        except (EOFError, KeyboardInterrupt):
            print("\n")
            return ""
    
    def select_from_list(self, prompt: str, options: List[str]) -> Optional[str]:
        """Let user select an option from a list."""
        if not options:
            print(f"{self.RED}No options available.{self.RESET}")
            return None
        
        print(f"\n{self.BOLD}{prompt}:{self.RESET}\n")
        for i, option in enumerate(options, 1):
            print(f"  {self.GREEN}{i}.{self.RESET} {option}")
        print(f"  {self.YELLOW}0.{self.RESET} Back\n")
        
        try:
            choice = input(f"{self.CYAN}Select: {self.RESET}").strip()
            if choice == "0":
                return None
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
            print(f"{self.RED}Invalid selection.{self.RESET}")
            return None
        except (ValueError, EOFError, KeyboardInterrupt):
            print(f"{self.RED}Invalid input.{self.RESET}")
            return None
    
    def action_list_themes(self):
        """List all available themes."""
        self.print_header()
        themes = self.manager.list_themes()
        
        print(f"{self.BOLD}📋 Available Themes:{self.RESET}\n")
        
        for i, theme_name in enumerate(themes, 1):
            theme = self.manager.get_theme(theme_name)
            builtin = f"{self.BLUE}[Built-in]{self.RESET}" if theme_name in self.manager.BUILTIN_THEMES else f"{self.GREEN}[Custom]{self.RESET}"
            
            if theme:
                # Show mini color preview
                colors = theme.get_ansi_colors()
                preview = "".join(self.print_color_block(c, 2) for c in colors[:8])
                
                print(f"  {self.GREEN}{i:2}.{self.RESET} {theme_name:20} {builtin}")
                print(f"       {preview}")
                if theme.description:
                    print(f"       {self.DIM}{theme.description[:60]}{self.RESET}")
                print()
        
        print(f"\n  {self.DIM}Total: {len(themes)} themes{self.RESET}")
        input(f"\n{self.CYAN}Press Enter to continue...{self.RESET}")
    
    def action_preview_theme(self):
        """Preview a theme."""
        self.print_header()
        themes = self.manager.list_themes()
        
        theme_name = self.select_from_list("Select a theme to preview", themes)
        if not theme_name:
            return
        
        theme = self.manager.get_theme(theme_name)
        if not theme:
            print(f"{self.RED}Theme not found.{self.RESET}")
            return
        
        self.print_header()
        print(f"{self.BOLD}🎨 Theme: {theme.name}{self.RESET}")
        print(f"   Author: {theme.author}")
        print(f"   Description: {theme.description or 'No description'}\n")
        
        colors = theme.get_ansi_colors()
        
        print(f"   {self.BOLD}Standard Colors:{self.RESET}")
        for i, color in enumerate(colors[:8]):
            block = self.print_color_block(color, 6)
            print(f"     {i}: {color.hex} {block}")
        
        print(f"\n   {self.BOLD}Bright Colors:{self.RESET}")
        for i, color in enumerate(colors[8:]):
            block = self.print_color_block(color, 6)
            print(f"     {i + 8}: {color.hex} {block}")
        
        print(f"\n   {self.BOLD}UI Colors:{self.RESET}")
        print(f"     Background: {theme.background.hex} {self.print_color_block(theme.background, 10)}")
        print(f"     Foreground: {theme.foreground.hex} {self.print_color_block(theme.foreground, 10)}")
        print(f"     Cursor:     {theme.cursor.hex} {self.print_color_block(theme.cursor, 10)}")
        
        # Demo text
        print(f"\n   {self.BOLD}Preview:{self.RESET}")
        print(f"     {self.print_color_block(theme.background, 80)}")
        demo_text = f"     \033[48;2;{theme.background.r};{theme.background.g};{theme.background.b}m"
        demo_text += f"\033[38;2;{theme.foreground.r};{theme.foreground.g};{theme.foreground.b}m"
        demo_text += "  The quick brown fox jumps over the lazy dog.  \033[0m"
        print(demo_text)
        print(f"     {self.print_color_block(theme.background, 80)}")
        
        input(f"\n{self.CYAN}Press Enter to continue...{self.RESET}")
    
    def action_generate_theme(self):
        """Generate a new theme."""
        self.print_header()
        print(f"{self.BOLD}🎨 Generate New Theme{self.RESET}\n")
        
        base_color = self.input_with_prompt("Base color (hex, e.g., #FF5733)")
        if not base_color:
            print(f"{self.RED}Cancelled.{self.RESET}")
            input(f"\n{self.CYAN}Press Enter to continue...{self.RESET}")
            return
        
        try:
            color = Color.from_hex(base_color)
        except ValueError as e:
            print(f"{self.RED}Error: {e}{self.RESET}")
            input(f"\n{self.CYAN}Press Enter to continue...{self.RESET}")
            return
        
        name = self.input_with_prompt("Theme name", "My Theme")
        author = self.input_with_prompt("Author", "TermChroma")
        
        style = self.select_from_list("Select style", ["dark", "light"])
        if not style:
            return
        
        theme = ThemeGenerator.generate_theme_from_base_color(
            base_color=color,
            name=name,
            author=author,
            style=style
        )
        
        self.manager.add_theme(theme)
        
        print(f"\n{self.GREEN}✅ Theme '{name}' generated successfully!{self.RESET}")
        
        # Preview
        colors = theme.get_ansi_colors()
        print(f"\n   Color Preview:")
        print(f"   {''.join(self.print_color_block(c, 4) for c in colors[:8])}")
        print(f"   {''.join(self.print_color_block(c, 4) for c in colors[8:])}")
        
        input(f"\n{self.CYAN}Press Enter to continue...{self.RESET}")
    
    def action_export_theme(self):
        """Export a theme."""
        self.print_header()
        themes = self.manager.list_themes()
        
        theme_name = self.select_from_list("Select a theme to export", themes)
        if not theme_name:
            return
        
        formats = ["iterm2", "alacritty", "kitty", "windows-terminal", "vscode", "json"]
        fmt = self.select_from_list("Select export format", formats)
        if not fmt:
            return
        
        theme = self.manager.get_theme(theme_name)
        if not theme:
            print(f"{self.RED}Theme not found.{self.RESET}")
            return
        
        exporters = {
            "iterm2": self.manager.export_to_iterm2,
            "alacritty": self.manager.export_to_alacritty,
            "kitty": self.manager.export_to_kitty,
            "windows-terminal": self.manager.export_to_windows_terminal,
            "vscode": self.manager.export_to_vscode,
            "json": lambda t: t.to_json(),
        }
        
        output = exporters[fmt](theme)
        
        filename = self.input_with_prompt("Output filename", f"{theme_name}.{fmt.replace('-', '.')}")
        
        try:
            with open(filename, 'w') as f:
                f.write(output)
            print(f"\n{self.GREEN}✅ Theme exported to {filename}{self.RESET}")
        except Exception as e:
            print(f"{self.RED}Error: {e}{self.RESET}")
        
        input(f"\n{self.CYAN}Press Enter to continue...{self.RESET}")
    
    def action_extract_colors(self):
        """Extract colors from text."""
        self.print_header()
        print(f"{self.BOLD}🔎 Extract Colors{self.RESET}\n")
        
        print("Enter text to extract colors from (empty line to finish):")
        lines = []
        while True:
            try:
                line = input()
                if not line:
                    break
                lines.append(line)
            except EOFError:
                break
        
        text = "\n".join(lines)
        
        hex_colors = ColorExtractor.extract_hex_colors(text)
        rgb_colors = ColorExtractor.extract_rgb_colors(text)
        
        colors = [Color.from_hex(h) for h in hex_colors]
        colors.extend([Color.from_rgb_tuple(rgb) for rgb in rgb_colors])
        
        if not colors:
            print(f"\n{self.YELLOW}No colors found in the input.{self.RESET}")
        else:
            print(f"\n{self.GREEN}Found {len(colors)} colors:{self.RESET}\n")
            
            sorted_colors = ColorExtractor.sort_colors_by_hue(colors)
            
            for color in sorted_colors:
                temp = ColorExtractor.get_color_temperature(color)
                bright = ColorExtractor.get_color_brightness(color)
                block = self.print_color_block(color, 6)
                print(f"  {color.hex}  {block}  [{temp:6}] [{bright:6}]")
        
        input(f"\n{self.CYAN}Press Enter to continue...{self.RESET}")
    
    def action_theme_info(self):
        """Show theme details."""
        self.print_header()
        themes = self.manager.list_themes()
        
        theme_name = self.select_from_list("Select a theme", themes)
        if not theme_name:
            return
        
        theme = self.manager.get_theme(theme_name)
        if not theme:
            print(f"{self.RED}Theme not found.{self.RESET}")
            return
        
        print(f"{self.BOLD}ℹ️  Theme Information{self.RESET}\n")
        print(theme.to_json())
        
        input(f"\n{self.CYAN}Press Enter to continue...{self.RESET}")
    
    def run(self):
        """Run the TUI main loop."""
        while self.running:
            self.print_header()
            self.print_menu()
            
            try:
                choice = input(f"{self.CYAN}Select option: {self.RESET}").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n")
                break
            
            actions = {
                "1": self.action_list_themes,
                "2": self.action_preview_theme,
                "3": self.action_generate_theme,
                "4": self.action_export_theme,
                "5": self.action_extract_colors,
                "6": self.action_theme_info,
                "0": lambda: setattr(self, 'running', False),
            }
            
            if choice in actions:
                actions[choice]()
            else:
                print(f"{self.RED}Invalid option.{self.RESET}")
                input(f"{self.CYAN}Press Enter to continue...{self.RESET}")
        
        self.clear_screen()
        print(f"{self.GREEN}👋 Thanks for using TermChroma!{self.RESET}\n")


def run_tui(manager: ThemeManager):
    """Entry point for the TUI."""
    tui = TUI(manager)
    tui.run()
