---
title: "腾讯 AI 应用开发 一面"
published: 2026-06-12
description: "来源：小红书笔记（作者：逸，2026-04-11） 链接：http://xhslink.com/o/2yiaDG9CXww 数据：3357 点赞 / 6245 收藏 / 120 评论 / 863 分享 --- Agent（智能体）是一种能够感知环境、做出决策并采取行动的系统。核心组件包括： - Planning（规划）：任务分解与反思 - Memory（记忆）：短期/长期记忆存储 - Tools（..."
category: "求职作战室"
tags: ["\u6c42\u804c\u4f5c\u6218\u5ba4", "\u9762\u7ecf"]
draft: false
lang: zh-CN
---
# 腾讯 AI 应用开发 一面

**来源**：小红书笔记（作者：逸，2026-04-11）  
**链接**：http://xhslink.com/o/2yiaDG9CXww  
**数据**：3357 点赞 / 6245 收藏 / 120 评论 / 863 分享

---

## 1. 什么是 Agent？

Agent（智能体）是一种能够感知环境、做出决策并采取行动的系统。核心组件包括：

- **Planning（规划）**：任务分解与反思
- **Memory（记忆）**：短期/长期记忆存储
- **Tools（工具）**：调用外部 API、代码执行等
- **Action（执行）**：实际执行操作

---

## 2. Agent 和普通 LLM 应用的区别？

- **普通 LLM 应用**：输入→输出，单轮对话
- **Agent**：具备自主规划、使用工具、多步推理的能力，可以循环执行直到完成任务

---

## 3. 常见的 Agent 框架有哪些？

- **LangChain**：最流行的 Agent 框架，链式调用
- **LlamaIndex**：专注 RAG 和数据索引
- **AutoGPT**：全自动 Agent
- **MetaGPT**：多 Agent 协作
- **CrewAI**：角色扮演多 Agent

---

## 4. 什么是 RAG？

RAG（Retrieval-Augmented Generation）检索增强生成：

1. 将文档切分成 chunks
2. 通过 embedding 模型转为向量
3. 存入向量数据库
4. 用户提问时，先检索相关文档
5. 将检索结果 + 用户问题一起传给 LLM 生成答案

---

## 5. RAG 的关键步骤？

- 文档解析与分块（Chunking）
- 向量化（Embedding）
- 检索（Retrieval）
- 增强生成（Generation）

---

## 6. 常见的 Embedding 模型？

- OpenAI text-embedding-3-small/large
- BGE 系列（BAAI）
- M3E
- Cohere Embed

---

## 7. 常见的向量数据库？

- **Milvus**：开源，高性能
- **Pinecone**：云原生
- **Weaviate**：支持混合搜索
- **Chroma**：轻量级
- **FAISS**：Facebook 开源

---

## 8. 什么是 Prompt Engineering？

通过设计和优化提示词来引导 LLM 生成期望的输出。常见技术：

- Zero-shot / Few-shot
- Chain-of-Thought (CoT)
- ReAct
- Self-consistency

---

## 9. LLM 的关键参数？

- **Temperature**：控制随机性（0=确定，1=随机）
- **Top-p**：核采样概率阈值
- **Max tokens**：最大输出长度
- **Frequency penalty**：重复惩罚

---

## 10. 什么是 Function Calling / Tool Use？

让 LLM 能够调用外部工具：

1. 定义工具的 JSON Schema
2. LLM 决定是否调用、调用哪个工具、传什么参数
3. 系统执行工具并返回结果
4. LLM 基于结果生成最终回答

---

## 11. Agent 中的记忆系统？

- **短期记忆**：当前对话上下文（Context Window）
- **长期记忆**：持久化存储（向量数据库、文件系统）
- **工作记忆**：任务执行过程中的中间状态

---

## 12. 什么是 Multi-Agent？

多个 Agent 协作完成复杂任务：

- 角色分工（研究员、程序员、审核员等）
- 通信机制（消息传递、共享状态）
- 常见模式：顺序执行、并行执行、层级管理

---

## 13. Fine-tuning vs RAG？

| 维度 | Fine-tuning | RAG |
|------|------------|-----|
| 成本 | 高（需要GPU训练） | 低 |
| 更新 | 需要重新训练 | 实时更新 |
| 适用 | 特定风格/格式 | 知识问答 |
| 幻觉 | 可能加剧 | 有参考减少 |

---

## 14. 如何处理 LLM 幻觉？

- RAG 提供参考文档
- 设置 temperature=0
- 要求模型引用来源
- 后处理验证
- 使用 Self-consistency

---

## 15. 如何评估 LLM 应用？

- **自动评估**：BLEU、ROUGE、BERTScore
- **人工评估**：准确性、相关性、流畅性
- **LLM-as-Judge**：用 GPT-4 评分
- **RAG 评估**：检索召回率、答案相关性

---

## 16. 部署 LLM 应用的考虑？

- 延迟优化（流式输出、缓存）
- 成本控制（模型选择、token 限制）
- 可扩展性
- 安全性（输入过滤、输出审查）

---

## 17. AI 安全和对齐问题？

- RLHF（基于人类反馈的强化学习）
- Constitutional AI
- Red Teaming
- 内容过滤和安全护栏

---

## 18. 你有什么想问的？

（面试反问环节建议）

---

*提取自小红书笔记图片（共18页），2026-05-31 整理*
