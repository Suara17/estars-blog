---
title: "面经库｜Compaction OpenClaw 策略 整理"
published: 2026-06-10
description: "# Compaction_OpenClaw_策略 ## 问题 Compaction_OpenClaw_策略 ## 标准回答 # 当对话历史太长、裁剪不够用时：Compaction（压缩）及 OpenClaw 策略 **Compaction（"
tags: ["面经", "面经库", "agent面经"]
category: "面经整理"
draft: false
lang: zh-CN
pinned: false
comment: true
---

# Compaction_OpenClaw_策略
## 问题
Compaction_OpenClaw_策略

## 标准回答

# 当对话历史太长、裁剪不够用时：Compaction（压缩）及 OpenClaw 策略

**Compaction（压实/压缩）**：当裁剪（直接丢早期消息）已经不够用时，换用？
LLM 把一大段对话历史压缩成一段精炼摘要，用摘要替换原始消息。这样大幅缩减 token 占用，但关键信息（决策、待办、结论）仍保留。

**OpenClaw 的 Compaction 核心流程（4 步）**：
**分块 (Chunking)**：按 token 预算切分消息（默认 2 段），保留最近 3 轮对话原文，只压缩更早的历史。
**逐块摘要**：每个 chunk 分别发给 LLM 生成摘要；若单条消息超大（>50% 窗口），降级处理（跳过超大消息并标注省略）。
**合并摘要**：再次调用 LLM 将多段局部摘要融合成一份最终摘要，要求保留：任务状态、进度、用户最后请求、决策及原因、待办、约束条件。
**摘要增强**：追加额外上下文，包括工具调用失败记录（exit code + error）、文件操作记录、最近几轮原文摘要、从 `AGENTS.md` 提取的关键规则。

最终摘要替换原始消息并写回会话历史。设计理念：宁可多花 token 调用 LLM 做摘要，也不丢关键信息。

---

## 扩展知识

### 1. 摘要质量检查与重试
- **质量审计**（默认关闭，需显式启用）检查摘要是否包含 5 个必要章节：`Decisions`、`Open TODOs`、`Constraints/Rules`、`Pending user asks`、`Exact identifiers`。
- 启用后若审计失败，会触发重试（最多 3 次）。
- 即使未启用审计，prompt 也会要求结构化章节。

### 2. 标识符严格保留策略
LLM 容易把 UUID、文件路径、API key 等概括掉。OpenClaw 默认采用 **strict 策略**，要求摘要中**原样保留**所有不可重构的标识符（如文件名、URL、hash、端口等），并在摘要中包含 `Exact identifiers` 章节。

### 3. Memory Flush 联动
在接近 Compaction 阈值时，会先触发一次额外 Agent 轮次（Memory Flush），让模型主动把重要信息写入 `memory/YYYY-MM-DD.md` 长期存储。相当于“考前再检查一遍”，防止压缩丢失关键信息。

### 4. Post-compaction Context 注入
压缩完成后，从 `AGENTS.md` 重新注入 “Session Startup” 和 “Red Lines” 两部分，避免模型遗忘红线规则。

### 5. 工具调用失败信息保留
Compaction 会专门提取并保留工具调用失败信息（exit code + error）。避免 Agent 压缩后重复尝试已知不可行的路径。

---

## 面试官追问

### Q1：Compaction 本身也要调 LLM，token 开销大吗？
**A**：单次 Compaction 消耗几千 token，但能把几万 token 的历史压缩到几千 token 的摘要，后续每轮都省大量 token。长对话收益显著，总 token 消耗远低于不做压缩。

### Q2：分段摘要的 chunk 大小怎么定？
**A**：按模型 Context 窗口的 40% 为基准，自适应调整（最低 15%），预留约 4096 token 给摘要 prompt。在消息边界切分，不跨消息。跨 chunk 的上下文关联靠合并摘要阶段弥补。

### Q3：Compaction 触发时机？
**A**：按 token 数触发，每次组装 prompt 前计算当前历史占比，超过阈值即触发。不用固定轮次，因为每轮长度差异大。

### Q4：strict 策略保留标识符会不会导致摘要膨胀？
**A**：会，但标识符通常只占几十 token，相比丢失标识符后任务失败再重试的代价，成本低得多。过时标识符可在 Memory Flush 阶段由 Agent 主动清理。

## 

## 关键点

- # 当对话历史太长、裁剪不够用时：Compaction（压缩）及 OpenClaw 策略

**Compaction（压实/压缩）**：当裁剪（直接丢早期消息）已经不够用时，换用 LLM 把一大段对话历史压缩成一段精炼摘要，用摘要替换原始消息。
- 这样大幅缩减 token 占用，但关键信息（决策、待办、结论）仍保留。
- **OpenClaw 的 Compaction 核心流程（4 步）**：
**分块 (Chunking)**：按 token 预算切分消息（默认 2 段），保留最近 3 轮对话原文，只压缩更早的历史。
- 2. **逐块摘要**：每个 chunk 分别发给 LLM 生成摘要；若单条消息超大（>50% 窗口），降级处理（跳过超大消息并标注省略）。
- 3. **合并摘要**：再次调用 LLM 将多段局部摘要融合成一份最终摘要，要求保留：任务状态、进度、用户最后请求、决策及原因、待办、约束条件。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

Compaction_OpenClaw_策略

**Compaction（压实/压缩）**：当裁剪（直接丢早期消息）已经不够用时，换用 LLM 把一大段对话历史压缩成一段精炼摘要，用摘要替换原始消息。这样大幅缩减 token 占用，但关键信息（决策、待办、结论）仍保留。
- **OpenClaw 的 Compaction 核心流程（4 步）**：
**分块 (Chunking)**：按 token 预算切分消息（默认 2 段），保留最近 3 轮对话原文，只压缩更早的历史。
- 2. **逐块摘要**：每个 chunk 分别发给 LLM 生成摘要；若单条消息超大（>50% 窗口），降级处理（跳过超大消息并标注省略）。
- 3. **合并摘要**：再次调用 LLM 将多段局部摘要融合成一份最终摘要，要求保留：任务状态、进度、用户最后请求、决策及原因、待办、约束条件。
- 4. **摘要增强**：追加额外上下文，包括工具调用失败记录（exit code + error）、文件操作记录、最近几轮原文摘要、从 `AGENTS.md` 提取的关键规则。

- 本文已做格式统一与噪声清理，保留原始语义。
- LLM 把一大段对话历史压缩成一段精炼摘要，用摘要替换原始消息。这样大幅缩减 token 占用，但关键信息（决策、待办、结论）仍保留。
- **OpenClaw 的 Compaction 核心流程（4 步）**：
- 1. **分块 (Chunking)**：按 token 预算切分消息（默认 2 段），保留最近 3 轮对话原文，只压缩更早的历史。
- 2. **逐块摘要**：每个 chunk 分别发给 LLM 生成摘要；若单条消息超大（>50% 窗口），降级处理（跳过超大消息并标注省略）。
- 3. **合并摘要**：再次调用 LLM 将多段局部摘要融合成一份最终摘要，要求保留：任务状态、进度、用户最后请求、决策及原因、待办、约束条件。

- 本文已做格式统一与噪声清理，保留原始语义。
