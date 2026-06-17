---
title: '用 Skills 扩展 Claude——Claude Code 官方文档'
published: 2026-06-17
description: 'Skills 扩展了 Claude 的能力。创建一个 SKILL.md 文件，写入指令，Claude 会将其加入工具包。Claude 会在相关时自动使用 skill，你也可以直接输入 /skill-name 来调用。'
category: '外部精选'
tags: ['外部精选', '外文翻译']
draft: false
lang: zh-CN
---# 用 Skills 扩展 Claude——Claude Code 官方文档

> 原文标题：Extend Claude with skills
> **来源**：Claude Code Docs
> **原文链接**：https://code.claude.com/docs/en/skills

---

Skills 扩展了 Claude 的能力。创建一个 `SKILL.md` 文件，写入指令，Claude 会将其加入工具包。Claude 会在相关时自动使用 skill，你也可以直接输入 `/skill-name` 来调用。

**何时创建 skill：** 当你反复粘贴同样的指令、清单或多步骤流程到聊天中时，或者当 `CLAUDE.md` 的某个段落已经从事实说明变成了操作流程时。

与 `CLAUDE.md` 内容不同，**skill 的正文只在使用时才加载**，所以即使是很长的参考资料，在需要之前几乎不消耗上下文。

---

## 捆绑 Skill

Claude Code 内置了一套捆绑 skill，每个会话中默认可用（除非用 `disableBundledSkills` 设置禁用了），包括：

- `/code-review` — 代码审查
- `/batch` — 批量处理
- `/debug` — 调试
- `/loop` — 循环
- `/claude-api` — Claude API

与大多数直接执行固定逻辑的内置命令不同，捆绑 skill 是基于提示的：它们给 Claude 详细指令，让它用自身的工具来编排工作。

### 运行和验证你的应用

三个捆绑 skill 协同工作，可以直接启动应用并在运行中验证改动：

| Skill | 用途 |
|-------|------|
| `/run` | 启动并驱动你的应用，查看改动效果 |
| `/verify` | 构建并运行应用，确认代码改动效果，不依赖测试或类型检查 |
| `/run-skill-generator` | 教 `/run` 和 `/verify` 如何构建和启动你的项目 |

`/run-skill-generator` 从干净环境启动你的应用，记录安装命令、环境变量、启动脚本，将配方提交为项目级 skill（`.claude/skills/run-<name>/`）。之后 `run` 和 `/verify` 会遵循记录的配方，而不是每次都重新发现。

---

## 快速开始

### 创建你的第一个 Skill

以下例子创建一个 skill，总结 git 仓库中未提交的改动并标记风险。

**1. 创建 skill 目录**
```bash
mkdir -p ~/.claude/skills/summarize-changes
```

**2. 编写 SKILL.md**

每个 skill 需要两个部分：`---` 标记内的 YAML 前置元数据，以及 Markdown 正文指令。

写入 `~/.claude/skills/summarize-changes/SKILL.md`：

```markdown
---
description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
---

## Current changes
!`git diff HEAD`

## Instructions
Summarize the changes above in two or three bullet points, then list any risks you notice such as missing error handling, hardcoded values, or tests that need updating.
```

**3. 测试 skill**
在 git 项目中修改一个文件，然后运行 `claude`。你可以让 Claude 自动调用（问"我改了啥？"），或直接输入 `/summarize-changes`。

---

## Skill 存放位置

| 位置 | 路径 | 适用范围 |
|------|------|----------|
| **企业级** | 参见托管设置 | 组织内所有用户 |
| **个人** | `~/.claude/skills/<skill-name>/SKILL.md` | 所有项目 |
| **项目** | `.claude/skills/<skill-name>/SKILL.md` | 仅当前项目 |
| **插件** | `<plugin>/skills/<skill-name>/SKILL.md` | 启用插件的环境 |

优先级：**企业 > 个人 > 项目**。同名 skill 会覆盖捆绑 skill。

### 实时变更检测

