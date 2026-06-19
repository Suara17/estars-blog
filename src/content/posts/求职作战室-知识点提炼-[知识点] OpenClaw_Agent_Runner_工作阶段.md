---
title: 'OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？'
published: 2026-06-19
description: 'OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？'
category: '求职作战室'
tags: ['求职作战室', '知识点提炼']
draft: false
lang: zh-CN
---# OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？
## 问题
OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？

## 标准回答
OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？Agent Runner 是 OpenClaw 的核心调度器，可以理解为"指挥中心"，负责协调 LLM 调用、工具执行、错误处理等所有环节。一次完整的 Agent 运行从用户发消息到最终输出，大致经历以下阶段：1）排队，先进 session 级队列（保证同一会话串行），再进全局队列（控制总并发），防止资源被打满2）准备，解析 workspace、provider/model、thinking level 等基础参数3）插件 + Hook，加载运行时插件后，触发before_model_resolve和before_agent_start钩子，插件可以在模型解析之前动态覆盖 provider 和 model4）模型解析 + 鉴权，根据（可能被 Hook 修改过的）配置确定模型定义、上下文窗口大小，并按优先级选出可用的 API Key5）尝试执行（核心，可重试）：创建或恢复 Session，加载历史消息注册工具集（统一走 customTools 路径，保证沙箱和策略过滤一致性）根据 Provider 设置流式引擎（Ollama 直连、OpenAI WebSocket、通用 HTTP 等）触发执行循环：LLM 调用 → 工具执行 → 结果回传 → 再调 LLM，直到模型认为任务完成6）溢出降级，如果上下文超限：先 compaction 压缩历史 → 再截断超大 tool result → 都不行就报错引导用户开新会话整个流程的设计思路是每个阶段都可插拔。插件通过 Hook 介入、模型和 Provider 可动态切换、工具集按需组合。

## 扩展知识

attempt + fallback 容错机制Agent Runner 不是跑一次就完事，容错分两层：1）Auth Profile 轮转：如果一次尝试因为 auth 失败、限流或服务过载挂了，Runner 会自动切到同 Provider 的下一个 API Key 重试。比如配了三个 OpenAI Key，第一个被限流就自动换第二个。

2） 模型级 Fallback：如果所有 Key 都轮完还是失败，Runner 向外层抛出 FailoverError，外层的 model-fallback 层会切到配置的备用模型。比如 Claude 整体不可用就降级到 GPT-4o，用户几乎感知不到切换。重试有上限（根据 profile 数量动态计算，范围 32-160 次），不会无限重试。遇到服务过载还会加指数退避，避免继续打爆上游。工具调用的双层包装每个工具在注册时会经过两层包装：1）Hook 拦截层：插件可以在工具执行前异步检查参数、做权限校验，甚至直接阻止执行。这一层还内置了循环检测，防止 LLM 反复调用同一工具陷入死循环。

2） 取消机制层：把外部的 AbortSignal 和工具自带的信号合并。当用户发了新消息、超时了、或手动停止时，正在执行的工具可以被中断，不用干等到超时。流式处理的 Provider 适配Runner 默认用通用的streamSimple做流式输出，但不同 Provider 的流式 API 差异很大，所以会根据 Provider 类型动态替换流式引擎：Ollama：走原生/api/chat直连，绕过通用路径以获得更可靠的 streaming 和工具调用OpenAI：支持 WebSocket 通道，减少 HTTP 开销Google：额外 Gemini 特有的 thinking 字段所有 Provider 还会统一做工具名称规范化（有些模型输出的工具名带空格或前缀），确保工具分发能精确匹配这层适配做完后，执行循环的代码不用管底下是哪家 Provider，调同一个接口就行。新增 Provider 也只需要写一个流式适配函数。Context 溢出的三级降级执行循环跑着跑着 context 可能会超限，特别是工具返回了大量内容的时候。Runner 对此做了三级自动降级：1）先尝试compaction，调用 Context Engine 压缩历史消息，腾出 token 空间2）compaction 还不够的话，截断超大 tool result。截断策略是动态的：先检测尾部是否包含错误信息或结果摘要，如果尾部重要就保留首尾、砍掉中间；否则只保留开头。截断位置会插入说明提示模型内容被截断了。单个 tool result 最多占上下文窗口的 30%3）前两步都救不回来，报错降级，告诉用户 context 太长了，建议开新会话整个过程对用户透明，尽最大努力保证对话能继续下去。

