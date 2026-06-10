---
title: "面经库｜spring AI modular RAG architecture 整理"
published: 2026-06-10
description: "# Spring_AI_Modular_RAG_Architecture ## 问题 Spring_AI_Modular_RAG_Architecture ## 标准回答 # Spring AI 模块化 RAG 架构：预检索、检索、后检索三"
tags: ["面经", "面经库", "agent面经"]
category: "面经整理"
draft: false
lang: zh-CN
pinned: false
comment: true
---

# Spring_AI_Modular_RAG_Architecture
## 问题
Spring_AI_Modular_RAG_Architecture

## 标准回答

# Spring AI 模块化 RAG 架构：预检索、检索、后检索三阶段

Spring AI 提出的模块？
RAG 架构将检索增强生成过程分解为 **预检索 (Pre-Retrieval)**、**检索 (Retrieval)**、**检索后 (Post-Retrieval)** 三个核心阶段，每个阶段包含可配置的组件，以提升大模型响应的准确性和灵活性。

| 阶段 | 职责 | 核心组件 |
|------|------|----------|
| **预检索** | 接收原始查询，优化和转换，生成更适合检索的查询版本 | QueryTransformer：`RewriteQueryTransformer`（改写）、`TranslationQueryTransformer`（翻译）、`CompressionQueryTransformer`（压缩历史）、`MultiQueryExpander`（扩展为多查询提高召回） |
| **检索** | 使用优化后的查询，从知识库中搜索并召回最相关的文档片段 | `DocumentRetriever`（如 `VectorStoreDocumentRetriever`），负责相似性搜索和元数据过滤；多源检索时使用 `DocumentJoiner` 合并结果 |
| **检索后** | 对检索到的文档集进一步处理和优化，筛选最适合作为上下文的文档 | 文档重排序、无关文档移除、文档内容压缩或摘要等。Spring AI 提供 `DocumentPostProcessor` API 支持自定义后处理（目前尚不成熟） |

---

## 扩展知识

### 1. 为什么需要模块化 RAG？
- **灵活性**：不同场景（如问答、摘要、代码生成）需要不同的检索策略
- **可维护性**：各阶段独立演进，替换组件不影响整体流程
- **性能优化**：可针对瓶颈阶段单独调优（如预检索阶段增加查询改写，提升召回率）

### 2. 各阶段的典型实现
- **预检索**：在多轮对话中，使用 `CompressionQueryTransformer` 将历史对话压缩与当前问题合并，避免上下文爆炸
- **检索**：向量检索 + 关键词检索混合（Hybrid Search），提升召回和精度
- **检索后**：使用 `Cohere Rerank` 或 `Cross-Encoder` 模型对召回文档重排序，将最相关的放在前面

### 3. 与传统 RAG 的区别
传统 RAG 通常只包含“检索”和“生成”两步，查询优化和后处理硬编码或缺失。模块化 RAG 将每一步都暴露为可插拔组件，开发者可按需组合。

---

## 面试官追问

### Q1：预检索阶段的查询改写和扩展，会不会引入噪音？如何控制？
**A**：可能。例如将单查询扩展为多个查询，可能召回不相关文档。控制方法：
- 限制扩展数量（如最多 3 个变体）
- 使用相似度阈值过滤低相关性结果
- 在检索后阶段用重排序模型降噪

### Q2：检索阶段如果同时使用向量检索和关键词检索，结果如何合并？
**A**：使用 `DocumentJoiner`，常见策略：
- **加权合并**：向量和关键词得分加权平均
- **互惠排名融合**：根据排名位置融合，避免分数尺度问题
- **分集合并**：交替取出结果，保证多样性

### Q3：检索后阶段的文档压缩/摘要，会不会丢失关键信息？
**A**：会。但这是权衡 token 成本和信息完整性的必要手段。优化方法：
- **提取式摘要**：保留原文中的关键句子，而非生成式摘要
- **分块压缩**：对长文档按段落压缩，保留每段核心
- **重要性评分**：只压缩低重要性片段

### Q4：Spring AI 的模块化 RAG 与 LangChain 的 LCEL 有什么异同？
**A**：
- 相同：都支持链式组合和组件化
- 不同：Spring AI 更强调阶段划分（预、检、后），并提供了官方 QueryTransformer 实现；LangChain 更灵活但需要开发者自行组装。Spring AI 与 Spring 生态集成更好（如结合 Spring Boot 配置）。

---

## 总结

Spring AI 的模块化 RAG 架构通过将流程拆分为预检索、检索、后检索三个阶段，提供了高度的灵活性和可扩展性。开发者可根据业务需求替换或定制每个阶段的组件（如查询改写器、检索器、后处理器），实现更精准的检索增强生成。

## 

## 关键点

- # Spring AI 模块化 RAG 架构：预检索、检索、后检索三阶段

