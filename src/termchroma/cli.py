"""
Command-line interface for TermChroma.
"""

import argparse
import sys
import json
from typing import Optional, List
from pathlib import Path

from termchroma import __version__
from termchroma.core import ColorExtractor, ThemeGenerator, ThemeManager
from termchroma.models import Color, Theme


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="termchroma",
        description="🎨 TermChroma - Lightweight Terminal Color Theme Intelligent Generation & Management Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List built-in themes
  termchroma list

  # Generate theme from a base color
  termchroma generate --base "#FF5733" --name "My Theme"

  # Export theme to specific format
  termchroma export dracula --format alacritty --output dracula.yml

  # Extract colors from text
  termchroma extract --text "Colors: #FF5733 #00FF00 #0000FF"

  # Launch interactive TUI
  termchroma tui

  # Preview a theme
  termchroma preview dracula
        """
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available themes")
    list_parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a new theme")
    gen_parser.add_argument(
        "--base", "-b",
        required=True,
        help="Base color in hex format (e.g., #FF5733)"
    )
    gen_parser.add_argument(
        "--name", "-n",
        default="Generated Theme",
        help="Theme name"
    )
    gen_parser.add_argument(
        "--author", "-a",
        default="TermChroma",
        help="Theme author"
    )
    gen_parser.add_argument(
        "--style", "-s",
        choices=["dark", "light"],
        default="dark",
        help="Theme style"
    )
    gen_parser.add_argument(
        "--output", "-o",
        help="Output file path"
    )
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export a theme to specific format")
    export_parser.add_argument(
        "theme",
        help="Theme name to export"
    )
    export_parser.add_argument(
        "--format", "-f",
        required=True,
        choices=["iterm2", "alacritty", "kitty", "windows-terminal", "vscode", "json"],
        help="Output format"
    )
    export_parser.add_argument(
        "--output", "-o",
        help="Output file path"
    )
    
    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract colors from text or file")
    extract_parser.add_argument(
        "--text", "-t",
        help="Text to extract colors from"
    )
    extract_parser.add_argument(
        "--file", "-f",
        help="File to extract colors from"
    )
    extract_parser.add_argument(
        "--dedupe",
        action="store_true",
        help="Remove similar colors"
    )
    
    # Preview command
    preview_parser = subparsers.add_parser("preview", help="Preview a theme")
    preview_parser.add_argument(
        "theme",
        help="Theme name to preview"
    )
    
    # TUI command
    subparsers.add_parser("tui", help="Launch interactive TUI interface")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show theme details")
    info_parser.add_argument(
        "theme",
        help="Theme name"
    )
    
    return parser


def cmd_list(args, manager: ThemeManager):
    """Handle the list command."""
    themes = manager.list_themes()
    
    if args.json:
        output = [{"name": t, "builtin": t in manager.BUILTIN_THEMES} for t in themes]
        print(json.dumps(output, indent=2))
    else:
        print("🎨 Available Themes:\n")
        for theme_name in themes:
            theme = manager.get_theme(theme_name)
            builtin = "📦" if theme_name in manager.BUILTIN_THEMES else "💾"
            if theme:
                print(f"  {builtin} {theme_name:20} - {theme.description[:50] if theme.description else 'No description'}")
        print(f"\n  Total: {len(themes)} themes")


def cmd_generate(args, manager: ThemeManager):
    """Handle the generate command."""
    try:
        base_color = Color.from_hex(args.base)
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    theme = ThemeGenerator.generate_theme_from_base_color(
        base_color=base_color,
        name=args.name,
        author=args.author,
        style=args.style
    )
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(theme.to_json())
        print(f"✅ Theme '{args.name}' saved to {args.output}")
    else:
        print(theme.to_json())


def cmd_export(args, manager: ThemeManager):
    """Handle the export command."""
    theme = manager.get_theme(args.theme)
    
    if not theme:
        print(f"❌ Error: Theme '{args.theme}' not found", file=sys.stderr)
        sys.exit(1)
    
    format_exporters = {
        "iterm2": manager.export_to_iterm2,
        "alacritty": manager.export_to_alacritty,
        "kitty": manager.export_to_kitty,
        "windows-terminal": manager.export_to_windows_terminal,
        "vscode": manager.export_to_vscode,
        "json": lambda t: t.to_json(),
    }
    
    output = format_exporters[args.format](theme)
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output)
        print(f"✅ Theme exported to {args.output}")
    else:
        print(output)


def cmd_extract(args, manager: ThemeManager):
    """Handle the extract command."""
    text = args.text or ""
    
    if args.file:
        try:
            text = Path(args.file).read_text()
        except FileNotFoundError:
            print(f"❌ Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
    
    if not text:
        print("❌ Error: No text provided. Use --text or --file", file=sys.stderr)
        sys.exit(1)
    
    # Extract hex colors
    hex_colors = ColorExtractor.extract_hex_colors(text)
    rgb_colors = ColorExtractor.extract_rgb_colors(text)
    
    colors = [Color.from_hex(h) for h in hex_colors]
    colors.extend([Color.from_rgb_tuple(rgb) for rgb in rgb_colors])
    
    if args.dedupe:
        colors = ColorExtractor.deduplicate_colors(colors)
    
    if not colors:
        print("No colors found in the input")
        return
    
    print(f"🎨 Extracted {len(colors)} colors:\n")
    
    # Sort by hue for better visualization
    sorted_colors = ColorExtractor.sort_colors_by_hue(colors)
    
    for color in sorted_colors:
        temp = ColorExtractor.get_color_temperature(color)
        bright = ColorExtractor.get_color_brightness(color)
        print(f"  {color.hex}  {color.name or 'unnamed':15}  [{temp:6}] [{bright:6}]")


def cmd_preview(args, manager: ThemeManager):
    """Handle the preview command."""
    theme = manager.get_theme(args.theme)
    
    if not theme:
        print(f"❌ Error: Theme '{args.theme}' not found", file=sys.stderr)
        sys.exit(1)
    
    colors = theme.get_ansi_colors()
    
    print(f"\n🎨 Theme: {theme.name}")
    print(f"   Author: {theme.author}")
    print(f"   Description: {theme.description or 'No description'}\n")
    
    print("   Standard Colors:")
    for i, color in enumerate(colors[:8]):
        block = f"\033[48;2;{color.r};{color.g};{color.b}m{' ' * 6}\033[0m"
        print(f"     {i}: {color.hex} {block}")
    
    print("\n   Bright Colors:")
    for i, color in enumerate(colors[8:]):
        block = f"\033[48;2;{color.r};{color.g};{color.b}m{' ' * 6}\033[0m"
        print(f"     {i + 8}: {color.hex} {block}")
    
    print(f"\n   Background: {theme.background.hex}")
    print(f"   Foreground: {theme.foreground.hex}")
    print(f"   Cursor: {theme.cursor.hex}")


def cmd_info(args, manager: ThemeManager):
    """Handle the info command."""
    theme = manager.get_theme(args.theme)
    
    if not theme:
        print(f"❌ Error: Theme '{args.theme}' not found", file=sys.stderr)
        sys.exit(1)
    
    print(theme.to_json())


def cmd_tui(args, manager: ThemeManager):
    """Handle the TUI command."""
    try:
        from termchroma.tui import run_tui
        run_tui(manager)
    except ImportError:
        print("❌ TUI requires additional dependencies. Install with: pip install termchroma[tui]")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    manager = ThemeManager()
    
    commands = {
        "list": lambda: cmd_list(args, manager),
        "generate": lambda: cmd_generate(args, manager),
        "export": lambda: cmd_export(args, manager),
        "extract": lambda: cmd_extract(args, manager),
        "preview": lambda: cmd_preview(args, manager),
        "info": lambda: cmd_info(args, manager),
        "tui": lambda: cmd_tui(args, manager),
    }
    
    if args.command in commands:
        commands[args.command]()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
