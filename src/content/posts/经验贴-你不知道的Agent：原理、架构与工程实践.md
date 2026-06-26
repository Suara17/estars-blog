---
title: '你不知道的 Agent：原理、架构与工程实践'
published: 2026-06-26
description: '整理下来，有几处判断和原来想的不太一样：'
category: '经验贴'
tags: ['经验贴']
draft: false
lang: zh-CN
---# 你不知道的 Agent：原理、架构与工程实践

> **作者：** Tw93 @HiTw93  
> **来源：** https://x.com/i/status/2034627967926825175 / https://tw93.fun/2026-03-21/agent.html  
> **发布时间：** 2026年3月21日  
> **浏览量/互动：** 5160+ 赞  
> **保存时间：** 2026年6月19日  

---

> 在写完「你不知道的 Claude Code：架构、治理与工程实践」之后，发现自己对 Agent 底层的理解还不够深入，加上团队在 Agent 方向已经有不少业务落地经验，一直缺少一份系统梳理，所以我又把资料、开源实现和自己写的代码一起过了一遍，最后整理成了这篇文章。

---

## 📑 太长不读

整理下来，有几处判断和原来想的不太一样：
- **更贵的模型带来的提升，很多时候没有想象中那么大**
- **Harness 和验证测试质量对成功率的影响更大**
- 调试 Agent 时，应**优先检查工具定义**，多数工具选择错误都出在描述不准确
- **评测系统本身的问题，很多时候比 Agent 出问题更难发现**

---

## 📖 一、Agent Loop 的基本运转方式

核心实现逻辑抽象后不到 20 行代码——感知 → 决策 → 行动 → 反馈，循环直到模型返回纯文本。

**新能力只通过三种方式接入：**
1. 扩展工具集和 handler
2. 调整系统提示结构
3. 把状态外化到文件或数据库

> **原则：模型负责推理，外部系统负责状态和边界。**

---

## 📖 二、Workflow 和 Agent 有什么区别

| 维度 | Workflow | Agent |
|:---|:---|:---|
| 控制权 | 代码预定义，同输入必走同一路径 | LLM 动态决策 |
| 执行方式 | 工具顺序固定 | 工具按需选择 |
| 状态与记忆 | 显式状态机 | 隐式上下文 |
| 维护成本 | 改流程需改代码部署 | 调系统提示即可 |
| 可观测性 | 日志定位节点 | 需完整执行记录 |
| 适用场景 | 流程固定、输入边界清晰 | 需要中间推理与灵活判断 |

---

## 📖 三、五种常见控制模式

| 模式 | 说明 | 适合场景 |
|:---|:---|:---|
| **提示链 Prompt Chaining** | 任务拆成顺序步骤，中间可加代码检查点 | 翻译、先写大纲再写正文 |
| **路由 Routing** | 对输入分类定向到对应处理流程 | 简单/复杂问题分流 |
| **并行 Parallelization** | 分段发或投票法 | 高风险决策或多视角 |
| **编排器-工作者 Orchestrator-Workers** | 中央 LLM 分解任务，委派工作者 | 任务可拆、子任务可并行 |
| **评估器-优化器 Evaluator-Optimizer** | 生成器产出，评估器给反馈，循环达标 | 翻译、创意写作 |

> **选型看两件事：任务确定性和验证能不能自动化。**

---

## 📖 四、为什么 Harness 比模型更关键

Harness 是指围绕 Agent 构建的**测试、验证与约束基础设施**，包括四部分：验收基线、执行边界、反馈信号和回退手段。

### OpenAI 的 Agent 优先开发实践：3 个工程师 5 个月写了百万行代码

核心工程决策：
1. **Agent 看不到的内容等于不存在** — 知识必须在代码库本身
2. **约束编码化而非文档化** — 编码进 Linter 或 CI 的约束才可执行
3. **Agent 端到端自主完成任务** — 全链路不需要人介入
4. **最小化合并阻力** — 测试偶发失败用重跑处理，不阻塞进度

> **右上角（目标明确 + 结果可自动验证）是最适合 Agent 发挥的区域。**

---

## 📖 五、上下文工程为什么决定稳定性

### 上下文分层

| 层 | 内容 | 特点 |
|:---|:---|:---|
| 常驻层 | 身份定义、项目约定、禁止项 | 短、硬、可执行 |
| 按需加载 | Skills 和领域知识 | 描述符常驻，触发时注入 |
| 运行时注入 | 当前时间、渠道 ID、用户偏好 | 每轮按需拼入 |
| 记忆层 | 跨会话经验（MEMORY.md） | 需要时才读取 |
| 系统层 | Hooks 或代码规则 | 完全不进上下文 |

### 三种压缩策略