Spring AI 提出的模块化 RAG 架构将检索增强生成过程分解为 **预检索 (Pre-Retrieval)**、**检索 (Retrieval)**、**检索后 (Post-Retrieval)** 三个核心阶段，每个阶段包含可配置的组件，以提升大模型响应的准确性和灵活性。
- | 阶段 | 职责 | 核心组件 |
|------|------|----------|
| **预检索** | 接收原始查询，优化和转换，生成更适合检索的查询版本 | QueryTransformer：`RewriteQueryTransformer`（改写）、`TranslationQueryTransformer`（翻译）、`CompressionQueryTransformer`（压缩历史）、`MultiQueryExpander`（扩展为多查询提高召回） |
| **检索** | 使用优化后的查询，从知识库中搜索并召回最相关的文档片段 | `DocumentRetriever`（如 `VectorStoreDocumentRetriever`），负责相似性搜索和元数据过滤；多源检索时使用 `DocumentJoiner` 合并结果 |
| **检索后** | 对检索到的文档集进一步处理和优化，筛选最适合作为上下文的文档 | 文档重排序、无关文档移除、文档内容压缩或摘要等。
- Spring AI 提供 `DocumentPostProcessor` API 支持自定义后处理（目前尚不成熟） |

---

- - **灵活性**：不同场景（如问答、摘要、代码生成）需要不同的检索策略
- **可维护性**：各阶段独立演进，替换组件不影响整体流程
- **性能优化**：可针对瓶颈阶段单独调优（如预检索阶段增加查询改写，提升召回率）

- **预检索**：在多轮对话中，使用 `CompressionQueryTransformer` 将历史对话压缩与当前问题合并，避免上下文爆炸
- **检索**：向量检索 + 关键词检索混合（Hybrid Search），提升召回和精度
- **检索后**：使用 `Cohere Rerank` 或 `Cross-Encoder` 模型对召回文档重排序，将最相关的放在前面

传统 RAG 通常只包含“检索”和“生成”两步，查询优化和后处理硬编码或缺失。
- 模块化 RAG 将每一步都暴露为可插拔组件，开发者可按需组合。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

Spring_AI_Modular_RAG_Architecture

Spring AI 提出的模块化 RAG 架构将检索增强生成过程分解为 **预检索 (Pre-Retrieval)**、**检索 (Retrieval)**、**检索后 (Post-Retrieval)** 三个核心阶段，每个阶段包含可配置的组件，以提升大模型响应的准确性和灵活性。
- | 阶段 | 职责 | 核心组件 |
|------|------|----------|
| **预检索** | 接收原始查询，优化和转换，生成更适合检索的查询版本 | QueryTransformer：`RewriteQueryTransformer`（改写）、`TranslationQueryTransformer`（翻译）、`CompressionQueryTransformer`（压缩历史）、`MultiQueryExpander`（扩展为多查询提高召回） |
| **检索** | 使用优化后的查询，从知识库中搜索并召回最相关的文档片段 | `DocumentRetriever`（如 `VectorStoreDocumentRetriever`），负责相似性搜索和元数据过滤；多源检索时使用 `DocumentJoiner` 合并结果 |
| **检索后** | 对检索到的文档集进一步处理和优化，筛选最适合作为上下文的文档 | 文档重排序、无关文档移除、文档内容压缩或摘要等。Spring AI 提供 `DocumentPostProcessor` API 支持自定义后处理（目前尚不成熟） |

---

- - **灵活性**：不同场景（如问答、摘要、代码生成）需要不同的检索策略
- **可维护性**：各阶段独立演进，替换组件不影响整体流程
- **性能优化**：可针对瓶颈阶段单独调优（如预检索阶段增加查询改写，提升召回率）

- **预检索**：在多轮对话中，使用 `CompressionQueryTransformer` 将历史对话压缩与当前问题合并，避免上下文爆炸
- **检索**：向量检索 + 关键词检索混合（Hybrid Search），提升召回和精度
- **检索后**：使用 `Cohere Rerank` 或 `Cross-Encoder` 模型对召回文档重排序，将最相关的放在前面

传统 RAG 通常只包含“检索”和“生成”两步，查询优化和后处理硬编码或缺失。模块化 RAG 将每一步都暴露为可插拔组件，开发者可按需组合。
- ---

- **A**：可能。例如将单查询扩展为多个查询，可能召回不相关文档。控制方法：
- 限制扩展数量（如最多 3 个变体）
- 使用相似度阈值过滤低相关性结果
- 在检索后阶段用重排序模型降噪

- 本文已做格式统一与噪声清理，保留原始语义。
- RAG 架构将检索增强生成过程分解为 **预检索 (Pre-Retrieval)**、**检索 (Retrieval)**、**检索后 (Post-Retrieval)** 三个核心阶段，每个阶段包含可配置的组件，以提升大模型响应的准确性和灵活性。
- | 阶段 | 职责 | 核心组件 |
- |------|------|----------|
- | **预检索** | 接收原始查询，优化和转换，生成更适合检索的查询版本 | QueryTransformer：`RewriteQueryTransformer`（改写）、`TranslationQueryTransformer`（翻译）、`CompressionQueryTransformer`（压缩历史）、`MultiQueryExpander`（扩展为多查询提高召回） |
- | **检索** | 使用优化后的查询，从知识库中搜索并召回最相关的文档片段 | `DocumentRetriever`（如 `VectorStoreDocumentRetriever`），负责相似性搜索和元数据过滤；多源检索时使用 `DocumentJoiner` 合并结果 |

- 本文已做格式统一与噪声清理，保留原始语义。
