---
title: '当对话历史实在太长、裁剪也不够用时，还有什么办法？什么是 Compaction？OpenClaw 的 Compaction 策略是怎样的？'
published: 2026-06-19
description: '当对话历史实在太长、裁剪也不够用时，还有什么办法？什么是 Compaction？OpenClaw 的 Compaction 策略是怎样的？'
category: '求职作战室'
tags: ['求职作战室', '知识点提炼']
draft: false
lang: zh-CN
---# 当对话历史实在太长、裁剪也不够用时，还有什么办法？什么是 Compaction？OpenClaw 的 Compaction 策略是怎样的？
## 问题
当对话历史实在太长、裁剪也不够用时，还有什么办法？什么是 Compaction？OpenClaw 的 Compaction 策略是怎样的？

## 标准回答
当对话历史实在太长、裁剪也不够用时，还有什么办法？什么是 Compaction？OpenClaw 的 Compaction 策略是怎样的？NEW中等AIOpenClaw大模型应用开发AI应用开发Agent开发裁剪是把早期消息直接丢掉，简单粗暴但会丢信息。Compaction（压实/压缩）换了个思路：用 LLM 把一大段对话历史"压缩"成一段精炼摘要，然后用摘要替换掉原始消息。打个比方，就像把一本 300 页的会议记录压缩成 5 页的纪要。篇幅大幅缩减，但关键决议、待办事项、重要结论都保留了。这样 Context 窗口腾出来了，关键信息也没丢。OpenClaw 的 Compaction 核心流程分 4 步走：分块（Chunking）：先把待压缩的消息按 token 预算切成多个 chunk（默认切 2 段）。切分在单条消息的边界进行，chunk 大小由 Context 窗口比例自适应计算。同时把最近几轮对话（默认 3 轮）分离出来保留原文，只压缩更早的消息。逐块摘要（Per-chunk Summarization）：每个 chunk 分别发给 LLM 生成一段摘要。如果某条消息超大（超过 Context 窗口的 50%），会走降级路径：先跳过超大消息只压缩小消息，再标注超大消息被省略了。合并摘要（Merge Summaries）：把多段局部摘要再调一次 LLM 融合成一份连贯的最终摘要，要求保留：进行中的任务状态、批量操作进度、用户最后的请求、决策及原因、待办事项和约束条件。摘要增强（Summary Augmentation）：在合并摘要基础上，追加额外上下文，比如工具调用失败记录（包含 exit code 和 error 状态）、文件操作记录（读过和修改过的文件列表）、最近几轮对话的原文摘要、以及从 AGENTS.md 提取的关键规则。最终结果替换掉原始消息，写入 session 历史。这个设计的核心理念是：宁可多花点 token 调一次 LLM 做摘要，也不要丢掉关键信息让后续任务翻车。

## 扩展知识

摘要质量检查压缩不是调一次 LLM 就完事了，OpenClaw 做了专门的质量校验。压缩完成后会检查摘要是否包含 5 个必要的结构化章节：Decisions（做过的决策）Open TODOs（未完成的任务）Constraints/Rules（约束条件）Pending user asks（用户尚未被回应的请求）Exact identifiers（需要精确保留的标识符）除了章节完整性之外，质量审计还会检查两个方面：摘要是否保留了从最近消息中提取的关键标识符（strict 策略下）以及摘要内容是否反映了用户最新的请求。不过需要注意，这套质量检查+重试机制（quality guard）默认是关闭的，需要在配置中显式启用。启用后，如果摘要未通过质量审计，会触发重试（最多重试 1 次，可配置，上限 3 次）。即使不启用 quality guard，结构化章节的要求也会通过 prompt 指令传达给 LLM，只是不会做事后校验和自动重试。标识符保留策略摘要有一个特别容易踩的坑：LLM 会把 UUID、hash、API key、URL、文件名这些标识符"概括"掉。比如把file: src/controllers/UserController.ts概括成"修改了一个控制器文件"，后续 Agent 想继续操作这个文件就找不到了。OpenClaw 默认采用strict 策略，要求摘要中精确保留所有不可重构的标识符。Compaction 的 prompt 里会给 LLM 一条通用指令，明确要求原样保留 UUID、hash、ID、token、API key、主机名、IP、端口、URL、文件名等。同时要求摘要必须包含一个 Exact identifiers 章节来列出关键标识符。注意 prompt 不会列举本次对话中出现的具体标识符，具体标识符的检验是在质量审计阶段，从最近 10 条消息中自动提取并比对摘要内容。Memory Flush 联动OpenClaw 还有一个很巧妙的设计：在接近 Compaction 阈值的时候，会先触发一次额外的 Agent 轮次（Memory Flush），让模型把重要信息主动写入 memory 目录。你可以把它理解成"考试交卷前最后再检查一遍"。模型知道自己的对话历史马上要被压缩了，所以赶紧把最重要的信息往长期存储里写一份。这样即使 Compaction 的摘要质量不理想，关键信息在 memory 目录里还有一份备份。这是短期记忆到长期记忆的逃生通道，保证信息不会因为压缩而彻底丢失。Post-compaction Context 注入压缩完成后，系统会从 AGENTS.md 里读取 "Session Startup" 和 "Red Lines" 两个部分，重新注入到上下文里。为什么要这么做？因为 Compaction 把早期消息替换成了摘要，但 Agent 的启动流程和红线规则可能就在那些被替换掉的早期消息里。如果不重新注入，模型压缩完之后可能忘了自己有哪些不能碰的红线，行为就可能失控。工具调用失败的特殊处理Compaction 还会专门提取并保留工具调用失败的信息，包括 exit code 和 error 状态。这些失败信息对后续任务成功率至关重要。比如 Agent 之前尝试过写入某个文件被权限拒绝了，如果这条失败记录在压缩时被丢掉，Agent 压缩后又会傻傻地去试一次，再失败，白白浪费一轮循环。保留失败记录就能让 Agent 直接跳过已知不可行的路径，换别的方案。

