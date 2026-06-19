---
title: '🚀 速通 · LangGraph Agent开发'
published: 2026-06-19
description: '做一个多步推理的研究Agent（面试王牌项目）：'
category: '求职作战室'
tags: ['求职作战室', '整理版']
draft: false
lang: zh-CN
---# 🚀 速通 · LangGraph Agent开发

---

## 🎯 你要做到什么级别的小Demo

做一个**多步推理的研究Agent**（面试王牌项目）：

```
用户问："对比一下Transformer和Mamba架构的优缺点"
Agent会：
  1. 拆解问题 → 生成搜索关键词
  2. 调用搜索工具获取信息
  3. 阅读搜索结果 → 提取关键点
  4. 综合对比 → 输出结构化的对比报告
```

**为什么是这个Demo：** 这是当前Agent面试的"标准答案"项目。它展示了状态管理、工具调用、多步推理、条件分支——LangGraph最核心的能力全用上了。面试官看到这个项目会点点头："该会的都会了。"

---

## 📄 核心代码框架（逐行解释）

```python
# ===== 第1步：导入LangGraph核心 =====
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

# 解释：LangGraph的核心思想是将Agent流程定义为一个状态图（StateGraph）
# 状态（State）在节点之间传递，节点是处理逻辑，边决定流转方向

# ===== 第2步：定义状态（State） =====
class AgentState(TypedDict):
    messages: list        # 对话历史
    next_step: str        # 当前步骤标记
    research_result: str  # 研究结果
    final_answer: str     # 最终回答
# 解释：State是一个字典，用来在各个节点之间传递数据。
# LangGraph会自动维护这个状态，你只需在节点函数中读取和修改它。

# ===== 第3步：初始化LLM和工具 =====
llm = ChatOpenAI(model="gpt-4o")
search_tool = TavilySearchResults(max_results=3)   # 需要tavily API key，实在没有可以用requests写一个搜索函数代替

# ===== 第4步：定义节点函数（每个节点是Agent的一步） =====

# 节点1：分析问题，判断需要搜索什么
def analyze_question(state: AgentState) -> AgentState:
    """根据用户问题，决定搜索关键词"""
    question = state["messages"][-1]["content"]
    # 用LLM生成搜索关键词
    response = llm.invoke(f"针对'{question}'这个问题，生成3个最合适的搜索关键词，直接返回关键词列表，每行一个。")
    keywords = response.content.strip().split("\n")
    state["next_step"] = "search"
    state["research_result"] = "\n".join(keywords)
    return state
# 解释：这个节点用LLM做"思考"，把问题转化成可执行的搜索计划

# 节点2：执行搜索
def search(state: AgentState) -> AgentState:
    """使用工具搜索信息"""
    keywords = state["research_result"]
    # 搜索第一个关键词
    results = search_tool.invoke(keywords.split("\n")[0])
    state["research_result"] = str(results[:2])  # 取前2条结果
    state["next_step"] = "synthesize"
    return state
# 解释：这个节点通过工具（Tool）与外部世界交互，获取实时信息

# 节点3：综合回答
def synthesize(state: AgentState) -> AgentState:
    """基于搜索结果生成最终回答"""
    question = state["messages"][-1]["content"]
    search_data = state["research_result"]
    prompt = f"""基于以下搜索结果，回答用户的问题：

搜索结果：
{search_data}

问题：{question}

请用中文给出详细、结构化的回答，包含优缺点对比。"""
    response = llm.invoke(prompt)
    state["final_answer"] = response.content
    state["next_step"] = END
    return state
# 解释：把搜索结果作为上下文，让LLM生成最终答案

# ===== 第5步：定义条件边（决定流转路径） =====
def router(state: AgentState) -> Literal["analyze", "search", "synthesize", "__end__"]:
    """根据当前状态决定下一步"""
    step = state.get("next_step", "analyze")
    if step == "analyze":
        return "analyze"
    elif step == "search":
        return "search"
    elif step == "synthesize":
        return "synthesize"
    else:
        return "__end__"
# 解释：条件边让Agent可以根据当前状态动态决定下一步做什么
# 这里用next_step字段控制，也可以用LLM自己判断

# ===== 第6步：构建状态图 =====
# 创建一个状态图，指定状态结构
graph = StateGraph(AgentState)

# 添加节点
graph.add_node("analyze", analyze_question)
graph.add_node("search", search)
graph.add_node("synthesize", synthesize)

# 设置入口
graph.set_entry_point("analyze")

# 添加条件边：从"analyze"节点出来后，根据router函数决定去向
graph.add_conditional_edges(
    "analyze",       # 起始节点
    router,          # 路由函数
    {                 # 映射：返回值 → 目标节点
        "analyze": "analyze",
        "search": "search",
        "synthesize": "synthesize",
        "__end__": END
    }
)
graph.add_conditional_edges("search", router, {
    "analyze": "analyze",
    "search": "search",
    "synthesize": "synthesize",
    "__end__": END
})
graph.add_conditional_edges("synthesize", router, {
    "analyze": "analyze",
    "search": "search",
    "synthesize": "synthesize",
    "__end__": END
})

# 编译成可执行的应用
app = graph.compile()

# ===== 第7步：执行 =====
if __name__ == "__main__":
    # 初始状态
    initial_state = {
        "messages": [{"role": "user", "content": "对比Transformer和Mamba架构的优缺点"}],
        "next_step": "analyze",
        "research_result": "",
        "final_answer": ""
    }
    # 运行
    result = app.invoke(initial_state)
    print("最终回答：")
    print(result["final_answer"])
```