## 面试官追问

- **提问**：你说排队执行保证并发安全，那如果用户快速连发两条消息会怎样？后面那条是排队等还是直接丢弃？回答：后面那条消息会进入 session 级队列排队等，不会丢弃也不会并发执行。设计上是嵌套两级队列：先进 session 队列（保证同 session 串行），再进全局队列（控制总并发）。等前一条消息的 Agent 运行完成后才处理下一条。用户体验上是第二条消息会等一会儿才开始响应。- **提问**：fallback 机制切换模型之后，之前的对话历史格式兼容吗？不同模型的消息格式不一样怎么办？
- **回答**：历史消息以统一的中间格式存储在 session 文件中。切换模型时用的是同一份 session file，新的 attempt 启动时会根据目标 Provider 的特性做格式适配。比如 Gemini 和 Anthropic 的 turn 交替规则不同、thinking block 处理不同，这些都在 session 历史清洗阶段自动处理。所以 fallback 切换对历史消息是透明的，不需要手动做格式迁移。- **提问**：工具的 Hook 拦截层会不会引入性能问题？每次工具调用都多走两层包装，延迟能接受吗？
- **回答**：两层包装本身的开销可以忽略不计，就是几个函数调用和 Promise 包装，微秒级别。真正可能有性能影响的是 Hook 里的具体逻辑，比如某个插件在 beforeToolCall 里做了一次网络请求做权限校验，那这个延迟是插件自己的问题，不是框架的问题。没注册 Hook 的话，拦截层会直接透传到原始工具函数，几乎零开销。- **提问**：Context 溢出的时候截断 tool result，截断策略是什么？会不会截掉关键信息？
- **回答**：截断策略是动态的。它会先检测 tool result 尾部是否包含错误信息、结果摘要或 JSON 闭合结构。如果尾部重要，采用"头+尾"策略保留首尾、砍掉中间并插入省略标记；如果尾部不重要，只保留头部。截断后会追加说明告诉模型内容被截断了，模型可以决定是否需要重新调用工具分段读取。当然会有丢关键信息的风险，这是工程上的折中，总比直接报错中断对话要好。作者：Yes面试鸭官方
attempt + fallback 容错机制工具调用的双层包装流式处理的 Provider 适配Context 溢出的三级降级

## 答案


attempt + fallback 容错机制Agent Runner 不是跑一次就完事，容错分两层：1）Auth Profile 轮转：如果一次尝试因为 auth 失败、限流或服务过载挂了，Runner 会自动切到同 Provider 的下一个 API Key 重试。比如配了三个 OpenAI Key，第一个被限流就自动换第二个。

2） 模型级 Fallback：如果所有 Key 都轮完还是失败，Runner 向外层抛出 FailoverError，外层的 model-fallback 层会切到配置的备用模型。比如 Claude 整体不可用就降级到 GPT-4o，用户几乎感知不到切换。重试有上限（根据 profile 数量动态计算，范围 32-160 次），不会无限重试。遇到服务过载还会加指数退避，避免继续打爆上游。工具调用的双层包装每个工具在注册时会经过两层包装：1）Hook 拦截层：插件可以在工具执行前异步检查参数、做权限校验，甚至直接阻止执行。这一层还内置了循环检测，防止 LLM 反复调用同一工具陷入死循环。

