---
title: "面经库｜Contextual Query Augmentation 整理"
published: 2026-06-10
description: "# Contextual_Query_Augmentation ## 问题 Contextual_Query_Augmentation ## 标准回答 ``` ### 3？ 空上下文处理策略 当检索不到相关文档时，系统需要优雅降级： - *"
tags: ["面经", "面经库", "agent面经"]
category: "面经整理"
draft: false
lang: zh-CN
pinned: false
comment: true
---

# Contextual_Query_Augmentation
## 问题
Contextual_Query_Augmentation

## 标准回答

```

### 3？
空上下文处理策略
当检索不到相关文档时，系统需要优雅降级：
- **保守策略**：指示模型不要回答（默认行为）
- **自定义策略**：通过自定义模板引导模型给出友好提示，避免生成幻觉内容
- **混合策略**：允许模型基于自身知识回答，但明确告知信息来源

---

## 面试官追问

### Q1：上下文查询增强和查询重写有什么区别？
**A**：
- **查询重写**：修改用户查询本身，使其更适合检索（如扩写、缩写、纠错）
- **上下文查询增强**：将原始查询与检索到的文档拼接，形成完整的 prompt
- **关系**：查询重写发生在检索前，上下文查询增强发生在检索后、生成前

### Q2：如何避免增强后的 prompt 超过 token 限制？
**A**：
- 对检索到的文档做截断或摘要（保留最相关的片段）
- 使用动态窗口，根据可用 token 预算调整注入的文档数量
- 采用滑动窗口或重排序，只保留 top-k 最相关的文档

### Q3：上下文查询增强和 RAG 是什么关系？
**A**：上下文查询增强是 RAG 流程中的一环。完整 RAG 流程为：
查询重写（预检索）
向量检索
**上下文查询增强**（将查询与检索结果结合）
LLM 生成回答

Spring AI 的 `RetrievalAugmentationAdvisor` 封装了这一流程，`ContextualQueryAugmenter` 专门负责增强步骤。

### Q4：如果检索到的文档包含矛盾信息，怎么办？
**A**：
- 在增强 prompt 中明确要求模型基于"最可信"的信息回答
- 使用重排序模型，将高置信度文档放在前面
- 让模型在回答中标注信息来源，或明确指出信息冲突

---

## 总结

上下文查询增强是连接检索和生成的桥梁，通过将检索到的文档与用户查询智能结合，显著提升 RAG 系统的回答质量。Spring AI 通过 `ContextualQueryAugmenter` 和空上下文处理机制，提供了灵活的实现方式，可优雅处理检索失败等边界情况。

##
