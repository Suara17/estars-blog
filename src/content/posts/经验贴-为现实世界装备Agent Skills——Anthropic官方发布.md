---
title: '为现实世界装备 Agent Skills'
published: 2026-06-17
description: 'Claude 很强大，但真正的工作需要流程性知识和组织上下文。为此我们推出 Agent Skills——一种用文件和文件夹构建专用 Agent 的新方式。'
category: '外部精选'
tags: ['外部精选', '外文翻译']
draft: false
lang: zh-CN
---# 为现实世界装备 Agent Skills

## Anthropic：用 Skill 为 Agent 注入领域专长

> 原文标题：Equipping agents for the real world with Agent Skills
> **作者**：Barry Zhang, Keith Lazuka, Mahesh Murag  
> **发布**：Anthropic Engineering Blog · 2025年10月16日  
> **更新**：2025年12月18日 — Agent Skills 已作为跨平台开放标准发布  
> **原文链接**：https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

---

Claude 很强大，但真正的工作需要流程性知识和组织上下文。为此我们推出 **Agent Skills**——一种用文件和文件夹构建专用 Agent 的新方式。

随着模型能力的提升，我们现在可以构建与完整计算环境交互的通用 Agent。例如，Claude Code 可以利用本地代码执行和文件系统跨领域完成复杂任务。但随着这些 Agent 变得更加强大，我们需要更可组合、可扩展、可移植的方式来为它们装备领域专长。

这促使我们创造了 **Agent Skills**：有组织的指令、脚本和资源文件夹，Agent 可以动态发现并按需加载，以更好地完成特定任务。

> 为 Agent 构建 Skill，就像为新员工准备入职指南。它不是为每个用例构建碎片化的定制 Agent，而是通过捕获和共享流程性知识，让任何人都能用可组合的能力来专业化自己的 Agent。

在这篇文章中，我们将解释什么是 Skill、它们如何工作，以及构建 Skill 的最佳实践。

---

## 什么是 Skill？

**Skill 是一个包含 `SKILL.md` 文件的目录**，其中包含有组织的指令、脚本和资源文件夹，为 Agent 提供额外能力。

### Skill 的解剖结构

让我们通过一个真实例子来了解 Skill 的运作方式：Claude 最近推出的文档编辑能力所用的 skill。

Claude 已经了解很多关于 PDF 的知识，但直接操作 PDF 的能力有限（例如填写表单）。这个 **PDF Skill** 让我们赋予 Claude 这些新能力。

最简单的情况下，一个 skill 就是一个包含 `SKILL.md` 文件的目录。该文件必须以 YAML 前置元数据开头，包含必需的元数据：**名称**和**描述**。

启动时，Agent 会将每个已安装 skill 的名称和描述预加载到系统提示中。这是**渐进式披露**的第一层：它只提供足够的信息让 Claude 知道何时应该使用某个 skill，而无需将所有内容加载到上下文中。

SKILL.md 的实际正文是第二层细节。如果 Claude 认为某个 skill 与当前任务相关，它会通过读取完整的 SKILL.md 将 skill 加载到上下文中。

随着 skill 变得复杂，单个 SKILL.md 可能容纳不下所有上下文，或者某些上下文只在特定场景下相关。这时，skill 可以在 skill 目录内捆绑额外文件，并从 SKILL.md 中按名称引用它们。这些额外链接的文件是第三层及更深层的细节，Claude 可以根据需要选择导航和发现。

在 PDF skill 的示例中，SKILL.md 引用了两个额外文件（`reference.md` 和 `forms.md`）。通过将表单填写指令移到一个单独的文件（`forms.md`），skill 作者能够保持 skill 核心的精简，确信 Claude 只会在需要填写表单时读取 `forms.md`。

**渐进式披露**是使 Agent Skills 灵活且可扩展的核心设计原则。就像一本组织良好的手册，从目录开始，然后是具体章节，最后是详细附录——Skill 让 Claude 只在需要时加载信息。

---

## Skill 与上下文窗口

下图展示了当 skill 被用户消息触发时上下文窗口的变化。操作的顺序：

1. 上下文窗口包含核心系统提示和每个已安装 skill 的元数据，以及用户的初始消息
2. Claude 通过调用 Bash 工具读取 `pdf/SKILL.md` 的内容来触发 PDF skill
3. Claude 选择读取捆绑在 skill 中的 `forms.md` 文件
4. 现在 Claude 已加载了来自 PDF skill 的相关指令，开始处理用户的任务