2） 取消机制层：把外部的 AbortSignal 和工具自带的信号合并。当用户发了新消息、超时了、或手动停止时，正在执行的工具可以被中断，不用干等到超时。流式处理的 Provider 适配Runner 默认用通用的streamSimple做流式输出，但不同 Provider 的流式 API 差异很大，所以会根据 Provider 类型动态替换流式引擎：Ollama：走原生/api/chat直连，绕过通用路径以获得更可靠的 streaming 和工具调用OpenAI：支持 WebSocket 通道，减少 HTTP 开销Google：额外 Gemini 特有的 thinking 字段所有 Provider 还会统一做工具名称规范化（有些模型输出的工具名带空格或前缀），确保工具分发能精确匹配这层适配做完后，执行循环的代码不用管底下是哪家 Provider，调同一个接口就行。新增 Provider 也只需要写一个流式适配函数。Context 溢出的三级降级执行循环跑着跑着 context 可能会超限，特别是工具返回了大量内容的时候。Runner 对此做了三级自动降级：1）先尝试compaction，调用 Context Engine 压缩历史消息，腾出 token 空间2）compaction 还不够的话，截断超大 tool result。截断策略是动态的：先检测尾部是否包含错误信息或结果摘要，如果尾部重要就保留首尾、砍掉中间；否则只保留开头。截断位置会插入说明提示模型内容被截断了。单个 tool result 最多占上下文窗口的 30%3）前两步都救不回来，报错降级，告诉用户 context 太长了，建议开新会话整个过程对用户透明，尽最大努力保证对话能继续下去。

- **提问**：你说排队执行保证并发安全，那如果用户快速连发两条消息会怎样？后面那条是排队等还是直接丢弃？回答：后面那条消息会进入 session 级队列排队等，不会丢弃也不会并发执行。设计上是嵌套两级队列：先进 session 队列（保证同 session 串行），再进全局队列（控制总并发）。等前一条消息的 Agent 运行完成后才处理下一条。用户体验上是第二条消息会等一会儿才开始响应。- **提问**：fallback 机制切换模型之后，之前的对话历史格式兼容吗？不同模型的消息格式不一样怎么办？
- **回答**：历史消息以统一的中间格式存储在 session 文件中。切换模型时用的是同一份 session file，新的 attempt 启动时会根据目标 Provider 的特性做格式适配。比如 Gemini 和 Anthropic 的 turn 交替规则不同、thinking block 处理不同，这些都在 session 历史清洗阶段自动处理。所以 fallback 切换对历史消息是透明的，不需要手动做格式迁移。- **提问**：工具的 Hook 拦截层会不会引入性能问题？每次工具调用都多走两层包装，延迟能接受吗？
- **回答**：两层包装本身的开销可以忽略不计，就是几个函数调用和 Promise 包装，微秒级别。真正可能有性能影响的是 Hook 里的具体逻辑，比如某个插件在 beforeToolCall 里做了一次网络请求做权限校验，那这个延迟是插件自己的问题，不是框架的问题。没注册 Hook 的话，拦截层会直接透传到原始工具函数，几乎零开销。- **提问**：Context 溢出的时候截断 tool result，截断策略是什么？会不会截掉关键信息？
- **回答**：截断策略是动态的。它会先检测 tool result 尾部是否包含错误信息、结果摘要或 JSON 闭合结构。如果尾部重要，采用"头+尾"策略保留首尾、砍掉中间并插入省略标记；如果尾部不重要，只保留头部。截断后会追加说明告诉模型内容被截断了，模型可以决定是否需要重新调用工具分段读取。当然会有丢关键信息的风险，这是工程上的折中，总比直接报错中断对话要好。作者：Yes面试鸭官方
attempt + fallback 容错机制工具调用的双层包装流式处理的 Provider 适配Context 溢出的三级降级

---

> 来源: OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？.mhtml

## 

## 关键点

- # OpenClaw 的 Agent Runner 是如何工作的？
- 一次 Agent 运行经历了哪些阶段？
- ## 问题
OpenClaw 的 Agent Runner 是如何工作的？
- 一次 Agent 运行经历了哪些阶段？
- Agent Runner 是 OpenClaw 的核心调度器，可以理解为"指挥中心"，负责协调 LLM 调用、工具执行、错误处理等所有环节。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？
- ## 标准回答