## 面试官追问

- **提问**：Compaction 本身也要调 LLM，那 token 开销大不大？会不会得不偿失？回答：单次 Compaction 大概消耗几千 token，跟一轮正常对话差不多。但它能把几万 token 的对话历史压缩到几千 token 的摘要，后续每一轮对话都省了大量 Context 开销。从整个 session 生命周期看，做 Compaction 的 token 总消耗远低于不做 Compaction 把完整历史一直带着。越长的对话收益越明显，100 轮的对话如果不压缩，光 Context 填充就要烧掉几十万 token 甚至更多。- **提问**：分段摘要的 chunk 大小怎么定的？切太小会不会丢上下文？
- **回答**：chunk 大小按 token 上限来切，默认是模型 Context 窗口的 40%（基准比例），会根据消息平均大小自适应调整（最低 15%），同时预留约 4096 token 给摘要 prompt 和推理预算。切的时候是在单条消息的边界切，不会把一条消息拆到两个 chunk 里，但不会刻意保证 user+assistant 对话回合的完整性。chunk 之间确实可能丢跨 chunk 的上下文关联，所以才需要合并摘要阶段，让 LLM 把多段摘要融合起来，补上跨段的逻辑关系。另外还有 20% 的安全缓冲来补偿 token 估算不准的问题。- **提问**：Compaction 触发的时机是什么？是固定轮次触发还是按 token 数触发？
- **回答**：按 token 数触发。每次拼完整的 prompt 之前会算一下当前对话历史占了多少 token，超过阈值就触发 Compaction。用固定轮次不靠谱，因为每轮对话的长度差异很大，有的轮次用户就说了一句话，有的轮次 Agent 调了 5 个工具返回一大堆结果。按 token 数控制才能精确地管住 Context 窗口的使用率。- **提问**：strict 策略保留标识符，但有些标识符已经过时了不需要了，不会造成摘要膨胀吗？
- **回答**：会。这是 strict 策略的一个已知代价，摘要会比宽松策略长一些。但在实际场景中，标识符占的 token 比例并不大，通常几十个 token 就能覆盖一个 session 里的所有关键标识符。相比丢失标识符导致后续任务失败再重试的 token 浪费，保留它们的成本低得多。如果确实需要清理过时标识符，可以在 Memory Flush 阶段让 Agent 主动判断哪些标识符还有用，只把有用的写入长期记忆。作者：Yes面试鸭官方
Compaction 压缩：用 LLM 把一大段对话历史压缩成一段精炼摘要，然后用摘要替换掉原始消息

摘要质量检查标识符保留策略Memory Flush 联动Post-compaction Context 注入工具调用失败的特殊处理

## 答案


