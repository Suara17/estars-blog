---
title: "面经库｜Tool Calling Complete Link 整理"
published: 2026-06-10
description: "# Tool_Calling_Complete_Link ## 问题 Tool_Calling_Complete_Link ## 标准回答 # Tool Calling（工具调用）完整链路：定义、调用与回传 Tool Calling 的核心"
tags: ["面经", "面经库"]
category: "面经整理"
draft: false
lang: zh-CN
pinned: false
comment: true
---

# Tool_Calling_Complete_Link
## 问题
Tool_Calling_Complete_Link

## 标准回答

# Tool Calling（工具调用）完整链路：定义、调用与回传

Tool Calling 的核心链路就四步：**定义工具 → LLM 决策 → 系统？
行 → 结果回传**。

打个比方：LLM 就像一个只会动嘴的指挥官，它不能亲自去查数据库、读文件，但它可以"下命令"让外部系统去执行，然后看执行报告决定下一步。Tool Calling 就是这个"下命令再拿报告"的标准化流程。

### 1. 工具定义
每个工具本质上是一段 JSON Schema，包含：
- 工具的名字
- 一段自然语言描述
- 参数的类型约束

LLM 不直接执行代码，只认这段 Schema 文本。示例：
```json
{
"name": "get_weather",
"description": "查询指定城市的当前天气",
"parameters": {
"type": "object",
"properties": {
"city": { "type": "string", "description": "城市名称" }
},
"required": ["city"]
}
}
```

### 2. LLM 决策调用
LLM 收到用户消息和工具列表后，若判断需要调用工具，返回一个特殊的 `tool_use` 消息（OpenAI 用 `tool_calls`，Anthropic 用 `tool_use`），包含工具名和填好的参数 JSON。注意：LLM 只是"说"要调什么工具、传什么参数，它自己**不会执行**。

### 3. 系统执行
系统侧拿到 `tool_use` 后，解析出工具名，找到本地注册的对应函数，传入参数执行。

### 4. 结果回传
执行完拿到结果，包装成 `tool_result` 消息追加到对话历史，再发回给 LLM。LLM 看到后有两种选择：
- 信息够了 → 直接生成最终回答
- 需要更多信息 → 再发一个 `tool_use`，形成循环

**完整链路**：
```
用户发消息 → LLM 分析消息和工具列表 → LLM 返回 tool_use → 系统执行工具函数 → 系统构造 tool_result → 发回 LLM → LLM 决定继续调用或输出最终回复
```

---

## 扩展知识

### 1. 从 Function Calling 到 Tool Calling 的演进
- **Function Calling**（OpenAI 2023.06）：一次只能调一个函数
- **Tool Calling**（2023.11）：支持 parallel tool calls，LLM 一次返回多个 tool_use，系统并行执行，一轮搞定多查询场景

不同厂商在 Schema 处理上有差异：Gemini 不支持 `patternProperties`，xAI 不支持 `minLength`/`maxLength`，OpenAI 要求参数顶层必须是 `type: "object"`。工程上需要一层 Schema 归一化来抹平差异。

### 2. 工具结果的上下文管理
工具返回数据量可能很大（如代码搜索返回 50KB）。生产级系统一般做截断：
- **head+tail 保留**：取开头和结尾各一部分，中间用省略标记替代
- **设置单条上限**：如占上下文窗口 20%-30% 或字符数硬上限

### 3. 安全与权限控制
工具调用是 Agent 系统中最容易出安全问题的环节。LLM 可能被 prompt injection 诱导调用不该调的工具（删除文件、发送邮件）。生产环境至少做三件事：
**工具白名单**：只暴露当前场景必需的工具
**参数校验**：服务端做 Schema 验证和业务规则校验
**敏感操作加人工确认**（如 LangChain 的 `HumanApprovalCallbackHandler`）

### 4. 错误处理和重试
工具执行失败是常态（网络超时、API 限流、参数格式错误）。好的做法：
- 将错误信息包装成 `tool_result` 返回给 LLM，让它自己决定怎么处理
- 设置最大重试次数（一般 3-5 次），超时强制返回，避免死循环

---

## 面试官追问

### Q1：LLM 返回的工具参数格式不对（少必填字段或类型不匹配），怎么处理？
**A**：两层防线。第一层：系统侧用 JSON Schema 做参数校验，不合规直接拦住不执行，把校验错误信息包装成 `tool_result` 返回给 LLM，大多数模型会自己修正参数重新调用。第二层：设置重试上限（一般 3 次），避免来回纠错死循环。

### Q2：parallel tool calls 并行执行多个工具时，其中一个失败怎么办？
**A**：各工具的执行结果独立回传，失败的那个单独返回错误信息，成功的正常返回结果。所有 `tool_result` 一起发回给 LLM，让它自己判断：可能只用成功的那几个结果就够了，也可能决定重试失败的那个。不需要全部成功才继续，类似 `Promise.allSettled` 的思路。