- ## 问题
OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？Agent Runner 是 OpenClaw 的核心调度器，可以理解为"指挥中心"，负责协调 LLM 调用、工具执行、错误处理等所有环节。一次完整的 Agent 运行从用户发消息到最终输出，大致经历以下阶段：1）排队，先进 session 级队列（保证同一会话串行），再进全局队列（控制总并发），防止资源被打满2）准备，解析 workspace、provider/model、thinking level 等基础参数3）插件 + Hook，加载运行时插件后，触发before_model_resolve和before_agent_start钩子，插件可以在模型解析之前动态覆盖 provider 和 model4）模型解析 + 鉴权，根据（可能被 Hook 修改过的）配置确定模型定义、上下文窗口大小，并按优先级选出可用的 API Key5）尝试执行（核心，可重试）：创建或恢复 Session，加载历史消息注册工具集（统一走 customTools 路径，保证沙箱和策略过滤一致性）根据 Provider 设置流式引擎（Ollama 直连、OpenAI WebSocket、通用 HTTP 等）触发执行循环：LLM 调用 → 工具执行 → 结果回传 → 再调 LLM，直到模型认为任务完成6）溢出降级，如果上下文超限：先 compaction 压缩历史 → 再截断超大 tool result → 都不行就报错引导用户开新会话整个流程的设计思路是每个阶段都可插拔。插件通过 Hook 介入、模型和 Provider 可动态切换、工具集按需组合。

attempt + fallback 容错机制Agent Runner 不是跑一次就完事，容错分两层：1）Auth Profile 轮转：如果一次尝试因为 auth 失败、限流或服务过载挂了，Runner 会自动切到同 Provider 的下一个 API Key 重试。比如配了三个 OpenAI Key，第一个被限流就自动换第二个。

2） 模型级 Fallback：如果所有 Key 都轮完还是失败，Runner 向外层抛出 FailoverError，外层的 model-fallback 层会切到配置的备用模型。比如 Claude 整体不可用就降级到 GPT-4o，用户几乎感知不到切换。重试有上限（根据 profile 数量动态计算，范围 32-160 次），不会无限重试。遇到服务过载还会加指数退避，避免继续打爆上游。工具调用的双层包装每个工具在注册时会经过两层包装：1）Hook 拦截层：插件可以在工具执行前异步检查参数、做权限校验，甚至直接阻止执行。这一层还内置了循环检测，防止 LLM 反复调用同一工具陷入死循环。

2） 取消机制层：把外部的 AbortSignal 和工具自带的信号合并。当用户发了新消息、超时了、或手动停止时，正在执行的工具可以被中断，不用干等到超时。流式处理的 Provider 适配Runner 默认用通用的streamSimple做流式输出，但不同 Provider 的流式 API 差异很大，所以会根据 Provider 类型动态替换流式引擎：Ollama：走原生/api/chat直连，绕过通用路径以获得更可靠的 streaming 和工具调用OpenAI：支持 WebSocket 通道，减少 HTTP 开销Google：额外 Gemini 特有的 thinking 字段所有 Provider 还会统一做工具名称规范化（有些模型输出的工具名带空格或前缀），确保工具分发能精确匹配这层适配做完后，执行循环的代码不用管底下是哪家 Provider，调同一个接口就行。新增 Provider 也只需要写一个流式适配函数。Context 溢出的三级降级执行循环跑着跑着 context 可能会超限，特别是工具返回了大量内容的时候。Runner 对此做了三级自动降级：1）先尝试compaction，调用 Context Engine 压缩历史消息，腾出 token 空间2）compaction 还不够的话，截断超大 tool result。截断策略是动态的：先检测尾部是否包含错误信息或结果摘要，如果尾部重要就保留首尾、砍掉中间；否则只保留开头。截断位置会插入说明提示模型内容被截断了。单个 tool result 最多占上下文窗口的 30%3）前两步都救不回来，报错降级，告诉用户 context 太长了，建议开新会话整个过程对用户透明，尽最大努力保证对话能继续下去。

