---
title: "Agent_Super_Result_Handling"
published: 2026-06-12
description: "Agent_Super_Result_Handling Agent 调用工具返回超大结果（如代码搜索返回 50KB 文本）会带来三个？ 接问题： - Token 爆炸：50KB 文本按 1 token≈4 字符估算，单条结果吃掉 12000+ token。 - 挤占上下文空间：128K 窗口下，一条结果占近 10%，挤压历史、System Prompt 和用户消息。 - 延迟飙升：处理大结果增加计..."
category: "求职作战室"
tags: ["\u6c42\u804c\u4f5c\u6218\u5ba4", "\u9762\u7ecf"]
draft: false
lang: zh-CN
---
# Agent_Super_Result_Handling
## 问题
Agent_Super_Result_Handling

## 标准回答

# Agent 调用工具返回超大结果的处理与 OpenClaw 实践

Agent 调用工具返回超大结果（如代码搜索返回 50KB 文本）会带来三个？
接问题：
- **Token 爆炸**：50KB 文本按 1 token≈4 字符估算，单条结果吃掉 12000+ token。
- **挤占上下文空间**：128K 窗口下，一条结果占近 10%，挤压历史、System Prompt 和用户消息。
- **延迟飙升**：处理大结果增加计算和传输成本。

处理思路分两步：**限额 + 截断**。为每条 tool result 设字符上限，超限则采用 **head+tail 截断**：保留开头让模型理解内容，保留尾部抓住错误信息，中间砍掉并加省略标记。

OpenClaw 实现两层防护：
**单条截断**：按 context window 的 30% 设上限（硬上限 400K 字符）。检测尾部是否包含错误关键词（error/exception/traceback 等），有则 head 占约 70%（最少 2000 字符）、tail 占 30%（上限 4000 字符）分割；否则只保留开头。截断后附加提示，告知内容不完整，可用 offset/limit 重新获取。
**全局预算守卫**：每次请求前计算总字符开销，超过 context window 的 75% 时，从最早的 tool result 开始替换为占位提示，优先牺牲早期结果，保证新内容空间。

---

## 扩展知识

### 1. 为什么不能只保留前 N 个字符
- 直接 substring(0, maxLen) 会丢失关键信息。例如 grep 搜索最相关匹配可能在中后部；命令执行失败时，真正的错误栈在末尾。
- head+tail 策略虽不完美，但能兜住两头。OpenClaw 的 `truncateToolResultMessage()` 对多 block 内容按比例分配字符，避免单一 block 独占。
- `hasImportantTail()` 动态检测尾部是否包含错误关键词或 JSON 闭合结构，只有命中才启用 head+tail，否则只保留开头。

### 2. 字符预算计算
- 单条上限 ≈ context window tokens × 每 token 字符数 × 30%（代码文本 token 密度高，OpenClaw 对 tool result 用换算系数 2）。128K 模型：单条约 150K 字符。
- 全局预算 ≈ 128K × 4 × 75% ≈ 384K 字符。

### 3. 其他框架处理对比
- **LangChain**：ToolMessage 默认不截断，社区实践在 parser 层加限制。
- **Anthropic Claude**：文档建议单条 tool result 不超过 100K 字符。
- **AutoGPT**：早期无截断，context 常被撑爆，后加 `max_length` 参数。

---

## 面试官追问

### Q1：截断后模型基于不完整信息做错误判断，怎么处理？
**A**：在截断标记中明确告知内容被截断，并建议使用 offset/limit 或请求特定部分重新获取。OpenClaw 截断后缀会说明“Content truncated”并提供重新获取指引。更优做法是附上原始内容的字符数和行数，让模型判断信息损失程度，必要时发起二次精确查询（如缩小范围、指定行号）。

### Q2：head+tail 的比例怎么定？
**A**：无通用最优比例，依赖 tool 类型：
- 搜索类工具（结果按相关性排序）：head 更重要，可 head 占 70%、tail 占 30%。
- 命令执行类工具（关键信息在末尾）：head 40%、tail 60%。

OpenClaw 实际使用 tail 占 30%（上限 4000 字符），head 拿剩余且最少保留 2000 字符。仅当 `hasImportantTail()` 检测到尾部有关键词时才走 head+tail，否则默认只保留开头。

### Q3：除了截断，还有哪些方式处理超大 tool result？
**A**：
**工具端过滤**：如代码搜索只返回最相关 top 10，不吐全量。
**摘要模型压缩**：用 sub-agent 先将大结果压缩成摘要再喂给主模型（如 Anthropic 内部实践）。
**分页**：将大结果拆成多页，模型可选翻页获取更多内容。

截断是最简单的兜底方案，理想情况下应在工具端控制输出量。

## 

## 关键点

- # Agent 调用工具返回超大结果的处理与 OpenClaw 实践

Agent 调用工具返回超大结果（如代码搜索返回 50KB 文本）会带来三个直接问题：
- **Token 爆炸**：50KB 文本按 1 token≈4 字符估算，单条结果吃掉 12000+ token。
- - **挤占上下文空间**：128K 窗口下，一条结果占近 10%，挤压历史、System Prompt 和用户消息。
- - **延迟飙升**：处理大结果增加计算和传输成本。
- 处理思路分两步：**限额 + 截断**。
- 为每条 tool result 设字符上限，超限则采用 **head+tail 截断**：保留开头让模型理解内容，保留尾部抓住错误信息，中间砍掉并加省略标记。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

Agent_Super_Result_Handling

Agent 调用工具返回超大结果（如代码搜索返回 50KB 文本）会带来三个直接问题：
- **Token 爆炸**：50KB 文本按 1 token≈4 字符估算，单条结果吃掉 12000+ token。
- - **挤占上下文空间**：128K 窗口下，一条结果占近 10%，挤压历史、System Prompt 和用户消息。
- - **延迟飙升**：处理大结果增加计算和传输成本。
- 处理思路分两步：**限额 + 截断**。为每条 tool result 设字符上限，超限则采用 **head+tail 截断**：保留开头让模型理解内容，保留尾部抓住错误信息，中间砍掉并加省略标记。
- OpenClaw 实现两层防护：
**单条截断**：按 context window 的 30% 设上限（硬上限 400K 字符）。检测尾部是否包含错误关键词（error/exception/traceback 等），有则 head 占约 70%（最少 2000 字符）、tail 占 30%（上限 4000 字符）分割；否则只保留开头。截断后附加提示，告知内容不完整，可用 offset/limit 重新获取。

- 本文已做格式统一与噪声清理，保留原始语义。
- - **Token 爆炸**：50KB 文本按 1 token≈4 字符估算，单条结果吃掉 12000+ token。
- - **挤占上下文空间**：128K 窗口下，一条结果占近 10%，挤压历史、System Prompt 和用户消息。
- - **延迟飙升**：处理大结果增加计算和传输成本。
- 处理思路分两步：**限额 + 截断**。为每条 tool result 设字符上限，超限则采用 **head+tail 截断**：保留开头让模型理解内容，保留尾部抓住错误信息，中间砍掉并加省略标记。
- OpenClaw 实现两层防护：

- 本文已做格式统一与噪声清理，保留原始语义。