---

## Skill 与代码执行

Skill 还可以包含代码，供 Claude 自行决定作为工具执行。

大语言模型擅长许多任务，但某些操作更适合传统的代码执行。例如，通过 token 生成来排序列表远比运行排序算法昂贵得多。除了效率考虑，许多应用还需要只有代码才能提供的不确定可靠性。

在 PDF skill 示例中，它包含一个预写的 Python 脚本，用于读取 PDF 并提取所有表单字段。Claude 可以运行这个脚本，而无需将脚本或 PDF 加载到上下文窗口中。而且由于代码是确定性的，这个工作流是一致且可重复的。

---

## 开发和评估 Skill

以下是开始编写和测试 Skill 的一些有用指南：

### 从评估开始
在代表性任务上运行 Agent，观察它们在哪些地方遇到困难或需要额外上下文，识别 Agent 能力的具体缺口，然后逐步构建 skill 来解决这些问题。

### 结构化扩展
当 SKILL.md 变得臃肿时，将内容拆分到单独文件中并引用它们。如果某些上下文互斥或很少一起使用，保持路径分离将减少 token 使用量。最后，代码既可以作为可执行工具，也可以作为文档。应该明确 Claude 是应该直接运行脚本，还是将其读入上下文作为参考。

### 从 Claude 的角度思考
监控 Claude 在真实场景中如何使用你的 skill，并根据观察进行迭代：注意意外轨迹或对某些上下文的过度依赖。

**特别关注 skill 的名称和描述**。Claude 将根据这些来决定是否在响应当前任务时触发 skill。

### 与 Claude 迭代
与 Claude 一起处理任务时，让它把成功的方法和常见错误捕获到可复用的上下文和代码中，构建成 skill。如果它在使用 skill 完成任务时偏离了方向，让它自我反思哪里出了问题。这个过程将帮助你发现 Claude 实际需要什么上下文，而不是你事先预期的。

---

## Skill 的安全考虑

Skill 通过指令和代码为 Claude 提供新能力。虽然这使它们很强大，但也意味着恶意 skill 可能会在使用它们的环境中引入漏洞，或指示 Claude 泄露数据和执行意外操作。

我们建议仅从**可信来源**安装 skill。当从不太可信的来源安装 skill 时，在使用前彻底审计它。首先阅读 skill 中捆绑的文件内容以了解其功能，特别注意代码依赖和捆绑资源（如图像或脚本）。同样，注意指示 Claude 连接到潜在不可信外部网络源的指令或代码。

---

## Skill 的未来

Agent Skills 目前在以下平台得到支持：**Claude.ai、Claude Code、Claude Agent SDK 和 Claude 开发者平台**。

在接下来的几周内，我们将继续添加支持 Skill 完整生命周期（创建、编辑、发现、共享和使用）的功能。我们对 Skill 帮助组织和个人与 Claude 共享其上下文和工作流程的机会感到特别兴奋。

我们还将探索 Skill 如何补充 **MCP（模型上下文协议）服务器**，通过教导涉及外部工具和软件的更复杂工作流。

放眼未来，我们希望使 Agent 能够**自主创建、编辑和评估 Skill**，让它们将自己行为模式编码为可复用的能力。

Skill 是一个简单的概念，配以同样简单的格式。这种简单性使组织、开发者和最终用户更容易构建定制 Agent 并赋予它们新能力。

---

## 致谢

本文由 **Barry Zhang、Keith Lazuka 和 Mahesh Murag** 撰写，他们都很喜欢文件夹。特别感谢 Anthropic 内部众多推动、支持和构建 Skills 的同仁。

---

## 快速上手指南

**开始使用：** 查看我们的 [Skills 文档](https://code.claude.com/docs/en/skills) 和 [cookbook](https://github.com/anthropics/skills)。

### 核心要点

| 概念 | 说明 |
|------|------|
| **渐进式披露** | Skill 只在需要时加载内容，上下文总量理论无上限 |
| **YAML 前置元数据** | 必需的 name + description，预加载到系统提示 |
| **捆绑文件** | 将额外指令拆分到独立文件，按需加载 |
| **代码执行** | Skill 可以包含脚本，Claude 自行决定是否运行 |
| **跨平台标准** | 2025年12月起作为开放标准发布，已获多平台支持 |
