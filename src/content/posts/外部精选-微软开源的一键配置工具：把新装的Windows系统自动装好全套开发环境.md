---
title: "微软开源的一键配置工具：把新装的 Windows 系统自动装好全套开发环境"
published: 2026-06-11
description: "**来源：** 微信公众号（南烛推荐） **发布日期：** 2026年6月"
category: "外部精选"
tags: ["外部精选", "公众号精选", "微软", "开源", "Windows", "开发环境"]
draft: false
lang: zh-CN
---

# 微软开源的一键配置工具：把新装的 Windows 系统自动装好全套开发环境

> **来源：** 微信公众号（南烛推荐）
> **发布日期：** 2026年6月
> **原文链接：** [https://github.com/microsoft/WindowsDeveloperConfig](https://github.com/microsoft/WindowsDeveloperConfig)

---

## 概述

微软开源的 **WindowsDeveloperConfig**，一条命令把新电脑配成开发机。旨在帮助开发者通过一条命令自动化配置 Windows 开发环境，将刚装好的纯净 Windows 系统变成开箱即用的开发工作站。所有配置均为**声明式、幂等**（可安全多次运行），而且经过 CI 测试。

---

## 三种配置方案

### 1️⃣ 完整的开发工作站（Windows Dev Config）

最全的一套，非交互式一键跑完，把全新 Windows 11 变成无干扰开发机。自动安装的包括：

| 类别 | 工具 |
|------|------|
| **终端** | PowerShell 7、Oh My Posh、Cascadia Mono NF 字体 |
| **版本控制** | Git、GitHub CLI |
| **编辑器** | VS Code |
| **开发框架** | .NET SDK 10、Python 3.14 + uv、Node.js |
| **系统增强** | PowerToys |
| **子系统** | WSL + Ubuntu |

**系统层面优化：**
- 自动开启深色主题、开发者模式、长路径支持
- 文件资源管理器优化
- 终端默认配成 PowerShell 7 加 Cascadia Mono NF 字体
- WSL 自动配好并装 Ubuntu（启用 WSL 需要重启，脚本会在重启后通过 RunOnce 任务自动继续跑完剩下的配置，无需手动干预）

### 2️⃣ WSL 命令行环境（WSL Comfort）

专注打磨命令行体验，支持交互式和非交互式两种跑法：
- 可自选用 **zsh** 或 **bash** 作为默认 Shell
- 可选装 **Starship** 提示符、**Homebrew**
- 现代 CLI 替代工具：**fzf**、**rg**、**bat**、**eza**、**zoxide**
- Windows 端会配好带 **Cascadia Code Nerd Font** 字体的美化版 Windows Terminal 配置文件

### 3️⃣ 单语言工作负载

目前支持以下语言，每种都有对应的 `install.ps1` 脚本，跑完自动刷新当前会话的 PATH：

| TypeScript | PHP | .NET | Go | Java | Rust | Python | WinForms | WinUI 3 |
|------------|-----|------|----|------|------|--------|----------|---------|

---

## ⚠️ 注意事项

1. 底层依赖 Windows 的包管理器命令 **winget configure**
2. **关键坑：** 在非管理员权限下运行，必须提前装好 **Microsoft Visual C++ Redistributable** 运行库，否则会报内部错误
3. WSL 安装如果在虚拟机里跑，需要确认虚拟化支持（**VT-x/AMD-V** 或嵌套虚拟化）已经开启

---

## 项目地址

🔗 https://github.com/microsoft/WindowsDeveloperConfig

---

*整理于 2026-06-11*
