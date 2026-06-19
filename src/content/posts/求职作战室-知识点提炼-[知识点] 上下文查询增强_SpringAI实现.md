---
title: '什么是上下文查询增强？它有什么作用？如何基于 Spring AI 实现上下文查询增强来处理无关问题？'
published: 2026-06-19
description: '什么是上下文查询增强？它有什么作用？如何基于 Spring AI 实现上下文查询增强来处理无关问题？'
category: '求职作战室'
tags: ['求职作战室', '知识点提炼']
draft: false
lang: zh-CN
---# 什么是上下文查询增强？它有什么作用？如何基于 Spring AI 实现上下文查询增强来处理无关问题？

## 问题
什么是上下文查询增强？它有什么作用？如何基于 Spring AI 实现上下文查询增强来处理无关问题？

## 标准回答
上下文查询增强是 RAG 流程中的一个核心环节，指的是把用户的原始查询与从知识库中检索到的相关文档进行结合，形成一个信息更丰富的增强提示，然后将这个增强提示提供给 AI，让模型能基于这些特定知识生成回答。主要作用是为大模型提供必要的、实时的外部知识，这样 AI 的回答就不仅仅依赖于其预训练的通用知识，提高答案的准确性、相关性和时效性。

Spring AI 的 RetrievalAugmentationAdvisor 内部使用 ContextualQueryAugmenter 来实现上下文查询增强。当处理用户提出的无关问题时，ContextualQueryAugmenter 提供了空上下文处理机制。我们可以配置 allowEmptyContext(false)，并提供一个自定义的 emptyContextPromptTemplate。检索不到相关文档时，系统会使用这个自定义模板来指示大模型如何回应。

默认情况下，RetrievalAugmentationAdvisor 内部就使用了上下文查询增强，当它没有找到相关文档时，它会指示模型不要回答用户查询。这是一种保守的策略，可以防止模型在没有足够信息的情况下生成不准确的回答。

> 来源: 面试鸭 - 上下文查询增强（已清理重复内容和爬虫残留）
