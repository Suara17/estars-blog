---
title: "面经库｜LLM Long Conversation Handling 整理"
published: 2026-06-10
description: "# LLM_Long_Conversation_Handling ## 问题 LLM_Long_Conversation_Handling ## 标准回答 # LLM 的 Context Window 有上限，长对话时如何保证 Agent "
tags: ["面经", "面经库"]
category: "面经整理"
draft: false
lang: zh-CN
pinned: false
comment: true
---

# LLM_Long_Conversation_Handling
## 问题
LLM_Long_Conversation_Handling

## 标准回答

# LLM 的 Context Window 有上限，长对话时如何保证 Agent 仍然能正常工作？
OpenClaw 是怎么做的？

长对话的核心风险是 Context Window 溢出，导致请求报错或模型"失忆"。

OpenClaw 采用**分层防御**策略，从轻到重依次处理：
**Context Pruning（上下文修剪）**
每次请求前，清理不重要的早期 Tool Result。采用两级阈值：
- `softTrimRatio`（默认 0.3）：对超大的 tool result 做 head+tail 裁剪
- `hardClearRatio`（默认 0.5）：直接替换为 placeholder
保护规则：保留最近 3 条 assistant 消息、第一条 user message 之前的内容（System Prompt 等）。
**Tool Result Context Guard（工具返回兜底）**
计算全局预算（Context Window × 4 × 0.75），先单条截断，若总量仍超则从最早的 tool result 开始替换为 `[compacted: tool output removed to free context]`。确保送给 LLM 的 Context 永远安全。
**Memory Flush（记忆刷盘）**
Token 用量接近 compaction 阈值时，让 Agent 将关键信息写入 `memory/YYYY-MM-DD.md`，防止压缩丢失重要细节。
**Compaction（压缩）**
用 LLM 将旧对话历史压缩为摘要，替换原始消息。例如 100 条消息压成一段摘要，token 消耗降一个数量级。由于已做 Memory Flush，有损压缩可接受。

---

## 扩展知识

### 1. Context Pruning 的巧妙保护
- 基于 pi-coding-agent 的 extension，注册在 `context` 事件上。
- 可修剪的对象是早期的 tool result（默认全部可修剪，支持 allow/deny glob 配置）。
- 有 cache-ttl 冷却期（默认 5 分钟），避免每次请求重复扫描。

### 2. Tool Result 截断的智能检测
在 `tool-result-truncation.ts` 中，通过 `hasImportantTail()` 检测尾部是否包含 `error`、`exception`、`exit code`、`traceback` 等关键词。若有则优先保留尾部（head+tail 策略），因为错误信息通常比正常输出更有价值。

### 3. Compaction 摘要的质量保障
- **Identifier Preservation**：摘要必须保留 UUID、hash、URL、文件名等不可重建的标识符。
- **Memory Flush 前置**：在 compaction 前先落盘关键信息，降低摘要的有损风险。

---

## 面试官追问

### Q1：Compaction 压缩摘要的时机怎么选？
**A**：太频繁会浪费 token 和增加延迟，太晚则 context 逼近上限。OpenClaw 采用自动触发机制：当 context token 逼近模型窗口时自动触发。在 compaction 之前，Context Pruning 已在低阈值（30% 裁剪、50% 替换）做了减负，因此 compaction 不需要太频繁。同时 Memory Flush 有独立触发条件（`softThresholdTokens` 默认 4000），确保关键信息提前落盘。

### Q2：压缩后的摘要本身也会越来越长，怎么处理？
**A**：采用**滚动摘要**策略。例如第一次压缩 1-50 条生成摘要 A，第二次将摘要 A + 51-100 条一起压缩成摘要 B。每次压缩保持摘要长度稳定，早期保真度虽会降低，但对多数场景 50 轮前的细节已不重要。

### Q3：Context Pruning 删掉的 tool result，如果后面模型又需要了怎么办？
**A**：两种恢复途径：
**再次读取**：如果是文件内容类（如 `read_file`），文件仍在磁盘，模型可再次调用工具。
**Memory Flush 语义存储**：在 compaction 前，LLM 自行提取关键信息（决策、配置、进度等）以语义形式写入 `memory/YYYY-MM-DD.md`，而非保存原始 tool result。模型后续可通过读取该文件获取上下文。

---

## 总结

OpenClaw 的四层防御体系（修剪 → 守卫 → 刷盘 → 压缩）层层递进，既保证了长对话的持续性，又通过智能检测（错误尾部优先、标识符保留）和信息落盘，最大程度降低了有损处理带来的副作用。

## 

## 关键点

- # LLM 的 Context Window 有上限，长对话时如何保证 Agent 仍然能正常工作？
- OpenClaw 是怎么做的？
- ## 核心回答

长对话的核心风险是 Context Window 溢出，导致请求报错或模型"失忆"。
- OpenClaw 采用**分层防御**策略，从轻到重依次处理：
**Context Pruning（上下文修剪）**
每次请求前，清理不重要的早期 Tool Result。
- 采用两级阈值：
- `softTrimRatio`（默认 0.3）：对超大的 tool result 做 head+tail 裁剪
- `hardClearRatio`（默认 0.5）：直接替换为 placeholder
保护规则：保留最近 3 条 assistant 消息、第一条 user message 之前的内容（System Prompt 等）。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

LLM_Long_Conversation_Handling

# LLM 的 Context Window 有上限，长对话时如何保证 Agent 仍然能正常工作？OpenClaw 是怎么做的？
- ## 核心回答

长对话的核心风险是 Context Window 溢出，导致请求报错或模型"失忆"。
- OpenClaw 采用**分层防御**策略，从轻到重依次处理：
**Context Pruning（上下文修剪）**
每次请求前，清理不重要的早期 Tool Result。采用两级阈值：
- `softTrimRatio`（默认 0.3）：对超大的 tool result 做 head+tail 裁剪
- `hardClearRatio`（默认 0.5）：直接替换为 placeholder
保护规则：保留最近 3 条 assistant 消息、第一条 user message 之前的内容（System Prompt 等）。
- 2. **Tool Result Context Guard（工具返回兜底）**
计算全局预算（Context Window × 4 × 0.75），先单条截断，若总量仍超则从最早的 tool result 开始替换为 `[compacted: tool output removed to free context]`。确保送给 LLM 的 Context 永远安全。
- 3. **Memory Flush（记忆刷盘）**
Token 用量接近 compaction 阈值时，让 Agent 将关键信息写入 `memory/YYYY-MM-DD.md`，防止压缩丢失重要细节。

- 本文已做格式统一与噪声清理，保留原始语义。
- OpenClaw 是怎么做的？
- 长对话的核心风险是 Context Window 溢出，导致请求报错或模型"失忆"。
- OpenClaw 采用**分层防御**策略，从轻到重依次处理：
- 1. **Context Pruning（上下文修剪）**
- 每次请求前，清理不重要的早期 Tool Result。采用两级阈值：

- 本文已做格式统一与噪声清理，保留原始语义。
