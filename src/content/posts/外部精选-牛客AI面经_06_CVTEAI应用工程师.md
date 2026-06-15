---
title: '🖥️ CVTE AI 应用工程师 面经'
published: 2026-06-15
description: 'title: 牛客AI面经06CVTEAI应用工程师'
category: '外部精选'
tags: ['外部精选', '牛客AI面经']
draft: false
lang: zh-CN
---
---
title: "牛客AI面经_06_CVTEAI应用工程师"
created: 2025-05-15
source: "牛客网（搜索结果页摘要）"
author: "在写文章的她很伟大"
tags: [面经, CVTE, AI应用工程师, MCP, Skill, LangGraph, E2B, 合成数据]
---

# 🖥️ CVTE AI 应用工程师 面经

> **作者**：在写文章的她很伟大  
> **发布**：2025-05-14 15:28  
> **来源**：牛客网（搜索结果页摘要，全文因登录限制不可访问）  
> **备注**：26 道题，纯血 AI 应用工程化方向，涵盖 MCP/Skill/E2B/LangGraph 等前沿技术

## 📋 面试题目

### 一面（约 1h，16 题）

**项目引入（4题）**
1. 自我介绍
2. 为什么选择做这两个项目？
3. 项目为什么选择 **E2B 沙箱**？选型的理由是什么？E2B 相比其他方案的优点？
4. 和其他沙箱方案（如 Docker、gVisor、Firecracker）对比，E2B 在 AI Agent 场景下的独特优势？

**AI Agent 核心组件（7题）**
5. **MCP（Model Context Protocol）** 是什么？你在项目中是怎么用的？它解决了什么问题？
6. **Skill 机制**：你实现的 Skill 机制是如何设计注册和调度流程的？Skill 和普通函数调用有什么区别？
7. **LangGraph 架构**：为什么选用 LangGraph？它的 StateGraph 和 MessageGraph 的适用场景分别是什么？
8. **短期记忆实现**：LangGraph 中你是怎么用 **SQLite Checkpointer** 实现短期记忆管理的？
9. **长期记忆机制**：除了短期记忆，长期记忆是怎么落地的？有借鉴 **OpenClaw 的记忆机制**吗？
10. **工具调用（Function Calling）**：你是如何设计和约束模型的工具调用的？当模型选错工具时怎么 fallback？
11. **Program-of-Thought（PoT）**：你提到用代码来解决逻辑问题，PoT 和 CoT 在什么场景下各有优势？

**合成数据与评测（3题）**
12. **Synthetic Data（合成数据）**：你是如何构建合成数据的？为什么要用合成数据而不用真实数据？
13. **Harness Engineering**：你理解的 Harness Engineering 是什么？在 AI Agent 开发中扮演什么角色？
14. **Prompt 调优**：你在项目中是怎么做 Prompt 调优的？有没有形成一套方法论或评估指标？

**基础理论知识（2题）**
15. **Transformer 基础**：你能讲讲 Transformer 的结构吗？Self-Attention 的时间复杂度是多少？为什么是 O(n²)？
16. **大模型幻觉**：大模型产生幻觉的原因是什么？从模型结构层面和训练数据层面分别分析？

### 二面（约 40min，10 题）

**职业规划与视野（5题）**
17. 职业规划是什么？五年内你希望达到什么状态？
18. 你是如何跟踪 AI 前沿技术的？推荐几个你常看的博客/论文来源。
19. 聊聊最近在读的一篇印象深刻论文？它的启发是什么？
20. 对于 Agent 的未来发展方向，你是怎么判断的？
21. 你觉得作为一个 AI 应用工程师，最核心的能力是什么？

**技术深度挖掘（5题）**
22. **MCP vs Function Calling**：觉得 MCP 和 OpenAI Function Calling 是一回事吗？本质区别在哪？
23. **Agent 的自主性边界**：你设计的 Agent 可以自主到什么程度？哪些步骤需要人工介入？
24. **安全性考虑**：如果 Agent 可以执行代码和操作外部系统，怎么保证安全性？沙箱逃逸如何防范？
25. **模型选型思考**：你们团队在项目中为什么选择了现在的模型？如果换一个更小的模型，对你的架构设计有什么影响？
26. **Scaling Law 在 Agent 中的体现**：大模型的 Scaling Law 在 Agent 场景下还成立吗？Agent 是否越大越好？

## 📊 知识点图谱

| 领域 | 知识点 | 重要度 |
|:---:|---|:---:|
| Agent 协议 | MCP / Skill 注册调度 / Function Calling | ⭐⭐⭐⭐⭐ |
| 沙箱与安全 | E2B 选型 / 沙箱逃逸 / 多方案对比 | ⭐⭐⭐⭐⭐ |
| Agent 框架 | LangGraph / StateGraph / Checkpointer | ⭐⭐⭐⭐ |
| 记忆机制 | SQLite 短期记忆 / OpenClaw 长期记忆 | ⭐⭐⭐⭐ |
| 数据工程 | 合成数据构建 / Harness Engineering | ⭐⭐⭐⭐ |
| 基础理论 | Transformer / Self-Attention / 幻觉成因 | ⭐⭐⭐ |
| 工程视野 | 模型选型 / Scaling Law / 安全性 | ⭐⭐⭐⭐ |
| 软素质 | 职业规划 / 技术跟踪 / 论文阅读 | ⭐⭐⭐ |

> 💡 **一句话总结**：纯正的 AI 应用工程化面经，从 MCP/Skill 到 E2B/LangGraph 再到合成数据，全面覆盖当前 Agent 开发最前沿技术栈。
