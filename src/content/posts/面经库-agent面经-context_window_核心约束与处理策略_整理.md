---
title: "面经库｜Context Window 核心约束与处理策略 整理"
published: 2026-06-10
description: "# Context_Window_核心约束与处理策略 ## 问题 Context_Window_核心约束与处理策略 ## 标准回答 # Agent 的 Context Window：核心约束与处理策略 ## 什么是 Context Wind"
tags: ["面经", "面经库", "agent面经"]
category: "面经整理"
draft: false
lang: zh-CN
pinned: false
comment: true
---

# Context_Window_核心约束与处理策略
## 问题
Context_Window_核心约束与处理策略

## 标准回答

# Agent 的 Context Window：核心约束与处理策略

## 什么是 Context Window？
Context Window（上下文窗口）是大语言模型（LLM）单次请求能处理的最大 token 数量。Token 是模型处理文本的最小单位，英文约 1 token ≈ 4 个字符，中文 1 个汉字通常 2-3 个 token。

**为什么是 Agent 工程中最核心的约束？**

Agent 的上下文里塞的东西太多：
- System Prompt（2000-5000 token）
- 工具定义列表（每个 200-500 token，20 个工具就是 4000-10000 token）
- 完整对话历史
- 每次工具调用的入参和返回结果
- 模型回复预留空间

一次 Agent 运行可能跑几十轮，每一轮结果都追加到历史中，Context 像滚雪球一样越来越大。一旦超出窗口，要么直接报错中断任务，要么被迫裁剪历史导致关键信息丢失，Agent 行为变得不可预测。

---

## 扩展知识

### 1. Context Window 里到底塞了什么？

以典型编程 Agent 为例：
- **固定开销**：System Prompt + 工具定义，每次请求都得带，约 6000-15000 token
- **对话历史**：每调一次工具增加两条消息（tool_call + tool_result）。工具返回一个文件内容可能占 3000-8000 token。跑 10 轮，历史轻松突破 50K token。

OpenClaw 在 `src/agents/context.ts` 中将这些组成部分拆分，按优先级管理空间占用。

### 2. OpenClaw 的 Context Window 管理机制

**窗口大小确定优先级**（从高到低）：
`modelsConfig` 用户显式指定的值
模型注册表自动发现的值
默认 128K token
`agents.defaults.contextTokens` 做全局上限截断

**两道防线**：
- 硬下限：`CONTEXT_WINDOW_HARD_MIN_TOKENS = 16,000`，低于此值拒绝运行
- 软告警：`CONTEXT_WINDOW_WARN_BELOW_TOKENS = 32,000`，低于此值警告用户

**检测到 overflow 时的渐进式处理**：
先尝试 **compaction**（压缩早期对话历史为摘要）
再尝试**截断过大的 tool result**（保留头尾加摘要）
最后报错，建议用户 `/reset` 或换更大窗口的模型

### 3. 主流的 Context 管理策略

| 策略 | 做法 | 优点 | 缺点 |
|------|------|------|------|
| 滑动窗口 | 只保留最近 N 轮对话 | 实现简单 | 易丢失任务关键信息（如最初需求） |
| 摘要压缩 | 用额外 LLM 调用压缩长对话 | 效果好 | 延迟 + token 成本，可能丢失细节 |
| 分层存储 | 按优先级分级：System + 最近2轮永久保留，中间做摘要，大文本截断 | 平衡保真度和空间 | 实现复杂 |
| 外部检索 | 历史存向量数据库，每轮检索相关片段 | 适合超长会话 | 检索质量依赖 embedding |

**实际生产**：混合使用，不依赖单一策略。

### 4. Token 计算的坑

- 同样长度中文比英文 token 开销高 2-3 倍
- 不同模型的 tokenizer 不同，同一段文本在 GPT 和 Claude 中 token 数可能差 10%-20%
- **OpenClaw 做法**：用各模型对应的 tokenizer 精确计算，留出 10% 安全余量

---

## 面试官追问

### Q1：实现 compaction 机制时，摘要格式怎么设计？哪些信息不能丢？

**必须保留三类信息**：
用户的原始任务目标
已经完成了哪些关键步骤
当前的执行状态和中间产物

**格式建议**：结构化文本，分块标注，方便 LLM 快速抓重点。

