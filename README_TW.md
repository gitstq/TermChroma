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
  <strong>輕量級終端顏色主題智慧生成與管理引擎</strong><br>
  <sub>Lightweight Terminal Color Theme Intelligent Generation & Management Engine</sub>
</p>

---

## 🎉 專案介紹

**TermChroma** 是一款**零依賴**的命令列工具，專為注重終端美學的開發者設計。它幫助您從各種來源**提取、生成、預覽和匯出**終端顏色主題。

### 🎯 解決什麼問題？

- 😫 **厭倦了手動配置終端顏色？** TermChroma 可以從單一基礎色自動生成完整主題！
- 🎨 **在網上發現了漂亮的顏色卻不知道如何使用？** 從任何文字中提取顏色並即時生成主題！
- 🔄 **在不同終端之間切換？** 一鍵匯出到 iTerm2、Alacritty、Kitty、Windows Terminal 和 VS Code！
- 👀 **想在應用前預覽效果？** 互動式 TUI 讓您在匯出前查看主題效果！

### ✨ 自研差異化亮點

- 🚀 **零依賴** - 純 Python 實作，無需任何外部套件
- 🎨 **智慧顏色提取** - 從十六進位代碼、RGB值和文字中提取顏色
- 🌈 **自動主題生成** - 從單一基礎色生成完整的16色主題
- 📦 **5款內建熱門主題** - Dracula、Nord、Gruvbox、Tokyo Night、One Dark
- 🔧 **多格式匯出** - 支援 iTerm2、Alacritty、Kitty、Windows Terminal、VS Code
- 💻 **互動式 TUI** - 美觀的終端介面，輕鬆導航
- ⚡ **快速輕量** - 冷啟動低於100毫秒，記憶體佔用極小

---

## ✨ 核心特性

### 🎨 顏色提取
- 從任何文字中提取十六進位顏色（`#FF5733`）
- 從程式碼中提取 RGB 顏色（`rgb(255, 0, 128)`）
- 智慧去除相似顏色
- 顏色溫度檢測（暖色/冷色/中性）
- 感知顏色距離計算

### 🌈 主題生成
- 從單一基礎色生成完整主題
- 支援深色和淺色主題風格
- 自動生成互補色和類似色
- 符合 WCAG 標準的對比度計算

### 📦 主題管理
- 5款內建熱門主題開箱即用
- 新增、刪除和列出自訂主題
- JSON 格式的完整主題資訊

### 🔧 多格式匯出
| 格式 | 描述 |
|------|------|
| **iTerm2** | `.itermcolors` XML plist 格式 |
| **Alacritty** | YAML 設定檔 |
| **Kitty** | `.conf` 顏色方案 |
| **Windows Terminal** | JSON 設定片段 |
| **VS Code** | `settings.json` 設定片段 |

### 💻 互動式 TUI
- 美觀的終端介面
- 即時顏色預覽
- 輕鬆瀏覽和選擇主題

---

## 🚀 快速開始

### 📋 環境要求
- Python 3.8 或更高版本
- 無需任何外部依賴！

### 📦 安裝方式

```bash
# 從 PyPI 安裝（推薦）
pip install termchroma

# 或從原始碼安裝
git clone https://github.com/gitstq/TermChroma.git
cd TermChroma
pip install -e .
```

### ⚡ 快速命令

```bash
# 列出可用主題
termchroma list

# 預覽主題
termchroma preview dracula

# 從基礎色生成新主題
termchroma generate --base "#FF5733" --name "我的主題"

# 匯出主題到指定格式
termchroma export dracula --format alacritty --output dracula.yml

# 從文字提取顏色
termchroma extract --text "顏色: #FF5733 #00FF00 #0000FF"

# 啟動互動式 TUI
termchroma tui
```

---

## 📖 詳細使用指南

### 🎨 生成主題

從單一基礎色生成完整的16色主題：

```bash
# 生成深色主題
termchroma generate --base "#6272A4" --name "MyCustom" --style dark

# 生成淺色主題
termchroma generate --base "#6272A4" --name "MyCustom" --style light

# 儲存到檔案
termchroma generate --base "#FF5733" --name "Sunset" --output sunset.json
```