摘要质量检查压缩不是调一次 LLM 就完事了，OpenClaw 做了专门的质量校验。压缩完成后会检查摘要是否包含 5 个必要的结构化章节：Decisions（做过的决策）Open TODOs（未完成的任务）Constraints/Rules（约束条件）Pending user asks（用户尚未被回应的请求）Exact identifiers（需要精确保留的标识符）除了章节完整性之外，质量审计还会检查两个方面：摘要是否保留了从最近消息中提取的关键标识符（strict 策略下）以及摘要内容是否反映了用户最新的请求。不过需要注意，这套质量检查+重试机制（quality guard）默认是关闭的，需要在配置中显式启用。启用后，如果摘要未通过质量审计，会触发重试（最多重试 1 次，可配置，上限 3 次）。即使不启用 quality guard，结构化章节的要求也会通过 prompt 指令传达给 LLM，只是不会做事后校验和自动重试。标识符保留策略摘要有一个特别容易踩的坑：LLM 会把 UUID、hash、API key、URL、文件名这些标识符"概括"掉。比如把file: src/controllers/UserController.ts概括成"修改了一个控制器文件"，后续 Agent 想继续操作这个文件就找不到了。OpenClaw 默认采用strict 策略，要求摘要中精确保留所有不可重构的标识符。Compaction 的 prompt 里会给 LLM 一条通用指令，明确要求原样保留 UUID、hash、ID、token、API key、主机名、IP、端口、URL、文件名等。同时要求摘要必须包含一个 Exact identifiers 章节来列出关键标识符。注意 prompt 不会列举本次对话中出现的具体标识符，具体标识符的检验是在质量审计阶段，从最近 10 条消息中自动提取并比对摘要内容。Memory Flush 联动OpenClaw 还有一个很巧妙的设计：在接近 Compaction 阈值的时候，会先触发一次额外的 Agent 轮次（Memory Flush），让模型把重要信息主动写入 memory 目录。你可以把它理解成"考试交卷前最后再检查一遍"。模型知道自己的对话历史马上要被压缩了，所以赶紧把最重要的信息往长期存储里写一份。这样即使 Compaction 的摘要质量不理想，关键信息在 memory 目录里还有一份备份。这是短期记忆到长期记忆的逃生通道，保证信息不会因为压缩而彻底丢失。Post-compaction Context 注入压缩完成后，系统会从 AGENTS.md 里读取 "Session Startup" 和 "Red Lines" 两个部分，重新注入到上下文里。为什么要这么做？因为 Compaction 把早期消息替换成了摘要，但 Agent 的启动流程和红线规则可能就在那些被替换掉的早期消息里。如果不重新注入，模型压缩完之后可能忘了自己有哪些不能碰的红线，行为就可能失控。工具调用失败的特殊处理Compaction 还会专门提取并保留工具调用失败的信息，包括 exit code 和 error 状态。这些失败信息对后续任务成功率至关重要。比如 Agent 之前尝试过写入某个文件被权限拒绝了，如果这条失败记录在压缩时被丢掉，Agent 压缩后又会傻傻地去试一次，再失败，白白浪费一轮循环。保留失败记录就能让 Agent 直接跳过已知不可行的路径，换别的方案。

- **提问**：Compaction 本身也要调 LLM，那 token 开销大不大？会不会得不偿失？回答：单次 Compaction 大概消耗几千 token，跟一轮正常对话差不多。但它能把几万 token 的对话历史压缩到几千 token 的摘要，后续每一轮对话都省了大量 Context 开销。从整个 session 生命周期看，做 Compaction 的 token 总消耗远低于不做 Compaction 把完整历史一直带着。越长的对话收益越明显，100 轮的对话如果不压缩，光 Context 填充就要烧掉几十万 token 甚至更多。- **提问**：分段摘要的 chunk 大小怎么定的？切太小会不会丢上下文？
- **回答**：chunk 大小按 token 上限来切，默认是模型 Context 窗口的 40%（基准比例），会根据消息平均大小自适应调整（最低 15%），同时预留约 4096 token 给摘要 prompt 和推理预算。切的时候是在单条消息的边界切，不会把一条消息拆到两个 chunk 里，但不会刻意保证 user+assistant 对话回合的完整性。chunk 之间确实可能丢跨 chunk 的上下文关联，所以才需要合并摘要阶段，让 LLM 把多段摘要融合起来，补上跨段的逻辑关系。另外还有 20% 的安全缓冲来补偿 token 估算不准的问题。- **提问**：Compaction 触发的时机是什么？是固定轮次触发还是按 token 数触发？
- **回答**：按 token 数触发。每次拼完整的 prompt 之前会算一下当前对话历史占了多少 token，超过阈值就触发 Compaction。用固定轮次不靠谱，因为每轮对话的长度差异很大，有的轮次用户就说了一句话，有的轮次 Agent 调了 5 个工具返回一大堆结果。按 token 数控制才能精确地管住 Context 窗口的使用率。- **提问**：strict 策略保留标识符，但有些标识符已经过时了不需要了，不会造成摘要膨胀吗？
- **回答**：会。这是 strict 策略的一个已知代价，摘要会比宽松策略长一些。但在实际场景中，标识符占的 token 比例并不大，通常几十个 token 就能覆盖一个 session 里的所有关键标识符。相比丢失标识符导致后续任务失败再重试的 token 浪费，保留它们的成本低得多。如果确实需要清理过时标识符，可以在 Memory Flush 阶段让 Agent 主动判断哪些标识符还有用，只把有用的写入长期记忆。作者：Yes面试鸭官方
Compaction 压缩：用 LLM 把一大段对话历史压缩成一段精炼摘要，然后用摘要替换掉原始消息