**这个Demo做完，你在面试中能展示：**
- 📐 理解了**StateGraph**状态管理
- 🔄 会设计**Node**和**Edge**
- 🤔 能用**条件边**实现动态决策
- 🔧 集成了**Tool**调用
- 💬 能说清楚Agent的工作流程

---

## ❓ 面试官最爱问的3个问题

| 问题 | 满分回答要点 |
|:----|:-----------|
| **1. LangGraph和普通的LangChain Chain有什么区别？为什么用LangGraph？** | 普通Chain是固定顺序（A→B→C），而LangGraph的StateGraph支持**循环、分支、条件跳转**。Agent需要反复推理-行动-观察，用Chain无法实现循环；LangGraph可以通过条件边实现"如果搜索结果不够，就重新搜索"这种迭代逻辑。|
| **2. 你的Agent陷入死循环了怎么办？** | ① 在条件边里设置**最大迭代步数**（比如最多执行10步） ② 或者用LLM判断"是否已经得到足够信息"来终止 ③ LangGraph的`recursion_limit`参数可以控制最大递归次数。如果达到限制仍未完成，就返回已有结果并提示用户。 |
| **3. 你的Agent怎么处理工具调用失败？** | ① 在tool调用时加try-except，捕获异常后返回给LLM错误信息，让它决定是重试还是换一种方式 ② 可以设置重试机制（如最多重试2次） ③ 如果工具多次失败，Agent应该能给出一个备选回答，而不是卡住或崩溃。 |

---

**⏱ 练熟这个Demo预计时间：** 3天（已有LLM调用和Function Calling基础）
**有了它你能在面试中展示：** LangGraph核心概念、Agent全流程设计、多步推理、错误处理意识、工程化能力。

**这是你面试的王牌项目，一定要放到GitHub上！**

---

## 📖 进阶知识补充：Agent 核心理论

### Agent 四范式（不是进化关系，是层次关系）

| 层次 | 范式 | 职责 |
|------|------|------|
| 基础能力层 | Tool Use / Function Calling | 模型能否调用外部工具 |
| 推理框架层 | ReAct | 推理与行动如何交替 |
| 控制流程层 | Plan & Execute | 先规划还是边想边做 |
| 组织架构层 | Multi-Agent | 多个 Agent 如何协作 |

**关键：** 层次可以叠加——一个 Agent 可以同时用 ReAct + Function Calling，整体又是 Multi-Agent 架构。

**各范式对比：**

| 范式 | 优势 | 劣势 | 适用场景 |
|------|------|------|----------|
| Tool Use | 延迟低，架构简单 | 缺全局规划 | 单一工具调用 |
| ReAct | 每一步决策可追溯 | 延迟累积 | 中等复杂度，需观测性 |
| Plan & Execute | 全局规划，减少试错 | 计划可能过时 | 步骤明确的批量任务 |
| Multi-Agent | 职责分离，并行执行 | 通信开销大 | 复杂业务流 |

### Agent 评测体系

| 层 | 评测内容 | 方法 |
|----|----------|------|
| L1 基础能力 | 工具调用准确性、参数格式 | 单元测试 |
| L2 任务完成 | 端到端任务成功率 | 人工标注 + 自动化验证 |
| L3 鲁棒性 | 异常输入、干扰信息下的表现 | 对抗测试 |
| L4 安全性 | prompt injection、权限越界 | 红队测试 |

### Context Window 约束与应对

**核心限制：** Token 上限、注意力衰减、KV Cache 显存占用、填充耗时

**应对策略：**
1. 滑动窗口 — 只保留最近 N 轮对话
2. Compaction — 用 LLM 将早期对话压缩为摘要
3. 记忆分层 — 短期记忆（会话内）→ 长期记忆（跨会话持久化）
4. 分块 + 摘要 — 超长内容分段摘要后合并