- **提问**：你说排队执行保证并发安全，那如果用户快速连发两条消息会怎样？后面那条是排队等还是直接丢弃？回答：后面那条消息会进入 session 级队列排队等，不会丢弃也不会并发执行。设计上是嵌套两级队列：先进 session 队列（保证同 session 串行），再进全局队列（控制总并发）。等前一条消息的 Agent 运行完成后才处理下一条。用户体验上是第二条消息会等一会儿才开始响应。- **提问**：fallback 机制切换模型之后，之前的对话历史格式兼容吗？不同模型的消息格式不一样怎么办？
- **回答**：历史消息以统一的中间格式存储在 session 文件中。切换模型时用的是同一份 session file，新的 attempt 启动时会根据目标 Provider 的特性做格式适配。比如 Gemini 和 Anthropic 的 turn 交替规则不同、thinking block 处理不同，这些都在 session 历史清洗阶段自动处理。所以 fallback 切换对历史消息是透明的，不需要手动做格式迁移。- **提问**：工具的 Hook 拦截层会不会引入性能问题？每次工具调用都多走两层包装，延迟能接受吗？
- **回答**：两层包装本身的开销可以忽略不计，就是几个函数调用和 Promise 包装，微秒级别。真正可能有性能影响的是 Hook 里的具体逻辑，比如某个插件在 beforeToolCall 里做了一次网络请求做权限校验，那这个延迟是插件自己的问题，不是框架的问题。没注册 Hook 的话，拦截层会直接透传到原始工具函数，几乎零开销。- **提问**：Context 溢出的时候截断 tool result，截断策略是什么？会不会截掉关键信息？
- **回答**：截断策略是动态的。它会先检测 tool result 尾部是否包含错误信息、结果摘要或 JSON 闭合结构。如果尾部重要，采用"头+尾"策略保留首尾、砍掉中间并插入省略标记；如果尾部不重要，只保留头部。截断后会追加说明告诉模型内容被截断了，模型可以决定是否需要重新调用工具分段读取。当然会有丢关键信息的风险，这是工程上的折中，总比直接报错中断对话要好。作者：Yes面试鸭官方
attempt + fallback 容错机制工具调用的双层包装流式处理的 Provider 适配Context 溢出的三级降级


attempt + fallback 容错机制Agent Runner 不是跑一次就完事，容错分两层：1）Auth Profile 轮转：如果一次尝试因为 auth 失败、限流或服务过载挂了，Runner 会自动切到同 Provider 的下一个 API Key 重试。比如配了三个 OpenAI Key，第一个被限流就自动换第二个。

2） 模型级 Fallback：如果所有 Key 都轮完还是失败，Runner 向外层抛出 FailoverError，外层的 model-fallback 层会切到配置的备用模型。比如 Claude 整体不可用就降级到 GPT-4o，用户几乎感知不到切换。重试有上限（根据 profile 数量动态计算，范围 32-160 次），不会无限重试。遇到服务过载还会加指数退避，避免继续打爆上游。工具调用的双层包装每个工具在注册时会经过两层包装：1）Hook 拦截层：插件可以在工具执行前异步检查参数、做权限校验，甚至直接阻止执行。这一层还内置了循环检测，防止 LLM 反复调用同一工具陷入死循环。

2） 取消机制层：把外部的 AbortSignal 和工具自带的信号合并。当用户发了新消息、超时了、或手动停止时，正在执行的工具可以被中断，不用干等到超时。流式处理的 Provider 适配Runner 默认用通用的streamSimple做流式输出，但不同 Provider 的流式 API 差异很大，所以会根据 Provider 类型动态替换流式引擎：Ollama：走原生/api/chat直连，绕过通用路径以获得更可靠的 streaming 和工具调用OpenAI：支持 WebSocket 通道，减少 HTTP 开销Google：额外 Gemini 特有的 thinking 字段所有 Provider 还会统一做工具名称规范化（有些模型输出的工具名带空格或前缀），确保工具分发能精确匹配这层适配做完后，执行循环的代码不用管底下是哪家 Provider，调同一个接口就行。新增 Provider 也只需要写一个流式适配函数。Context 溢出的三级降级执行循环跑着跑着 context 可能会超限，特别是工具返回了大量内容的时候。Runner 对此做了三级自动降级：1）先尝试compaction，调用 Context Engine 压缩历史消息，腾出 token 空间2）compaction 还不够的话，截断超大 tool result。截断策略是动态的：先检测尾部是否包含错误信息或结果摘要，如果尾部重要就保留首尾、砍掉中间；否则只保留开头。截断位置会插入说明提示模型内容被截断了。单个 tool result 最多占上下文窗口的 30%3）前两步都救不回来，报错降级，告诉用户 context 太长了，建议开新会话整个过程对用户透明，尽最大努力保证对话能继续下去。

