---
title: '20+ 个 Agent Skills、仓库与市场，值得收藏'
published: 2026-06-17
description: '作者：Bilgin Ibryam'
category: '外部精选'
tags: ['外部精选', '外文翻译']
draft: false
lang: zh-CN
---# 20+ 个 Agent Skills、仓库与市场，值得收藏

> 一份有观点的 Agent Skills 货架：官方仓库、精选合集、第三方市场，以及值得安装、收藏或用作模板的周边工具。

**作者**：Bilgin Ibryam  
**来源**：The Generative Programmer（Substack）  
**日期**：2026年6月14日  
**原文链接**：https://generativeprogrammer.com/p/20-agent-skills-repos-and-marketplaces

---

> 一张粗略的热度地图，而非质量排名。

## 什么是 Skill？

**Skill 是 Coding Agent 的复用单元**。它是一个包含 `SKILL.md` 的文件夹，教会 Agent 一项能力——你只需教一次，之后每次会话就无需重复解释，且 Agent 只在任务需要时才加载它。

如果你想要背景知识，以下两篇是最值得先读的原始资料：
- Anthropic 的 *Equipping agents for the real world with Agent Skills*
- Claude Code skills 文档

本文是 [The Agentic Coding Reading List](https://generativeprogrammer.com/p/the-agentic-coding-reading-list) 的姊妹篇。那一篇精选了值得关注的人，这一篇精选了值得安装的能力。

核心观点：**最好的 skill 通常是你为自己的代码库写的那一个**。但你不应该从一个空文件夹开始。先安装经过验证的，学会它的形状，再写你自己的。

以下每一个链接都经过实地验证。

---

## 简短版：安装路线图

如果你只想要安装路径，按这个顺序来：

1. **先从官方仓库开始**，了解一个好的 `SKILL.md` 长什么样
2. **收藏市场和 awesome 列表**，用来发现新东西
3. **安装一套工作流框架**，再收集零散技巧
4. **添加你实际使用的技术栈的厂商 skill**
5. **当你重复同样的指令三遍时，写你自己的 skill**

### Skills 正在走向可移植

它们始于 Claude 生态，但 `SKILL.md` 格式正在扩散。OpenAI 现在已经在 ChatGPT 和 Codex 中记录 skills，这里的多个合集已经可以跨 Claude Code、Codex、Cursor 和 Gemini 运行。**选 skill 看它能做什么，而不是看它属于哪个厂商。**

---

## 一、哪里能找到 Skills

在接触任何单个 skill 之前，先了解它们都住在哪。从源头出发，向外扩展。

### 官方仓库

- **[anthropics/skills](https://github.com/anthropics/skills)** — Claude 官方仓库，也是正确的第一站。包含随 Claude 附带的文档 skills、mcp-builder 和 skill-creator（本文末尾还会提到它）。读几个这里的 skill 是学会"好的 SKILL.md 长什么样"最快的方式。

- **[openai/skills](https://github.com/openai/skills)** — 来自另一边的同类想法：Codex 的官方 skills 目录，包含像 Linear skill 这样开箱即用的集成。它的存在是最清晰的信号：**Skills 正在成为跨 Agent 的通用格式，而不仅仅是 Claude 的约定**。

### 第三方市场

- **[Claude Skills Marketplace](https://claude. skills/)** — 社区 skills 的可搜索目录。当你心里有某个具体任务，想看看在动手写之前已经有什么现成的时候就去这里。

- **[Smithery](https://smithery.ai/)** — Skill 和 MCP 服务器的注册中心，支持一键安装。适合想快速接入，而不是手动 clone 和复制文件时使用。

- **[Agensi](https://agensi.ai/)** — 包含付费 skills 的市场。值得知道商业层的存在，尽管你安装的大部分还是免费的。

### 我收藏的精选合集

有用的不是"安装最大的工具箱"，而是"研究什么正在获得关注以及为什么"。以下三个精选列表帮你做了筛选。当一个新 skill 流行起来，它通常会在到达官方仓库之前先出现在这些地方：

- **[ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)** — Claude skills、资源和工具的宽泛 awesome 列表。我想看整个全景图时第一个检查的地方。

- **[VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)** — 收集了来自官方开发团队和社区的一千多个 skill，按它们运行的 Agent 打标签。如果你不是只用 Claude，这个的跨 CLI 覆盖更强。

- **[Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)**，by Murat Can Koylan — 专注方向：上下文工程、多 Agent 架构和生产级 Agent 系统的 skills。当你自己在构建 Agent 而不只是使用它们时，就找这个。

---

## 二、从框架开始，而不是单个 Skill

最高杠杆的动作不是一个 skill，而是一个连贯的合集，带来一整套工作方式。以下是我在用的，外加两个广受关注的合集：

- **[superpowers](https://github.com/jessev6/superpowers)**，by Jesse Vincent — 一个 Agentic Skills 框架和开发方法论，而不是一袋松散技巧。它给 Agent 养成有纪律的习惯：先头脑风暴再构建、测试驱动开发、系统化调试、编写和执行计划、在合适时机请求审查。**这是我每天运行的那个**，因为它改变了 Agent 的工作方式，而不仅仅是它知道什么。

- **[andrej-karpathy-skills](https://github.com/anthropics/andrej-karpathy-skills)** — 将 Andrej Karpathy 关于语言模型在编写代码时哪里容易出错的观察，提炼成一个轻量级防护栏。也安装在这里了，小但效果超群：它在错误到达你的 diff 之前就拦截了常见失败模式。

- **[gstack](https://github.com/garrytan/gstack)**，by Garry Tan — 他精确的 Claude Code 配置打包供任何人采用：几十个有观点的工具，充当 CEO、设计师、工程经理、发布经理和 QA。当你想要一个完整预接线的工作方式而不是自己拼装部件时，就用它。

- **[mattpocock/skills](https://github.com/mattpocock/skills)**，by Matt Pocock — "写给真正的工程师的 skills，直接来自我的 .claude 目录"。一个实际从业者的真实配置，往往比任何为了分享而构建的东西都更有用。

---

## 三、为你技术栈定制的最佳实践

最有用的类别之一来自你已经使用的工具的官方 skills。这指向了厂商交付知识方式的真正转变：**不再是让你阅读的文档网站，而是越来越多的团队直接交付一个 Agent 运行的 skill——将最佳实践变成可执行的规定，而不是丢给你一份希望被人遵循的指南。**

以下是我根据自己技术栈安装的：

- **[database-skills](https://github.com/planetscale/database-skills)**，来自 PlanetScale — 教会 Agent 正确处理数据库：schema、查询和迁移，而不是凭空编造看起来对但悄悄出错的 SQL。搭配 [neondatabase/agent-skills](https://github.com/neondatabase/agent-skills)（Neon 无服务器 Postgres）和 [redis/agent-skills](https://github.com/redis/agent-skills) 效果更佳。

- **[next-skills](https://github.com/vercel/next-skills)**，来自 Vercel 工程团队 — 承载前端部分，其中 `next-best-practices` skill 让 Agent 保持在框架预期的模式内。

- **[supabase/agent-skills](https://github.com/supabase/supabase-agent-skills)** — 为 Supabase 平台做同样的事。

厂商列表现在读起来像一张技术栈图：**Stripe**（支付）、**Cloudflare**（边缘计算）、**HashiCorp**（Terraform）、**Hugging Face**（模型）、**Trail of Bits**（安全），还有 Netlify、Sanity、WordPress、Expo。**检查一下你依赖的工具是否已经推出了 skill——越来越多的厂商正在这样做。**

---

## 四、按角色选择 Skill

框架之后，剩下的就是按角色划分。根据你的工作，挑选匹配的 skill。远不止这四个，但它们清晰地对应了四种工作类型。沿着这条路走足够远，你就会想要一个还不存在的 skill——这就是下一节的内容。

- **软件工程师** → **[agent-skills](https://github.com/addyosmani/agent-skills)**，by Addy Osmani — 一套生产级工程 skills，不是单个技巧，而是精心、可维护代码的编写框架。

- **设计师** → **[open-design](https://github.com/nexu-ai/open-design)**，by Nexu — Claude 设计工具的原生开放替代方案，让 Agent 能够在多个 Agent CLI 上生成界面、原型和幻灯片。

- **写作者** → **[humanizer](https://github.com/anthropics/humanizer)** — 剥去 AI 生成文本的痕迹——那些让文章读起来像机器写的 giveaway 措辞和节奏。

- **研究者与永不满足的好奇心** → **[last30days-skill](https://github.com/mattvh/last30days-skill)**，by Matt Van Horn — 在 Reddit、X、YouTube、Hacker News、Polymarket 和开放网络上研究任何话题，然后综合出有依据的摘要。不是为了写代码，而是在你动手之前收集当前的信号。

---

## 五、当它们都不适合时，自己动手构建

沿着列表走到这里，你就会遇到那个应该存在但还不存在的 skill。一旦你看到了一个好 `SKILL.md` 的样子，**你重复的指令就是下一个要捕捉的东西**。有两个 skill 正好帮你做这件事：

- **[skill-creator](https://github.com/anthropics/skill-creator)** — Anthropic 用来构建 skill 的 skill。它会搭起一个新 skill 的骨架，并且按照方法论的精神，让你在信任它之前先在几个测试用例上运行并阅读转录结果。

- **[Skill_Seekers](https://github.com/yusufkar s/Skill_Seekers)**，by Yusuf Karaaslan — 从另一个方向入手：自动将文档网站、GitHub 仓库和 PDF 转换为 skill，并带冲突检测。当你想要的技能已经以文档的形式存在，只需要打包时，这是快速路径。

---

## 六、Skills 与 MCP 的交界地带

并非所有有用的东西都以 skill 的形式打包，而 skill 和 MCP 服务器之间的界线正变得越来越模糊。两个工具比任何定义都更好地说明了这一点：

- **[context7](https://github.com/upstash/context7)**，来自 Upstash — 将最新、版本正确的文档和代码示例直接拉入模型的上下文，这样 Agent 就不会根据训练时半记忆的 API 来写代码。它也是这一转变最清晰的例子：**它同时以 MCP 服务器、CLI 和 skill 三种形式发布**。同样的能力，三种打包方式，你的环境喜欢哪种就装哪种。我一直开着它。

- **Playwright** — 同一个分裂的活例子。微软的 [playwright-mcp](https://github.com/microsoft/playwright-mcp) 是给 Agent 提供真实浏览器控制能力以进行自动化和测试的广泛使用的方式——它是一个 MCP 服务器。[playwright-skill](https://github.com/jordanlackey/playwright-skill)，by Jordan Lackey，则将同样的能力重建为一个模型调用的 skill，它编写并运行自己的浏览器自动化。**两者都试试**：如果你想要今天的成熟方案，用 MCP；如果你想要 context7 已经指向的"只在需要时加载"的行为，用 skill。

---

## 结语

市场会用成千上万的 skill 来诱惑你。**这个数字是个陷阱**。你真正理解并信任的那几个，比一个你永远不会打开的目录对你的工作帮助更大——就像一份精简的持久阅读清单胜过无休止的信息流一样。

**收藏合集，运行一个改变 Agent 工作方式的框架，添加匹配你技术栈的厂商 skill，拿一个匹配你角色的 skill，然后写一个还不存在的 skill。**

最后那一步，才是所有其他步骤的意义所在。

---

> *这是一份持续更新的文档。最后检查日期：2026-06-14。如果你发现某个 skill 已经迁移，或者觉得少了什么重要的东西，告诉我，我会更新。*

---

*原文：The Generative Programmer — Bilgin Ibryam*
*翻译于 2026-06-17*
