---
title: "什么是 Re Reading？如何基于 Spring AI 实现 Re Reading Advisor？ 整理"
published: 2026-06-10
description: "# 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？ ## 问题 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？ ## 标准回"
tags: ["求职作战室", "面经"]
category: "求职作战室"
draft: false
lang: zh-CN
pinned: false
comment: true
---

# 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？
## 问题
什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？

## 标准回答
什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？VIP中等后端编程导航标记分享131891Re-Reading (重读)，也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术。核心思想是，对于复杂问题，重复阅读和审视问题有助于模型更好地理解题意和约束，从而生成更准确、更深入的回答，有文献研究证明这是有一定效果的。不过，这种方法会因为重复处理输入导致成本加倍，所以在面向 C 端开放的应用中需要谨慎使用。在 Spring AI 中，可以通过自定义 Advisor 来实现 Re-Reading 功能：1）创建自定义 Advisor 类：该类需要同时实现CallAroundAdvisor（用于同步请求）和StreamAroundAdvisor（用于流式请求）接口，让该类更通用

(在 Spring AI 1.0 版本中，上述两个接口需要更改为CallAdvisor和StreamAdvisor)2）修改用户提示词：在 Advisor 的前置处理逻辑中（例如aroundCall或aroundStream方法调用之前），对用户的原始输入文本进行改写。 改写的格式通常是将原始输入重复一遍，并用明确的指令引导模型重新阅读，通过看源码能够看到提示词：▼markdown复制代码{Input_Query}

Read the question again: {Input_Query}其中，{Input_Query}是用户原始的提问内容。

3） 传递给模型：将改写后的提示词传递给大语言模型进行处理。
对复杂问题，重复阅读，让模型能够更好理解，从而生成更加准确的答案

Spring AI实现

1.可以通过自定义Advisor类进行实现

2.在拦截之后进行修改提示词

改写格式一般是将原始输入重新重复一遍（让模型再次读取一遍）

3.展开新页面打开2026-03-18  16:5200回复迷途者之博士退学中特训营重读是一种让LLM重新阅读问题，从而提高LLM推理能力的技术，核心思想就是，对于复杂问题，重复阅读和审视问题有助于模型更好地理解题意和约束，从而生成更准确、更深入的回答，有文献研究证明这是有一定效果的，不过这种方法会因为重复处理请求导致api成本加倍，所以面对C端应用时需要谨慎使用。然后，我在项展开新页面打开2025-12-22  20:2600回复我一定要找到工作Re-Reading(重读)，核心思想是，对于复杂问题，让ai重复阅读一次问题，有助于模型更好地理解我们的问题，从而生成更准确的答案。缺点是：重复处理输入导致成本加倍，所以在面向 C端开放的应用中需要谨慎使用。在SpringAI中，可以通过自展开新页面打开2025-11-29  16:2600回复yyc什么是 Re-Reading?如何基于 Spring Al 实现 Re-Reading Advisor?Re-Reading（Re2）是通过让大语言模型重读问题提升推理能力的技术。核心思想是重复阅读帮助模型更好理解题意约束，生成更准确深入的回答。使用注意：文献证明有效，但因重复处理输展开新页面打开2025-11-13  17:2800回复XiCallAroundAdvidor以及StreamAroundAdvisor接口：展开新页面打开2025-09-23  12:5000回复面试鸭5102特训营Re-Reading也叫Read2，是指在AI遇到复杂问题的情况下，通过让AI重复阅读一次用户的提示词从而提高AI回复的准确度。

Read2的实现通过自定义一个advisor类，该advidor类实现CallAroundAdvidor以及StreamAroundAdvisor接口以及实现里面的方法，展开新页面打开2025-09-04  16:4000回复超大桶可乐特训营Re-Reading 是指在提示词中，显示的指示LLM重新阅读一遍用户的输入，这样可以让LLM的输出更准确。有文献研究表明这是一种有效的手段。具体实现时，通过定义一个ReReadingAdvisor，继承 BaseAdvisor 类，重写 before() 方法，将用户的提示修改为如下格展开新页面打开2025-08-26  15:0100回复拒绝内耗特训营ReReading简称Re2，实际上是一种提示词工程，它将用户的提示词重复了一遍，起到了一个强调的作用。我们可以利用 Advisor 接口，来实现一个Re-Reading Advisor，关键在于对用户的提示词进行修改。2025-08-04  18:0800回复云墨总结：Spring AI 的Re-reading（重读）Re-reading（重读）是 Spring AI 中用于对大模型返回的结果进行再次处理或解析的一种机制。核心作用：对 AI 模型生成的内容进行结构化提取或**格式转展开新页面打开2025-07-17  09:2600回复一口南瓜饼Re-Reading (重读)，也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术

