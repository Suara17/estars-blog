---
title: 'Agent八股分享：一天速通记忆/检索（RAG）'
published: 2026-06-15
description: '来源：小红书笔记'
category: '求职作战室'
tags: ['求职作战室', '面经']
draft: false
lang: zh-CN
---# Agent八股分享：一天速通记忆/检索（RAG）

**来源**：小红书笔记  
**链接**：http://xhslink.com/o/8tkHC8Q3yVK  
**标签**：互联网大厂、agent、java、后端开发、实习、暑期实习

---

## 1️⃣ 必问主线

1. 什么是 RAG？为什么它比直接让模型回答更适合企业知识问答？
2. RAG 和微调有什么区别？什么时候用哪个？
3. RAG 和长上下文模型谁更好？
4. 为什么说 RAG 不是一个"向量库项目"？
5. 一个 RAG 系统为什么会答错？
6. RAG 的核心指标有哪些？
7. 什么时候不应该上 RAG？
8. 为什么很多 RAG demo 看起来能跑，线上却不好用？

---

## 2️⃣ 检索链路与效果优化

1. 为什么说 chunking 决定了检索系统的上限？
2. chunk size 应该怎么定？
3. overlap 有什么作用，为什么不能太大？
4. embedding 模型怎么选？
5. 为什么很多系统要加 rerank？
6. cross-encoder rerank 和向量召回的关系是什么？
7. 为什么 dense retrieval 很强了，生产里还要 sparse？
8. Hybrid Retrieval 的本质是什么？
9. Query Rewrite 的目的是什么？
10. query rewrite 有什么风险？
11. Hybrid Retrieval 和 rerank 的关系是什么？
12. 元数据为什么对检索效果重要？
13. late chunking 解决什么问题？
14. Contextual Retrieval 的核心思想是什么？

---

## 3️⃣ Memory 与 RAG 边界

1. RAG 和 Memory 最本质的区别是什么？
2. 为什么会话历史不等于长期记忆？
3. session state 和 memory 有什么区别？
4. 缓存是不是一种记忆？
5. 为什么说 memory 需要写入策略？

---

## 4️⃣ 长期记忆与用户记忆

- 长期记忆和用户画像有什么区别？
- 为什么长期记忆不能每轮都写？
- 你会把哪些信息写成常驻记忆？

---

## 5️⃣ Agentic RAG / GraphRAG 进阶题

- 什么是 Agentic RAG？
- 什么情况下普通 RAG 不够用？

---

*提取自小红书笔记文字描述，2026-05-31 整理*
