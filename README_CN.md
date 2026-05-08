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
  <strong>轻量级终端颜色主题智能生成与管理引擎</strong><br>
  <sub>Lightweight Terminal Color Theme Intelligent Generation & Management Engine</sub>
</p>

---

## 🎉 项目介绍

**TermChroma** 是一款**零依赖**的命令行工具，专为注重终端美学的开发者设计。它帮助您从各种来源**提取、生成、预览和导出**终端颜色主题。

### 🎯 解决什么问题？

- 😫 **厌倦了手动配置终端颜色？** TermChroma 可以从单一基础色自动生成完整主题！
- 🎨 **在网上发现了漂亮的颜色却不知道如何使用？** 从任何文本中提取颜色并即时生成主题！
- 🔄 **在不同终端之间切换？** 一键导出到 iTerm2、Alacritty、Kitty、Windows Terminal 和 VS Code！
- 👀 **想在应用前预览效果？** 交互式 TUI 让您在导出前查看主题效果！

### ✨ 自研差异化亮点

- 🚀 **零依赖** - 纯 Python 实现，无需任何外部包
- 🎨 **智能颜色提取** - 从十六进制代码、RGB值和文本中提取颜色
- 🌈 **自动主题生成** - 从单一基础色生成完整的16色主题
- 📦 **5款内置热门主题** - Dracula、Nord、Gruvbox、Tokyo Night、One Dark
- 🔧 **多格式导出** - 支持 iTerm2、Alacritty、Kitty、Windows Terminal、VS Code
- 💻 **交互式 TUI** - 美观的终端界面，轻松导航
- ⚡ **快速轻量** - 冷启动低于100毫秒，内存占用极小

---

## ✨ 核心特性

### 🎨 颜色提取
- 从任何文本中提取十六进制颜色（`#FF5733`）
- 从代码中提取 RGB 颜色（`rgb(255, 0, 128)`）
- 智能去除相似颜色
- 颜色温度检测（暖色/冷色/中性）
- 感知颜色距离计算

### 🌈 主题生成
- 从单一基础色生成完整主题
- 支持深色和浅色主题风格
- 自动生成互补色和类似色
- 符合 WCAG 标准的对比度计算

### 📦 主题管理
- 5款内置热门主题开箱即用
- 添加、删除和列出自定义主题
- JSON 格式的完整主题信息

### 🔧 多格式导出
| 格式 | 描述 |
|------|------|
| **iTerm2** | `.itermcolors` XML plist 格式 |
| **Alacritty** | YAML 配置文件 |
| **Kitty** | `.conf` 颜色方案 |
| **Windows Terminal** | JSON 设置片段 |
| **VS Code** | `settings.json` 配置片段 |

### 💻 交互式 TUI
- 美观的终端界面
- 实时颜色预览
- 轻松浏览和选择主题

---

## 🚀 快速开始

### 📋 环境要求
- Python 3.8 或更高版本
- 无需任何外部依赖！

### 📦 安装方式

```bash
# 从 PyPI 安装（推荐）
pip install termchroma

# 或从源码安装
git clone https://github.com/gitstq/TermChroma.git
cd TermChroma
pip install -e .
```

### ⚡ 快速命令

```bash
# 列出可用主题
termchroma list

# 预览主题
termchroma preview dracula

# 从基础色生成新主题
termchroma generate --base "#FF5733" --name "我的主题"

# 导出主题到指定格式
termchroma export dracula --format alacritty --output dracula.yml

# 从文本提取颜色
termchroma extract --text "颜色: #FF5733 #00FF00 #0000FF"

# 启动交互式 TUI
termchroma tui
```

---

## 📖 详细使用指南

### 🎨 生成主题

从单一基础色生成完整的16色主题：

```bash
# 生成深色主题
termchroma generate --base "#6272A4" --name "MyCustom" --style dark

# 生成浅色主题
termchroma generate --base "#6272A4" --name "MyCustom" --style light

# 保存到文件
termchroma generate --base "#FF5733" --name "Sunset" --output sunset.json
```

