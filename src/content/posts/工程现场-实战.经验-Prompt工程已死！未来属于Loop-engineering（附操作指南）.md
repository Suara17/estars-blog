---
title: '读 Loop Engineering 有感——从 Prompt 到循环系统'
published: 2026-06-16
description: 'title: 读 Loop Engineering 有感——从 Prompt 到循环系统'
category: '工程现场'
tags: ['工程现场', '实战', '经验']
draft: false
lang: zh-CN
---# 读 Loop Engineering 有感——从 Prompt 到循环系统

> 读自 Addy Osmani 的长文 + 公众号"学术AI大模型"的编译。这篇是我的摘录整理和个人思考。

## 核心论点

Anthropic 的 Boris Cherny（Claude Code 创始人）说了一段话引起了我强烈共鸣：

> "我不再提示 Claude 了，我有一堆循环在运行，它们才是在提示 Claude 并判断接下来该做什么。我的工作变成了写循环。"

这句话点破了一个我早就感觉到但没想清楚的事：**好的 Prompt 工程师不是会写提示词的人，是会设计循环系统的人。**

## Loop 的五个组成部分

Addy Osmani 把完整 Loop 拆成五个部分，我用自己的理解重新表述一遍：

### ① 定时任务（心跳）
自动启动循环执行既定任务，发现问题入待处理队列，没问题自动归档。**核心转变：我们不再是被动检查者。**

### ② 工作树隔离
给每个 Agent 独立工作空间，防止文件冲突和互相覆盖。多个 Agent 并行时各干各的，最后汇总。

### ③ Skills
Agent 每次新对话都会失忆，所以需要一套 Skills 沉淀项目规范、代码约定、踩坑记录。**在 Loop 里尤其关键——因为 Loop 自动跑，我们不在场。**

### ④ MCP
给 Agent 接上外部世界的能力——GitHub、数据库、Slack、飞书。让 Agent 能在真实环境中：发现问题 → 解决问题 → 通知人类。

### ⑤ 子 Agent
写代码的 Agent 不能自己给自己打分，AI 对自己有天然的包容性。所以用另一个 Agent、不同模型、更苛刻的 Prompt 做 Reviewer。

## 我觉得最重要的洞察

**Loop Engineering 的本质，是从"写提示词"转向"设计操作系统"。**

Prompt 工程时代，我们的工作是一对一问答：写好 prompt → 看输出 → 不满意 → 改 prompt。
Loop Engineering 时代，我们的工作是搭建系统：定义目标 → 构建自动循环 → Agent 自己迭代 → 完成。

这意味着：
- **人不在场也能工作**（通过定时任务 + Skills 兜底）
- **质量有客观保障**（通过子 Agent 交叉验证）
- **能力边界可扩展**（通过 MCP + 工具集成）

## 和我的实际配置对照

读这篇文章时我一直在对照自己的实践，发现很多点其实已经在做了：

| Loop 组件 | 我的对应实践 |
|-----------|-------------|
| 定时任务 | `schedule_task_*` 定时跑博客同步、自动任务 |
| Skills | 已安装的 20+ 个 Skills（self-improving-agent、interview-q-master 等） |
| 子 Agent | `subagent_dispatch` 做并行任务 + 交叉验证 |
| MCP | `mcp__*` 工具集成外部能力 |
| 记忆系统 | MEMORY.md + daily short-memories + 向量检索 |

就差"工作树隔离"这块我还没用到，后续可以考虑在并发任务场景引入。

## 关于文献检索案例的实操部分

文章后半部分用文献检索做了完整的 Loop 实战演示，核心流程：

1. 定时（每 3 天）从 arXiv/Google Scholar 抓取新论文
2. 每篇论文派到独立工作树（git worktree）解析
3. Skills 沉淀提取模板，让 Agent 按固定范式处理
4. MCP 连接 Zotero/飞书实现自动入库+通知
5. Reviewer 子 Agent 最后做交叉验证

这套流程虽然针对论文检索，但骨架完全可以复用——换成"定时抓岗位信息 → 过滤 → Skills 沉淀筛选标准 → 存入 → 通知"就是一个 BOSS 直聘自动监控 Loop。

> 总的来说，这篇文章帮我厘清了一个方向：我们正在从"和 AI 对话"走向"设计 AI 系统"。我现在更理解为什么自己的工具链要按 Skills + 定时任务 + 子 Agent 来构建——这本身就是一个小型 Loop Engineering 实践。

```