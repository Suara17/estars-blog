---
title: 'Loop Engineering ，新词登基，提示词工程下线。'
published: 2026-06-26
description: '作者：雨飞'
category: '经验贴'
tags: ['经验贴']
draft: false
lang: zh-CN
---# Loop Engineering ，新词登基，提示词工程下线。

**作者**：雨飞  
**来源**：雨飞AI笔记  
**日期**：2026年6月16日 19:47  
**原文链接**：https://mp.weixin.qq.com/s/F54MefnbF3wSN76xNsA-Eg

---

你好啊，我是雨飞，见字如面。感谢阅读，期待我们下一次的相遇。

短短数月，AI圈又来说造新词了，这次是 Loop Engineering，上次被宣布死亡的还是 Context Engineering。

最近谷歌云AI总监 Addy 的长文 Loop Engineering 则有开创了这一个新的词汇，这个所谓的新词和之前的又有何区别，一文给你讲清楚。

在了解所谓的XX Engineering 之前，我们先要了解下相关的背景，最一开始的时候，我们只是和 AI 进行简单的对话，其核心的诉求就是：

> 给模型一个好的提示词，然后等待模型返回结果

也正是因为如此，我们需要不断的优化提示词书写的格式、内容，不断调试相关格式以满足不同任务的诉求，这一阶段也就是所谓的 **Prompt Engineering**。

而随着 AI 的能力逐渐强大，各种 Agent、智能体的时代，我们就不再局限于让 AI 完成简单的任务，而是让他能够调用工具、读取数据、进行分析等完成更复杂的任务。在这种情况下，提供给模型的就不再局限于提示词本身，还有工具的信息，命令的执行结果等等，因此提出了所谓了 **Context Engineering**。

而 **Loop Engineering**，则是最近 ClaudeCode 的负责人提到的，自己现在主要是写好 loop 去驱动 Claude 完成任务，而不是直接编写提示词，引起了业界的关注。当然 Claude 这群人本身也喜欢造词，Skills、MCP 这种就是出自他们，然后造完以后在推翻了出新词，大家也见怪不怪了。

### 那这个 Loop 到底是什么？和现在所谓的 Harness 有什么区别？

根据大佬们的发言，Loop Engineering 的核心就是不需要每次都需要编写提示词指挥 Agent 干活，而是将发现问题、拆解任务、并行处理、检测以及继续的过程封装成一个系统，让它自己持续运行。

而 Harness 的核心则是除模型以外的内容都可以算作 Harness 的范围，主要是使用系统程序（脚本）去自动完成调用AI、执行结果、验证收集结果、反馈、再生成的过程。

从要解决的问题上来看，Harness 可以算是 Loop Engineering 的超集，但仍有一些细节上的不同，当然这些不同并不是区分两者的核心。

1. **Harness** 并没有强调和界定系统程序和脚本，而 **Loop** 是创建一个完整的程序或是系统，Loop 使用的程序能力会更强。
2. 在 Harness 的原生定义中，每一个 Harness 是定制的，针对特定的任务进行工作，比如之前的 SWE-agent、Devin 等；而后来的 ClaudeCode、Codex 则是可以完成多种不同的任务，更偏向于 Loop 的范畴。在 Addy 的文章中，就对 ClaudeCode 和 Codex 在 Loop Engineering 中的各个部分进行了更详细的描述。

另外一个更典型的 Loop Engineering 的产品则应该算 **小龙虾**，通过定时化任务、多Agent管理、本地协同，小龙虾可以完成多种多样的任务。与此同时，龙虾还具有记忆，能够对输出的结果进行检查并记录犯错的内容，保证后面不再犯错。

### 对于普通人或者说开发者来说，你应该了解什么？

1. **Loop Engineering 其实算是 Harness 含义的扩展**，就好比从简单的专家 Agent 到 ClaudeCode 这种可以完成更多复杂任务的 Agent。无需焦虑所谓的新词，选一个合适的工具，不管是 CC、Codex 还是小龙虾先用起来，感受下和之前智能体的区别。
2. **如果你想开发一个 Loop 的产品**，那一定要明确 loop 本身的 token 成本极大，之前小龙虾一会就能消耗几百万、几千万的 token，有可能还没有测试几轮，成本就上去了。另外，一定要有校验环节，loop 本身无法校验结果的对错，一定要有人力的介入去约束 Agent，不然则会带来更多的灾难。

更多关于 Loop Engineering 的内容，欢迎阅读原文：[addyosmani/status/2064127981161959567](https://x.com/addyosmani/status/2064127981161959567)

---

*#AI编程 #OpenClaw*