在 Spring AI 中，可以通过自定义 Advisor 来实现 Re-Reading 功能：

）创建自定义 Advisor 类：该类需要同时实现 CallAroundAdvisor（用于同步展开新页面打开2025-07-12  15:5900回复添加回答编辑预览请输入回答内容...（支持使用 Markdown ）xMarkdown 语法一级标题# 标题二级标题## 标题三级标题### 标题粗体**粗体文本**斜体*斜体文本*引用> 引用文本链接[链接描述](url)图片![alt](url "图片描述")代码`代码`代码块```编程语言↵无序列表- 项目有序列表1. 项目分割线---删除线~~文本~~任务列表- [ ] 待办事项行内公式$公式$块级公式$$↵公式↵$$Mermaid图表```mermaid快捷键粗体Ctrl-B斜体Ctrl-I链接Ctrl-K图片Shift-Ctrl-I代码Shift-Ctrl-K代码块Shift-Ctrl-C无序列表Shift-Ctrl-U有序列表Shift-Ctrl-O目录字数:0行数:1回到顶部提交热门面试题目榜更多说说 Java 中 HashMap 的原理？9130Java 中的序列化和反序列化是什么？6255MySQL 索引的最左前缀匹配原则是什么？5662Java 中 ConcurrentHashMap 1.7 和 1.8 之间有哪些区别？5067Java 中有哪些集合类？请简单介绍4854MySQL 的索引类型有哪些？4845详细描述一条 SQL 语句在 MySQL 中的执行过程。4218什么是 RAG？RAG 的主要流程是什么？4151MySQL 的存储引擎有哪些？它们之间有什么区别？4092数据库的脏读、不可重复读和幻读分别是什么？3900推荐教程更多AI 超级智能体亿级流量点赞系统教程智能协同云图库项目教程预览用户交流一起刷题学习、求职交流、反馈建议、获取更新通知面试鸭《用户协议》《隐私政策》友情链接编程导航老鱼简历代码小抄剪切助手联系我们商务合作站长：程序员鱼皮关注我们扫码关注面试鸭公众号
## 答案

你在 AI 超级智能体项目中如何利用 Spring AI 开发应用？用到了哪些特性？上次浏览：2026-03-16 15:12:36你有多个知识库，做 RAG 的时候，怎么保证查询效率和准确性兼容，并尽可能减少幻觉？如何实现程序和 AI 大模型的集成？有哪些方式？Agent 死循环问题有遇到过吗？如何解决？如何实现 AI 多轮对话功能？如何解决对话记忆持久化问题？如果一个GPU集群的LLM处理能力为1000tokens/s，那1000个用户同时并发访问，响应给每个用户的性能只有1 token/s吗？怎么分析性能瓶颈什么是结构化输出？Spring AI 是怎么实现结构化输出的？什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？什么是 Spring AI 框架？它有哪些核心特性？上次浏览：2026-03-18 18:41:27什么是 AI Agent？它和直接调用大模型 API 做一次问答有什么本质区别？请解释 Tool Calling（工具调用）的完整链路：工具是怎么定义的、LLM 怎么调用它、结果怎么回传?System Prompt 在 Agent 系统中承载了哪些职责？如果 System Prompt 越来越长，你会怎么处理？11764. 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？VIP中等后端编程导航标记分享131891Re-Reading (重读)，也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术。核心思想是，对于复杂问题，重复阅读和审视问题有助于模型更好地理解题意和约束，从而生成更准确、更深入的回答，有文献研究证明这是有一定效果的。不过，这种方法会因为重复处理输入导致成本加倍，所以在面向 C 端开放的应用中需要谨慎使用。在 Spring AI 中，可以通过自定义 Advisor 来实现 Re-Reading 功能：1）创建自定义 Advisor 类：该类需要同时实现CallAroundAdvisor（用于同步请求）和StreamAroundAdvisor（用于流式请求）接口，让该类更通用