### 📤 匯出主題

將主題匯出到您喜愛的終端模擬器：

```bash
# 匯出到 Alacritty (YAML)
termchroma export nord --format alacritty --output ~/.config/alacritty/colors.yml

# 匯出到 Kitty
termchroma export gruvbox --format kitty --output ~/.config/kitty/theme.conf

# 匯出到 iTerm2
termchroma export tokyo-night --format iterm2 --output tokyo-night.itermcolors

# 匯出到 Windows Terminal
termchroma export one-dark --format windows-terminal --output theme.json

# 匯出到 VS Code
termchroma export dracula --format vscode --output vscode-settings.json
```

### 🔎 提取顏色

從文字或檔案中提取顏色：

```bash
# 從文字提取
termchroma extract --text "設計: #FF5733 主色, #00FF00 成功, #0000FF 連結"

# 從檔案提取
termchroma extract --file styles.css

# 去除相似顏色
termchroma extract --text "#FF0000 #FF0001 #FF0002" --dedupe
```

### 💻 互動式 TUI

啟動互動式終端介面：

```bash
termchroma tui
```

TUI 提供：
- 📋 主題列表與顏色預覽
- 🔍 主題預覽與範例文字
- 🎨 主題生成精靈
- 📤 多格式匯出
- 🔎 顏色提取工具

---

## 💡 設計理念與迭代規劃

### 🎯 設計理念

TermChroma 基於以下原則構建：

1. **零依賴** - 無外部套件意味著更快的安裝和更少的相容性問題
2. **開發者優先** - 專注於命令列，提供強大的自動化選項
3. **視覺回饋** - 顏色預覽幫助您做出明智的決策
4. **可擴展性** - 清晰的架構使新增新匯出格式變得容易

### 🗓️ 迭代規劃

| 版本 | 功能 |
|------|------|
| **v1.1** | 從現有終端設定匯入主題 |
| **v1.2** | 從圖片生成配色方案 |
| **v1.3** | 主題市集和分享功能 |
| **v1.4** | AI 驅動的主題推薦 |

### 🤝 參與貢獻

歡迎貢獻！以下是參與方式：

1. 🍴 Fork 本儲存庫
2. 🌿 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 💾 提交變更 (`git commit -m 'feat: add amazing feature'`)
4. 📤 推送到分支 (`git push origin feature/amazing-feature`)
5. 📬 提交 Pull Request

請遵循 [Angular 提交規範](https://www.conventionalcommits.org/)。

---

## 📦 建置與部署

### 🔨 從原始碼建置

```bash
# 複製儲存庫
git clone https://github.com/gitstq/TermChroma.git
cd TermChroma

# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
python -m pytest tests/ -v

# 建置分發套件
pip install build
python -m build
```

### 📋 專案結構

```
TermChroma/
├── src/termchroma/
│   ├── __init__.py      # 套件初始化
│   ├── cli.py           # 命令列介面
│   ├── core.py          # 核心功能
│   ├── models.py        # 資料模型
│   ├── tui.py           # 終端介面
│   └── themes/          # 內建主題
├── tests/               # 測試套件
├── pyproject.toml       # 專案設定
└── README.md            # 文件
```

---

## 🤝 貢獻指南

我們歡迎各種貢獻！請遵循以下指南：

### 🐛 回報問題

- 使用問題範本
- 包含重現步驟
- 說明您的 Python 版本和作業系統

### 💡 功能請求

- 清晰描述功能
- 解釋使用場景
- 考慮實作複雜度

### 🔧 Pull Request

- 遵循程式碼風格（Black 格式化）
- 為新功能新增測試
- 更新文件
- 使用規範的提交訊息

---

## 📄 開源授權

本專案基於 **MIT 授權條款** 開源 - 詳見 [LICENSE](LICENSE) 檔案。

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
  由 <a href="https://github.com/gitstq">Lobster Agent</a> 用 ❤️ 製作
</p>

<p align="center">
  <strong>⭐ 如果您覺得 TermChroma 有用，請給它一個星標！ ⭐</strong>
</p>