- **提问**：你说排队执行保证并发安全，那如果用户快速连发两条消息会怎样？后面那条是排队等还是直接丢弃？回答：后面那条消息会进入 session 级队列排队等，不会丢弃也不会并发执行。设计上是嵌套两级队列：先进 session 队列（保证同 session 串行），再进全局队列（控制总并发）。等前一条消息的 Agent 运行完成后才处理下一条。用户体验上是第二条消息会等一会儿才开始响应。- **提问**：fallback 机制切换模型之后，之前的对话历史格式兼容吗？不同模型的消息格式不一样怎么办？
- **回答**：历史消息以统一的中间格式存储在 session 文件中。切换模型时用的是同一份 session file，新的 attempt 启动时会根据目标 Provider 的特性做格式适配。比如 Gemini 和 Anthropic 的 turn 交替规则不同、thinking block 处理不同，这些都在 session 历史清洗阶段自动处理。所以 fallback 切换对历史消息是透明的，不需要手动做格式迁移。- **提问**：工具的 Hook 拦截层会不会引入性能问题？每次工具调用都多走两层包装，延迟能接受吗？
- **回答**：两层包装本身的开销可以忽略不计，就是几个函数调用和 Promise 包装，微秒级别。真正可能有性能影响的是 Hook 里的具体逻辑，比如某个插件在 beforeToolCall 里做了一次网络请求做权限校验，那这个延迟是插件自己的问题，不是框架的问题。没注册 Hook 的话，拦截层会直接透传到原始工具函数，几乎零开销。- **提问**：Context 溢出的时候截断 tool result，截断策略是什么？会不会截掉关键信息？
- **回答**：截断策略是动态的。它会先检测 tool result 尾部是否包含错误信息、结果摘要或 JSON 闭合结构。如果尾部重要，采用"头+尾"策略保留首尾、砍掉中间并插入省略标记；如果尾部不重要，只保留头部。截断后会追加说明告诉模型内容被截断了，模型可以决定是否需要重新调用工具分段读取。当然会有丢关键信息的风险，这是工程上的折中，总比直接报错中断对话要好。作者：Yes面试鸭官方
attempt + fallback 容错机制工具调用的双层包装流式处理的 Provider 适配Context 溢出的三级降级

---

> 来源: OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？.mhtml

- # OpenClaw 的 Agent Runner 是如何工作的？
- - 一次 Agent 运行经历了哪些阶段？
- - ## 问题
OpenClaw 的 Agent Runner 是如何工作的？

- 本文已做格式统一与噪声清理，保留原始语义。
- OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？
- # OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？
- 13228. OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？Agent Runner 是 OpenClaw 的核心调度器，可以理解为"指挥中心"，负责协调 LLM 调用、工具执行、错误处理等所有环节。一次完整的 Agent 运行从用户发消息到最终输出，大致经历以下阶段：1）排队，先进 session 级队列（保证同一会话串行），再进全局队列（控制总并发），防止资源被打满2）准备，解析 workspace、provider/model、thinking level 等基础参数3）插件 + Hook，加载运行时插件后，触发before_model_resolve和before_agent_start钩子，插件可以在模型解析之前动态覆盖 provider 和 model4）模型解析 + 鉴权，根据（可能被 Hook 修改过的）配置确定模型定义、上下文窗口大小，并按优先级选出可用的 API Key5）尝试执行（核心，可重试）：创建或恢复 Session，加载历史消息注册工具集（统一走 customTools 路径，保证沙箱和策略过滤一致性）根据 Provider 设置流式引擎（Ollama 直连、OpenAI WebSocket、通用 HTTP 等）触发执行循环：LLM 调用 → 工具执行 → 结果回传 → 再调 LLM，直到模型认为任务完成6）溢出降级，如果上下文超限：先 compaction 压缩历史 → 再截断超大 tool result → 都不行就报错引导用户开新会话整个流程的设计思路是每个阶段都可插拔。插件通过 Hook 介入、模型和 Provider 可动态切换、工具集按需组合。

attempt + fallback 容错机制Agent Runner 不是跑一次就完事，容错分两层：1）Auth Profile 轮转：如果一次尝试因为 auth 失败、限流或服务过载挂了，Runner 会自动切到同 Provider 的下一个 API Key 重试。比如配了三个 OpenAI Key，第一个被限流就自动换第二个。

