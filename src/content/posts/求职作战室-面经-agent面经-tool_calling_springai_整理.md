---
title: "求职作战室｜Tool Calling SpringAI 整理"
published: 2026-06-10
description: "# Tool_Calling_SpringAI ## 问题 Tool_Calling_SpringAI ## 标准回答 # 什么是工具调用 Tool Calling？ 如何利用 Spring AI 实现工具调用？ **Tool Callin"
tags: ["求职作战室", "面经"]
category: "求职作战室"
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

**在 Spring AI 中实现工具调用**：
**定义工具（Function）**：使用 `@Tool` 注解或实现 `Function` 接口。
**注册工具**：在 `ChatClient` 或 `ChatModel` 配置中注册工具 Bean。
**发起请求**：模型自动识别需要调用工具的场景，返回 `ToolCall` 对象。
**执行与回传**：应用执行工具后，将结果作为 `ToolExecutionResult` 消息追加到对话中，模型基于结果生成最终回答。

**示例代码**：

```java
@Component
public class WeatherService {
@Tool(description = "查询指定城市的当前天气")
public String getWeather(String city) {
// 实现天气查询逻辑
return "晴天，25°C";
}
}

// 配置 ChatClient
@Bean
ChatClient chatClient(ChatModel chatModel, WeatherService weatherService) {
return ChatClient.builder(chatModel)
.defaultTools(weatherService)
.build();
}

// 使用
String response = chatClient.prompt()
.user("北京今天天气怎么样？")
.call()
.content();
```

Spring AI 自动处理工具调用的完整链路：模型返回 `tool_calls` → 框架执行对应方法 → 结果回填 → 模型生成最终回复。

---

## 扩展知识

### 1. Tool Calling 的工作流程
- **第一步**：用户消息发送给 LLM，同时附上可用工具的定义（JSON Schema）。
- **第二步**：LLM 判断是否需要调用工具。如果是，返回包含 `tool_calls` 字段的响应（工具名和参数）。
- **第三步**：应用解析 `tool_calls`，执行对应函数，获得结果。
- **第四步**：应用将结果作为 `tool` 角色的消息再次发送给 LLM。
- **第五步**：LLM 基于工具结果生成最终回答，或继续请求调用其他工具。

### 2. Spring AI 的工具注册方式
- **`@Tool` 注解**：在任意 Spring Bean 的方法上使用，框架自动扫描并注册。
- **`FunctionCallback` 接口**：手动实现 `call` 方法，通过 `ChatClient.Builder.defaultFunctions()` 注册。
- **动态工具**：通过 `Prompt` 的 `options` 参数动态传入工具实例。

### 3. 处理并行工具调用
Spring AI 支持模型一次返回多个 `tool_calls`，框架默认串行执行，也可以配置线程池并行执行。

### 4. 错误处理与重试
- 工具执行抛异常时，Spring AI 会将异常信息作为 `tool` 消息返回给模型，让模型自行决定下一步（如修正参数重试或报告错误）。
- 可以配置 `RetryTemplate` 对工具调用进行重试。

---

## 面试官追问

### Q1：Tool Calling 和 Function Calling 是一回事吗？
**A**：本质相同，但 OpenAI 在 2023 年 11 月将 `functions` 参数升级为 `tools`，支持并行调用和更丰富的工具类型（如代码解释器）。Spring AI 统一抽象为工具。

### Q2：如何处理工具返回的数据过大导致上下文超限？
**A**：Spring AI 不提供自动截断，但可以在工具方法内部对结果进行摘要、截断或只返回关键信息。也可以结合 Spring AI 的 `Advice` 对工具结果进行后处理。

### Q3：如何让模型在特定条件下才调用工具？
**A**：通过 `@Tool` 的 `description` 写清楚工具的适用场景，并利用 System Prompt 引导模型的行为。复杂场景可自定义 `ToolCallingChatClient` 进行前置判断。

---

## 总结

Spring AI 简化了 Tool Calling 的集成，开发者只需定义带 `@Tool` 注解的方法，框架自动完成函数调用链路。这为构建具备行动能力的智能 Agent 提供了基础。

## 

## 关键点

- # 什么是工具调用 Tool Calling？
- 如何利用 Spring AI 实现工具调用？
- ## 核心回答

**Tool Calling（工具调用）** 是一种让大语言模型能够请求调用外部函数或 API 的机制。
- 模型不直接执行代码，而是输出结构化的调用请求（函数名和参数），由应用程序负责实际执行并将结果回传给模型。
- 这使 LLM 能够获取实时信息、操作外部系统、执行计算等。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

Tool_Calling_SpringAI

# 什么是工具调用 Tool Calling？如何利用 Spring AI 实现工具调用？
- ## 核心回答

**Tool Calling（工具调用）** 是一种让大语言模型能够请求调用外部函数或 API 的机制。模型不直接执行代码，而是输出结构化的调用请求（函数名和参数），由应用程序负责实际执行并将结果回传给模型。这使 LLM 能够获取实时信息、操作外部系统、执行计算等。
- **在 Spring AI 中实现工具调用**：
**定义工具（Function）**：使用 `@Tool` 注解或实现 `Function` 接口。
- 2. **注册工具**：在 `ChatClient` 或 `ChatModel` 配置中注册工具 Bean。
- 3. **发起请求**：模型自动识别需要调用工具的场景，返回 `ToolCall` 对象。

- 本文已做格式统一与噪声清理，保留原始语义。
- 如何利用 Spring AI 实现工具调用？
- **Tool Calling（工具调用）** 是一种让大语言模型能够请求调用外部函数或 API 的机制。模型不直接执行代码，而是输出结构化的调用请求（函数名和参数），由应用程序负责实际执行并将结果回传给模型。这使 LLM 能够获取实时信息、操作外部系统、执行计算等。
- **在 Spring AI 中实现工具调用**：
- 1. **定义工具（Function）**：使用 `@Tool` 注解或实现 `Function` 接口。
- 2. **注册工具**：在 `ChatClient` 或 `ChatModel` 配置中注册工具 Bean。

- 本文已做格式统一与噪声清理，保留原始语义。
