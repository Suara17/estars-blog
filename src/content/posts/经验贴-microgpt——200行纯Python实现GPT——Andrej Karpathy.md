---
title: 'microgpt——200行纯Python实现GPT'
published: 2026-06-17
description: '作者：Andrej Karpathy'
category: '外部精选'
tags: ['外部精选', '外文翻译']
draft: false
lang: zh-CN
---# microgpt——200行纯Python实现GPT

**作者**：Andrej Karpathy  
**发布**：2026年2月12日 · karpathy.github.io  
**原文链接**：https://karpathy.github.io/2026/02/12/microgpt/  
**源码**：https://gist.github.com/karpathy/***（microgpt.py）

---

这是我对我的新艺术项目 **microgpt** 的简要介绍——一个单文件、200行纯 Python、零依赖，就能训练和推理 GPT 的库。这个文件包含了所需的全部算法内容：文档数据集、分词器、自动求导引擎、类 GPT-2 神经网络架构、Adam 优化器、训练循环和推理循环。除此之外的一切都只是效率优化。

这是我无法再简化的极致。这个脚本是多个项目（**micrograd、makemore、nanogpt** 等）的集大成者，也是我十年来痴迷于将 LLM 精简到最本质核心的成果。我觉得它很美 🥹。

它甚至完美地分成了三栏。

---

## 为什么是 microgpt？

大语言模型（如 GPT-4、Claude）的核心知识可以压缩到一个文件里。当然，生产级系统还需要分布式训练、推理优化、数据管道等——但所有这些都只是效率工程。

microgpt 的目标是展示：**GPT 的本质是什么**。用 200 行 Python，你将看到：
- 数据集如何准备
- 分词器如何工作
- 自注意力机制怎么实现
- 训练循环如何运行
- 推理（生成文本）怎么完成

---

## 一、数据集

大型语言模型的燃料是文本数据流。在生产级应用中，每个文档是一张网页。在 microgpt 里，我们用 32,000 个人名作为数据集，每行一个：

```python
docs = [l.strip() for l in open('input.txt').read().strip().split('\n') if l.strip()]
```

数据集看起来像：
```
emma
olivia
ava
isabella
sophia
charlotte
mia
amelia
harper
...
```

模型的目标是学习数据中的统计模式，然后生成相似的新文档。最终模型会"幻觉"出听起来合理的新名字：`kamon`、`karai`、`karia`、`anna`、`kaina`……

从 ChatGPT 的角度看，你和它的对话也不过是一个"看起来有点滑稽的文档"。当你用提示词初始化文档时，模型的响应在它看来只是统计性的"文档补全"。

---

## 二、分词器

神经网络处理数字而非字符，所以我们需要一种在文本和整数 token ID 序列之间转换的方式。

最简单的方式是给数据集中每个唯一字符分配一个整数：

```python
uchars = sorted(set(''.join(docs)))
# 每个字符成为一个 token ID，0 到 n-1
```

再创建一个特殊的 **BOS（Beginning of Sequence）** token，告诉模型"文档在此开始/结束"。

---

## 三、自注意力机制

microgpt 实现了一个简化版的 GPT-2 架构。核心是**自注意力机制**：

```python
def self_attention(x):
    # x: (B, T, C) - batch, time, channels
    # 1. 将输入映射为 Q、K、V
    q = x @ W_q
    k = x @ W_k
    v = x @ W_v
    # 2. 计算注意力分数
    attn = softmax(q @ k.T / sqrt(d_k), dim=-1)
    # 3. 加权聚合价值
    out = attn @ v
    return out
```

这个简单机制让模型能够"关注"输入序列的不同位置——这是 GPT 理解上下文的核心能力。

---

## 四、训练

使用标准的 Adam 优化器，在字符级语言模型上进行训练。损失函数是交叉熵——衡量模型对下一个 token 预测的不确定性。

不需要 GPU，这个简单的示例在 CPU 上几秒钟就能跑起来，看到效果。

---

## 五、推理

训练完成后，模型可以逐个 token 地生成新文本：给定已生成的前缀，预测下一个 token 的概率分布，采样得到下一个 token，重复直到产生终止 token。

---

## microgpt 的哲学

这个项目的核心理念是：**理解一个东西的最好方式是从头实现它**。当你把 GPT 的核心代码压缩到 200 行，每一行都承载着不可删除的语义。

microgpt 不适合生产——但很适合学习。如果你曾经对"ChatGPT 是怎么工作的"感到好奇，这个 200 行的文件就是你需要的完整答案。

> *"Everything else is just efficiency."* —— Andrej Karpathy
>
> *"除此之外的一切都只是效率优化。"*

---

**哪里找到它：**
- GitHub Gist：[microgpt.py](https://gist.github.com/karpathy/...)
- 网页版：https://karpathy.ai/microgpt.html
- Google Colab notebook
- 艺术商店：https://karpathy.art（三连画印刷版）