(在 Spring AI 1.0 版本中，上述两个接口需要更改为CallAdvisor和StreamAdvisor)2）修改用户提示词：在 Advisor 的前置处理逻辑中（例如aroundCall或aroundStream方法调用之前），对用户的原始输入文本进行改写。 改写的格式通常是将原始输入重复一遍，并用明确的指令引导模型重新阅读，通过看源码能够看到提示词：▼markdown复制代码{Input_Query}

Read the question again: {Input_Query}其中，{Input_Query}是用户原始的提问内容。

3） 传递给模型：将改写后的提示词传递给大语言模型进行处理。
对复杂问题，重复阅读，让模型能够更好理解，从而生成更加准确的答案

Spring AI实现

1.可以通过自定义Advisor类进行实现

2.在拦截之后进行修改提示词

改写格式一般是将原始输入重新重复一遍（让模型再次读取一遍）

3.展开新页面打开2026-03-18  16:5200回复迷途者之博士退学中特训营重读是一种让LLM重新阅读问题，从而提高LLM推理能力的技术，核心思想就是，对于复杂问题，重复阅读和审视问题有助于模型更好地理解题意和约束，从而生成更准确、更深入的回答，有文献研究证明这是有一定效果的，不过这种方法会因为重复处理请求导致api成本加倍，所以面对C端应用时需要谨慎使用。然后，我在项展开新页面打开2025-12-22  20:2600回复我一定要找到工作Re-Reading(重读)，核心思想是，对于复杂问题，让ai重复阅读一次问题，有助于模型更好地理解我们的问题，从而生成更准确的答案。缺点是：重复处理输入导致成本加倍，所以在面向 C端开放的应用中需要谨慎使用。在SpringAI中，可以通过自展开新页面打开2025-11-29  16:2600回复yyc什么是 Re-Reading?如何基于 Spring Al 实现 Re-Reading Advisor?Re-Reading（Re2）是通过让大语言模型重读问题提升推理能力的技术。核心思想是重复阅读帮助模型更好理解题意约束，生成更准确深入的回答。使用注意：文献证明有效，但因重复处理输展开新页面打开2025-11-13  17:2800回复XiCallAroundAdvidor以及StreamAroundAdvisor接口：展开新页面打开2025-09-23  12:5000回复面试鸭5102特训营Re-Reading也叫Read2，是指在AI遇到复杂问题的情况下，通过让AI重复阅读一次用户的提示词从而提高AI回复的准确度。

Read2的实现通过自定义一个advisor类，该advidor类实现CallAroundAdvidor以及StreamAroundAdvisor接口以及实现里面的方法，展开新页面打开2025-09-04  16:4000回复超大桶可乐特训营Re-Reading 是指在提示词中，显示的指示LLM重新阅读一遍用户的输入，这样可以让LLM的输出更准确。有文献研究表明这是一种有效的手段。具体实现时，通过定义一个ReReadingAdvisor，继承 BaseAdvisor 类，重写 before() 方法，将用户的提示修改为如下格展开新页面打开2025-08-26  15:0100回复拒绝内耗特训营ReReading简称Re2，实际上是一种提示词工程，它将用户的提示词重复了一遍，起到了一个强调的作用。我们可以利用 Advisor 接口，来实现一个Re-Reading Advisor，关键在于对用户的提示词进行修改。2025-08-04  18:0800回复云墨总结：Spring AI 的Re-reading（重读）Re-reading（重读）是 Spring AI 中用于对大模型返回的结果进行再次处理或解析的一种机制。核心作用：对 AI 模型生成的内容进行结构化提取或**格式转展开新页面打开2025-07-17  09:2600回复一口南瓜饼Re-Reading (重读)，也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术

在 Spring AI 中，可以通过自定义 Advisor 来实现 Re-Reading 功能：