2） 模型级 Fallback：如果所有 Key 都轮完还是失败，Runner 向外层抛出 FailoverError，外层的 model-fallback 层会切到配置的备用模型。比如 Claude 整体不可用就降级到 GPT-4o，用户几乎感知不到切换。重试有上限（根据 profile 数量动态计算，范围 32-160 次），不会无限重试。遇到服务过载还会加指数退避，避免继续打爆上游。工具调用的双层包装每个工具在注册时会经过两层包装：1）Hook 拦截层：插件可以在工具执行前异步检查参数、做权限校验，甚至直接阻止执行。这一层还内置了循环检测，防止 LLM 反复调用同一工具陷入死循环。

2） 取消机制层：把外部的 AbortSignal 和工具自带的信号合并。当用户发了新消息、超时了、或手动停止时，正在执行的工具可以被中断，不用干等到超时。流式处理的 Provider 适配Runner 默认用通用的streamSimple做流式输出，但不同 Provider 的流式 API 差异很大，所以会根据 Provider 类型动态替换流式引擎：Ollama：走原生/api/chat直连，绕过通用路径以获得更可靠的 streaming 和工具调用OpenAI：支持 WebSocket 通道，减少 HTTP 开销Google：额外 Gemini 特有的 thinking 字段所有 Provider 还会统一做工具名称规范化（有些模型输出的工具名带空格或前缀），确保工具分发能精确匹配这层适配做完后，执行循环的代码不用管底下是哪家 Provider，调同一个接口就行。新增 Provider 也只需要写一个流式适配函数。Context 溢出的三级降级执行循环跑着跑着 context 可能会超限，特别是工具返回了大量内容的时候。Runner 对此做了三级自动降级：1）先尝试compaction，调用 Context Engine 压缩历史消息，腾出 token 空间2）compaction 还不够的话，截断超大 tool result。截断策略是动态的：先检测尾部是否包含错误信息或结果摘要，如果尾部重要就保留首尾、砍掉中间；否则只保留开头。截断位置会插入说明提示模型内容被截断了。单个 tool result 最多占上下文窗口的 30%3）前两步都救不回来，报错降级，告诉用户 context 太长了，建议开新会话整个过程对用户透明，尽最大努力保证对话能继续下去。

- **提问**：你说排队执行保证并发安全，那如果用户快速连发两条消息会怎样？后面那条是排队等还是直接丢弃？回答：后面那条消息会进入 session 级队列排队等，不会丢弃也不会并发执行。设计上是嵌套两级队列：先进 session 队列（保证同 session 串行），再进全局队列（控制总并发）。等前一条消息的 Agent 运行完成后才处理下一条。用户体验上是第二条消息会等一会儿才开始响应。- **提问**：fallback 机制切换模型之后，之前的对话历史格式兼容吗？不同模型的消息格式不一样怎么办？
- **回答**：历史消息以统一的中间格式存储在 session 文件中。切换模型时用的是同一份 session file，新的 attempt 启动时会根据目标 Provider 的特性做格式适配。比如 Gemini 和 Anthropic 的 turn 交替规则不同、thinking block 处理不同，这些都在 session 历史清洗阶段自动处理。所以 fallback 切换对历史消息是透明的，不需要手动做格式迁移。- **提问**：工具的 Hook 拦截层会不会引入性能问题？每次工具调用都多走两层包装，延迟能接受吗？
- **回答**：两层包装本身的开销可以忽略不计，就是几个函数调用和 Promise 包装，微秒级别。真正可能有性能影响的是 Hook 里的具体逻辑，比如某个插件在 beforeToolCall 里做了一次网络请求做权限校验，那这个延迟是插件自己的问题，不是框架的问题。没注册 Hook 的话，拦截层会直接透传到原始工具函数，几乎零开销。- **提问**：Context 溢出的时候截断 tool result，截断策略是什么？会不会截掉关键信息？
attempt + fallback 容错机制工具调用的双层包装流式处理的 Provider 适配Context 溢出的三级降级


attempt + fallback 容错机制Agent Runner 不是跑一次就完事，容错分两层：1）Auth Profile 轮转：如果一次尝试因为 auth 失败、限流或服务过载挂了，Runner 会自动切到同 Provider 的下一个 API Key 重试。比如配了三个 OpenAI Key，第一个被限流就自动换第二个。

