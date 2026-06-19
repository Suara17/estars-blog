---
title: 'ReAct_模式构建自主规划智能体'
published: 2026-06-19
description: 'ReAct模式构建自主规划智能体'
category: '求职作战室'
tags: ['求职作战室', '知识点提炼']
draft: false
lang: zh-CN
---# ReAct_模式构建自主规划智能体
## 问题
ReAct_模式构建自主规划智能体

## 标准回答

# 什么是 ReAct？
如何基于 ReAct 模式构建具备自主规划能力的 AI 智能体？

**ReAct（Reasoning + Acting）** 是一种让大语言模型交替进行推理和行动的 Prompt 范式。模型在每一步先“思考”（Reasoning），然后“行动”（Acting），再根据观察结果（Observation）继续思考，形成闭环。这使得 AI 能主动调用工具、获取外部信息，并动态调整计划。

**基于 ReAct 构建自主规划 Agent 的关键步骤**：
**定义工具集**：提供模型可调用的外部函数（如搜索、计算器、API）。
**设计 Prompt 格式**：明确要求模型输出 `Thought:`（推理）、`Action:`（行动）、`Observation:`（观察）的结构。
**解析与执行**：应用层解析 `Action:` 字段，执行对应工具，将结果填入 `Observation:`。
**循环迭代**：重复上述过程，直到模型输出 `Final Answer:`。

**示例 Prompt 结构**：
```
你是一个能使用工具的智能体。你有以下工具：
- search(query): 搜索互联网
- calculate(expression): 计算数学表达式

请按以下格式回答：
Thought: 你的思考过程
Action: 工具名称(参数)
Observation: 工具返回结果
...（重复）
Final Answer: 最终答案
```

---

## 扩展知识

### 1. ReAct 与 CoT 的区别
- **CoT（Chain of Thought）**：仅推理，不执行动作，适合数学逻辑题。
- **ReAct**：推理 + 行动，通过外部反馈修正推理，适合需要实时信息或工具操作的任务。

### 2. 常见框架实现
- **LangChain**：`AgentExecutor` + `ReActDocstoreAgent`。
- **Spring AI**：`ChatClient` + `@Tool` 注解 + `Advisor` 自定义输出解析。
- **AutoGen**：多 Agent 协作中的 ReAct 模式。

### 3. 优化技巧
- **限制最大循环次数**：防止死循环。
- **错误恢复**：当工具调用失败时，将错误信息作为 `Observation` 让模型自己修正。
- **思维链压缩**：对历史 `Thought` 进行摘要，避免上下文超限。

---

## 面试官追问

### Q1：ReAct 模式会显著增加 token 消耗，如何优化？
**A**：① 使用更精简的 Prompt 模板（如只要求输出 `Action` 和 `Observation`，隐藏 `Thought`）。② 对历史观察结果进行摘要。③ 设置最大循环次数，及时终止。

### Q2：ReAct 与 Plan-and-Solve 模式有何不同？
**A**：ReAct 是逐步决策，每次根据最新观察调整下一步；Plan-and-Solve 先生成完整计划再执行，灵活性较低，但 token 消耗更少。

### Q3：如何防止模型在 ReAct 中编造不存在的工具？
**A**：在 System Prompt 中明确列出可用工具，并强调“只能使用上述工具，不要编造”。应用层严格校验 `Action` 字段，只执行白名单内的工具。

---

## 总结

ReAct 让 LLM 具备自主规划与工具使用能力，是构建智能 Agent 的核心模式之一。通过结构化的 Thought-Action-Observation 循环，模型能动态适应环境变化，解决复杂任务。实现时需注意工具集设计、循环控制与错误处理。

## 

## 关键点

- # 什么是 ReAct？
- 如何基于 ReAct 模式构建具备自主规划能力的 AI 智能体？
- ## 核心回答

**ReAct（Reasoning + Acting）** 是一种让大语言模型交替进行推理和行动的 Prompt 范式。
- 模型在每一步先“思考”（Reasoning），然后“行动”（Acting），再根据观察结果（Observation）继续思考，形成闭环。
- 这使得 AI 能主动调用工具、获取外部信息，并动态调整计划。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

ReAct_模式构建自主规划智能体

# 什么是 ReAct？如何基于 ReAct 模式构建具备自主规划能力的 AI 智能体？
- ## 核心回答

**ReAct（Reasoning + Acting）** 是一种让大语言模型交替进行推理和行动的 Prompt 范式。模型在每一步先“思考”（Reasoning），然后“行动”（Acting），再根据观察结果（Observation）继续思考，形成闭环。这使得 AI 能主动调用工具、获取外部信息，并动态调整计划。
- **基于 ReAct 构建自主规划 Agent 的关键步骤**：
**定义工具集**：提供模型可调用的外部函数（如搜索、计算器、API）。
- 2. **设计 Prompt 格式**：明确要求模型输出 `Thought:`（推理）、`Action:`（行动）、`Observation:`（观察）的结构。
- 3. **解析与执行**：应用层解析 `Action:` 字段，执行对应工具，将结果填入 `Observation:`。

- 本文已做格式统一与噪声清理，保留原始语义。
- 如何基于 ReAct 模式构建具备自主规划能力的 AI 智能体？
- **ReAct（Reasoning + Acting）** 是一种让大语言模型交替进行推理和行动的 Prompt 范式。模型在每一步先“思考”（Reasoning），然后“行动”（Acting），再根据观察结果（Observation）继续思考，形成闭环。这使得 AI 能主动调用工具、获取外部信息，并动态调整计划。
- **基于 ReAct 构建自主规划 Agent 的关键步骤**：
- 1. **定义工具集**：提供模型可调用的外部函数（如搜索、计算器、API）。
- 2. **设计 Prompt 格式**：明确要求模型输出 `Thought:`（推理）、`Action:`（行动）、`Observation:`（观察）的结构。

- 本文已做格式统一与噪声清理，保留原始语义。