）创建自定义 Advisor 类：该类需要同时实现 CallAroundAdvisor（用于同步展开新页面打开2025-07-12  15:5900回复添加回答编辑预览请输入回答内容...（支持使用 Markdown ）xMarkdown 语法一级标题# 标题二级标题## 标题三级标题### 标题粗体**粗体文本**斜体*斜体文本*引用> 引用文本链接[链接描述](url)图片![alt](url "图片描述")代码`代码`代码块```编程语言↵无序列表- 项目有序列表1. 项目分割线---删除线~~文本~~任务列表- [ ] 待办事项行内公式$公式$块级公式$$↵公式↵$$Mermaid图表```mermaid快捷键粗体Ctrl-B斜体Ctrl-I链接Ctrl-K图片Shift-Ctrl-I代码Shift-Ctrl-K代码块Shift-Ctrl-C无序列表Shift-Ctrl-U有序列表Shift-Ctrl-O目录字数:0行数:1回到顶部提交热门面试题目榜更多说说 Java 中 HashMap 的原理？9130Java 中的序列化和反序列化是什么？6255MySQL 索引的最左前缀匹配原则是什么？5662Java 中 ConcurrentHashMap 1.7 和 1.8 之间有哪些区别？5067Java 中有哪些集合类？请简单介绍4854MySQL 的索引类型有哪些？4845详细描述一条 SQL 语句在 MySQL 中的执行过程。4218什么是 RAG？RAG 的主要流程是什么？4151MySQL 的存储引擎有哪些？它们之间有什么区别？4092数据库的脏读、不可重复读和幻读分别是什么？3900推荐教程更多AI 超级智能体亿级流量点赞系统教程智能协同云图库项目教程预览用户交流一起刷题学习、求职交流、反馈建议、获取更新通知面试鸭《用户协议》《隐私政策》友情链接编程导航老鱼简历代码小抄剪切助手联系我们商务合作站长：程序员鱼皮关注我们扫码关注面试鸭公众号

---

> 来源: 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？.mhtml

## 

## 关键点

- # 什么是 Re-Reading？
- 如何基于 Spring AI 实现 Re-Reading Advisor？
- ## 问题
什么是 Re-Reading？
- 如何基于 Spring AI 实现 Re-Reading Advisor？
- VIP中等后端编程导航标记分享131891Re-Reading (重读)，也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？
- ## 标准回答

- ## 问题
什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？VIP中等后端编程导航标记分享131891Re-Reading (重读)，也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术。核心思想是，对于复杂问题，重复阅读和审视问题有助于模型更好地理解题意和约束，从而生成更准确、更深入的回答，有文献研究证明这是有一定效果的。不过，这种方法会因为重复处理输入导致成本加倍，所以在面向 C 端开放的应用中需要谨慎使用。在 Spring AI 中，可以通过自定义 Advisor 来实现 Re-Reading 功能：1）创建自定义 Advisor 类：该类需要同时实现CallAroundAdvisor（用于同步请求）和StreamAroundAdvisor（用于流式请求）接口，让该类更通用

(在 Spring AI 1.0 版本中，上述两个接口需要更改为CallAdvisor和StreamAdvisor)2）修改用户提示词：在 Advisor 的前置处理逻辑中（例如aroundCall或aroundStream方法调用之前），对用户的原始输入文本进行改写。
- 改写的格式通常是将原始输入重复一遍，并用明确的指令引导模型重新阅读，通过看源码能够看到提示词：▼markdown复制代码{Input_Query}

Read the question again: {Input_Query}其中，{Input_Query}是用户原始的提问内容。

3） 传递给模型：将改写后的提示词传递给大语言模型进行处理。
对复杂问题，重复阅读，让模型能够更好理解，从而生成更加准确的答案

Spring AI实现

1.可以通过自定义Advisor类进行实现

2.在拦截之后进行修改提示词

改写格式一般是将原始输入重新重复一遍（让模型再次读取一遍）

