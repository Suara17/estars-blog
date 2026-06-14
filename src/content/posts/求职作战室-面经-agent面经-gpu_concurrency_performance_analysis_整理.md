---
title: "GPU_Concurrency_Performance_Analysis"
published: 2026-06-14
description: "GPU_Concurrency_Performance_Analysis"
category: "求职作战室"
tags: ['求职作战室', '面经']
draft: false
lang: zh-CN
---

# GPU_Concurrency_Performance_Analysis
## 问题
GPU_Concurrency_Performance_Analysis

## 标准回答

# GPU集群并发访问性能分析：为什么不是简单平均？
不会简单平均成每人 1 token/s，每个用户实际看到的响应速度可能是几十 token/s。LLM 推理不是把算力切成 1000 份分给 1000 个用户，而是靠批处理（Batching）把多个请求打包到一起算。GPU 擅长并行计算，100 个请求打成一个 batch，计算耗时与处理单个请求接近，吞吐量直接翻几十倍。

假设每次批处理包含 100 个用户的请求，每个用户请求 10 tokens，1000 个用户分 10 批处理完，单用户实际体验的速度是 10 tokens/s。

实际响应速度取决于三个核心因素：请求的 token 长度、batch 大小策略、排队调度机制。

---

## 扩展知识

### 1. 请求聚合与调度机制
LLM 推理每次 forward 只生成 1 个 token，然后循环生成下一个。1000 个用户同时请求，GPU 每轮同时计算这 1000 个请求的下一个 token。需要请求聚合器协调：
- 把同时到达的请求按 token 长度打包，短的补齐到相同长度，打成一个矩阵扔给 GPU
- 设置聚合窗口（如每 5ms 或攒够 32 个请求），平衡效率与延迟
- 控制粒度是 token-level batching，同一时刻处理所有请求的当前 token，再一起推进

### 2. 动态调度与优先级
请求进入异步队列，调度器决定处理顺序：
- 优先级策略：付费用户优先、重试请求优先、token 少的先算完让出位置
- 负载均衡：显存吃紧时减小 batch size，空闲时加大 batch
- 动态退场：已生成完的请求退出 batch，新请求插入，流水线持续运转

### 3. 实际场景分析
聊天机器人平台：1000 用户并发，请求平均 20 tokens，GPU 最大 batch 128，吞吐 1000 tokens/s。
- 每 10ms 打一批，聚合 50~100 个请求
- 所有请求每生成一个 token 进入下一轮调度
- pipeline 里同时跑多个 batch，每个 batch 装不同用户的不同 token
- 最终每个用户响应速度几十 token/s

### 4. 性能瓶颈分析思路
- **显存瓶颈**：KV Cache 占用大，batch size 上不去 → 看 nvidia-smi 显存占用
- **计算瓶颈**：GPU 利用率满但吞吐低 → 模型太大或 batch 太小
- **调度瓶颈**：队列堆积严重 → 看请求排队时间
- **网络瓶颈**：分布式推理节点间通信慢 → 看 NCCL 耗时占比

vLLM、TensorRT-LLM 等框架提供 metrics 接口，可观察 batch size 分布、排队延迟、吞吐曲线。

---

## 面试官追问

### Q1：vLLM 的 PagedAttention 机制怎么优化显存利用率？
**A**：传统做法预分配最大长度 KV Cache，浪费严重。PagedAttention 把 KV Cache 切成固定大小 block，按需分配，类似虚拟内存。显存利用率从 20~30% 提升到 90% 以上。

### Q2：Continuous Batching 和 Static Batching 区别？
**A**：Static Batching 等一批请求全部生成完才处理下一批，短请求需等长请求。Continuous Batching 动态调度，短请求生成完就退出，新请求立即插入，吞吐提升 2~3 倍。

### Q3：First Token Latency 和 Time Per Output Token 怎么优化？
**A**：First Token Latency 受 prefill 阶段影响，优化方向为 prompt 压缩、KV Cache 预计算、prefill/decode 分离。Time Per Output Token 受 decode 阶段影响，优化方向为加大 batch size、speculative decoding、量化。