### Q3：Tool Calling 和 RAG 都是给 LLM 补充外部信息，它们的边界在哪？
**A**：
- **RAG**：提前检索、一次性注入，把相关文档片段塞进 prompt，适合知识查询类场景
- **Tool Calling**：按需执行、多轮交互，LLM 动态决定要不要调、调哪个，适合需要实时数据或执行副作用的场景（查数据库、发请求、操作文件系统）

简单说：RAG 解决"LLM 不知道的事"，Tool Calling 解决"LLM 做不到的事"。

### Q4：怎么让 LLM 更准确地选择正确的工具？
**A**：
- **写好 description**：写清楚工具干什么、什么场景该用、什么场景不该用；参数的 description 也要写明白（如"用户的唯一标识符，必须是数字格式"）
- **控制工具数量**：超过 15-20 个时，LLM 选择准确率明显下降。解决方案：分场景加载不同工具集，或做一层路由先判断意图再加载对应工具

## 

## 关键点

- # Tool Calling（工具调用）完整链路：定义、调用与回传

Tool Calling 的核心链路就四步：**定义工具 → LLM 决策 → 系统执行 → 结果回传**。
- 打个比方：LLM 就像一个只会动嘴的指挥官，它不能亲自去查数据库、读文件，但它可以"下命令"让外部系统去执行，然后看执行报告决定下一步。
- Tool Calling 就是这个"下命令再拿报告"的标准化流程。
- ### 1. 工具定义
每个工具本质上是一段 JSON Schema，包含：
- 工具的名字
- 一段自然语言描述
- 参数的类型约束

LLM 不直接执行代码，只认这段 Schema 文本。
- 示例：
```json
{
"name": "get_weather",
"description": "查询指定城市的当前天气",
"parameters": {
"type": "object",
"properties": {
"city": { "type": "string", "description": "城市名称" }
},
"required": ["city"]
}
}
```

LLM 收到用户消息和工具列表后，若判断需要调用工具，返回一个特殊的 `tool_use` 消息（OpenAI 用 `tool_calls`，Anthropic 用 `tool_use`），包含工具名和填好的参数 JSON。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

Tool_Calling_Complete_Link

Tool Calling 的核心链路就四步：**定义工具 → LLM 决策 → 系统执行 → 结果回传**。
- 打个比方：LLM 就像一个只会动嘴的指挥官，它不能亲自去查数据库、读文件，但它可以"下命令"让外部系统去执行，然后看执行报告决定下一步。Tool Calling 就是这个"下命令再拿报告"的标准化流程。
- ### 1. 工具定义
每个工具本质上是一段 JSON Schema，包含：
- 工具的名字
- 一段自然语言描述
- 参数的类型约束

LLM 不直接执行代码，只认这段 Schema 文本。示例：
```json
{
"name": "get_weather",
"description": "查询指定城市的当前天气",
"parameters": {
"type": "object",
"properties": {
"city": { "type": "string", "description": "城市名称" }
},
"required": ["city"]
}
}
```

LLM 收到用户消息和工具列表后，若判断需要调用工具，返回一个特殊的 `tool_use` 消息（OpenAI 用 `tool_calls`，Anthropic 用 `tool_use`），包含工具名和填好的参数 JSON。注意：LLM 只是"说"要调什么工具、传什么参数，它自己**不会执行**。
- ### 3. 系统执行
系统侧拿到 `tool_use` 后，解析出工具名，找到本地注册的对应函数，传入参数执行。
- ### 4. 结果回传
执行完拿到结果，包装成 `tool_result` 消息追加到对话历史，再发回给 LLM。LLM 看到后有两种选择：
- 信息够了 → 直接生成最终回答
- 需要更多信息 → 再发一个 `tool_use`，形成循环

**完整链路**：
```
用户发消息 → LLM 分析消息和工具列表 → LLM 返回 tool_use → 系统执行工具函数 → 系统构造 tool_result → 发回 LLM → LLM 决定继续调用或输出最终回复
```

---

- **Function Calling**（OpenAI 2023.06）：一次只能调一个函数
- **Tool Calling**（2023.11）：支持 parallel tool calls，LLM 一次返回多个 tool_use，系统并行执行，一轮搞定多查询场景

不同厂商在 Schema 处理上有差异：Gemini 不支持 `patternProperties`，xAI 不支持 `minLength`/`maxLength`，OpenAI 要求参数顶层必须是 `type: "object"`。工程上需要一层 Schema 归一化来抹平差异。

- 本文已做格式统一与噪声清理，保留原始语义。
- 行 → 结果回传**。
- 打个比方：LLM 就像一个只会动嘴的指挥官，它不能亲自去查数据库、读文件，但它可以"下命令"让外部系统去执行，然后看执行报告决定下一步。Tool Calling 就是这个"下命令再拿报告"的标准化流程。
- ### 1. 工具定义
- 每个工具本质上是一段 JSON Schema，包含：
- - 工具的名字

- 本文已做格式统一与噪声清理，保留原始语义。