2） 模型级 Fallback：如果所有 Key 都轮完还是失败，Runner 向外层抛出 FailoverError，外层的 model-fallback 层会切到配置的备用模型。比如 Claude 整体不可用就降级到 GPT-4o，用户几乎感知不到切换。重试有上限（根据 profile 数量动态计算，范围 32-160 次），不会无限重试。遇到服务过载还会加指数退避，避免继续打爆上游。工具调用的双层包装每个工具在注册时会经过两层包装：1）Hook 拦截层：插件可以在工具执行前异步检查参数、做权限校验，甚至直接阻止执行。这一层还内置了循环检测，防止 LLM 反复调用同一工具陷入死循环。

2） 取消机制层：把外部的 AbortSignal 和工具自带的信号合并。当用户发了新消息、超时了、或手动停止时，正在执行的工具可以被中断，不用干等到超时。流式处理的 Provider 适配Runner 默认用通用的streamSimple做流式输出，但不同 Provider 的流式 API 差异很大，所以会根据 Provider 类型动态替换流式引擎：Ollama：走原生/api/chat直连，绕过通用路径以获得更可靠的 streaming 和工具调用OpenAI：支持 WebSocket 通道，减少 HTTP 开销Google：额外 Gemini 特有的 thinking 字段所有 Provider 还会统一做工具名称规范化（有些模型输出的工具名带空格或前缀），确保工具分发能精确匹配这层适配做完后，执行循环的代码不用管底下是哪家 Provider，调同一个接口就行。新增 Provider 也只需要写一个流式适配函数。Context 溢出的三级降级执行循环跑着跑着 context 可能会超限，特别是工具返回了大量内容的时候。Runner 对此做了三级自动降级：1）先尝试compaction，调用 Context Engine 压缩历史消息，腾出 token 空间2）compaction 还不够的话，截断超大 tool result。截断策略是动态的：先检测尾部是否包含错误信息或结果摘要，如果尾部重要就保留首尾、砍掉中间；否则只保留开头。截断位置会插入说明提示模型内容被截断了。单个 tool result 最多占上下文窗口的 30%3）前两步都救不回来，报错降级，告诉用户 context 太长了，建议开新会话整个过程对用户透明，尽最大努力保证对话能继续下去。

- **提问**：你说排队执行保证并发安全，那如果用户快速连发两条消息会怎样？后面那条是排队等还是直接丢弃？回答：后面那条消息会进入 session 级队列排队等，不会丢弃也不会并发执行。设计上是嵌套两级队列：先进 session 队列（保证同 session 串行），再进全局队列（控制总并发）。等前一条消息的 Agent 运行完成后才处理下一条。用户体验上是第二条消息会等一会儿才开始响应。- **提问**：fallback 机制切换模型之后，之前的对话历史格式兼容吗？不同模型的消息格式不一样怎么办？
- **回答**：历史消息以统一的中间格式存储在 session 文件中。切换模型时用的是同一份 session file，新的 attempt 启动时会根据目标 Provider 的特性做格式适配。比如 Gemini 和 Anthropic 的 turn 交替规则不同、thinking block 处理不同，这些都在 session 历史清洗阶段自动处理。所以 fallback 切换对历史消息是透明的，不需要手动做格式迁移。- **提问**：工具的 Hook 拦截层会不会引入性能问题？每次工具调用都多走两层包装，延迟能接受吗？
- **回答**：两层包装本身的开销可以忽略不计，就是几个函数调用和 Promise 包装，微秒级别。真正可能有性能影响的是 Hook 里的具体逻辑，比如某个插件在 beforeToolCall 里做了一次网络请求做权限校验，那这个延迟是插件自己的问题，不是框架的问题。没注册 Hook 的话，拦截层会直接透传到原始工具函数，几乎零开销。- **提问**：Context 溢出的时候截断 tool result，截断策略是什么？会不会截掉关键信息？
- **回答**：截断策略是动态的。它会先检测 tool result 尾部是否包含错误信息、结果摘要或 JSON 闭合结构。如果尾部重要，采用"头+尾"策略保留首尾、砍掉中间并插入省略标记；如果尾部不重要，只保留头部。截断后会追加说明告诉模型内容被截断了，模型可以决定是否需要重新调用工具分段读取。当然会有丢关键信息的风险，这是工程上的折中，总比直接报错中断对话要好。作者：Yes面试鸭官方
- 本文已做格式统一与噪声清理，保留原始语义。