### Q4：模型量化对性能影响？INT8 和 FP16 怎么选？
**A**：FP16 比 FP32 快一倍，INT8 再快一倍但精度可能下降。高精度场景用 FP16，极致吞吐且接受轻微效果损失用 INT8。混合精度 attention 用 FP16、FFN 用 INT8 是折中方案。AWQ、GPTQ 等方案精度损失更小。

## 

## 关键点

- # GPU集群并发访问性能分析：为什么不是简单平均？
- ## 核心回答

不会简单平均成每人 1 token/s，每个用户实际看到的响应速度可能是几十 token/s。
- LLM 推理不是把算力切成 1000 份分给 1000 个用户，而是靠批处理（Batching）把多个请求打包到一起算。
- GPU 擅长并行计算，100 个请求打成一个 batch，计算耗时与处理单个请求接近，吞吐量直接翻几十倍。
- 假设每次批处理包含 100 个用户的请求，每个用户请求 10 tokens，1000 个用户分 10 批处理完，单用户实际体验的速度是 10 tokens/s。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

GPU_Concurrency_Performance_Analysis

- ## 核心回答

不会简单平均成每人 1 token/s，每个用户实际看到的响应速度可能是几十 token/s。LLM 推理不是把算力切成 1000 份分给 1000 个用户，而是靠批处理（Batching）把多个请求打包到一起算。GPU 擅长并行计算，100 个请求打成一个 batch，计算耗时与处理单个请求接近，吞吐量直接翻几十倍。
- 假设每次批处理包含 100 个用户的请求，每个用户请求 10 tokens，1000 个用户分 10 批处理完，单用户实际体验的速度是 10 tokens/s。
- 实际响应速度取决于三个核心因素：请求的 token 长度、batch 大小策略、排队调度机制。
- ---

LLM 推理每次 forward 只生成 1 个 token，然后循环生成下一个。1000 个用户同时请求，GPU 每轮同时计算这 1000 个请求的下一个 token。需要请求聚合器协调：
- 把同时到达的请求按 token 长度打包，短的补齐到相同长度，打成一个矩阵扔给 GPU
- 设置聚合窗口（如每 5ms 或攒够 32 个请求），平衡效率与延迟
- 控制粒度是 token-level batching，同一时刻处理所有请求的当前 token，再一起推进

请求进入异步队列，调度器决定处理顺序：
- 优先级策略：付费用户优先、重试请求优先、token 少的先算完让出位置
- 负载均衡：显存吃紧时减小 batch size，空闲时加大 batch
- 动态退场：已生成完的请求退出 batch，新请求插入，流水线持续运转

聊天机器人平台：1000 用户并发，请求平均 20 tokens，GPU 最大 batch 128，吞吐 1000 tokens/s。

- 本文已做格式统一与噪声清理，保留原始语义。
- 不会简单平均成每人 1 token/s，每个用户实际看到的响应速度可能是几十 token/s。LLM 推理不是把算力切成 1000 份分给 1000 个用户，而是靠批处理（Batching）把多个请求打包到一起算。GPU 擅长并行计算，100 个请求打成一个 batch，计算耗时与处理单个请求接近，吞吐量直接翻几十倍。
- 假设每次批处理包含 100 个用户的请求，每个用户请求 10 tokens，1000 个用户分 10 批处理完，单用户实际体验的速度是 10 tokens/s。
- 实际响应速度取决于三个核心因素：请求的 token 长度、batch 大小策略、排队调度机制。
- ### 1. 请求聚合与调度机制
- LLM 推理每次 forward 只生成 1 个 token，然后循环生成下一个。1000 个用户同时请求，GPU 每轮同时计算这 1000 个请求的下一个 token。需要请求聚合器协调：

- 本文已做格式统一与噪声清理，保留原始语义。