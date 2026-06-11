---
title: "AI 烧 token 点网页的时代，要被这个 23k star 项目终结了"
published: 2026-06-11
description: "**来源：** 微信公众号「AgentFlow」 **作者：** AgentFlow"
category: "外部精选"
tags: ["外部精选", "公众号精选", "OpenCLI", "AI", "浏览器自动化"]
draft: false
lang: zh-CN
---

# AI 烧 token 点网页的时代，要被这个 23k star 项目终结了

> **来源：** 微信公众号「AgentFlow」
> **作者：** AgentFlow
> **发布时间：** 2026年6月11日 10:04（新加坡）
> **原文链接：** [mp.weixin.qq.com](https://mp.weixin.qq.com/s?__biz=MzIwMzc3Njc3Mg==&mid=2247484541&idx=1&sn=e34fbd3cced54ad6ee24e9bf28cccee8)

---

一个叫 **OpenCLI** 的开源项目，**23.5k star**，核心逻辑只有一句话：把任何网站固化成一条 CLI 命令，之后免费跑一万次。

它不是另一个 Playwright 封装，也不是又一个 MCP 工具。它是一种不同的思路。

---

## AI 点网页，到底贵在哪

AI agent 操作浏览器，大致经历了三代：

| 代际 | 方案 | 特点 |
|------|------|------|
| 第一代 | Selenium/Playwright 脚本 | 确定性强，但每个网站都要手写，维护成本高 |
| 第二代 | LLM 驱动（browser-use、Playwright MCP） | 通用性好，但慢、贵、不稳定 |

**成本对比（第三方测试数据）：**

| 路线 | Token 消耗 | 响应时间 |
|------|-----------|---------|
| Playwright MCP | ≈ 11.4 万 token | 10-60 秒 |
| OpenCLI（CLI 路线） | ≈ 2.7 万 token | 数秒 |

更根本的问题是：LLM 驱动方案每次执行都要**「重新理解」**页面——就像雇了个实习生，每次都得现学现卖，没有 SOP。

---

## OpenCLI 的核心逻辑：智能前置，执行免费

作者 **jackwener**（Apache Arrow / DataFusion PMC 成员）把数据库的一个基本思想搬了进来：**查询计划编译一次，执行多次**。

对应到 Web 自动化就是：用 AI 探索一次目标网站，把操作逻辑固化成确定性的适配器，之后每次执行都是纯 JS 跑 DOM，**零 LLM 参与**。

**「编译时智能 vs 运行时智能」**

100 次任务：
- LLM 驱动方案 → 调 100 次大模型
- OpenCLI 路线 → 生成适配器时调 **1 次**，之后 99 次零成本执行

每个适配器本质是一个 **TypeScript 模块**，内含确定性的 CSS 选择器和页面交互逻辑：**导航 → 提取 → 返回结构化 JSON**。没有 LLM 随机性，跑一万次结果一致。

---

## 登录态问题，它怎么解

这才是 OpenCLI 真正的差异点，也是国内开发者最该关注的地方。

小红书、知乎、B 站、微博——这些平台的 API 要么没有要么极贵，爬虫又风控严。browser-use 和 Stagehand 需要你手动注入凭证，Playwright 要自己管理 cookie。

**OpenCLI 的答案：直接用你正在用的那个 Chrome。**

### 架构

```
CLI (Node.js) → 本地 daemon (localhost:19825, WebSocket) → Chrome 扩展 → 页面内执行 JS
```

扩展在你已登录会话的页面上下文里执行 JavaScript，**凭证全程不离开浏览器**，没有任何凭证存储。

> 「No competitor can say this.」—— 你的密码从来没离开过你的浏览器，因为它用的就是你的浏览器。

这对国内平台尤其致命：**不用扫码、不用配 token、不触发风控**，因为从平台的视角看，这就是你本人在用浏览器正常操作。

---

## 安装与使用

- **Chrome 扩展：** Chrome Web Store 搜索 OpenCLI
- **CLI 端：** Node.js >= 20
- **Daemon：** 首次执行 browser 命令时自动启动，常驻后台

### 现成适配器覆盖 100+ 站点（含大量中文平台）

| 国内平台 | 国外平台 |
|---------|---------|
| B站、知乎、小红书、微博、雪球、V2EX、BOSS直聘 | Twitter/X、Reddit、HackerNews、YouTube |

典型体验：`opencli twitter search "关键词"`，数秒返回结构化 JSON。

### 5 种认证策略（适配器自动选用）

```
PUBLIC（无需登录）→ COOKIE → INTERCEPT（拦截API调用）→ UI（模拟操作）→ LOCAL（本地应用）
```

用户感知不到这些细节，装好就能跑。

### Agent 集成

v0.6.0 新增 `opencli setup` 交互式 TUI，一键把配置打进 **Claude Code、Gemini CLI、Cursor、Codex** 等工具。给 Claude Code 装上 `opencli-browser skill`，agent 就能直接用你登录中的 Chrome 搜推特、读 Reddit、发小红书，不需要任何 API key。

---

## 局限和边界

| 适合 | 不适合 |
|------|--------|
| 高频访问的固定站点 | 需要随机浏览的陌生页面 |
| 需要定时任务的数据抓取 | 动态变化的一次性任务 |
| Agent 工作流里的确定性操作 | — |

**通用浏览场景**，官方建议配合 browser-use/Stagehand 一起用。

还有一个亮点：**7 个桌面应用（Electron）适配器**，通过 CDP（Chrome DevTools Protocol）驱动 Electron，Obsidian 也能变成 CLI 操作。

---

## 为什么这个范式值得关注

**"先用 agent 探索一次，再固化成命令"**——这个叫 **crystallize** 的设计哲学，是 OpenCLI 最值得单独拿出来讲的东西。

这不只是一个产品功能，是 agent 工具的一种新范式。过去我们谈 AI agent，默认是「每次执行都让 AI 现场决策」。OpenCLI 在说：**决策应该发生在设计时，不是运行时。**

一旦流程跑通，就该把它变成零成本可重复的命令。

这个思路和当前社区趋势高度契合。2025 年底以来，「MCP 吃 token 太狠，agent 工具向 CLI/Skills 迁移」已经是明显趋势。OpenCLI 踩中了这个时间点，几个月从 15.6k 涨到 23.5k star，增速本身就说明了问题。

---

*整理于 2026-06-11*
