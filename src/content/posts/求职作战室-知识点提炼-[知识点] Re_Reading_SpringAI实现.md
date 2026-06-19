---
title: '什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？'
published: 2026-06-19
description: '什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？'
category: '求职作战室'
tags: ['求职作战室', '知识点提炼']
draft: false
lang: zh-CN
---# 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？
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


在 Spring AI 中，可以通过自定义 Advisor 来实现 Re-Reading 功能：


(在 Spring AI 1.0 版本中，上述两个接口需要更改为CallAdvisor和StreamAdvisor)2）修改用户提示词：在 Advisor 的前置处理逻辑中（例如aroundCall或aroundStream方法调用之前），对用户的原始输入文本进行改写。 改写的格式通常是将原始输入重复一遍，并用明确的指令引导模型重新阅读，通过看源码能够看到提示词：▼markdown复制代码{Input_Query}

Read the question again: {Input_Query}其中，{Input_Query}是用户原始的提问内容。

3） 传递给模型：将改写后的提示词传递给大语言模型进行处理。
对复杂问题，重复阅读，让模型能够更好理解，从而生成更加准确的答案

Spring AI实现

1.可以通过自定义Advisor类进行实现

2.在拦截之后进行修改提示词

改写格式一般是将原始输入重新重复一遍（让模型再次读取一遍）


在 Spring AI 中，可以通过自定义 Advisor 来实现 Re-Reading 功能：

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


在 Spring AI 中，可以通过自定义 Advisor 来实现 Re-Reading 功能：


(在 Spring AI 1.0 版本中，上述两个接口需要更改为CallAdvisor和StreamAdvisor)2）修改用户提示词：在 Advisor 的前置处理逻辑中（例如aroundCall或aroundStream方法调用之前），对用户的原始输入文本进行改写。

- 本文已做格式统一与噪声清理，保留原始语义。
- 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？
- # 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？
- 11764. 什么是 Re-Reading？如何基于 Spring AI 实现 Re-Reading Advisor？VIP中等后端编程导航标记分享131891Re-Reading (重读)，也称为 Re2，是一种通过让大语言模型重新阅读问题来提高其推理能力的技术。核心思想是，对于复杂问题，重复阅读和审视问题有助于模型更好地理解题意和约束，从而生成更准确、更深入的回答，有文献研究证明这是有一定效果的。不过，这种方法会因为重复处理输入导致成本加倍，所以在面向 C 端开放的应用中需要谨慎使用。在 Spring AI 中，可以通过自定义 Advisor 来实现 Re-Reading 功能：1）创建自定义 Advisor 类：该类需要同时实现CallAroundAdvisor（用于同步请求）和StreamAroundAdvisor（用于流式请求）接口，让该类更通用
- (在 Spring AI 1.0 版本中，上述两个接口需要更改为CallAdvisor和StreamAdvisor)2）修改用户提示词：在 Advisor 的前置处理逻辑中（例如aroundCall或aroundStream方法调用之前），对用户的原始输入文本进行改写。 改写的格式通常是将原始输入重复一遍，并用明确的指令引导模型重新阅读，通过看源码能够看到提示词：▼markdown复制代码{Input_Query}
- Read the question again: {Input_Query}其中，{Input_Query}是用户原始的提问内容。

3） 传递给模型：将改写后的提示词传递给大语言模型进行处理。
- 本文已做格式统一与噪声清理，保留原始语义。