### 📤 导出主题

将主题导出到您喜爱的终端模拟器：

```bash
# 导出到 Alacritty (YAML)
termchroma export nord --format alacritty --output ~/.config/alacritty/colors.yml

# 导出到 Kitty
termchroma export gruvbox --format kitty --output ~/.config/kitty/theme.conf

# 导出到 iTerm2
termchroma export tokyo-night --format iterm2 --output tokyo-night.itermcolors

# 导出到 Windows Terminal
termchroma export one-dark --format windows-terminal --output theme.json

# 导出到 VS Code
termchroma export dracula --format vscode --output vscode-settings.json
```

### 🔎 提取颜色

从文本或文件中提取颜色：

```bash
# 从文本提取
termchroma extract --text "设计: #FF5733 主色, #00FF00 成功, #0000FF 链接"

# 从文件提取
termchroma extract --file styles.css

# 去除相似颜色
termchroma extract --text "#FF0000 #FF0001 #FF0002" --dedupe
```

### 💻 交互式 TUI

启动交互式终端界面：

```bash
termchroma tui
```

TUI 提供：
- 📋 主题列表与颜色预览
- 🔍 主题预览与示例文本
- 🎨 主题生成向导
- 📤 多格式导出
- 🔎 颜色提取工具

---

## 💡 设计理念与迭代规划

### 🎯 设计理念

TermChroma 基于以下原则构建：

1. **零依赖** - 无外部包意味着更快的安装和更少的兼容性问题
2. **开发者优先** - 专注于命令行，提供强大的自动化选项
3. **视觉反馈** - 颜色预览帮助您做出明智的决策
4. **可扩展性** - 清晰的架构使添加新导出格式变得容易

### 🗓️ 迭代规划

| 版本 | 功能 |
|------|------|
| **v1.1** | 从现有终端配置导入主题 |
| **v1.2** | 从图片生成配色方案 |
| **v1.3** | 主题市场和分享功能 |
| **v1.4** | AI 驱动的主题推荐 |

### 🤝 参与贡献

欢迎贡献！以下是参与方式：

1. 🍴 Fork 本仓库
2. 🌿 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 💾 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 📤 推送到分支 (`git push origin feature/amazing-feature`)
5. 📬 提交 Pull Request

请遵循 [Angular 提交规范](https://www.conventionalcommits.org/)。

---

## 📦 构建与部署

### 🔨 从源码构建

```bash
# 克隆仓库
git clone https://github.com/gitstq/TermChroma.git
cd TermChroma

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
python -m pytest tests/ -v

# 构建分发包
pip install build
python -m build
```

### 📋 项目结构

```
TermChroma/
├── src/termchroma/
│   ├── __init__.py      # 包初始化
│   ├── cli.py           # 命令行接口
│   ├── core.py          # 核心功能
│   ├── models.py        # 数据模型
│   ├── tui.py           # 终端界面
│   └── themes/          # 内置主题
├── tests/               # 测试套件
├── pyproject.toml       # 项目配置
└── README.md            # 文档
```

---

## 🤝 贡献指南

我们欢迎各种贡献！请遵循以下指南：

### 🐛 报告问题

- 使用问题模板
- 包含复现步骤
- 说明您的 Python 版本和操作系统

### 💡 功能请求

- 清晰描述功能
- 解释使用场景
- 考虑实现复杂度

### 🔧 Pull Request

- 遵循代码风格（Black 格式化）
- 为新功能添加测试
- 更新文档
- 使用规范的提交信息

---

## 📄 开源协议

本项目基于 **MIT 协议** 开源 - 详见 [LICENSE](LICENSE) 文件。

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
  由 <a href="https://github.com/gitstq">Lobster Agent</a> 用 ❤️ 制作
</p>

<p align="center">
  <strong>⭐ 如果您觉得 TermChroma 有用，请给它一个星标！ ⭐</strong>
</p>