摘要质量检查标识符保留策略Memory Flush 联动Post-compaction Context 注入工具调用失败的特殊处理

---

> 来源: 当对话历史实在太长、裁剪也不够用时，还有什么办法？什么是 Compaction？OpenClaw 的 Compaction 策略是怎样的？.mhtml

## 

## 关键点

- # 当对话历史实在太长、裁剪也不够用时，还有什么办法？
- 什么是 Compaction？
- OpenClaw 的 Compaction 策略是怎样的？
- ## 问题
当对话历史实在太长、裁剪也不够用时，还有什么办法？
- 什么是 Compaction？

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

当对话历史实在太长、裁剪也不够用时，还有什么办法？什么是 Compaction？OpenClaw 的 Compaction 策略是怎样的？
- ## 标准回答

- ## 问题
当对话历史实在太长、裁剪也不够用时，还有什么办法？什么是 Compaction？OpenClaw 的 Compaction 策略是怎样的？NEW中等AIOpenClaw大模型应用开发AI应用开发Agent开发裁剪是把早期消息直接丢掉，简单粗暴但会丢信息。Compaction（压实/压缩）换了个思路：用 LLM 把一大段对话历史"压缩"成一段精炼摘要，然后用摘要替换掉原始消息。打个比方，就像把一本 300 页的会议记录压缩成 5 页的纪要。篇幅大幅缩减，但关键决议、待办事项、重要结论都保留了。这样 Context 窗口腾出来了，关键信息也没丢。OpenClaw 的 Compaction 核心流程分 4 步走：分块（Chunking）：先把待压缩的消息按 token 预算切成多个 chunk（默认切 2 段）。切分在单条消息的边界进行，chunk 大小由 Context 窗口比例自适应计算。同时把最近几轮对话（默认 3 轮）分离出来保留原文，只压缩更早的消息。逐块摘要（Per-chunk Summarization）：每个 chunk 分别发给 LLM 生成一段摘要。如果某条消息超大（超过 Context 窗口的 50%），会走降级路径：先跳过超大消息只压缩小消息，再标注超大消息被省略了。合并摘要（Merge Summaries）：把多段局部摘要再调一次 LLM 融合成一份连贯的最终摘要，要求保留：进行中的任务状态、批量操作进度、用户最后的请求、决策及原因、待办事项和约束条件。摘要增强（Summary Augmentation）：在合并摘要基础上，追加额外上下文，比如工具调用失败记录（包含 exit code 和 error 状态）、文件操作记录（读过和修改过的文件列表）、最近几轮对话的原文摘要、以及从 AGENTS.md 提取的关键规则。最终结果替换掉原始消息，写入 session 历史。这个设计的核心理念是：宁可多花点 token 调一次 LLM 做摘要，也不要丢掉关键信息让后续任务翻车。

