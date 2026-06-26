---
title: '用 Agent 架构做批发订单系统——一个实战复盘'
published: 2026-06-16
description: 'title: 用 Agent 架构做批发订单系统——一个实战复盘'
category: '工程现场'
tags: ['工程现场', '实战', '经验']
draft: false
lang: zh-CN
---# 用 Agent 架构做批发订单系统——一个实战复盘

## 起因

朋友做批发生意，有几百个客户微信群，24 小时随时可能有人下单。

下单的方式五花八门——有人发"10 件"，有人发"跟昨天一样"，有人发"加 3 件"，有人先说 8 件过会儿又说"改成 7 件"。每个群的说话习惯不一样，角色关系不一样（有的群老板先报预估数、实际经营者后来说的才算），规格默认值也不一样。需要有人 24 小时盯着群，手敲 Excel——漏单、错单、重复记是常态。

## 第一版：Parser 方案（失败）

第一版我写了 parser——正则匹配数字、规则引擎判断消息类型。写了 2000 行，发现根本兜不住。

"加 3 件"是加单，"3 件"可能是新单也可能是回答"你今天要多少"，"后面为准"意味着之前的数字作废。每个群的规矩不一样，规则越写越多，改一个崩三个。

后来想明白了：这些判断本质上是在理解人在说什么，这正是 LLM 擅长的事。

## 第二版：Agent 方案

推倒重来，用 Agent 架构重写——不写 parser，让 LLM 直接理解消息，调 tool 记录结果。

整个系统分三层：

```
Gateway（入口）→ Core / Harness（引擎）→ Capabilities（业务）
```

### 设计原则：Harness 是空壳

Core 是引擎，不知道自己在处理什么业务。它只做一件事：把消息给 LLM → LLM 说调 tool 就调 → 结果喂回去 → 循环。搜遍 core/ 目录，找不到任何业务词汇。这意味着换一个行业（物流、餐饮、零售），core/ 一行不改。

Capabilities 是业务层，放所有具体的东西——订单模型、数据库、5 个 tool、群画像。加新功能 = 写新文件 + 注册，永远不改已有文件。

### core/ 目录结构

```
core/                    # 无业务，通用引擎
├── agent.py             # while 循环
├── registry.py          # tool 注册表
├── session.py           # 对话上下文
├── llm.py               # LLM 接口
├── events.py            # 事件总线
├── types.py             # 基础类型
└── config.py            # 配置

capabilities/            # 纯业务
├── domain/models.py     # 领域模型
├── store/               # SQLite
├── tools/               # 5 个 tool
├── context/             # 提示词
├── memory/groups/       # 群画像
└── extensions/          # 扩展
```

## 扩展性设计的思路

系统的扩展性不是靠复杂的插件框架，而是靠 **一致的注册模式**：写文件 + 注册。

### 5 种扩展方式

| 方式 | 操作 | 说明 |
|------|------|------|
| 加 Tool | 写新 tool 文件 | LLM 自动知道有这能力可用 |
| 加群画像 | 写新 .md 文件 | 处理该群时自动注入 prompt |
| 加 Extension | 写新 .py 文件 | 数据管道的变换环节 |
| 换 Gateway | 改入口 | 只换数据源，其余不动 |
| 换业务 | 换 capabilities/ | core/ 不动 |

**Tool 的本质：** LLM 读到消息后自己判断要不要调、调哪个、传什么参数。代码不做这个判断——没有 if/elif 消息分类，没有正则匹配。LLM 就是 parser。

**Extension 的设计原则：** 纯函数，零 core 依赖。输入是什么、输出是什么，可以独立测试。不 import core/ 的任何东西。

### 3 种集成方式

**Skill** —— 领域知识 + 操作流程的封装。不是代码，是结构化的 markdown。复核订单的 skill 会告诉 LLM：先查今天所有待审查订单 → 逐条跟原始消息比对 → 确认或修正。

**Context** —— 运行时动态注入的 prompt 片段。群画像、今日订单汇总都在不同时机注入。

**EventBus** —— 模块间松耦合通信。Tool A 记录订单后发事件，审查模块、审计模块各自订阅。

## 踩过的模型坑

**Tool calling 死循环** — qwen3.6 的 assistant message 同时带分析文字和 tool_calls，LLM 看到自己写了"需记录"以为还没处理完就又调一遍。修复一行：有 tool_calls 时丢弃 content。

**Thinking 模式慢** — qwen3.6 默认开 thinking，53% token 花在内部推理上。简单 4 条消息从 9 秒变 33 秒。tool calling 场景不需要 thinking。

**Max tokens 截断** — 2048 太小输出被截断，增到 4096 搞定。

## Prompt 排列顺序的影响

按这个顺序给 LLM：

1. **business.md**（行业常识，固定不变）
2. **role.md**（角色设定）
3. **群画像**（per-group 知识）
4. **当天的消息**（每次不同）

两个原因：一是注意力 U 型分布（开头结尾注意力最高），二是 KV Cache 复用（越不常变的放越前面，缓存利用率越高）。

## 持续质疑复杂度

每加一个抽象层之前问：真的需要吗？

- Parser 基类？不需要，LLM 直接理解
- Tool 基类？不需要，`register()` 函数就够了
- 状态机？不需要，agent loop 是简单 while 循环
- EventBus hook chain？暂时不需要，只有 1 个消费者

## Reviewer Skill —— 用清单约束设计

每次写完一个阶段，跑一遍审查清单：

1. 🔗 解耦 — `grep "from capabilities" core/` 必须为空
2. 📌 SSOT — 每个概念只定义一次
3. 🔌 扩展性 — 加功能只加文件不改已有
4. 🕳️ Harness 空壳 — core/ 零业务字符串
5. 🧠 输入信任 LLM — 输入侧不用 enum
6. 📊 行业知识纯度 — business.md 换个行业仍成立
7. 🏷️ Tool 意图命名 — action+target
8. 🚫 代码不做 LLM 该做的事 — handler 里没有正则分类
9. 🌐 通用性 — 换业务只改 capabilities/
10. ✅ 真实数据验证 — 用真实消息验证

## 小结

这个项目本质上是把 Agent 框架的架构思想，从编程场景搬到了业务数据处理场景。代码核心不到千行，但扩展性比 2000 行 parser 好得多——因为正确的抽象比代码量重要。
```