3.展开新页面打开2026-03-18  16:5200回复迷途者之博士退学中特训营重读是一种让LLM重新阅读问题，从而提高LLM推理能力的技术，核心思想就是，对于复杂问题，重复阅读和审视问题有助于模型更好地理解题意和约束，从而生成更准确、更深入的回答，有文献研究证明这是有一定效果的，不过这种方法会因为重复处理请求导致api成本加倍，所以面对C端应用时需要谨慎使用。然后，我在项展开新页面打开2025-12-22  20:2600回复我一定要找到工作Re-Reading(重读)，核心思想是，对于复杂问题，让ai重复阅读一次问题，有助于模型更好地理解我们的问题，从而生成更准确的答案。缺点是：重复处理输入导致成本加倍，所以在面向 C端开放的应用中需要谨慎使用。在SpringAI中，可以通过自展开新页面打开2025-11-29  16:2600回复yyc什么是 Re-Reading?如何基于 Spring Al 实现 Re-Reading Advisor?Re-Reading（Re2）是通过让大语言模型重读问题提升推理能力的技术。核心思想是重复阅读帮助模型更好理解题意约束，生成更准确深入的回答。使用注意：文献证明有效，但因重复处理输展开新页面打开2025-11-13  17:2800回复XiCallAroundAdvidor以及StreamAroundAdvisor接口：展开新页面打开2025-09-23  12:5000回复面试鸭5102特训营Re-Reading也叫Read2，是指在AI遇到复杂问题的情况下，通过让AI重复阅读一次用户的提示词从而提高AI回复的准确度。
- Read2的实现通过自定义一个advisor类，该advidor类实现CallAroundAdvidor以及StreamAroundAdvisor接口以及实现里面的方法，展开新页面打开2025-09-04  16:4000回复超大桶可乐特训营Re-Reading 是指在提示词中，显示的指示LLM重新阅读一遍用户的输入，这样可以让LLM的输出更准确。有文献研究表明这是一种有效的手段。具体实现时，通过定义一个ReReadingAdvisor，继承 BaseAdvisor 类，重写 before() 方法，将用户的提示修改为如下格展开新页面打开2025-08-26  15:0100回复拒绝内耗特训营ReReading简称Re2，实际上是一种提示词工程，它将用户的提示词重复了一遍，起到了一个强调的作用。我们可以利用 Advisor 接口，来实现一个Re-Reading Advisor，关键在于对用户的提示词进行修改。2025-08-04  18:0800回复云墨总结：Spring AI 的Re-reading（重读）Re-reading（重读）是 Spring AI 中用于对大模型返回的结果进行再次处理或解析的一种机制。核心作用：对 AI 模型生成的内容进行结构化提取或**格式转展开新页面打开2025-07-17  09:2600回复一口南瓜饼Re-Reading (重读)，也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术

在 Spring AI 中，可以通过自定义 Advisor 来实现 Re-Reading 功能：

）创建自定义 Advisor 类：该类需要同时实现 CallAroundAdvisor（用于同步展开新页面打开2025-07-12  15:5900回复添加回答编辑预览请输入回答内容...（支持使用 Markdown ）xMarkdown 语法一级标题# 标题二级标题## 标题三级标题### 标题粗体**粗体文本**斜体*斜体文本*引用> 引用文本链接[链接描述](url)图片![alt](url "图片描述")代码`代码`代码块```编程语言↵无序列表- 项目有序列表1. 项目分割线---删除线~~文本~~任务列表- [ ] 待办事项行内公式$公式$块级公式$$↵公式↵$$Mermaid图表```mermaid快捷键粗体Ctrl-B斜体Ctrl-I链接Ctrl-K图片Shift-Ctrl-I代码Shift-Ctrl-K代码块Shift-Ctrl-C无序列表Shift-Ctrl-U有序列表Shift-Ctrl-O目录字数:0行数:1回到顶部提交热门面试题目榜更多说说 Java 中 HashMap 的原理？9130Java 中的序列化和反序列化是什么？6255MySQL 索引的最左前缀匹配原则是什么？5662Java 中 ConcurrentHashMap 1.7 和 1.8 之间有哪些区别？5067Java 中有哪些集合类？请简单介绍4854MySQL 的索引类型有哪些？4845详细描述一条 SQL 语句在 MySQL 中的执行过程。4218什么是 RAG？RAG 的主要流程是什么？4151MySQL 的存储引擎有哪些？它们之间有什么区别？4092数据库的脏读、不可重复读和幻读分别是什么？3900推荐教程更多AI 超级智能体亿级流量点赞系统教程智能协同云图库项目教程预览用户交流一起刷题学习、求职交流、反馈建议、获取更新通知面试鸭《用户协议》《隐私政策》友情链接编程导航老鱼简历代码小抄剪切助手联系我们商务合作站长：程序员鱼皮关注我们扫码关注面试鸭公众号