摘要质量检查压缩不是调一次 LLM 就完事了，OpenClaw 做了专门的质量校验。压缩完成后会检查摘要是否包含 5 个必要的结构化章节：Decisions（做过的决策）Open TODOs（未完成的任务）Constraints/Rules（约束条件）Pending user asks（用户尚未被回应的请求）Exact identifiers（需要精确保留的标识符）除了章节完整性之外，质量审计还会检查两个方面：摘要是否保留了从最近消息中提取的关键标识符（strict 策略下）以及摘要内容是否反映了用户最新的请求。不过需要注意，这套质量检查+重试机制（quality guard）默认是关闭的，需要在配置中显式启用。启用后，如果摘要未通过质量审计，会触发重试（最多重试 1 次，可配置，上限 3 次）。即使不启用 quality guard，结构化章节的要求也会通过 prompt 指令传达给 LLM，只是不会做事后校验和自动重试。标识符保留策略摘要有一个特别容易踩的坑：LLM 会把 UUID、hash、API key、URL、文件名这些标识符"概括"掉。比如把file: src/controllers/UserController.ts概括成"修改了一个控制器文件"，后续 Agent 想继续操作这个文件就找不到了。OpenClaw 默认采用strict 策略，要求摘要中精确保留所有不可重构的标识符。Compaction 的 prompt 里会给 LLM 一条通用指令，明确要求原样保留 UUID、hash、ID、token、API key、主机名、IP、端口、URL、文件名等。同时要求摘要必须包含一个 Exact identifiers 章节来列出关键标识符。注意 prompt 不会列举本次对话中出现的具体标识符，具体标识符的检验是在质量审计阶段，从最近 10 条消息中自动提取并比对摘要内容。Memory Flush 联动OpenClaw 还有一个很巧妙的设计：在接近 Compaction 阈值的时候，会先触发一次额外的 Agent 轮次（Memory Flush），让模型把重要信息主动写入 memory 目录。你可以把它理解成"考试交卷前最后再检查一遍"。模型知道自己的对话历史马上要被压缩了，所以赶紧把最重要的信息往长期存储里写一份。这样即使 Compaction 的摘要质量不理想，关键信息在 memory 目录里还有一份备份。这是短期记忆到长期记忆的逃生通道，保证信息不会因为压缩而彻底丢失。Post-compaction Context 注入压缩完成后，系统会从 AGENTS.md 里读取 "Session Startup" 和 "Red Lines" 两个部分，重新注入到上下文里。为什么要这么做？因为 Compaction 把早期消息替换成了摘要，但 Agent 的启动流程和红线规则可能就在那些被替换掉的早期消息里。如果不重新注入，模型压缩完之后可能忘了自己有哪些不能碰的红线，行为就可能失控。工具调用失败的特殊处理Compaction 还会专门提取并保留工具调用失败的信息，包括 exit code 和 error 状态。这些失败信息对后续任务成功率至关重要。比如 Agent 之前尝试过写入某个文件被权限拒绝了，如果这条失败记录在压缩时被丢掉，Agent 压缩后又会傻傻地去试一次，再失败，白白浪费一轮循环。保留失败记录就能让 Agent 直接跳过已知不可行的路径，换别的方案。

- **提问**：Compaction 本身也要调 LLM，那 token 开销大不大？会不会得不偿失？回答：单次 Compaction 大概消耗几千 token，跟一轮正常对话差不多。但它能把几万 token 的对话历史压缩到几千 token 的摘要，后续每一轮对话都省了大量 Context 开销。从整个 session 生命周期看，做 Compaction 的 token 总消耗远低于不做 Compaction 把完整历史一直带着。越长的对话收益越明显，100 轮的对话如果不压缩，光 Context 填充就要烧掉几十万 token 甚至更多。- **提问**：分段摘要的 chunk 大小怎么定的？切太小会不会丢上下文？
- **回答**：chunk 大小按 token 上限来切，默认是模型 Context 窗口的 40%（基准比例），会根据消息平均大小自适应调整（最低 15%），同时预留约 4096 token 给摘要 prompt 和推理预算。切的时候是在单条消息的边界切，不会把一条消息拆到两个 chunk 里，但不会刻意保证 user+assistant 对话回合的完整性。chunk 之间确实可能丢跨 chunk 的上下文关联，所以才需要合并摘要阶段，让 LLM 把多段摘要融合起来，补上跨段的逻辑关系。另外还有 20% 的安全缓冲来补偿 token 估算不准的问题。- **提问**：Compaction 触发的时机是什么？是固定轮次触发还是按 token 数触发？
- **回答**：按 token 数触发。每次拼完整的 prompt 之前会算一下当前对话历史占了多少 token，超过阈值就触发 Compaction。用固定轮次不靠谱，因为每轮对话的长度差异很大，有的轮次用户就说了一句话，有的轮次 Agent 调了 5 个工具返回一大堆结果。按 token 数控制才能精确地管住 Context 窗口的使用率。- **提问**：strict 策略保留标识符，但有些标识符已经过时了不需要了，不会造成摘要膨胀吗？
- **回答**：会。这是 strict 策略的一个已知代价，摘要会比宽松策略长一些。但在实际场景中，标识符占的 token 比例并不大，通常几十个 token 就能覆盖一个 session 里的所有关键标识符。相比丢失标识符导致后续任务失败再重试的 token 浪费，保留它们的成本低得多。如果确实需要清理过时标识符，可以在 Memory Flush 阶段让 Agent 主动判断哪些标识符还有用，只把有用的写入长期记忆。作者：Yes面试鸭官方
Compaction 压缩：用 LLM 把一大段对话历史压缩成一段精炼摘要，然后用摘要替换掉原始消息

摘要质量检查标识符保留策略Memory Flush 联动Post-compaction Context 注入工具调用失败的特殊处理


