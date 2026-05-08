<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Zero%20Dependencies-✓-brightgreen.svg" alt="Zero Dependencies">
</p>

<p align="center">
  <a href="README.md">English</a> | 
  <a href="README_CN.md">简体中文</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">🎨 TermChroma</h1>

<p align="center">
  <strong>Lightweight Terminal Color Theme Intelligent Generation & Management Engine</strong><br>
  <sub>轻量级终端颜色主题智能生成与管理引擎</sub>
</p>

---

## 🎉 Project Introduction

**TermChroma** is a **zero-dependency** CLI tool designed for developers who care about their terminal aesthetics. It helps you **extract, generate, preview, and export** terminal color themes for various terminal emulators.

### 🎯 What Problem Does It Solve?

- 😫 **Tired of manually configuring terminal colors?** TermChroma auto-generates themes from a single base color!
- 🎨 **Found beautiful colors online but don't know how to use them?** Extract colors from any text and generate themes instantly!
- 🔄 **Switching between different terminals?** Export to iTerm2, Alacritty, Kitty, Windows Terminal, and VS Code with one command!
- 👀 **Want to preview before applying?** Interactive TUI lets you see themes before exporting!

### ✨ Self-Developed Highlights

- 🚀 **Zero Dependencies** - Pure Python implementation, no external packages required
- 🎨 **Intelligent Color Extraction** - Extract colors from hex codes, RGB values, and text
- 🌈 **Auto Theme Generation** - Generate complete 16-color themes from a single base color
- 📦 **5 Built-in Popular Themes** - Dracula, Nord, Gruvbox, Tokyo Night, One Dark
- 🔧 **Multi-Format Export** - iTerm2, Alacritty, Kitty, Windows Terminal, VS Code
- 💻 **Interactive TUI** - Beautiful terminal interface for easy navigation
- ⚡ **Fast & Lightweight** - Cold start under 100ms, minimal memory footprint

---

## ✨ Core Features

### 🎨 Color Extraction
- Extract hex colors (`#FF5733`) from any text
- Extract RGB colors (`rgb(255, 0, 128)`) from code
- Smart deduplication of similar colors
- Color temperature detection (warm/cool/neutral)
- Perceptual color distance calculation

### 🌈 Theme Generation
- Generate complete themes from a single base color
- Support for dark and light theme styles
- Automatic complementary and analogous color generation
- WCAG-compliant contrast ratio calculations

### 📦 Theme Management
- 5 built-in popular themes ready to use
- Add, remove, and list custom themes
- Full theme information in JSON format

### 🔧 Multi-Format Export
| Format | Description |
|--------|-------------|
| **iTerm2** | `.itermcolors` XML plist format |
| **Alacritty** | YAML configuration |
| **Kitty** | `.conf` color scheme |
| **Windows Terminal** | JSON settings fragment |
| **VS Code** | `settings.json` snippet |

### 💻 Interactive TUI
- Beautiful terminal interface
- Real-time color preview
- Easy theme browsing and selection

---

## 🚀 Quick Start

### 📋 Requirements
- Python 3.8 or higher
- No external dependencies required!

### 📦 Installation

```bash
# Install from PyPI (recommended)
pip install termchroma

# Or install from source
git clone https://github.com/gitstq/TermChroma.git
cd TermChroma
pip install -e .
```

### ⚡ Quick Commands

```bash
# List available themes
termchroma list

# Preview a theme
termchroma preview dracula

# Generate a new theme from a base color
termchroma generate --base "#FF5733" --name "My Theme"

# Export theme to specific format
termchroma export dracula --format alacritty --output dracula.yml

# Extract colors from text
termchroma extract --text "Colors: #FF5733 #00FF00 #0000FF"

# Launch interactive TUI
termchroma tui
```

---

## 📖 Detailed Usage Guide

### 🎨 Generating Themes

Generate a complete 16-color theme from a single base color:

```bash
# Generate a dark theme
termchroma generate --base "#6272A4" --name "MyCustom" --style dark

# Generate a light theme
termchroma generate --base "#6272A4" --name "MyCustom" --style light

# Save to file
termchroma generate --base "#FF5733" --name "Sunset" --output sunset.json
```

### 📤 Exporting Themes

Export themes to your favorite terminal emulator:

```bash
# Export to Alacritty (YAML)
termchroma export nord --format alacritty --output ~/.config/alacritty/colors.yml

# Export to Kitty
termchroma export gruvbox --format kitty --output ~/.config/kitty/theme.conf

# Export to iTerm2
termchroma export tokyo-night --format iterm2 --output tokyo-night.itermcolors

# Export to Windows Terminal
termchroma export one-dark --format windows-terminal --output theme.json

# Export to VS Code
termchroma export dracula --format vscode --output vscode-settings.json
```

### 🔎 Extracting Colors

Extract colors from text or files:

```bash
# Extract from text
termchroma extract --text "Design: #FF5733 primary, #00FF00 success, #0000FF link"

# Extract from file
termchroma extract --file styles.css

# Remove similar colors
termchroma extract --text "#FF0000 #FF0001 #FF0002" --dedupe
```

### 💻 Interactive TUI

Launch the interactive terminal interface:

```bash
termchroma tui
```

The TUI provides:
- 📋 Theme listing with color previews
- 🔍 Theme preview with sample text
- 🎨 Theme generation wizard
- 📤 Export to multiple formats
- 🔎 Color extraction tool

---

## 💡 Design Philosophy & Roadmap

### 🎯 Design Philosophy

TermChroma was built with these principles in mind:

1. **Zero Dependencies** - No external packages means faster installs and fewer compatibility issues
2. **Developer-First** - CLI-focused with powerful options for automation
3. **Visual Feedback** - Color previews help you make informed decisions
4. **Extensibility** - Clean architecture makes it easy to add new export formats

### 🗓️ Roadmap

| Version | Features |
|---------|----------|
| **v1.1** | Import themes from existing terminal configs |
| **v1.2** | Color palette generation from images |
| **v1.3** | Theme marketplace and sharing |
| **v1.4** | AI-powered theme recommendations |

### 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 📬 Open a Pull Request

Please follow the [Angular Commit Convention](https://www.conventionalcommits.org/).

---

## 📦 Building & Deployment

### 🔨 Building from Source

```bash
# Clone the repository
git clone https://github.com/gitstq/TermChroma.git
cd TermChroma

# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Build distribution
pip install build
python -m build
```

### 📋 Project Structure

```
TermChroma/
├── src/termchroma/
│   ├── __init__.py      # Package initialization
│   ├── cli.py           # Command-line interface
│   ├── core.py          # Core functionality
│   ├── models.py        # Data models
│   ├── tui.py           # Terminal UI
│   └── themes/          # Built-in themes
├── tests/               # Test suite
├── pyproject.toml       # Project configuration
└── README.md            # Documentation
```

---

## 🤝 Contributing Guide

We welcome contributions! Please follow these guidelines:

### 🐛 Reporting Issues

- Use the issue template
- Include reproduction steps
- Specify your Python version and OS

### 💡 Feature Requests

- Describe the feature clearly
- Explain the use case
- Consider implementation complexity

### 🔧 Pull Requests

- Follow the code style (Black formatting)
- Add tests for new features
- Update documentation
- Use conventional commit messages

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 TermChroma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">Lobster Agent</a>
</p>

<p align="center">
  <strong>⭐ If you find TermChroma useful, please give it a star! ⭐</strong>
</p>
