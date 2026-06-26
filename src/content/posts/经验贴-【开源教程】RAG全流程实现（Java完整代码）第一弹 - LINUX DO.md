---
title: '【开源、教程】RAG全流程实现（Java+完整代码）：第一弹'
published: 2026-06-26
description: '本教程环境基于 JDK8 + LangChain4j 0.35，共三弹：'
category: '经验贴'
tags: ['经验贴']
draft: false
lang: zh-CN
---# 【开源、教程】RAG全流程实现（Java+完整代码）：第一弹

> **来源：** LINUX DO 社区 · 资源荟萃  
> **作者：** worenbudaoni（我认不到你）  
> **发布于：** 2026年6月10日  
> **链接：** https://linux.do/t/topic/2364008  
> **标签：** `开源推广` `人工智能` `软件开发` `教程` `原创` `Java`  

---

## 📋 文章系列

本教程环境基于 **JDK8 + LangChain4j 0.35**，共三弹：

| 篇目 | 内容 |
|:---:|:---:|
| 🟢 **第一弹** ✅ 本文 | RAG 实现全流程 |
| 🔵 第二弹 | 接入飞书 WIKI 文档 |
| 🟠 第三弹 | 接口限流：令牌桶 + AOP |

**源码：** [GitHub - worenbudaoni/rag-study-helper](https://github.com/worenbudaoni/rag-study-helper)

---

## 一、核心概念快速科普

| 概念 | 大白话解释 |
|:---|:---|
| **RAG**（检索增强生成） | 先从知识库检索相关信息，再"喂"给大模型，让它基于事实生成答案 |
| **Embedding**（文本嵌入模型） | 将文本转换为固定长度的向量，语义相似的内容在向量空间中距离更近 |
| **Reranker**（重排序模型） | 对初步检索结果二次精排，根据相关性重新打分排序 |
| **向量** | 文本/数据转换成的数值数组，如 `[0.1, 0.5, -0.2, ...]` |
| **向量数据库** | 专门存储和检索向量的数据库，支持余弦相似度等高效搜索 |

---

## 二、RAG 通用实现思路

### 📥 入库流程

```
文件 → 分割器 → Embedding → 向量数据库（入库）
```

- **文件**：Word、PDF、PPT、MD、Excel、图片 → 通过 POI、OCR 转成字符串
- **分割器**：把长文本拆解成文本段，避免大段无关内容混淆 LLM 回答
- **Embedding**：将文本段转为向量
- **向量数据库**：存储文本段 + 向量（可附加 Metadata 做权限管控）

### 📤 提问流程

```
问题 → 问题重写 → Embedding → 向量数据库（匹配出库）
  → 相关性筛选 → Rerank → Prompt优化（文本段+问题） → LLM回答
```

**关键环节详解：**

- **问题重写**：当用户问"他有什么好处"时，Embedding 不知道"他"指代什么，需要让 LLM 根据上下文重写问题（本例规则：提问 <5 字且包含"他/她/它/上述"时触发重写）
- **相关性筛选**：设置余弦相似度阈值（本例设为 0.77），过滤掉不相关结果
- **Rerank**：从 Top 20 中精排选出最相关的 3-5 条，提升上下文质量、节省 Token

---

## 三、代码实践（逐段详解）

### ① 配置 LangChain4j + Embedding 模型 + 向量数据库

**LangChain4jConfig.java** 中配置了三套向量数据库方案：

| 类型 | 场景 | 说明 |
|:---|:---|:---|
| **InMemory** | 本地测试 | 程序退出即丢失，**生产不要用** |
| **Chroma** | 中小型项目 | 零配置，部署极简，支持百万级向量 |
| **Milvus** | 大型项目 | 分布式云原生，十亿级向量，支持水平扩展与分片 |

LLM 和 Embedding 模型均选择支持 OpenAI API 的模型，替换配置即可。

### ② 入库流程：文件解析 → 分割器 → Embedding → 向量数据库

核心方法 `DocumentIngestionService.java`：

```
文件判重（SHA256）→ 解析文档 → 分割器切割
  → Embedding 分批转换（每批10条） → 存入向量数据库
  → 关系型数据库记录文档和分片信息
```

**分割器关键参数：**
- 基于 Token 的递归分割器（`DocumentSplitters.recursive`）
- 单段最大 Token：`512 - 文件名前缀Token数`
- 段落重叠 Token：51（约 10%-20%）
- Embedding 模型：`bge-large-zh-v1.5`（512 Token上限，免费）

### ③ 提问流程：问题重写 → Embedding → 检索 → 筛选 → Rerank → 回答

核心方法 `RagQueryService.java`：

```java
1. 获取历史上下文
2. 判断是否需要问题重写
3. Embedding 转换查询向量
4. 向量数据库检索 Top 20
5. 余弦相似度阈值过滤
6. Rerank 精排取 Top 5
7. 构建 Prompt → LLM 流式生成答案
8. 保存上下文
```

**Rerank 实现**（`RerankService.java`）：调用 SiliconFlow 的 rerank API，根据 query 对文档片段重新排序。

---

## 四、模型选型推荐

### Embedding 模型对比

| 模型 | 维度 | 最大上下文 | 特点 |
|:---|:---:|:---:|:---|
| **BAAI/bge-large-zh-v1.5** ✅ 项目选用 | 1024 | 512 tokens | C-MTEB 榜首，免费 |
| Youtu-Embedding（腾讯） | ~2048 | ~512-8k | C-MTEB 77.46 |
| Qwen3-Embedding（阿里） | 2048 | ~8k-32k | 同尺寸 SOTA |
| GLM-Embedding（智谱） | 1024 | 8k tokens | 中文召回率 83.5% |
| text-embedding-3-large（OpenAI） | 3072 | 8k tokens | 国际化应用 |

### Reranker 模型对比

| 模型 | 最大上下文 | 场景 |
|:---|:---:|:---|
| **BAAI/bge-reranker-v2-m3** ✅ 项目选用 | 8192 | 自托管性价比首选 |
| Qwen3-Reranker-8B | 32768 | 多语言，顶级精度 |
| Cohere Rerank v4 | 32768 | 商业便捷 |
| Jina Reranker v3 | 131072 | 超长文档处理 |

### 向量数据库对比

| 数据库 | 类型 | 场景 |
|:---|:---|:---|
| Chroma | 开源 | 原型验证、小型项目 |
| Milvus | 开源 | 企业级生产系统 |
| Pinecone | 商业 | 追求极简运维 |
| Qdrant | 开源 | 高并发低延迟 |
| Pgvector | 扩展 | 已在用 PG 的轻量 RAG |

---

## 五、后续优化方向

1. **Embedding 模型**：选择维数多、上下文大的模型
2. **Reranker 模型**：选择上下文大的模型
3. **权限管控**：RBAC 模型，文档分配角色→用户，MetaData 过滤
4. **Milvus**：使用**稠密向量 + 稀疏向量**混合搜索，结果更精准
5. **上下文持久化**：推荐 LLM 生成后异步存入关系型数据库（按 sessionId+userId）
6. **文件解析**：OCR 处理扫描版 PDF 和图片

---

## 💡 核心结论

> **Embedding 模型不能随意切换**——换模型后向量输出不同，之前入库的数据就报废了！

> **不要把所有 schema 都塞给模型**——先判断 domain → dataset → table → 压缩 column → 最后注入 metric definition

> **分割器没有银弹**——最合适才最重要！

---

*本文由 AI 助手根据 LINUX DO 社区帖子内容整理，仅供学习参考。*  
*社区链接：https://linux.do/t/topic/2364008*