摘要质量检查压缩不是调一次 LLM 就完事了，OpenClaw 做了专门的质量校验。压缩完成后会检查摘要是否包含 5 个必要的结构化章节：Decisions（做过的决策）Open TODOs（未完成的任务）Constraints/Rules（约束条件）Pending user asks（用户尚未被回应的请求）Exact identifiers（需要精确保留的标识符）除了章节完整性之外，质量审计还会检查两个方面：摘要是否保留了从最近消息中提取的关键标识符（strict 策略下）以及摘要内容是否反映了用户最新的请求。不过需要注意，这套质量检查+重试机制（quality guard）默认是关闭的，需要在配置中显式启用。启用后，如果摘要未通过质量审计，会触发重试（最多重试 1 次，可配置，上限 3 次）。即使不启用 quality guard，结构化章节的要求也会通过 prompt 指令传达给 LLM，只是不会做事后校验和自动重试。标识符保留策略摘要有一个特别容易踩的坑：LLM 会把 UUID、hash、API key、URL、文件名这些标识符"概括"掉。比如把file: src/controllers/UserController.ts概括成"修改了一个控制器文件"，后续 Agent 想继续操作这个文件就找不到了。OpenClaw 默认采用strict 策略，要求摘要中精确保留所有不可重构的标识符。Compaction 的 prompt 里会给 LLM 一条通用指令，明确要求原样保留 UUID、hash、ID、token、API key、主机名、IP、端口、URL、文件名等。同时要求摘要必须包含一个 Exact identifiers 章节来列出关键标识符。注意 prompt 不会列举本次对话中出现的具体标识符，具体标识符的检验是在质量审计阶段，从最近 10 条消息中自动提取并比对摘要内容。Memory Flush 联动OpenClaw 还有一个很巧妙的设计：在接近 Compaction 阈值的时候，会先触发一次额外的 Agent 轮次（Memory Flush），让模型把重要信息主动写入 memory 目录。你可以把它理解成"考试交卷前最后再检查一遍"。模型知道自己的对话历史马上要被压缩了，所以赶紧把最重要的信息往长期存储里写一份。这样即使 Compaction 的摘要质量不理想，关键信息在 memory 目录里还有一份备份。这是短期记忆到长期记忆的逃生通道，保证信息不会因为压缩而彻底丢失。Post-compaction Context 注入压缩完成后，系统会从 AGENTS.md 里读取 "Session Startup" 和 "Red Lines" 两个部分，重新注入到上下文里。为什么要这么做？因为 Compaction 把早期消息替换成了摘要，但 Agent 的启动流程和红线规则可能就在那些被替换掉的早期消息里。如果不重新注入，模型压缩完之后可能忘了自己有哪些不能碰的红线，行为就可能失控。工具调用失败的特殊处理Compaction 还会专门提取并保留工具调用失败的信息，包括 exit code 和 error 状态。这些失败信息对后续任务成功率至关重要。比如 Agent 之前尝试过写入某个文件被权限拒绝了，如果这条失败记录在压缩时被丢掉，Agent 压缩后又会傻傻地去试一次，再失败，白白浪费一轮循环。保留失败记录就能让 Agent 直接跳过已知不可行的路径，换别的方案。

- **提问**：Compaction 本身也要调 LLM，那 token 开销大不大？会不会得不偿失？回答：单次 Compaction 大概消耗几千 token，跟一轮正常对话差不多。但它能把几万 token 的对话历史压缩到几千 token 的摘要，后续每一轮对话都省了大量 Context 开销。从整个 session 生命周期看，做 Compaction 的 token 总消耗远低于不做 Compaction 把完整历史一直带着。越长的对话收益越明显，100 轮的对话如果不压缩，光 Context 填充就要烧掉几十万 token 甚至更多。- **提问**：分段摘要的 chunk 大小怎么定的？切太小会不会丢上下文？
- **回答**：chunk 大小按 token 上限来切，默认是模型 Context 窗口的 40%（基准比例），会根据消息平均大小自适应调整（最低 15%），同时预留约 4096 token 给摘要 prompt 和推理预算。切的时候是在单条消息的边界切，不会把一条消息拆到两个 chunk 里，但不会刻意保证 user+assistant 对话回合的完整性。chunk 之间确实可能丢跨 chunk 的上下文关联，所以才需要合并摘要阶段，让 LLM 把多段摘要融合起来，补上跨段的逻辑关系。另外还有 20% 的安全缓冲来补偿 token 估算不准的问题。- **提问**：Compaction 触发的时机是什么？是固定轮次触发还是按 token 数触发？
- **回答**：按 token 数触发。每次拼完整的 prompt 之前会算一下当前对话历史占了多少 token，超过阈值就触发 Compaction。用固定轮次不靠谱，因为每轮对话的长度差异很大，有的轮次用户就说了一句话，有的轮次 Agent 调了 5 个工具返回一大堆结果。按 token 数控制才能精确地管住 Context 窗口的使用率。- **提问**：strict 策略保留标识符，但有些标识符已经过时了不需要了，不会造成摘要膨胀吗？
- **回答**：会。这是 strict 策略的一个已知代价，摘要会比宽松策略长一些。但在实际场景中，标识符占的 token 比例并不大，通常几十个 token 就能覆盖一个 session 里的所有关键标识符。相比丢失标识符导致后续任务失败再重试的 token 浪费，保留它们的成本低得多。如果确实需要清理过时标识符，可以在 Memory Flush 阶段让 Agent 主动判断哪些标识符还有用，只把有用的写入长期记忆。作者：Yes面试鸭官方
Compaction 压缩：用 LLM 把一大段对话历史压缩成一段精炼摘要，然后用摘要替换掉原始消息