| 策略 | 成本 | 适用场景 |
|:---|:---|:---|
| 滑动窗口 | 极低 | 简短对话 |
| LLM 摘要 | 中 | 长任务、含关键决策 |
| 工具结果替换 | 极低 | 工具调用密集型 |

### 会话管理的五种分支

| 方式 | 说明 |
|:---|:---|
| **continue** | 继续发消息，最容易滥用 |
| **rewind** | 回到之前某一轮重来 |
| **clear** | 新开 session，写简报 |
| **compact** | 让模型摘要继续 |
| **subagents** | 委派独立上下文子 Agent |

> **出错时 rewind 往往比 correct 更稳。** 错误路径留在上下文里会继续干扰推理。

---

## 📖 六、Prompt Caching 减少重复开销

- 命中的前提是**精确前缀匹配**
- 系统提示、工具定义、长文档天然适合缓存
- 动态信息放后面，不影响前缀稳定性
- **稳定的大系统提示，比频繁变动的小提示实际成本更低**（写入成本只付一次，后续折扣可达 90%）

---

## 📖 七、为什么 Skills 要按需加载

### Skill 描述要包含反例

> 没有反例时准确率从 73% 掉到 53%，加上反例后升到 85%，响应时间还降了 18.1%。

### Skill 描述优化
```yaml
# 低效（~45 tokens）
description: 很长的一段功能介绍...

# 高效（~9 tokens）
description: Use when deploying to production or rolling back.
```

### Compact Instructions 模板
```markdown
保留优先级：
1. 架构决策，不得摘要
2. 已修改文件和关键变更
3. 验证状态，pass/fail
4. 未解决的 TODO 和回滚笔记
5. 工具输出，可删，只保留 pass/fail 结论
```

---

## 📖 八、工具设计决定 Agent 能做什么

### ACI（Agent-Computer Interface）原则

| 维度 | 好工具 | 差工具 |
|:---|:---|:---|
| 粒度 | 对应 Agent 要完成的目标 | 对应 API 能做的操作 |
| 返回 | 与下一步决策相关的字段 | 完整原始数据 |
| 错误 | 结构化，含修正建议 | 通用字符串 "Error" |
| 描述 | 说明何时用、何时不用 | 只写功能说明 |

### 工具设计三阶段演进

1. **第一代：API 封装** — 粒度过细
2. **第二代：ACI** — 工具应对应 Agent 的目标
3. **第三代：Advanced Tool Use**
   - **Tool Search**：动态工具发现，上下文保留率 95%
   - **Programmatic Tool Calling**：代码编排，token 从 150K 降到 ~2K
   - **Tool Use Examples**：示例驱动，准确率从 72% 提升到 90%

---

## 📖 九、记忆系统如何设计

### 四种记忆
| 类型 | 说明 | 存储 |
|:---|:---|:---|
| 工作记忆 | 当前任务最小信息 | 上下文窗口 |
| 程序性记忆 | 怎么做某事 | Skills 文件 |
| 情景记忆 | 发生了什么 | JSONL 会话历史 |
| 语义记忆 | 重要事实 | MEMORY.md |

### 记忆整合触发
tokenUsage / maxTokens >= 0.5 时触发：
- **成功**：摘要追加到 MEMORY.md
- **失败**：原始消息写入 archive/ 保留完整历史

---

## 📖 十、如何逐步放开 Agent 自主度

### 放权顺序（不能反）
1. **Harness** — 验收基线、执行边界、反馈信号、回退手段
2. **回退能力** — Provider 切换、工作空间隔离、白名单、审计日志
3. **放权** — 敏感操作显式确认、关键路径加独立 LLM 复核

### 长任务跨 session 继续
- **Initializer Agent**：生成 feature-list.json、init.sh、claude-progress.txt
- **Coding Agent**：从文件恢复现场，实现功能，跑测试，更新状态
- **进度放在文件里，不要放在上下文里**

---

## 📖 十一、多 Agent 如何组织

### 子 Agent 通信协议
```js
{
  request_id, from_agent, to_agent,
  content, status: 'pending' | 'approved' | 'rejected',
  timestamp
}
```

- 写入 `.team/inbox/{agentId}.jsonl`，append-only，崩溃可恢复
- 子 Agent 只回传摘要，搜索和调试细节留在自己上下文

### 多 Agent 下幻觉会互相放大
Agent A 带偏 → Agent B 跟着强化 → Agent C 再叠加 → 所有 Agent 收敛到同一个高置信度的错误结论。

> **用交叉验证打断这条链。**

---

## 📖 十二、Agent 评测如何做