你在 AI 超级智能体项目中如何利用 Spring AI 开发应用？用到了哪些特性？上次浏览：2026-03-16 15:12:36你有多个知识库，做 RAG 的时候，怎么保证查询效率和准确性兼容，并尽可能减少幻觉？如何实现程序和 AI 大模型的集成？有哪些方式？Agent 死循环问题有遇到过吗？如何解决？如何实现 AI 多轮对话功能？如何解决对话记忆持久化问题？如果一个GPU集群的LLM处理能力为1000tokens/s，那1000个用户同时并发访问，响应给每个用户的性能只有1 token/s吗？怎么分析性能瓶颈什么是结构化输出？Spring AI 是怎么实现结构化输出的？什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？什么是 Spring AI 框架？它有哪些核心特性？上次浏览：2026-03-18 18:41:27什么是 AI Agent？它和直接调用大模型 API 做一次问答有什么本质区别？请解释 Tool Calling（工具调用）的完整链路：工具是怎么定义的、LLM 怎么调用它、结果怎么回传?System Prompt 在 Agent 系统中承载了哪些职责？如果 System Prompt 越来越长，你会怎么处理？11764. 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？VIP中等后端编程导航标记分享131891Re-Reading (重读)，也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术。核心思想是，对于复杂问题，重复阅读和审视问题有助于模型更好地理解题意和约束，从而生成更准确、更深入的回答，有文献研究证明这是有一定效果的。不过，这种方法会因为重复处理输入导致成本加倍，所以在面向 C 端开放的应用中需要谨慎使用。在 Spring AI 中，可以通过自定义 Advisor 来实现 Re-Reading 功能：1）创建自定义 Advisor 类：该类需要同时实现CallAroundAdvisor（用于同步请求）和StreamAroundAdvisor（用于流式请求）接口，让该类更通用

(在 Spring AI 1.0 版本中，上述两个接口需要更改为CallAdvisor和StreamAdvisor)2）修改用户提示词：在 Advisor 的前置处理逻辑中（例如aroundCall或aroundStream方法调用之前），对用户的原始输入文本进行改写。

- 本文已做格式统一与噪声清理，保留原始语义。
- 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？
- # 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？
- 11764. 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？VIP中等后端编程导航标记分享131891Re-Reading (重读)，也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术。核心思想是，对于复杂问题，重复阅读和审视问题有助于模型更好地理解题意和约束，从而生成更准确、更深入的回答，有文献研究证明这是有一定效果的。不过，这种方法会因为重复处理输入导致成本加倍，所以在面向 C 端开放的应用中需要谨慎使用。在 Spring AI 中，可以通过自定义 Advisor 来实现 Re-Reading 功能：1）创建自定义 Advisor 类：该类需要同时实现CallAroundAdvisor（用于同步请求）和StreamAroundAdvisor（用于流式请求）接口，让该类更通用
- (在 Spring AI 1.0 版本中，上述两个接口需要更改为CallAdvisor和StreamAdvisor)2）修改用户提示词：在 Advisor 的前置处理逻辑中（例如aroundCall或aroundStream方法调用之前），对用户的原始输入文本进行改写。 改写的格式通常是将原始输入重复一遍，并用明确的指令引导模型重新阅读，通过看源码能够看到提示词：▼markdown复制代码{Input_Query}
- Read the question again: {Input_Query}其中，{Input_Query}是用户原始的提问内容。

3） 传递给模型：将改写后的提示词传递给大语言模型进行处理。
- 本文已做格式统一与噪声清理，保留原始语义。