摘要质量检查标识符保留策略Memory Flush 联动Post-compaction Context 注入工具调用失败的特殊处理

---

> 来源: 当对话历史实在太长、裁剪也不够用时，还有什么办法？什么是 Compaction？OpenClaw 的 Compaction 策略是怎样的？.mhtml

- # 当对话历史实在太长、裁剪也不够用时，还有什么办法？
- - 什么是 Compaction？
- - OpenClaw 的 Compaction 策略是怎样的？

- 本文已做格式统一与噪声清理，保留原始语义。
- 当对话历史实在太长、裁剪也不够用时，还有什么办法？什么是 Compaction？OpenClaw 的 Compaction 策略是怎样的？
- # 当对话历史实在太长、裁剪也不够用时，还有什么办法？什么是 Compaction？OpenClaw 的 Compaction 策略是怎样的？
- 13231. 当对话历史实在太长、裁剪也不够用时，还有什么办法？什么是 Compaction？OpenClaw 的 Compaction 策略是怎样的？NEW中等AIOpenClaw大模型应用开发AI应用开发Agent开发裁剪是把早期消息直接丢掉，简单粗暴但会丢信息。Compaction（压实/压缩）换了个思路：用 LLM 把一大段对话历史"压缩"成一段精炼摘要，然后用摘要替换掉原始消息。打个比方，就像把一本 300 页的会议记录压缩成 5 页的纪要。篇幅大幅缩减，但关键决议、待办事项、重要结论都保留了。这样 Context 窗口腾出来了，关键信息也没丢。OpenClaw 的 Compaction 核心流程分 4 步走：分块（Chunking）：先把待压缩的消息按 token 预算切成多个 chunk（默认切 2 段）。切分在单条消息的边界进行，chunk 大小由 Context 窗口比例自适应计算。同时把最近几轮对话（默认 3 轮）分离出来保留原文，只压缩更早的消息。逐块摘要（Per-chunk Summarization）：每个 chunk 分别发给 LLM 生成一段摘要。如果某条消息超大（超过 Context 窗口的 50%），会走降级路径：先跳过超大消息只压缩小消息，再标注超大消息被省略了。合并摘要（Merge Summaries）：把多段局部摘要再调一次 LLM 融合成一份连贯的最终摘要，要求保留：进行中的任务状态、批量操作进度、用户最后的请求、决策及原因、待办事项和约束条件。摘要增强（Summary Augmentation）：在合并摘要基础上，追加额外上下文，比如工具调用失败记录（包含 exit code 和 error 状态）、文件操作记录（读过和修改过的文件列表）、最近几轮对话的原文摘要、以及从 AGENTS.md 提取的关键规则。最终结果替换掉原始消息，写入 session 历史。这个设计的核心理念是：宁可多花点 token 调一次 LLM 做摘要，也不要丢掉关键信息让后续任务翻车。

