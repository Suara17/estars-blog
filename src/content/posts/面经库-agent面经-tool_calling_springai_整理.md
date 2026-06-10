---
title: "面经库｜Tool Calling SpringAI 整理"
published: 2026-06-10
description: "# Tool_Calling_SpringAI ## 问题 Tool_Calling_SpringAI ## 标准回答 # 什么是工具调用 Tool Calling？ 如何利用 Spring AI 实现工具调用？ **Tool Callin"
tags: ["面经", "面经库", "agent面经"]
category: "面经整理"
draft: false
lang: zh-CN
pinned: false
comment: true
---

# Tool_Calling_SpringAI
## 问题
Tool_Calling_SpringAI

## 标准回答

# 什么是工具调用 Tool Calling？
如何利用 Spring AI 实现工具调用？

**Tool Calling（工具调用）** 是一种让大语言模型能够请求调用外部函数或 API 的机制。模型不直接执行代码，而是输出结构化的调用请求（函数名和参数），由应用程序负责实际执行并将结果回传给模型。这使 LLM 能够获取实时信息、操作外部系统、执行计算等。

**实现工具调用**：
**定义工具（Function）**：使用 `@Tool` 注解或实现 `Function` 接口。
**注册工具**：在 `ChatClient` 或 `ChatModel` 配置中注册工具 Bean。
**发起请求**：模型自动识别需要调用工具的场景，返回 `ToolCall` 对象。
**执行与回传**：应用执行工具后，将结果作为 `ToolExecutionResult` 消息追加到对话中，模型基于结果生成最终回答。

## 扩展知识

### 1. Tool Calling 的工作流程
- **第一步**：用户消息发送给 LLM，同时附上可用工具的定义（JSON Schema）。
- **第二步**：LLM 判断是否需要调用工具。如果是，返回包含 `tool_calls` 字段的响应（工具名和参数）。
- **第三步**：应用解析 `tool_calls`，执行对应函数，获得结果。
- **第四步**：应用将结果作为 `tool` 角色的消息再次发送给 LLM。
- **第五步**：LLM 基于工具结果生成最终回答，或继续请求调用其他工具。

---

## 面试官追问

### Q1：Tool Calling 和 Function Calling 是一回事吗？
**A**：本质相同，但 OpenAI 在 2023 年 11 月将 `functions` 参数升级为 `tools`，支持并行调用和更丰富的工具类型（如代码解释器）。

### Q2：如何处理工具返回的数据过大导致上下文超限？
**A**：
### Q3：如何让模型在特定条件下才调用工具？
