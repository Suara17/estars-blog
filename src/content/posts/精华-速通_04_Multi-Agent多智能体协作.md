---
title: '🚀 速通 · Multi-Agent 多智能体协作'
published: 2026-06-16
description: '做一个两个Agent协作写报告的团队：'
category: '求职作战室'
tags: ['求职作战室', '整理版']
draft: false
lang: zh-CN
---# 🚀 速通 · Multi-Agent 多智能体协作

---

## 🎯 你要做到什么级别的小Demo

做一个**两个Agent协作写报告的团队**：

```
你有一个"研究员Agent"和一个"写手Agent"：
1. 你提需求："写一份关于2026年AI Agent发展趋势的报告"
2. 研究员Agent → 搜索资料、整理要点
3. 写手Agent → 拿到研究员的结果，写成结构化报告
4. 返回一份完整的报告给你
```

**为什么是这个Demo：** 多Agent协作是2026年最火的进阶方向，能体现出你对"复杂系统拆分、角色分工、任务协作"的理解。面试官看到这个会眼睛一亮——大部分候选人只会单Agent。

---

## 📄 核心代码框架（逐行解释）

```python
# ===== 使用 CrewAI 实现多Agent协作（最简洁的框架） =====
from crewai import Agent, Task, Crew, Process

# 解释：CrewAI是最容易上手的多Agent框架
# 核心概念：Agent（角色） + Task（任务） + Crew（团队） + Process（流程）

# ===== 第1步：创建工具（Agent可用的能力） =====
from langchain_community.tools.tavily_search import TavilySearchResults
search_tool = TavilySearchResults(max_results=3)

# ===== 第2步：定义Agent角色 =====

researcher = Agent(
    role="高级研究员",
    goal="搜索并收集高质量信息，提炼关键发现",
    backstory="你是一名经验丰富的研究员，擅长从海量信息中提取有价值的洞察。",
    tools=[search_tool],     # 研究员可以搜索
    verbose=True,            # 打印思考过程，方便调试
    allow_delegation=False   # 不允许把任务派给别的Agent（保持职责清晰）
)
# 解释：Agent = 角色 + 目标 + 背景故事 + 工具
# role和backstory决定了LLM的行为风格，goal是任务的北极星

writer = Agent(
    role="高级报告撰写人",
    goal="将研究结果写成清晰、结构化、有洞察力的报告",
    backstory="你是一名专业的报告撰写专家，擅长将复杂信息转化为易于理解的报告。",
    verbose=True,
    allow_delegation=False
)
# 解释：两个Agent有不同的角色定位，各司其职

# ===== 第3步：定义任务 =====

research_task = Task(
    description="搜索2026年AI Agent发展趋势，提炼5个最重要的趋势并给出详细说明",
    expected_output="一份研究要点清单，每个趋势包含：趋势名称、关键数据、主要玩家、影响分析",
    agent=researcher          # 分配给研究员
)
# 解释：每个Task绑定一个Agent，明确谁做什么

writing_task = Task(
    description="基于研究员提供的资料，撰写一份专业的趋势分析报告，包含标题、摘要、正文、结论",
    expected_output="一份完整的Markdown格式报告，字数不少于1000字",
    agent=writer              # 分配给写手
)
# 解释：write_task依赖research_task的输出结果

# ===== 第4步：组建团队并执行 =====

crew = Crew(
    agents=[researcher, writer],          # 团队成员
    tasks=[research_task, writing_task],   # 任务列表（按顺序执行）
    process=Process.sequential,            # 顺序执行：研究→写报告
    verbose=True
)
# 解释：Process.sequential表示串行——研究员先干完，写手再开始
# Process.hierarchical则是有管理者Agent分配任务

# ===== 第5步：启动！ =====
result = crew.kickoff()
print("========== 最终报告 ==========")
print(result)
```

**如果你不想用CrewAI，想自己控制底层逻辑，用LangGraph也可以：**

```python
# ===== 用LangGraph实现多Agent协作（更灵活、可控） =====
# 核心思路：创建两个独立的Agent节点，一个负责研究、一个负责写作
# 研究Agent的输出作为写作Agent的输入

from langgraph.graph import StateGraph, END
from typing import TypedDict

class MultiAgentState(TypedDict):
    user_request: str
    research_result: str
    final_report: str

def research_node(state: MultiAgentState) -> MultiAgentState:
    """研究员Agent节点"""
    # 实际项目中在这里调用搜索工具
    state["research_result"] = f"针对'{state['user_request']}'的研究结果..."
    return state

def writing_node(state: MultiAgentState) -> MultiAgentState:
    """写手Agent节点"""
    # 基于research_result生成报告
    state["final_report"] = f"基于研究结果撰写的报告..."
    return state

# 构建图
graph = StateGraph(MultiAgentState)
graph.add_node("researcher", research_node)
graph.add_node("writer", writing_node)
graph.set_entry_point("researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", END)

app = graph.compile()
result = app.invoke({"user_request": "分析AI Agent趋势", "research_result": "", "final_report": ""})
```

---

## ❓ 面试官最爱问的3个问题

| 问题 | 满分回答要点 |
|:----|:-----------|
| **1. 什么时候用单Agent，什么时候用多Agent？** | 单Agent适合功能明确、不需要分工的任务（如简单问答）。多Agent适合：① 任务涉及不同专业领域 ② 需要不同角色协同（研究+写作+审核）③ 单个Agent上下文太长、prompt太复杂，拆分成多个更清晰。**原则：能不拆就不拆，拆了要能讲清楚为什么拆。** |
| **2. 多Agent之间怎么通信和同步？** | 常见三种方式：① **共享状态**（如LangGraph的State）— 所有Agent读写同一个状态对象 ② **消息传递**（A2A协议）— Agent之间通过消息队列发送任务/结果 ③ **顺序传递**（CrewAI模式）— Agent1的输出直接作为Agent2的输入。同步问题主要靠：等待上一个Agent完成（串行）或加消息队列做异步解耦。 |
| **3. 多Agent系统怎么避免"三个和尚没水喝"？** | ① **角色边界清晰**：每个Agent职责不重叠，避免推诿 ② **任务拆分粒度合适**：太大Agent干不了，太小管理成本高 ③ **加一个协调者Agent**：负责任务分配和结果汇总 ④ **设置超时和兜底**：某个Agent卡住了有备用方案。 |

---

**⏱ 练熟时间：** 1天（有Agent基础的话）
**面试杀伤力：** ⭐⭐⭐⭐⭐ 大部分候选人只能聊单Agent，你能聊多Agent就是降维打击。
