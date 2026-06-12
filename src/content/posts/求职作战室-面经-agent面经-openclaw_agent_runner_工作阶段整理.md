---
title: "OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？"
published: 2026-06-12
description: "Agent Runner 是 OpenClaw 的核心调度器（指挥中心），负责协调 LLM 调用、工具执行、错误处理等所有环节。一次完整的 Agent 运行（从用户发消息到最终输出）大致经历以下 6 个阶段： 1. 排队 先进 session 级队列（保证同一会话串行），再进全局队列（控制总并发），防止资源被打满。 2. 准备 解析 workspace、provider/model、thinkin..."
category: "求职作战室"
tags: ["\u6c42\u804c\u4f5c\u6218\u5ba4", "\u9762\u7ecf"]
draft: false
lang: zh-CN
---
# OpenClaw 的 Agent Runner 是如何工作的？一次 Agent 运行经历了哪些阶段？

## 核心回答

Agent Runner 是 OpenClaw 的核心调度器（指挥中心），负责协调 LLM 调用、工具执行、错误处理等所有环节。一次完整的 Agent 运行（从用户发消息到最终输出）大致经历以下 6 个阶段：

1. **排队**  
   先进 session 级队列（保证同一会话串行），再进全局队列（控制总并发），防止资源被打满。

2. **准备**  
   解析 workspace、provider/model、thinking level 等基础参数。

3. **插件 + Hook**  
   加载运行时插件后，触发 `before_model_resolve` 和 `before_agent_start` 钩子。插件可以在模型解析之前动态覆盖 provider 和 model。

4. **模型解析 + 鉴权**  
   根据（可能被 Hook 修改过的）配置确定模型定义、上下文窗口大小，并按优先级选出可用的 API Key。

5. **尝试执行（核心，可重试）**  
   - 创建或恢复 Session，加载历史消息。
   - 注册工具集（统一走 customTools 路径，保证沙箱和策略过滤一致性）。
   - 根据 Provider 设置流式引擎（Ollama 直连、OpenAI WebSocket、通用 HTTP 等）。
   - 触发执行循环：**LLM 调用 → 工具执行 → 结果回传 → 再调 LLM**，直到模型认为任务完成。

6. **溢出降级**  
   如果上下文超限：
   - 先 compaction 压缩历史；
   - 再截断超大 tool result；
   - 都不行就报错并引导用户开新会话。

整个流程的设计思路是**每个阶段都可插拔**：插件通过 Hook 介入、模型和 Provider 可动态切换、工具集按需组合。

---

## 扩展知识

### 1. attempt + fallback 容错机制

Agent Runner 不是跑一次就完事，容错分两层：

- **Auth Profile 轮转**：如果一次尝试因为 auth 失败、限流或服务过载挂了，Runner 会自动切到同 Provider 的下一个 API Key 重试。
- **模型级 Fallback**：如果所有 Key 都轮完还是失败，Runner 向外层抛出 FailoverError，外层的 model-fallback 层会切到配置的备用模型。

重试有上限（根据 profile 数量动态计算，范围 32-160 次），不会无限重试。遇到服务过载还会加指数退避，避免继续打爆上游。

### 2. 工具调用的双层包装

每个工具在注册时会经过两层包装：

- **Hook 拦截层**：插件可以在工具执行前异步检查参数、做权限校验，甚至直接阻止执行。还内置了循环检测，防止 LLM 反复调用同一工具陷入死循环。
- **取消机制层**：把外部的 AbortSignal 和工具自带的信号合并。当用户发了新消息、超时或手动停止时，正在执行的工具可以被中断。

### 3. 流式处理的 Provider 适配

Runner 默认用通用的 `streamSimple` 做流式输出，但不同 Provider 的流式 API 差异很大，因此会根据 Provider 类型动态替换流式引擎：

- **Ollama**：走原生 `/api/chat` 直连，绕过通用路径以获得更可靠的 streaming 和工具调用。
- **OpenAI**：支持 WebSocket 通道，减少 HTTP 开销。
- **Google**：额外 Gemini 特有的 thinking 字段。

所有 Provider 还会统一做工具名称规范化，确保工具分发能精确匹配。这层适配做完后，执行循环的代码不用管底下是哪家 Provider，调同一个接口即可。新增 Provider 也只需要写一个流式适配函数。

### 4. Context 溢出的三级降级

执行循环中 context 可能超限，Runner 做了三级自动降级：

1. **compaction**：调用 Context Engine 压缩历史消息，腾出 token 空间。
2. **截断超大 tool result**：动态策略——先检测尾部是否包含错误信息或结果摘要；如果尾部重要则保留首尾、砍掉中间并插入省略标记，否则只保留开头。单个 tool result 最多占上下文窗口的 30%。
3. **报错降级**：前两步都救不回来时，告诉用户 context 太长了，建议开新会话。

整个过程对用户透明，尽最大努力保证对话能继续下去。

---

## 面试官追问（常见问题）

**Q1：排队执行保证并发安全，如果用户快速连发两条消息会怎样？后面那条是排队等还是直接丢弃？**  
A：后面那条消息会进入 session 级队列排队等待，不会丢弃也不会并发执行。设计上是嵌套两级队列：先进 session 队列（保证同 session 串行），再进全局队列（控制总并发）。等前一条消息的 Agent 运行完成后才处理下一条。用户体验上是第二条消息会等一会儿才开始响应。

**Q2：fallback 机制切换模型之后，之前的对话历史格式兼容吗？不同模型的消息格式不一样怎么办？**  
A：历史消息以统一的中间格式存储在 session 文件中。切换模型时用的是同一份 session file，新的 attempt 启动时会根据目标 Provider 的特性做格式适配（例如 Gemini 和 Anthropic 的 turn 交替规则不同、thinking block 处理不同）。这些都在 session 历史清洗阶段自动处理，fallback 切换对历史消息透明，不需要手动做格式迁移。

**Q3：工具的 Hook 拦截层会不会引入性能问题？每次工具调用都多走两层包装，延迟能接受吗？**  
A：两层包装本身的开销可以忽略不计（几个函数调用和 Promise 包装，微秒级别）。真正可能有性能影响的是 Hook 里的具体逻辑（例如某个插件在 beforeToolCall 里做了一次网络请求做权限校验），那是插件自己的问题，不是框架的问题。没注册 Hook 的话，拦截层会直接透传到原始工具函数，几乎零开销。

**Q4：Context 溢出的时候截断 tool result，截断策略是什么？会不会截掉关键信息？**  
A：截断策略是动态的。它会先检测 tool result 尾部是否包含错误信息、结果摘要或 JSON 闭合结构。如果尾部重要，采用“头+尾”策略保留首尾、砍掉中间并插入省略标记；如果尾部不重要，只保留头部。截断后会追加说明，提示模型内容被截断了，模型可以决定是否需要重新调用工具分段读取。当然会有丢失关键信息的风险，这是工程上的折中，总比直接报错中断对话要好。