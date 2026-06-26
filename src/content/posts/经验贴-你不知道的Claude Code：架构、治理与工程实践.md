---
title: '你不知道的 Claude Code：架构、治理与工程实践'
published: 2026-06-26
description: '刚开始也把它当 ChatBot 用，后来很快发现不对劲：上下文越来越乱、工具越来越多效果越来越差、规则越写越长却越不遵守。'
category: '经验贴'
tags: ['经验贴']
draft: false
lang: zh-CN
---# 你不知道的 Claude Code：架构、治理与工程实践

> **作者：** Tw93 @HiTw93  
> **来源：** https://x.com/i/status/2032091246588518683 / https://tw93.fun/2026-03-12/claude.html  
> **发布时间：** 2026年3月12日  
> **浏览量：** 303.3万  
> **保存时间：** 2026年6月19日

---

> 今天这篇来自最近半年深度用 Claude Code 的实际踩坑，两个账号每月 40 刀，算是交了点学费。

---

## 📑 太长不读

刚开始也把它当 ChatBot 用，后来很快发现不对劲：上下文越来越乱、工具越来越多效果越来越差、规则越写越长却越不遵守。

最直接的理解方式，是把 Claude Code 拆成**六层**来看：

| 层 | 职责 |
|:---|:---|
| CLAUDE.md / rules / memory | 长期上下文，告诉 Claude "是什么" |
| Tools / MCP | 动作能力，告诉 Claude "能做什么" |
| Skills | 按需加载的方法论，告诉 Claude "怎么做" |
| Hooks | 强制执行某些行为，不依赖 Claude 自己判断 |
| Subagents | 隔离上下文的工作者，负责受控自治 |
| Verifiers | 验证闭环，让输出可验、可回滚、可审计 |

---

## 📖 一、它底层是怎么运行的

Claude Code 跑的是一个反复循环的代理过程：

```
收集上下文 → 采取行动 → 验证结果 → [完成 or 回到收集]
     ↑                    ↓
  CLAUDE.md          Hooks / 权限 / 沙箱
  Skills             Tools / MCP
  Memory
```

### 五个诊断层面

| 层面 | 核心问题 | 主要载体 |
|:---|:---|:---|
| Context surface | 哪些信息常驻，哪些按需加载 | CLAUDE.md、rules、memory、skills |
| Action surface | Claude 当前具备哪些动作能力 | built-in tools、MCP、plugins |
| Control surface | 哪些动作必须被约束、阻断或审计 | permissions、sandbox、hooks |
| Isolation surface | 哪些任务需要隔离上下文和权限 | subagents、worktrees、forked sessions |
| Verification surface | 如何判断任务完成且结果可信 | tests、lint、screenshots、logs、CI |

---

## 📖 二、概念边界：搞清楚六个概念，别混用