**最忌讳**：丢了任务目标 → Agent 压缩完不知道自己在干嘛。

**示例**（调试 bug 场景）：
> 用户报告了 NPE 异常，已经定位到是 UserService 第 87 行空指针，尝试了加 null check 但测试仍然失败。

### Q2：不同模型的 Context Window 差异很大，怎么处理兼容性？

**核心思路**：自适应。

- Agent 启动时查模型注册表拿到窗口大小
- 动态计算固定开销占多少，留给对话历史的空间有多少
- 小模型（如 8K）更要激进压缩，甚至限制可注册的工具数量
- OpenClaw 设硬下限 16K token，低于此值拒绝运行
- 上层给用户推荐清单，标明每个模型适合跑的复杂度的任务

### Q3：工具返回结果特别大时（如 1 万行日志），怎么处理？

**不能全塞**（30K-50K token，一次吃大半窗口）。

**处理思路**：按需截断 + 智能提取

- **最简单**：设 tool result token 上限，超了就保留头尾各几百行 + "中间省略 N 行" 标记
- **更聪明**：截断前让 LLM 做一轮 relevance extraction，只留与当前任务相关的内容
- OpenClaw 在 `context-window-guard` 中有类似处理，优先截断大的 tool result（最“胖”也最容易压缩）

---

## 总结

Context Window 是 Agent 工程的物理瓶颈。优秀的管理策略不是单点优化，而是组合使用**滑动窗口、摘要压缩、分层存储、外部检索**等多种手段，并根据模型能力自适应调整。OpenClaw 的渐进式降级（compaction → 截断 → 报错）和精确 token 计算（含 10% 余量）是值得参考的实践。

> 

## 关键点

算力够，但装不下那么多信息。工程上必须主动管理，而不是被动等溢出报错。

## 

- # Agent 的 Context Window：核心约束与处理策略

- Context Window（上下文窗口）是大语言模型（LLM）单次请求能处理的最大 token 数量。
- Token 是模型处理文本的最小单位，英文约 1 token ≈ 4 个字符，中文 1 个汉字通常 2-3 个 token。
- **为什么是 Agent 工程中最核心的约束？
- **

Agent 的上下文里塞的东西太多：
- System Prompt（2000-5000 token）
- 工具定义列表（每个 200-500 token，20 个工具就是 4000-10000 token）
- 完整对话历史
- 每次工具调用的入参和返回结果
- 模型回复预留空间

一次 Agent 运行可能跑几十轮，每一轮结果都追加到历史中，Context 像滚雪球一样越来越大。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

Context_Window_核心约束与处理策略

- Context Window（上下文窗口）是大语言模型（LLM）单次请求能处理的最大 token 数量。Token 是模型处理文本的最小单位，英文约 1 token ≈ 4 个字符，中文 1 个汉字通常 2-3 个 token。
- **为什么是 Agent 工程中最核心的约束？**

Agent 的上下文里塞的东西太多：
- System Prompt（2000-5000 token）
- 工具定义列表（每个 200-500 token，20 个工具就是 4000-10000 token）
- 完整对话历史
- 每次工具调用的入参和返回结果
- 模型回复预留空间

一次 Agent 运行可能跑几十轮，每一轮结果都追加到历史中，Context 像滚雪球一样越来越大。一旦超出窗口，要么直接报错中断任务，要么被迫裁剪历史导致关键信息丢失，Agent 行为变得不可预测。
- ---

- 以典型编程 Agent 为例：
- **固定开销**：System Prompt + 工具定义，每次请求都得带，约 6000-15000 token
- **对话历史**：每调一次工具增加两条消息（tool_call + tool_result）。工具返回一个文件内容可能占 3000-8000 token。跑 10 轮，历史轻松突破 50K token。

- 本文已做格式统一与噪声清理，保留原始语义。
- Context Window（上下文窗口）是大语言模型（LLM）单次请求能处理的最大 token 数量。Token 是模型处理文本的最小单位，英文约 1 token ≈ 4 个字符，中文 1 个汉字通常 2-3 个 token。
- **为什么是 Agent 工程中最核心的约束？**
- Agent 的上下文里塞的东西太多：
- - System Prompt（2000-5000 token）
- - 工具定义列表（每个 200-500 token，20 个工具就是 4000-10000 token）

- 本文已做格式统一与噪声清理，保留原始语义。