摘要质量检查压缩不是调一次 LLM 就完事了，OpenClaw 做了专门的质量校验。压缩完成后会检查摘要是否包含 5 个必要的结构化章节：Decisions（做过的决策）Open TODOs（未完成的任务）Constraints/Rules（约束条件）Pending user asks（用户尚未被回应的请求）Exact identifiers（需要精确保留的标识符）除了章节完整性之外，质量审计还会检查两个方面：摘要是否保留了从最近消息中提取的关键标识符（strict 策略下）以及摘要内容是否反映了用户最新的请求。不过需要注意，这套质量检查+重试机制（quality guard）默认是关闭的，需要在配置中显式启用。启用后，如果摘要未通过质量审计，会触发重试（最多重试 1 次，可配置，上限 3 次）。即使不启用 quality guard，结构化章节的要求也会通过 prompt 指令传达给 LLM，只是不会做事后校验和自动重试。标识符保留策略摘要有一个特别容易踩的坑：LLM 会把 UUID、hash、API key、URL、文件名这些标识符"概括"掉。比如把file: src/controllers/UserController.ts概括成"修改了一个控制器文件"，后续 Agent 想继续操作这个文件就找不到了。OpenClaw 默认采用strict 策略，要求摘要中精确保留所有不可重构的标识符。Compaction 的 prompt 里会给 LLM 一条通用指令，明确要求原样保留 UUID、hash、ID、token、API key、主机名、IP、端口、URL、文件名等。同时要求摘要必须包含一个 Exact identifiers 章节来列出关键标识符。注意 prompt 不会列举本次对话中出现的具体标识符，具体标识符的检验是在质量审计阶段，从最近 10 条消息中自动提取并比对摘要内容。Memory Flush 联动OpenClaw 还有一个很巧妙的设计：在接近 Compaction 阈值的时候，会先触发一次额外的 Agent 轮次（Memory Flush），让模型把重要信息主动写入 memory 目录。你可以把它理解成"考试交卷前最后再检查一遍"。模型知道自己的对话历史马上要被压缩了，所以赶紧把最重要的信息往长期存储里写一份。这样即使 Compaction 的摘要质量不理想，关键信息在 memory 目录里还有一份备份。这是短期记忆到长期记忆的逃生通道，保证信息不会因为压缩而彻底丢失。Post-compaction Context 注入压缩完成后，系统会从 AGENTS.md 里读取 "Session Startup" 和 "Red Lines" 两个部分，重新注入到上下文里。为什么要这么做？因为 Compaction 把早期消息替换成了摘要，但 Agent 的启动流程和红线规则可能就在那些被替换掉的早期消息里。如果不重新注入，模型压缩完之后可能忘了自己有哪些不能碰的红线，行为就可能失控。工具调用失败的特殊处理Compaction 还会专门提取并保留工具调用失败的信息，包括 exit code 和 error 状态。这些失败信息对后续任务成功率至关重要。比如 Agent 之前尝试过写入某个文件被权限拒绝了，如果这条失败记录在压缩时被丢掉，Agent 压缩后又会傻傻地去试一次，再失败，白白浪费一轮循环。保留失败记录就能让 Agent 直接跳过已知不可行的路径，换别的方案。

- **提问**：Compaction 本身也要调 LLM，那 token 开销大不大？会不会得不偿失？回答：单次 Compaction 大概消耗几千 token，跟一轮正常对话差不多。但它能把几万 token 的对话历史压缩到几千 token 的摘要，后续每一轮对话都省了大量 Context 开销。从整个 session 生命周期看，做 Compaction 的 token 总消耗远低于不做 Compaction 把完整历史一直带着。越长的对话收益越明显，100 轮的对话如果不压缩，光 Context 填充就要烧掉几十万 token 甚至更多。- **提问**：分段摘要的 chunk 大小怎么定的？切太小会不会丢上下文？
- **回答**：chunk 大小按 token 上限来切，默认是模型 Context 窗口的 40%（基准比例），会根据消息平均大小自适应调整（最低 15%），同时预留约 4096 token 给摘要 prompt 和推理预算。切的时候是在单条消息的边界切，不会把一条消息拆到两个 chunk 里，但不会刻意保证 user+assistant 对话回合的完整性。chunk 之间确实可能丢跨 chunk 的上下文关联，所以才需要合并摘要阶段，让 LLM 把多段摘要融合起来，补上跨段的逻辑关系。另外还有 20% 的安全缓冲来补偿 token 估算不准的问题。- **提问**：Compaction 触发的时机是什么？是固定轮次触发还是按 token 数触发？
- **回答**：按 token 数触发。每次拼完整的 prompt 之前会算一下当前对话历史占了多少 token，超过阈值就触发 Compaction。用固定轮次不靠谱，因为每轮对话的长度差异很大，有的轮次用户就说了一句话，有的轮次 Agent 调了 5 个工具返回一大堆结果。按 token 数控制才能精确地管住 Context 窗口的使用率。- **提问**：strict 策略保留标识符，但有些标识符已经过时了不需要了，不会造成摘要膨胀吗？
- **回答**：会。这是 strict 策略的一个已知代价，摘要会比宽松策略长一些。但在实际场景中，标识符占的 token 比例并不大，通常几十个 token 就能覆盖一个 session 里的所有关键标识符。相比丢失标识符导致后续任务失败再重试的 token 浪费，保留它们的成本低得多。如果确实需要清理过时标识符，可以在 Memory Flush 阶段让 Agent 主动判断哪些标识符还有用，只把有用的写入长期记忆。作者：Yes面试鸭官方- Compaction 压缩：用 LLM 把一大段对话历史压缩成一段精炼摘要，然后用摘要替换掉原始消息
摘要质量检查标识符保留策略Memory Flush 联动Post-compaction Context 注入工具调用失败的特殊处理

- 本文已做格式统一与噪声清理，保留原始语义。
