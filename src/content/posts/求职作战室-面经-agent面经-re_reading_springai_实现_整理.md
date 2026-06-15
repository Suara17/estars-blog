---
title: 'Re_Reading_SpringAI_实现'
published: 2026-06-15
description: 'ReReadingSpringAI实现'
category: '求职作战室'
tags: ['求职作战室', '面经']
draft: false
lang: zh-CN
---# Re_Reading_SpringAI_实现
## 问题
Re_Reading_SpringAI_实现

## 标准回答

# 什么是 Re-Reading？
如何基于 Spring AI 实现 Re-Reading Advisor？

Re-Reading（重读），也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术。核心思想是：对于复杂问题，重复阅读和审视问题有助于模型更好地理解题意和约束，从而生成更准确、更深入的回答。有文献研究证明这是有一定效果的。

**注意**：这种方法会因重复处理输入导致成本加倍，在面向 C 端开放的应用中需谨慎使用。

**基于 Spring AI 的实现步骤**：
**创建自定义 Advisor 类**：该类需同时实现 `CallAroundAdvisor`（同步请求）和 `StreamAroundAdvisor`（流式请求）接口，让该类更通用。
*（在 Spring AI 1.0 版本中，上述两个接口需改为 `CallAdvisor` 和 `StreamAdvisor`）*
**修改用户提示词**：在 Advisor 的前置处理逻辑中（如 `aroundCall` 或 `aroundStream` 方法调用之前），对用户的原始输入文本进行改写。改写的格式通常是将原始输入重复一遍，并用明确的指令引导模型重新阅读。通过看源码能够看到提示词格式：
```
{Input_Query}
Read the question again: {Input_Query}
```
其中 `{Input_Query}` 是用户原始的提问内容。
**传递给模型**：将改写后的提示词传递给大语言模型进行处理。

---

## 扩展知识

### 1. Re-Reading 的适用场景
- **复杂推理题**：数学、逻辑、多步骤任务
- **长指令遵循**：包含多个约束条件的任务
- **易产生歧义的问题**：通过重读可消除理解偏差

### 2. 成本与收益权衡
- **成本**：每次请求 token 消耗翻倍（输入翻倍，输出不变）
- **收益**：准确率提升 5-15%（取决于模型和任务复杂度）
- **决策**：对高价值任务（如医疗、金融）可接受；对高并发 C 端场景需谨慎

### 3. 与类似技术的对比
| 技术 | 原理 | 成本 | 适用场景 |
|------|------|------|----------|
| Re-Reading | 重复输入 + 明确指令 | token ×2 | 复杂推理 |
| Chain-of-Thought | 中间推理步骤 | 输出长 | 数学/逻辑题 |
| Self-Consistency | 多次采样投票 | token ×N | 高准确率要求 |
| ReAct | 推理+行动循环 | 多次 LLM 调用 | Agent 任务 |

---

## 面试官追问

### Q1：Re-Reading 和简单的“再说一遍”有什么区别？
**A**：Re-Reading 不是让用户重复输入，而是在系统层面用明确指令（如“Read the question again:”）引导模型重新审视问题。这种结构化重复比自然语言重复更有效，且可封装为 Advisor 自动应用。

### Q2：如果模型本身足够强大（如 GPT-4），Re-Reading 还有用吗？
**A**：有用，但提升幅度较小。研究表明，对复杂推理任务，即使 SOTA 模型也能从 Re-Reading 中获益（3-8% 准确率提升）。对小模型（7B-13B）效果更显著。

### Q3：如何避免 Re-Reading 带来的重复计费问题？
**A**：
- **选择性启用**：仅对高复杂度任务启用（如通过分类器判断是否需要）
- **Prompt 缓存**：利用 LLM 提供商的 prompt 缓存功能（如 Anthropic、DeepSeek），相同前缀可降低成本
- **模型筛选**：对简单的日常问答跳过 Re-Reading

### Q4：Spring AI 的 Advisor 链中，Re-Reading Advisor 应该放在什么位置？
**A**：建议放在**早期**，在参数验证、日志等基础 Advisor 之后，但在 RAG 检索、工具调用等业务 Advisor 之前。因为 Re-Reading 仅修改用户输入，不依赖外部数据，提前处理可让后续 Advisor 基于增强后的输入工作。

---

## 总结

Re-Reading 是一种简单有效的提示工程技巧，通过结构化重复输入提升模型推理准确率。在 Spring AI 中，实现自定义 Advisor 即可无缝集成。需根据任务复杂度和成本敏感性决定是否启用。

## 

## 关键点

- # 什么是 Re-Reading？
- 如何基于 Spring AI 实现 Re-Reading Advisor？
- ## 核心回答

Re-Reading（重读），也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术。
- 核心思想是：对于复杂问题，重复阅读和审视问题有助于模型更好地理解题意和约束，从而生成更准确、更深入的回答。
- 有文献研究证明这是有一定效果的。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

Re_Reading_SpringAI_实现

# 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？
- ## 核心回答

Re-Reading（重读），也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术。核心思想是：对于复杂问题，重复阅读和审视问题有助于模型更好地理解题意和约束，从而生成更准确、更深入的回答。有文献研究证明这是有一定效果的。
- **注意**：这种方法会因重复处理输入导致成本加倍，在面向 C 端开放的应用中需谨慎使用。
- **基于 Spring AI 的实现步骤**：
**创建自定义 Advisor 类**：该类需同时实现 `CallAroundAdvisor`（同步请求）和 `StreamAroundAdvisor`（流式请求）接口，让该类更通用。
- *（在 Spring AI 1.0 版本中，上述两个接口需改为 `CallAdvisor` 和 `StreamAdvisor`）*
**修改用户提示词**：在 Advisor 的前置处理逻辑中（如 `aroundCall` 或 `aroundStream` 方法调用之前），对用户的原始输入文本进行改写。改写的格式通常是将原始输入重复一遍，并用明确的指令引导模型重新阅读。通过看源码能够看到提示词格式：
```
{Input_Query}
Read the question again: {Input_Query}
```
其中 `{Input_Query}` 是用户原始的提问内容。

- 本文已做格式统一与噪声清理，保留原始语义。
- 如何基于 Spring AI 实现 Re-Reading Advisor？
- Re-Reading（重读），也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术。核心思想是：对于复杂问题，重复阅读和审视问题有助于模型更好地理解题意和约束，从而生成更准确、更深入的回答。有文献研究证明这是有一定效果的。
- **注意**：这种方法会因重复处理输入导致成本加倍，在面向 C 端开放的应用中需谨慎使用。
- **基于 Spring AI 的实现步骤**：
- 1. **创建自定义 Advisor 类**：该类需同时实现 `CallAroundAdvisor`（同步请求）和 `StreamAroundAdvisor`（流式请求）接口，让该类更通用。

- 本文已做格式统一与噪声清理，保留原始语义。