### 关键指标
| 指标 | 含义 | 场景 |
|:---|:---|:---|
| **Pass@k** | k 次至少一次正确 | 探索能力上限 |
| **Pass^k** | k 次全部正确 | 上线回归 |

### 三类评分器
| 类型 | 确定性 | 适用场景 |
|:---|:---|:---|
| 代码评分器 | 最高 | 有明确正确答案 |
| 模型评分器 | 中 | 语义质量、风格 |
| 人工评分器 | 可靠但慢 | 建立基准、校准 |

### 从零搭评测体系
- **20~50 个真实失败案例就够启动**
- 先评测再改 Agent — 看到分数下降先查环境，再动 Agent
- 环境隔离：每次从干净状态开始，测试之间不能共享缓存/临时文件
- 测试用例要同时覆盖正例和反例

---

## 📖 十三、如何追踪 Agent 的执行过程

### Trace 需要记录
```
每次 Agent 运行：
├── 完整 Prompt（含系统提示）
├── 多轮交互的完整 messages[]
├── 每次工具调用 + 参数 + 返回值
├── 推理链（如有 thinking 模式）
├── 最终输出
└── token 消耗 + 延迟
```

### 两层可观测性
1. **人工抽样标注** — 摸清失败模式，提供校准数据
2. **LLM 自动评估** — 全量覆盖，以第一层校准

### 在线评测采样规则
- 负反馈触发：100% 进队列
- 高成本对话：token 超过阈值优先审查
- 时间窗口采样：每天固定时间段随机采
- 模型/Prompt 变更后：头 48 小时全量审查

---

## 📖 十四、用 OpenClaw 看 Agent 如何落地

### 五层解耦架构

| 层 | 实现 | 职责 |
|:---|:---|:---|
| Gateway | WebSocket 服务 | 接住外部连接，统一路由 |
| Channel 适配器 | 23+ 渠道统一 adapter | 对接 Telegram、Discord 等 |
| Pi Agent | 维护主循环、会话状态 | 工具调用支持流式返回 |
| 工具集 | shell/fs/web/browser/MCP | ACI 原则设计 |
| 上下文 + 记忆 | Skills 延迟加载 + MEMORY.md | 50% token 阈值自动整合 |

### 系统提示按层叠加
**SOUL.md** 定义身份、约束和完成标准，再按层加载：平台信息 → 身份层 → 记忆层 → Skills 层 → 运行时注入。

### 安全和可用性两层兜底
- **Prompt Injection**：source-sink 拆、最小权限、不可信输入显式标注
- **Provider 故障切换**：Anthropic → OpenAI → Sonnet 逐级 fallback

---

## 📖 十五、工程实现顺序

1. 单渠道先跑通，不要第一版就抽象多渠道
2. 安全边界先于功能
3. 记忆整合要早做（不加整合第 20 轮就垮）
4. Skills 先于新工具
5. 第一个失败就建评测

---

## 📖 十六、常见反模式

| 反模式 | 问题 | 怎么修 |
|:---|:---|:---|
| 系统提示当知识库 | 越来越长，关键规则被忽略 | 约定留系统提示，领域知识移 Skills |
| 工具数量失控 | Agent 频繁选错工具 | 合并重叠工具，明确命名空间 |
| 缺少验证机制 | Agent 说完成了但没法验证 | 每类任务绑定可执行验收标准 |
| 多 Agent 无边界 | 状态漂移，故障归因困难 | 明确角色/权限，worktree 隔离 |
| 记忆不整合 | 长对话第 20 轮后决策质量下降 | 监控 token，超阈值自动整合 |
| 没有评测 | 改一个地方不知有无回归 | 真实失败案例转测试用例 |
| 过早引入多 Agent | 协调开销超过并行收益 | 先建任务图，验证单 Agent 上限 |

---

## 💡 划重点

1. **Harness 比模型更关键** — 验收基线、执行边界、反馈信号、回退手段
2. **上下文工程防 Context Rot** — 分层管理 + 三类压缩 + Skills 延迟加载
3. **工具设计按 ACI 原则** — 面向 Agent 目标，不是面向底层 API
4. **记忆分四层** — MEMORY.md + 按需检索 + 可回退整合
5. **评测系统先修** — 不要基于失真信号调整方向
6. **事件流做可观测性底座** — 一次发布，多路消费

---

## 🔗 参考资料

- [OpenAI - Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- [Anthropic - Introducing Agent Skills](https://claude.com/blog/skills)
- [Anthropic - Managing context on the Claude Developer Platform](https://claude.com/blog/context-management)
- [LangChain - State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering)
- [OpenAI - Designing AI agents to resist prompt injection](https://openai.com/index/designing-agents-to-resist-prompt-injection/)
- [Anthropic - Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [OpenClaw 项目](https://github.com/tw93/waza)
