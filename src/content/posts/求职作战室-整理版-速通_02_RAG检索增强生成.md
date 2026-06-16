---
title: '🚀 速通 · RAG检索增强生成'
published: 2026-06-16
description: '做一个能回答PDF文档内容的问答机器人：'
category: '求职作战室'
tags: ['求职作战室', '整理版']
draft: false
lang: zh-CN
---# 🚀 速通 · RAG检索增强生成

---

## 🎯 你要做到什么级别的小Demo

做一个**能回答PDF文档内容的问答机器人**：

```
你上传一份《AI Agent学习笔记.pdf》
然后问："ReAct模式是什么？"
程序会：
  1. 从PDF中检索相关内容块
  2. 把检索结果作为上下文 + 问题一起发给LLM
  3. LLM基于检索到的内容回答
  4. 返回："ReAct是Reasoning + Acting的缩写，让Agent交替进行推理和行动……"
```

**为什么是这个Demo：** RAG是解决LLM知识局限的标配方案，几乎每个岗位都要求。面试官会问"你做过RAG吗"，你直接说"我搭过一个完整的RAG管道"——立马拉开差距。

---

## 📄 核心代码框架（逐行解释）

```python
# ===== 第1步：导入库 & 准备文档 =====
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 解释：整个RAG管道分为5步：加载 → 分割 → 向量化 → 检索 → 生成

# ===== 第2步：加载文档 =====
loader = PyPDFLoader("你的文档.pdf")         # 支持PDF、网页、Markdown等
documents = loader.load()                     # 返回Document对象列表
# 解释：LangChain的Loader统一了各种数据源，PDF自动解析文本

# ===== 第3步：分割文本 =====
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,          # 每块500字符
    chunk_overlap=50,        # 块之间有50字符重叠，保证上下文不割裂
    separators=["\n\n", "\n", "。", "!", "？", " ", ""]   # 优先按段落/句号分割
)
chunks = text_splitter.split_documents(documents)
# 解释：chunk_size决定了检索的粒度，太大会包含无关信息，太小会丢失上下文。
# overlap是为了避免刚好切在关键句中间。separators优先级保证尽量在语义边界分割。

# ===== 第4步：向量化 + 存入向量库 =====
embedding = OpenAIEmbeddings(model="text-embedding-3-small")   # 把文本变成向量
vectorstore = Chroma.from_documents(                          # Chroma是本地向量库
    documents=chunks,
    embedding=embedding,
    persist_directory="./chroma_db"           # 持久化到磁盘，下次不用重新计算
)
# 解释：向量库把每个chunk转为高维向量，检索时把问题也转成向量，找最相似的chunk

# ===== 第5步：构建检索链 =====
retriever = vectorstore.as_retriever(
    search_type="similarity",      # 也可以mmr（最大边际相关性）增加多样性
    search_kwargs={"k": 4}         # 返回最相似的4个chunk
)

# ===== 第6步：组装RAG Chain =====
# 提示词模板：把检索到的context和问题组装起来
prompt = ChatPromptTemplate.from_template("""
你是一个文档问答助手，请基于以下上下文回答用户的问题。
如果你不知道答案，就说"我没找到相关信息"，不要编造。

上下文：
{context}

问题：{input}
""")

# combine_documents_chain：负责把检索到的多个文档合并、格式化后喂给LLM
combine_docs_chain = create_stuff_documents_chain(
    llm=chat,                    # 你的LLM实例（见速通01）
    prompt=prompt
)

# retrieval_chain：接收问题 → 自动检索 → 传给combine_docs_chain
rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

# ===== 第7步：查询 =====
result = rag_chain.invoke({"input": "ReAct模式是什么？"})
print(result["answer"])
# 解释：invoke后，内部自动完成：检索4个chunk → 合成prompt → 调用LLM → 生成回答
```

**这个Demo你写完，面试官问RAG你直接无敌：**
- 你能说清楚 `chunk_size/chunk_overlap` 怎么选
- 你能解释 `similarity` vs `mmr` 检索的区别
- 你能说出向量数据库是把文本变向量再做相似度搜索
- 你能描述整个"加载→分割→向量化→检索→生成"管道

---

## ❓ 面试官最爱问的3个问题

| 问题 | 满分回答要点 |
|:----|:-----------|
| **1. 为什么RAG比直接微调模型更常用？** | ① 无需训练成本，快速适配新数据 ② 数据更新只需换向量库，不用重新训练模型 ③ 可追溯信息来源，降低幻觉 ④ 保留原始知识，不丢失模型原有能力。 |
| **2. 检索效果不好怎么办？你会怎么优化？** | ① 调整分块策略（chunk_size、overlap、语义分块） ② 改用混合检索（稠密+稀疏如BM25） ③ 加Query改写（HyDE让问题变成假设性回答再检索）④ 加ReRanker重排序 ⑤ 针对专业领域微调Embedding模型。 |
| **3. 如何评估RAG系统的好坏？** | 分两部分：① **检索评估**：准确率、召回率、MRR（平均排序倒数），看是否把相关文档排前面 ② **生成评估**：答案准确性、忠实度（是否基于给定上下文）、有用性。可以用LLM-as-Judge自动化评分。 |

---

**⏱ 练熟这个Demo预计时间：** 1天（已有LLM调用基础的话）
**有了它你能在面试中展示：** 完整RAG管道、分块策略理解、检索优化意识、工程化能力。
