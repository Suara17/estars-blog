---
title: 'Claude Code 深度操作指南：从零到专家，把这个 AI 编程助手真正用起来'
published: 2026-06-26
description: '你可能已经知道 Claude Code 怎么用，但它比你想象的更强大。'
category: '经验贴'
tags: ['经验贴']
draft: false
lang: zh-CN
---# Claude Code 深度操作指南：从零到专家，把这个 AI 编程助手真正用起来

> 来源：架构工具栈  
> 发布时间：2026年6月11日 09:23 广东  
> 原文链接：[https://mp.weixin.qq.com/s?__biz=Mzk0MzUyNTMwNA==&mid=2247498809&idx=1&sn=0636cd2d00942576c6417914adeb70c0](https://mp.weixin.qq.com/s?__biz=Mzk0MzUyNTMwNA==&mid=2247498809&idx=1&sn=0636cd2d00942576c6417914adeb70c0)

## 写在前面

你可能已经知道 Claude Code 怎么用，但它比你想象的更强大。

这篇会把 Claude Code 的两种交互方式、IDE 集成、模型切换、上下文压缩、撤销恢复、图像理解、深度思考、命令历史管理、CLAUDE.md 记忆、SDK 与 MCP、Git Worktree 并行、GitHub Actions 自动化、以及常见故障排查全部串一遍——读完你应该能把它至少多用出 5 倍。

---

## 两种主要的交互方式

Claude Code 提供两种主要的交互方式：

- **交互模式**：运行 `claude` 启动 REPL 会话
- **单次模式**：使用 `claude -p "查询"` 进行快速命令

可以参考：

```bash
# 启动交互模式
claude

# 以初始查询启动
claude "解释这个项目"

# 运行单个命令并退出
claude -p "这个函数做什么？"

# 处理管道内容
cat logs.txt | claude -p "分析这些错误"
```

对于 Claude Code Client 的常用参数和功能，可以访问官方文档：[CLI 使用和控制 - Anthropic](https://docs.anthropic.com)

---

## IDE 集成：直接在编辑器里看到改动

Claude Code 现在支持 VSCode 与 JetBrains：可以直接在 IDE 中看到 Claude Code 的改动，并在 IDE 中与其交互。

### Linux / macOS 用户

- **VSCode**：在 VSCode 的内置终端唤起 Claude Code，插件将被自动安装
- **JetBrains**：需要通过 JetBrains 应用市场下载 Claude Code [Beta] 插件

可能需要手动指定 IDE 或检查 IDE 连接，通过以下命令测试：

```
/ide
```

### VSCode + WSL 用户

请提前在 VSCode 插件商店安装 WSL 插件。

更多的用法，可以参考 Claude Code 的官方文档：[IDE integrations - Anthropic](https://docs.anthropic.com)

---

## 模型切换：Sonnet vs Opus

Claude Code 支持 Claude Opus 4.8 与 Claude Sonnet 4.6 灵活切换：

| 模型 | 体验 | 计费倍率 | 推荐场景 |
|------|------|---------|---------|
| Claude Sonnet 4.6 | 与 Opus 没有明显差别 | **1x（默认）** | 日常开发、绝大多数任务 |
| Claude Opus 4.8 | 最强推理 | **5x** | 复杂调试、深度规划、长线任务 |

> 💡 **强烈推荐**使用 Claude Sonnet 4.6——使用体验与 Claude Opus 4.8 没有明显差别，但计费倍率仅为 Opus 的 1/5。

在 Claude Code 中使用此命令切换模型：

```
/model
```

---

## 上下文压缩：节省 token

Claude Code 通常会有长上下文，建议使用以下斜杠命令来压缩以节省点数。较长的上下文往往需要更多点数。

```
/compact [您的描述]
```

---

## 恢复上一步修改

Claude Code 支持使用 `Ctrl+Z` 或在 Vim 模式下使用 `u` 撤销 Claude Code 的上一步修改。

### 恢复以前的对话

使用以下命令可以恢复上次的对话：

```bash
claude --continue
```

这会立即恢复最近的对话，无需任何提示。

如果需要在多个历史对话中选择，可以输入此命令：

```bash
claude --resume
```

这会显示一个交互式对话选择器，显示：
- 对话开始时间
- 初始提示或对话摘要
- 消息数量

使用箭头键导航并按 Enter 选择对话，可以用这个方法选择上下文。

---

## 图像信息处理

Claude Code 可以处理图像信息，可以使用以下任何方法：

- 将图像拖放到 Claude Code 窗口中（在 macOS 上）
- 复制图像并使用 `Ctrl+v` 粘贴到 CLI 中（在 macOS 上）
- 提供图像路径：`分析这个图像：/path/to/your/image.png`

可以完全使用自然语言要求它进行工作，如：

- "这是错误的截图。是什么导致了它？"
- "这个图像显示了什么？"
- "描述这个截图中的 UI 元素。"
- "生成 CSS 以匹配这个设计模型。"
- "什么 HTML 结构可以重新创建这个组件？"

---

## 深入思考（Deep Thinking）

需要通过自然语言要求它进行深入思考：

- "我需要使用 OAuth2 为我们的 API 实现一个新的身份验证系统。深入思考在我们的代码库中实现这一点的最佳方法。"
- "思考这种方法中潜在的安全漏洞。"
- "更深入地思考我们应该处理的边缘情况。"

> ⚠️ 推荐在使用复杂问题的时候使用这一功能，这也会消耗大量的额度点数。

---

## 命令历史管理

- 历史按工作目录存储
- 使用 `/clear` 命令清除
- 使用上 / 下箭头导航
- `Ctrl+R`：反向搜索历史（如果终端支持）
- 注意：历史扩展（`!`）默认禁用

---

## CLAUDE.md：存储项目记忆

可以使用以下命令设置一个 CLAUDE.md 文件来存储重要的项目信息、约定和常用命令：

```
/init
```

CLAUDE.md 里建议放这些内容：

- 常用命令（构建、测试、lint）以避免重复搜索
- 代码风格偏好和命名约定
- 特定于项目的重要架构模式

CLAUDE.md 记忆可用于与团队共享的指令和个人偏好。

更多关于记忆的设置，可以访问此官方文档了解：[Claude Code 概述 - Anthropic](https://docs.anthropic.com)。常用用法参考：[管理 Claude 的记忆 - Anthropic](https://docs.anthropic.com)。

---

## SDK 与 MCP

### Claude Code Python SDK

Claude Code 支持 Python SDK，请参考官方文档：[Claude Code SDK - Anthropic](https://docs.anthropic.com)。

直接访问 Python SDK GitHub 仓库：[GitHub - anthropics/claude-code-sdk-python](https://github.com/anthropics/claude-code-sdk-python)。

### MCP 模型上下文协议

[模型上下文协议（MCP）](https://modelcontextprotocol.io) 是一个开放协议，使 LLM 能够访问外部工具和数据源。

这是高级功能，可以访问此文档获取更多配置信息：[Introduction - Model Context Protocol](https://modelcontextprotocol.io)。

Claude Code 不仅支持接入 MCP，同样支持作为 MCP 服务器等各类高级功能，可以访问此文档获得更多信息：[教程 - Anthropic](https://docs.anthropic.com)。

---

## Git 中的高级用法

### 自然语言操作 Git

Claude Code 支持使用自然语言操作 Git，如：

- "提交我的更改"
- "创建一个 PR"
- "哪个提交在去年十二月添加了 markdown 测试？"
- "在 main 分支上变基并解决任何合并冲突"

### Git Worktree：并行隔离的编码环境

如果需要同时处理多个任务，并在 Claude Code 实例之间完全隔离代码，可以使用 Git Worktree 功能。

Git 工作树允许从同一存储库中检出多个分支到单独的目录。每个工作树都有自己的工作目录，文件是隔离的，同时共享相同的 Git 历史。

**创建新工作树：**

```bash
# 创建带有新分支的工作树
git worktree add ../project-feature-a -b feature-a

# 或使用现有分支创建工作树
git worktree add ../project-bugfix bugfix-123
```

这会创建一个包含存储库单独工作副本的新目录。

**在每个工作树中运行 Claude Code：**

```bash
# 导航到您的工作树
cd ../project-feature-a

# 在这个隔离环境中运行 Claude Code
claude
```

在另一个终端中：

```bash
cd ../project-bugfix
claude
```

**管理工作树：**

```bash
# 列出所有工作树
git worktree list

# 完成后移除工作树
git worktree remove ../project-feature-a
```

**Worktree + Claude Code 的优势**

- 每个工作树都有自己独立的文件状态，非常适合并行 Claude Code 会话
- 在一个工作树中所做的更改不会影响其他工作树，防止 Claude 实例相互干扰
- 所有工作树共享相同的 Git 历史和远程连接
- 对于长时间运行的任务，可以让 Claude 在一个工作树中工作，同时你在另一个工作树中继续开发
- 使用描述性目录名称，以便轻松识别每个工作树的任务

**Worktree 环境初始化**

记得根据项目的设置在每个新工作树中初始化开发环境。根据技术栈，这可能包括：

- JavaScript 项目：运行依赖安装（`npm install`、`yarn`）
- Python 项目：设置虚拟环境或使用包管理器安装
- 其他语言：遵循项目的标准设置流程

---

## GitHub Actions：@claude 触发自动化

此功能仍是 Beta 版本，可访问此链接获取使用：

- [GitHub - anthropics/claude-code-action](https://github.com/anthropics/claude-code-action)
- [Claude Code GitHub Actions - Anthropic](https://docs.anthropic.com)

这是一个适用于 GitHub PR 和 issues 的通用 Claude Code 动作，可以回答问题并实现代码更改。此动作会在评论中监听触发词并根据请求激活 Claude 动作。

> Claude Code GitHub Actions 为 GitHub 工作流程带来 AI 驱动的自动化。只需在任何 PR 或 issue 中简单地提及 @claude，Claude 就可以分析代码、创建拉取请求、实现功能和修复错误——所有这些都遵循项目的标准。  
> ——Anthropic

通过以下命令部署 Claude Code GitHub App，此命令将引导你完成设置 GitHub 应用和所需的密钥：

```
/install-github-app
```

安装成功后，可用 `@` 命令，如：

- `@claude 根据 issue 描述实现此功能`
- `@claude 我应该如何为此端点实现用户身份验证？`

---

## 其他自然语言功能

**识别未文档化的代码**

> "在 auth 模块中查找没有适当 JSDoc 注释的函数"

**生成文档**

> "为 auth.js 中未文档化的函数添加 JSDoc 注释"

**理解陌生代码**

> "支付处理系统做什么？"  
> "查找用户权限在哪里被检查"  
> "解释缓存层是如何工作的"

**智能编辑代码**

> "为注册表单添加输入验证"  
> "重构日志记录器以使用新的 API"  
> "修复工作队列中的竞态条件"

**测试或编辑代码**

> "运行 auth 模块的测试并修复失败"  
> "查找并修复安全漏洞"  
> "解释为什么这个测试失败了"

---

## 常用斜杠命令、CLI 命令、参数与快捷键

参考：[交互模式 - Anthropic](https://docs.anthropic.com)

---

## 其他高级功能

- **类 Unix 工具**：Claude Code 可以被用作类 Unix 工具——[教程 - Anthropic](https://docs.anthropic.com)
- **自定义斜杠指令**：[教程 - Anthropic](https://docs.anthropic.com)
- **$ARGUMENTS 添加命令参数**：[教程 - Anthropic](https://docs.anthropic.com)
- **高级设置**：可以参考此文档——[Claude Code 设置 - Anthropic](https://docs.anthropic.com)
- **安全设置**：请参考此官方文档——[管理权限和安全 - Anthropic](https://docs.anthropic.com)

---

## 常见问题排查

**Q：Claude Code 如何存储记忆？**  
A：Claude Code 将记忆存储在 `~/.claude` 中，如果没有特殊要求，请不要删除此目录。

**Q：Claude Code 偶尔回复错误的模型名称，这是为什么？**  
A：这是因为 Claude Code 在使用简单任务时，不会使用 Claude 4 系列模型。可以了解：[Bedrock、Vertex 和代理 - Anthropic](https://docs.anthropic.com)。

**Q：Claude Code 执行的命令行参数错误？**  
A：此类问题在 WSL 上常见，是 Agent 自身的错误。推荐使用 macOS / Ubuntu，这类环境往往问题较少。

**Q：Claude Code 如何彻底清理？**  
A：可以执行以下命令清理 Claude Code 的登录信息：

```bash
rm ~/.claude* -rf
```

**Q：Claude Code 出现 API Error / Tools Error？**  
A：这通常是网络问题，请退出后使用 `claude -c` 重新执行。如果问题依然存在，请联系售后支持。

**Q：Claude Code 在登录使用 OAuth 时验证错误？**  
A：请确保环境变量中没有配置任何代理再进行登录验证。  
如果问题仍然存在，请无视弹出的浏览器并复制终端中的链接并打开，通过验证码方式验证。

**Q：Claude Code 长时间没有响应？**  
A：建议按下 `Ctrl+C` 并重启 Claude Code，这往往是网络问题。  
如果命令行仍然无响应，建议杀死进程并重新进行会话，这将不会影响工作进度。  
可以通过以下命令恢复上次的会话：

```bash
claude -c
```

若问题仍然出现，请寻求售后支持。

---

## 写在最后

把上面这些功能串起来看，Claude Code 真正的能力远不止"在终端里写代码"——Worktree 并行 + 多 IDE 集成 + @claude GitHub Actions + 自定义 Skills + MCP，组合起来基本就是把一个 AI 工程师塞进了你的开发流程里。

对国内开发者来说，最大的卡点反而不是怎么用，而是怎么稳定连上 Claude Opus 4.8 这种旗舰模型——官方订阅需要海外信用卡、海外网络、还有时不时被封号的风险。如果想直接跳过这些麻烦，可以看看 Code80，真实订阅账号转 API，换个 endpoint 就能在 Claude Code 里直接跑 Opus 4.8、Sonnet 4.6，体验跟官方完全一致。详情可以到官网了解：[code.ai80.vip](https://code.ai80.vip)。

---

## 常见问题（FAQ）

### Q1：交互模式和单次模式怎么选？

A：长任务、要反复迭代用交互模式（`claude` 启动 REPL）；一次性问答、脚本调用、管道处理用单次模式（`claude -p "..."`）。比如 `cat logs.txt | claude -p "分析这些错误"` 这种就是单次模式的典型用法。

### Q2：模型默认是 Sonnet，要不要切到 Opus？

A：绝大多数情况下不用切——Sonnet 4.6 体验和 Opus 4.8 没有明显差别，但点数只用 1/5。只在复杂调试、深度规划、安全审查、长线研究这类真正吃推理的任务上切到 Opus。`/model` 命令随时可以换。

### Q3：上下文太长导致点数烧得快怎么办？

A：用 `/compact [描述]` 压缩上下文。这个命令会让 Claude 把当前会话的关键信息总结成精简版，然后基于压缩后的上下文继续，能显著降低 token 消耗。长会话建议每跑一段就 compact 一次。

### Q4：Git Worktree + Claude Code 到底有什么用？

A：可以同时跑多个 Claude Code 实例处理不同任务，彼此互不干扰。比如一个工作树里让 Claude 跑长时间重构，另一个工作树里你自己继续开发新功能。每个工作树文件状态独立，共享同一份 Git 历史。适合"一边让 AI 干活、一边自己也在写"的并行场景。

### Q5：CLAUDE.md 和 /init 是什么关系？

A：`/init` 是一键生成 CLAUDE.md 的命令——它会扫描你的项目，自动生成一份初始的 CLAUDE.md。生成之后你可以再手动补充：常用命令（build/test/lint）、代码风格、架构模式。CLAUDE.md 每次会话开始时 Claude 都会自动读，相当于给它的"项目入门文档"。

### Q6：怎么用 @claude 在 GitHub PR 里触发 Claude Code？

A：先在仓库里跑 `/install-github-app` 配置 GitHub App 和密钥。装好之后，在任何 PR 或 Issue 评论里 `@claude 帮我实现这个功能` 就能触发。它会分析代码、创建 PR、实现功能或修复 bug，按项目规范走。这是个 Beta 功能。

### Q7：Claude Code 总是 API Error 或长时间无响应？

A：大概率是网络问题。先 `Ctrl+C` 中断，用 `claude -c` 恢复上次会话。如果还不行就杀进程重启——不会丢工作进度，下次还能 `claude -c` 续上。OAuth 登录失败的话，确保环境变量里没配代理，或者直接复制终端里的链接手动打开做验证。

### Q8：国内开发者怎么稳定用上 Claude Opus 4.8？

A：官方 Claude 订阅需要海外信用卡 + 海外稳定网络环境，且有封号风险。可以走 Code80 这种真实订阅账号转 API 的渠道——按拿到的 Base URL 和 Key 配进 Claude Code 或 CC Switch 就能直接跑 Opus 4.8，体验跟官方一致。

---

*本文整理自「架构工具栈」微信公众号*