| 概念 | 运行时角色 | 解决什么 | 典型误用 |
|:---|:---|:---|:---|
| **CLAUDE.md** | 项目级持久契约 | 每次会话都必须成立的命令、边界、禁止项 | 写成团队知识库 |
| **.claude/rules/*** | 路径或语言相关规则 | 目录、文件类型或语言级局部规范 | 所有规则都堆到根 CLAUDE.md |
| **Built-in Tools** | 内置能力 | 读文件、改文件、跑命令、搜索 | 把所有集成都塞进 shell |
| **MCP** | 外部能力接入协议 | 让 Claude 访问 GitHub、Sentry、数据库 | 接太多 server，工具定义挤爆上下文 |
| **Plugin** | 打包分发层 | 把 Skills/Hooks/MCP 一起分发 | 把 plugin 当成运行时 primitive |
| **Skill** | 按需加载的知识/工作流 | 给 Claude 一个方法包 | skill 既像百科全书又像部署脚本 |
| **Hook** | 强制执行规则的拦截层 | 在生命周期事件前后执行规则 | 用 hook 替代所有模型判断 |
| **Subagent** | 隔离上下文的工作单元 | 并行研究、限制工具与权限 | 无边界 fan-out，治理失控 |

> **简单记：** 给 Claude 新动作能力用 **Tool/MCP**，给它一套工作方法用 **Skill**，需要隔离执行环境用 **Subagent**，要强制约束和审计用 **Hook**，跨项目分发用 **Plugin**。

---

## 📖 三、上下文工程：最重要的系统约束

### 真实上下文成本构成

```
200K 总上下文
├── 固定开销 (~15-20K)
│   ├── 系统指令: ~2K
│   ├── 所有启用的 Skill 描述符: ~1-5K
│   ├── MCP Server 工具定义: ~10-20K  ← 最大隐形杀手
│   └── LSP 状态: ~2-5K
│
├── 半固定 (~5-10K)
│   ├── CLAUDE.md: ~2-5K
│   └── Memory: ~1-2K
│
└── 动态可用 (~160-180K)
    ├── 对话历史
    ├── 文件内容
    └── 工具调用结果
```

> 一个典型 MCP Server（如 GitHub）包含 20-30 个工具定义，每个约 200 tokens，合计 4,000-6,000 tokens。接 5 个 Server，光这部分固定开销就到了 25,000 tokens（12.5%）。

### 推荐的上下文分层

- **始终常驻** → CLAUDE.md：项目契约 / 构建命令 / 禁止事项
- **按路径加载** → rules：语言 / 目录 / 文件类型特定规则
- **按需加载** → Skills：工作流 / 领域知识
- **隔离加载** → Subagents：大量探索 / 并行研究
- **不进上下文** → Hooks：确定性脚本 / 审计 / 阻断

### 上下文最佳实践

1. 保持 CLAUDE.md **短、硬、可执行**——Anthropic 官方自己只有 ~2.5K tokens
2. 大型参考文档拆到 Skills 的 supporting files，不要塞进 SKILL.md 正文
3. 使用 `.claude/rules/` 做路径/语言规则
4. 长会话主动用 `/context` 观察消耗
5. 任务切换优先 `/clear`，同一任务进入新阶段用 `/compact`
6. 把 **Compact Instructions** 写进 CLAUDE.md

### Tool Output 噪声（隐形杀手）

`cargo test` 一次完整输出动辄几千行，Claude 不需要全看。推荐用 **RTK（Rust Token Killer）** 在命令输出到 Claude 之前自动过滤，只留决策需要的核心信息：

```bash
# Claude 看到的原始输出
running 262 tests
test auth::test_login ... ok
...（几千行）

# 走 RTK 之后
✓ cargo test: 262 passed (1 suite, 0.08s)
```

### 压缩机制的陷阱

默认压缩算法会优先删掉早期 Tool Output 和文件内容，**连带架构决策和约束理由也一起扔了**。

**解决方案**：在 CLAUDE.md 里写明 Compact Instructions：

```markdown
## Compact Instructions

When compressing, preserve in priority order:
1. Architecture decisions (NEVER summarize)
2. Modified files and their key changes
3. Current verification status (pass/fail)
4. Open TODOs and rollback notes
5. Tool outputs (can delete, keep pass/fail only)
```

另一种主动方案：开新会话前让 Claude 写 **HANDOFF.md**，把当前进度、试过什么、哪些走通了、哪些是死路、下一步该做什么写清楚。

### Plan Mode 的工程价值

核心是把探索和执行拆开，探索阶段不动文件。进阶玩法：**开一个 Claude 写计划，再开一个 Codex 以"高级工程师"身份审这个计划**——让 AI 审 AI。

---

## 📖 四、Skills 设计：不是模板库，是用的时候才加载的工作流

### 一个好 Skill 的结构

```
.claude/skills/
└── incident-triage/
    ├── SKILL.md
    ├── runbook.md
    ├── examples.md
    └── scripts/
        └── collect-context.sh
```

### 三种典型 Skill 类型

**类型一：检查清单型（质量门禁）**
```yaml
---
name: release-check
description: Use before cutting a release to verify build, version, and smoke test.
---
## Pre-flight (All must pass)
- [ ] `cargo build --release` passes
- [ ] `cargo clippy -- -D warnings` clean
- [ ] Version bumped in Cargo.toml
- [ ] CHANGELOG updated
- [ ] `kaku doctor` passes on clean env
```

**类型二：工作流型（标准化操作）**
```yaml
---
name: config-migration
description: Migrate config schema. Run only when explicitly requested.
disable-model-invocation: true
---
## Steps
1. Backup: `cp ~/.config/kaku/config.toml ~/.config/kaku/config.toml.bak`
2. Dry run: `kaku config migrate --dry-run`
3. Apply: remove `--dry-run` after confirming output
4. Verify: `kaku doctor` all pass

## Rollback
`cp ~/.config/kaku/config.toml.bak ~/.config/kaku/config.toml`
```

**类型三：领域专家型（封装决策框架）**
```yaml
---
name: runtime-diagnosis
description: Use when kaku crashes, hangs, or behaves unexpectedly at runtime.
---
## Evidence Collection
1. Run `kaku doctor` and capture full output
2. Last 50 lines of `~/.local/share/kaku/logs/`
3. Plugin state: `kaku --list-plugins`

## Decision Matrix
| Symptom | First Check |
|---|---|
| Crash on startup | doctor output → Lua syntax error |
| Rendering glitch | GPU backend / terminal capability |
| Config not applied | Config path + schema version |
```

### 描述符优化

低效（~45 tokens）→ 高效（~9 tokens）：
```yaml
# 低效
description: This skill helps you review code changes in Rust projects...

# 高效
description: Use for PR reviews with focus on correctness.
```

### Skills 反模式
- 描述过短（什么都能触发）
- 正文过长（几百行全塞 SKILL.md）
- 一个 Skill 覆盖 review、deploy、debug、docs、incident 五件事
- 有副作用的 Skill 允许模型自动调用

---

## 📖 五、工具设计：怎么让 Claude 少选错

### 好工具 vs 坏工具

| 维度 | 好工具 | 坏工具 |
|:---|:---|:---|
| 名称 | `jira_issue_get`, `sentry_errors_search` | `query`, `fetch`, `do_action` |
| 参数 | `issue_key`, `project_id`, `response_format` | `id`, `name`, `target` |
| 返回 | 与下一步决策直接相关的信息 | 一堆 UUID、内部字段、原始噪声 |
| 规模 | 单一目标，边界清楚 | 多个动作混杂，副作用不透明 |
| 成本 | 默认输出受控、可截断 | 默认返回过大上下文 |
| 错误信息 | 包含修正建议 | 仅返回 opaque error code |

### 实用设计原则
1. 名称前缀按系统或资源分层：`github_pr_*`、`jira_issue_*`
2. 对大响应支持 `response_format: concise / detailed`
3. 错误响应要教模型如何修正
4. 能合并成高层任务工具时，不要暴露过多底层碎片工具

### 工具演进的有趣教训

**AskUserQuestion 的演进史：**
1. **第一版**：给 Bash 工具加 `question` 参数 → 模型忽略
2. **第二版**：要求输出特定 markdown 格式 → 模型经常"忘了"
3. **第三版**：做成独立 `AskUserQuestion` 工具 → 调用即暂停，没有歧义 ✅

**Todo 工具的教训**：早期因为模型不够强加了 TodoWrite 工具，模型变强后反而成了限制。→ **定期检查当初加的限制还成不成立。**

### 什么时候不该再加 Tool
- 本地 shell 可以可靠完成的事情
- 模型只需要静态知识
- 需求更适合 Skill 的工作流约束
- 还没验证过工具描述和返回格式能被模型稳定使用

---

## 📖 六、Hooks：在 Claude 执行操作前后，强制插入你自己的逻辑

### Hook 配置示例

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "pattern": "*.rs",
        "hooks": [{
          "type": "command",
          "command": "cargo check 2>&1 | head -30",
          "statusMessage": "Checking Rust..."
        }]
      }
    ],
    "Notification": [
      {
        "type": "command",
        "command": "osascript -e 'display notification \"Task completed\" with title \"Claude Code\"'"
      }
    ]
  }
}
```

### Hooks + Skills + CLAUDE.md 三层叠加

| 层 | 作用 |
|:---|:---|
| CLAUDE.md | 声明"提交前必须通过测试和 lint" |
| Skill | 告诉 Claude 运行顺序、如何看失败、如何修复 |
| Hook | 对关键路径执行硬性校验，必要时阻断 |

---

## 📖 七、Subagents：派一个独立的 Claude 去干一件具体的事

Subagent 最大的价值不是"并行"，而是**隔离**——扫代码库、跑测试会产生大量输出，交给 Subagent 做，主线程只拿一个摘要。

### 配置时要显式约束
- `tools / disallowedTools`：限定工具范围
- `model`：探索用 Haiku/Sonnet，重要审查用 Opus
- `maxTurns`：防止跑飞
- `isolation: worktree`：需要动文件时隔离文件系统

### 常见反模式
- 子代理权限和主线程一样宽
- 输出格式不固定，主线程拿到没法用
- 子任务之间强依赖，频繁共享中间状态

---

## 📖 八、Prompt Caching：Claude Code 内部架构的核心

### Prompt 顺序（缓存前缀匹配）

```
1. System Prompt → 静态，锁定
2. Tool Definitions → 静态，锁定
3. Chat History → 动态，在后面
4. 当前用户输入 → 最后
```

### 破坏缓存的常见陷阱
- 在静态 System Prompt 中放入带时间戳的内容
- 非确定性地打乱工具定义顺序
- 会话中途增删工具

> **技巧：** 当前时间等动态信息，放到下一条消息的 `<system-reminder>` 标签里传进去，不动 System Prompt。

### 会话中途不要切换模型
Prompt 缓存是模型唯一的。切换模型实际上比继续用原模型更贵（要重建整个缓存）。确实需要切换的话，用 Subagent 交接。

### defer_loading：工具的延迟加载
Claude Code 有数十个 MCP 工具，通过发送轻量级 stub（只有工具名，标记 `defer_loading: true`），完整 schema 只在模型选择后才加载，**缓存前缀保持稳定**。

---

## 📖 九、验证闭环：没有 Verifier 就没有工程上的 Agent

### Verifier 的层级
- **最低层**：命令退出码、lint、typecheck、unit test
- **中间层**：集成测试、截图对比、contract test、smoke test
- **更高层**：生产日志验证、监控指标、人工审查清单

### 在 Prompt 中显式定义验证

```markdown
## Verification

For backend changes:
- Run `make test` and `make lint`
- For API changes, update contract tests under `tests/contracts/`

For UI changes:
- Capture before/after screenshots if visual

Definition of done:
- All tests pass
- Lint passes
- No TODO left behind unless explicitly tracked
```

---

## 📖 十、高频命令的工程意义

### 上下文管理
| 命令 | 作用 |
|:---|:---|
| `/context` | 查看 token 占用结构 |
| `/clear` | 清空会话 |
| `/compact` | 压缩但保留重点 |
| `/memory` | 确认哪些 CLAUDE.md 被加载 |

### 能力与治理
| 命令 | 作用 |
|:---|:---|
| `/mcp` | 管理 MCP 连接，检查 token 成本 |
| `/hooks` | 管理 hooks |
| `/permissions` | 查看或更新权限白名单 |
| `/sandbox` | 配置沙箱隔离 |
| `/model` | 切换模型 |

### 会话连续性与并行
| 命令 | 作用 |
|:---|:---|
| `claude --continue` | 恢复最近会话 |
| `claude --resume` | 打开选择器恢复历史会话 |
| `claude --continue --fork` | 从已有会话分叉 |
| `claude -p "prompt"` | 非交互模式，接入 CI |
| `claude -p --output-format json` | 结构化输出 |

### 不常见但很好用的命令
| 命令 | 作用 |
|:---|:---|
| `/simplify` | 对刚改完的代码做三维检查（复用、质量、效率） |
| `/rewind` | 回到某个会话 checkpoint 重新总结 |
| `/btw` | 不打断主任务快速问一个侧问题 |
| `/insight` | 分析当前会话，提炼值得沉淀到 CLAUDE.md 的内容 |
| **双击 ESC** | 回到上一条输入重新编辑 |
| `claude -p --output-format stream-json` | 实时 JSON 事件流 |

---

## 📖 十一、如何写一个好的 CLAUDE.md

> CLAUDE.md 是**协作契约**，不是团队文档，也不是知识库。只放那些每次会话都得成立的事。

### 应该放什么
- 怎么 build、怎么 test、怎么跑（最核心）
- 关键目录结构与模块边界
- 代码风格和命名约束
- 那些不明显的环境坑
- **绝对不能干的事（NEVER 列表）**
- 压缩时必须保留的信息（Compact Instructions）

### 不该放什么
- 大段背景介绍
- 完整 API 文档
- 空泛原则（如"写高质量代码"）
- 显然信息（Claude 读仓库即可推断）
- 大量背景资料和低频任务知识（放到 Skills）

### 高质量模板

```markdown
# Project Contract

## Build And Test
- Install: `pnpm install`
- Dev: `pnpm dev`
- Test: `pnpm test`
- Typecheck: `pnpm typecheck`
- Lint: `pnpm lint`

## Architecture Boundaries
- HTTP handlers live in `src/http/handlers/`
- Domain logic lives in `src/domain/`
- Do not put persistence logic in handlers
- Shared types live in `src/contracts/`

## Coding Conventions
- Prefer pure functions in domain layer
- Do not introduce new global state without explicit justification
- Reuse existing error types from `src/errors/`

## NEVER
- Modify `.env`, lockfiles, or CI secrets without explicit approval
- Remove feature flags without searching all call sites
- Commit without running tests

## ALWAYS
- Show diff before committing
- Update CHANGELOG for user-facing changes

## Verification
- Backend changes: `make test` + `make lint`
- API changes: update contract tests under `tests/contracts/`
- UI changes: capture before/after screenshots

## Compact Instructions
Preserve:
1. Architecture decisions (NEVER summarize)
2. Modified files and key changes
3. Current verification status (pass/fail commands)
4. Open risks, TODOs, rollback notes
```

### 让 Claude 维护自己的 CLAUDE.md

每次纠正错误后，让它更新 CLAUDE.md：

> "Update your CLAUDE.md so you don't make that mistake again."

Claude 在给自己补规则时还挺好用，但也要定期 review，过时的限制要及时清理。

---

## 📖 十二、最近折腾中得到的新经验

### "环境透明"比你想象中重要
Claude Code 调用的是真实的 shell、git、package manager。只要有一层不透明，它就猜，一猜可靠性就掉。

**做法**：在项目里加个 `doctor` 命令，把环境状态统一收上来。Claude Code 开始做事前先跑一次 doctor。

### 混合语言项目的 Hooks 实践
两套语言、两套检查，用 Hooks 按文件类型分别触发：
- `*.rs` → `cargo check`
- `*.lua` → `luajit -b`

### 完整工程化布局参考

```
Project/
├── CLAUDE.md
├── .claude/
│   ├── rules/
│   │   ├── core.md
│   │   ├── config.md
│   │   └── release.md
│   ├── skills/
│   │   ├── runtime-diagnosis/
│   │   ├── config-migration/
│   │   ├── release-check/
│   │   └── incident-triage/
│   ├── agents/
│   │   ├── reviewer.md
│   │   └── explorer.md
│   └── settings.json
└── docs/
    └── ai/
        ├── architecture.md
        └── release-runbook.md
```

---

## 📖 十三、常见反模式

| 反模式 | 症状 | 修复 |
|:---|:---|:---|
| CLAUDE.md 当 wiki | 每次加载污染上下文，关键指令被稀释 | 只保留契约，资料拆到 Skills 和 rules |
| Skill 大杂烩 | 描述无法稳定触发，工作流冲突 | 一个 Skill 只做一类事，副作用显式控制 |
| 工具太多描述模糊 | 选错工具，schema 挤爆上下文 | 合并重叠工具，做明确 namespacing |
| 没有验证闭环 | Claude 只能觉得自己完成了 | 给每类任务绑定 verifier |
| 过度自治 | 多 agent 并行无边界，出错难止损 | 角色/权限/worktree 最小化 |
| 上下文不做切分 | 研究、实现、审查全堆在主线程 | 任务切换 /clear，阶段切换 /compact |
| 自治范围过宽但治理不足 | 多 agent、外部工具全开，缺乏边界 | permissions + sandbox + hooks + subagent |
| 已批准命令堆积不清理 | settings.json 残留危险操作 | 定期审查 allowedTools 列表 |

---

## 📖 十四、配置健康检查

作者将文章六层框架整理成开源 Skill 项目 **tw93/waza**，可以一键检查 Claude Code 配置状态：

```bash
claude plugin marketplace add tw93/waza
claude plugin install health@waza
```

装好后在任意会话里跑 `/health`，输出优先级报告：需要立刻修 / 结构性问题 / 可以慢慢做。

---

## 💡 结语

用 Claude Code 大概会经历三个阶段：

| 阶段 | 关注点 | 效率感知 |
|:---:|:---|:---:|
| 工具使用者 | "这个功能怎么用" | 有帮助但有限 |
| 流程优化者 | "如何让协作更顺"——写 CLAUDE.md 和 Skills | 明显提升 |
| 系统设计者 | "如何让 Agent 在约束下自主运作" | **质变** |

> 有一个问题挺值得想的：**假如一个任务你说不清楚"什么叫做完"，那大概率也不适合直接扔给 Claude 自主完成。** 验证标准本身都没有，Claude 再聪明也跑不出正确答案。

---

## 🔗 参考资料

- **RTK（Rust Token Killer）**：https://www.rtk-ai.app/ | [开源在 GitHub](https://github.com/rtk-ai/rtk)
- **Kaku**（Tw93 的开源 terminal 项目）：https://github.com/tw93/Kaku
- **tw93/waza**（配置健康检查）：https://github.com/tw93/waza
- 请 Tw93 喝冰可乐 🥤：https://cats.tw93.fun/?name=Tw93

---

> *"觉得不错，请 Tw93 喝冰可乐 🥤"*