Claude Code 会监控 skill 目录的文件变化。在 `~/.claude/skills/` 或项目 `.claude/skills/` 中增、删、改 skill，在当前会话中立即生效，无需重启。

---

## 配置 Skill

### 前置元数据参考

```yaml
---
name: my-skill
description: What this skill does
when_to_use: Additional context for when Claude should invoke
disable-model-invocation: true
user-invocable: false
allowed-tools: Read Grep
disallowed-tools: AskUserQuestion
model: claude-sonnet-4-5
effort: high
context: fork
agent: Explore
paths: "src/**/*.ts"
---
```

**关键字段说明：**

| 字段 | 说明 |
|------|------|
| `name` | 显示名称，默认使用目录名 |
| `description` | **推荐**。描述 skill 做什么以及何时使用 |
| `when_to_use` | 对 Claude 的额外触发提示，接在 description 后 |
| `disable-model-invocation` | `true` 时仅用户可手动调用（如 `/deploy`）|
| `user-invocable` | `false` 时仅 Claude 可调用（如背景知识）|
| `allowed-tools` | Claude 在 skill 激活时无需确认即可使用的工具 |
| `disallowed-tools` | skill 激活时从 Claude 工具池中移除的工具 |
| `context: fork` | 在**分支 subagent** 中隔离运行 |
| `agent` | 与 `context: fork` 配合，指定 subagent 类型 |
| `paths` | Glob 模式，限制仅当匹配文件时才激活 skill |

### 调用控制对照

| 前置元数据 | 你可调用 | Claude 可调用 | 上下文加载 |
|-----------|---------|-------------|-----------|
| （默认） | ✅ | ✅ | 描述在上下文，调用时加载完整 skill |
| `disable-model-invocation: true` | ✅ | ❌ | 描述不在上下文，你调用时才加载 |
| `user-invocable: false` | ❌ | ✅ | 描述在上下文，调用时加载完整 skill |

---

## 高级模式

### 注入动态上下文

`!`\`<command>\`` 语法在 skill 内容发送给 Claude 之前执行 shell 命令。命令输出替换占位符，Claude 收到的是真实数据：

```markdown
## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`
```

多行命令则用 ` ```! ` 代码块。

### 在 Subagent 中运行 Skill

添加 `context: fork` 让 skill 在隔离环境中运行：

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---
Research $ARGUMENTS thoroughly:
1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

### 参数替换

| 变量 | 说明 |
|------|------|
| `$ARGUMENTS` | 所有传入参数 |
| `$ARGUMENTS[N]` 或 `$N` | 按位置访问参数 |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID |
| `${CLAUDE_EFFORT}` | 当前 effort 级别 |
| `${CLAUDE_SKILL_DIR}` | skill 所在目录 |

### 预审批工具

`allowed-tools` 字段让 Claude 在 skill 激活时无需逐次确认即可使用指定工具：

```yaml
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

### 生成可视化输出

Skill 可以捆绑任意语言的脚本，一个强大的模式是生成交互式 HTML 可视化。Claude Code 文档中提供了一个完整的 **codebase-visualizer** 示例——它扫描项目目录，生成一个自包含的 HTML 文件，包含可折叠目录树、文件类型条形图等。

---

## 故障排查

- **Skill 不触发**：检查 description 包含用户自然语言关键词；尝试直接 `/skill-name` 调用
- **Skill 触发太频繁**：使 description 更具体，或添加 `disable-model-invocation: true`
- **描述被截断**：运行 `/doctor` 检查预算溢出。所有 skill 描述共享模型上下文窗口 1% 的预算，每条上限 1,536 字符

---

## 相关资源

- **Subagents**：将任务委托给专门 Agent
- **Plugins**：打包并分发 skill 及扩展
- **Hooks**：围绕工具事件自动化工作流
- **Memory**：管理 `CLAUDE.md` 持久上下文
- **Commands**：内置命令和捆绑 skill 参考
- **Permissions**：控制工具和 skill 访问权限
