---
title: "面经库｜现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑 整理"
published: 2026-06-10
description: "# 现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑 ## 问题 现场实操：给定一个包含数据Schema的API文档，请使用AI工具？ 15分钟内"
tags: ["面经", "面经库"]
category: "面经整理"
draft: false
lang: zh-CN
pinned: false
comment: true
---

# 现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑
## 问题
现场实操：给定一个包含数据Schema的API文档，请使用AI工具？
15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑

## 标准回答
现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑VIP中等大模型为方便拷贝至编辑器，以下文档以 Markdown 源码进行展示▼markdown复制代码# TodoList API 文档 (v1.0)## 基础信息-**Base URL**:`https://api.example.com/v1`-**数据格式**: JSON-认证方式: Bearer Token (需在Header中添加`Authorization: Bearer <token>`)

---## 数据结构 Schema### Todo 对象| 字段名       | 类型    | 必填 | 描述                     |

|--------------|---------|------|--------------------------|

|`id`| string  | 是   | 唯一标识符 (UUIDv4)      |

|`title`| string  | 是   | 任务标题 (1-100字符)     |

|`description`| string  | 否   | 任务描述 (可选)          |

|`status`| enum    | 是   |`pending`/`completed`|

|`dueDate`| string  | 否   | 截止日期 (ISO8601格式)   |

|`createdAt`| string  | 是   | 创建时间 (ISO8601格式)   |

|`updatedAt`| string  | 是   | 最后更新时间 (ISO8601)   |

---## API 接口列表### 1. 获取Todo列表**GET**`/todos`#### 参数| 参数名     | 类型    | 默认值 | 描述                     |

|------------|---------|--------|--------------------------|

|`status`| string  | -      | 过滤状态 (`pending/completed`) |

|`page`| integer | 1      | 分页页码                 |

|`limit`| integer | 20     | 每页数量 (最大100)       |#### 响应示例```json

{

"total": 45,

"page": 1,

"limit": 20,

"items": [

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "购买食材",

"status": "pending",

"dueDate": "2025-03-30T09:00:00Z",

"createdAt": "2025-03-28T14:30:00Z"

}

]

}

` ` `

---

### 2. 创建新Todo

**POST** `/todos`

#### 请求体

```json

{

"title": "项目会议准备",

"description": "准备季度项目汇报材料",

"dueDate": "2025-04-01T14:00:00Z"

}` ``#### 响应 (201 Created)```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "项目会议准备",

"status": "pending",

"dueDate": "2025-04-01T14:00:00Z",

"createdAt": "2025-03-28T15:00:00Z"

}

` ` `

---

### 3. 获取单个Todo详情

**GET** `/todos/{id}`

#### 响应示例

```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "项目会议准备",

"description": "准备季度项目汇报材料",

"status": "pending",

"dueDate": "2025-04-01T14:00:00Z",

"createdAt": "2025-03-28T15:00:00Z",

"updatedAt": "2025-03-28T15:00:00Z"

}` ``

---### 4. 更新Todo信息**PATCH**`/todos/{id}`#### 请求体 (部分更新)```json

{

"title": "更新后的会议准备",

"status": "completed"

}

` ` `

#### 响应

```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "更新后的会议准备",

"status": "completed",

"updatedAt": "2025-03-28T16:00:00Z"

}` ``

---### 5. 删除Todo**DELETE**`/todos/{id}`#### 响应 (204 No Content)---### 6. 批量更新状态**POST**`/todos/batch-update`#### 请求体```json

{

"ids": ["id1", "id2"],

"status": "completed"

}

` ` `

#### 响应

```json

{

"updatedCount": 2

}` ``

---## 错误处理| 状态码 | 描述                  |

|--------|-----------------------|

| 400    | 请求参数验证失败      |

| 401    | 未授权访问            |

| 404    | 资源不存在            |

| 429    | 请求频率限制          |

| 500    | 服务器内部错误        |

错误响应示例：```json

{

"error": {

"code": "INVALID_DUE_DATE",

"message": "截止日期不能早于当前时间"

}

}

` ` `标记分享51006这道实操题考察的是Prompt 工程能力和对 RESTful 规范的理解，核心思路是把 Schema 喂给 AI，再通过结构化 Prompt 引导它生成标准 CRUD 代码。整个操作流程分 3 步：1）先把 API 文档里的 Schema 提取出来，比如一个用户表有 id、name、email、created_at 这些字段2）构造一个精准的 Prompt，明确告诉 AI 要用什么框架、遵循什么规范、返回什么格式3）拿到生成的代码后快速 review，重点看路由设计、参数校验、异常处理这几块假设 Schema 是这样的：▼json复制代码{"User":{"id":"long, 主键","name":"string, 必填, 最大50字符","email":"string, 必填, 邮箱格式","created_at":"datetime, 自动生成"}}给 AI 的 Prompt 可以这样写：▼text复制代码基于以下 Schema 生成 Spring Boot 的 RESTful CRUD 接口：-框架：Spring Boot 3.x + Spring Data JPA-规范：严格遵循 RESTful，GET 用于查询，POST 用于创建，PUT 用于全量更新，DELETE 用于删除-响应格式：统一包装成 {code, message, data} 结构-要求：包含参数校验注解、异常处理Schema:

{粘贴上面的 JSON}AI 生成的 Controller 核心代码大概长这样：▼java复制代码@RestController@RequestMapping("/api/users")publicclassUserController{@AutowiredprivateUserService userService;@GetMapping("/{id}")publicResult<User>getById(@PathVariableLong id){returnResult.success(userService.findById(id));

}@PostMappingpublicResult<User>create(@Valid@RequestBodyUserCreateDTO dto){returnResult.success(userService.create(dto));

}@PutMapping("/{id}")publicResult<User>update(@PathVariableLong id,@Valid@RequestBodyUserUpdateDTO dto){returnResult.success(userService.update(id, dto));

}@DeleteMapping("/{id}")publicResult<Void>delete(@PathVariableLong id){

userService.delete(id);returnResult.success(null);

}

}拿到代码后重点检查这几个地方：路由是不是用了复数名词、HTTP 方法用得对不对、有没有加@Valid做参数校验。

## 扩展知识

Prompt 优化技巧很多人用 AI 生成代码效果不好，问题往往出在 Prompt 太模糊。AI 不是人，它猜不到你想要 Spring Boot 还是 Express，猜不到你们公司用的是驼峰还是下划线命名。一个高质量的 Prompt 要包含 4 个要素：1）技术栈版本，比如 Spring Boot 3.2、JDK 17、MyBatis Plus 3.52）编码规范，比如 RESTful 风格、统一响应体结构、驼峰命名3）完整上下文，Schema 要全贴上去，字段类型、约束条件一个都不能少4）反例约束，告诉 AI 不要干什么，比如"不要用 Lombok"、"不要用 XML 配置"生成代码的 Review 重点AI 生成的代码不能直接用，至少要检查这几个地方：1）安全性漏洞，有没有 SQL 注入风险、有没有做权限校验2）异常处理是不是完善，空指针、资源不存在这些边界情况覆盖了没有3）事务边界对不对，涉及多表操作的有没有加@Transactional4）日志是不是规范，关键操作有没有打日志，日志级别用得对不对不同 AI 工具的差异现在市面上 AI 编程工具很多，Cursor、GitHub Copilot、通义灵码、CodeGeeX 各有特点：工具强项弱项Cursor上下文理解强，能读懂整个项目收费，国内网络不稳定Copilot补全速度快，和 IDE 集成好对中文注释理解一般通义灵码中文支持好，免费额度多复杂逻辑生成质量不如前两者CodeGeeX完全免费，国产模型偶尔会生成过时 API面试现场实操建议15 分钟时间很紧，建议这样分配：1）前 3 分钟，快速阅读 Schema，理解业务含义，想清楚要生成哪些接口2）中间 8 分钟，写 Prompt、喂给 AI、拿到代码、快速调整明显问题3）最后 4 分钟，给面试官讲解代码结构和设计决策，展示你的工程思维关键是要表现出你不是在无脑用 AI，而是知道 AI 生成的东西哪里可能有坑、怎么 review、怎么改进。

## 面试官追问

- **提问**：如果 AI 生成的代码有明显的安全漏洞，你会怎么处理？回答：拿到代码第一件事就是扫一遍安全问题。如果发现有 SQL 拼接这种明显漏洞，直接手动改成参数化查询。如果是鉴权没做，补上@PreAuthorize或者自定义拦截器。改完之后会反向给 AI 一个反馈，告诉它下次要注意这个点，后续生成的代码质量会提升。- **提问**：RESTful 规范里 PUT 和 PATCH 有什么区别，生成代码时要怎么选？
- **回答**：PUT 是全量更新，客户端得把所有字段都传过来，没传的字段会被置空。PATCH 是部分更新，只更新传了的字段。实际项目里 PATCH 用得更多，因为前端很少会一次性改全部字段。生成代码时如果是编辑场景，优先用 PATCH 加一个非空校验逻辑。- **提问**：如果时间来不及，AI 生成的代码只来得及做部分修改，你会优先改哪里？
- **回答**：优先级是安全 > 正确性 > 规范性。第一改安全漏洞，比如 SQL 注入、越权访问。第二改逻辑错误，比如空指针、边界条件没处理。第三才是代码风格、命名规范这些。规范性的问题不影响功能，面试完再改也行。

Prompt 优化技巧生成代码的 Review 重点不同 AI 工具的差异面试现场实操建议

提问：如果 AI 生成的代码有明显的安全漏洞，你会怎么处理？提问：RESTful 规范里 PUT 和 PATCH 有什么区别，生成代码时要怎么选？提问：如果时间来不及，AI 生成的代码只来得及做部分修改，你会优先改哪里？热门面试题目榜更多说说 Java 中 HashMap 的原理？9130Java 中的序列化和反序列化是什么？6255MySQL 索引的最左前缀匹配原则是什么？5662Java 中 ConcurrentHashMap 1.7 和 1.8 之间有哪些区别？5067Java 中有哪些集合类？请简单介绍4854MySQL 的索引类型有哪些？4845详细描述一条 SQL 语句在 MySQL 中的执行过程。4218什么是 RAG？RAG 的主要流程是什么？4151MySQL 的存储引擎有哪些？它们之间有什么区别？4092数据库的脏读、不可重复读和幻读分别是什么？3900推荐教程更多AI 超级智能体亿级流量点赞系统教程智能协同云图库项目教程预览用户交流一起刷题学习、求职交流、反馈建议、获取更新通知面试鸭《用户协议》《隐私政策》友情链接编程导航老鱼简历代码小抄剪切助手联系我们商务合作站长：程序员鱼皮关注我们扫码关注面试鸭公众号

## 答案

设计智能客服系统时，如何通过知识库构建解决长尾问题？请描述具体实现步骤当大模型API响应延迟超过1秒时，前端可以采取哪些优化策略保证用户体验？上次浏览：2026-03-16 15:08:14使用LangChain时，如何实现多路召回结果的动态权重分配？上次浏览：2026-03-16 15:09:02当大模型上下文窗口扩展到100万token时，哪些现有业务场景可能发生质变？当发现RAG系统召回结果与用户query意图不匹配时，有哪些可能的改进方向？使用LangChain实现RAG系统时，如何处理PDF文档中的表格数据召回问题？现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑参数高效微调（PEFT）如何减少计算成本？冻结层在微调中的作用是什么？为什么需要混合精度训练？上次浏览：2026-03-16 15:09:27模型输出重复和幻觉如何微调解决？上次浏览：2026-03-16 15:10:0511345. 现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑VIP中等大模型为方便拷贝至编辑器，以下文档以 Markdown 源码进行展示▼markdown复制代码# TodoList API 文档 (v1.0)## 基础信息-**Base URL**:`https://api.example.com/v1`-**数据格式**: JSON-认证方式: Bearer Token (需在Header中添加`Authorization: Bearer <token>`)

---## 数据结构 Schema### Todo 对象| 字段名       | 类型    | 必填 | 描述                     |

|--------------|---------|------|--------------------------|

|`id`| string  | 是   | 唯一标识符 (UUIDv4)      |

|`title`| string  | 是   | 任务标题 (1-100字符)     |

|`description`| string  | 否   | 任务描述 (可选)          |

|`status`| enum    | 是   |`pending`/`completed`|

|`dueDate`| string  | 否   | 截止日期 (ISO8601格式)   |

|`createdAt`| string  | 是   | 创建时间 (ISO8601格式)   |

|`updatedAt`| string  | 是   | 最后更新时间 (ISO8601)   |

---## API 接口列表### 1. 获取Todo列表**GET**`/todos`#### 参数| 参数名     | 类型    | 默认值 | 描述                     |

|------------|---------|--------|--------------------------|

|`status`| string  | -      | 过滤状态 (`pending/completed`) |

|`page`| integer | 1      | 分页页码                 |

|`limit`| integer | 20     | 每页数量 (最大100)       |#### 响应示例```json

{

"total": 45,

"page": 1,

"limit": 20,

"items": [

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "购买食材",

"status": "pending",

"dueDate": "2025-03-30T09:00:00Z",

"createdAt": "2025-03-28T14:30:00Z"

}

]

}

` ` `

---

**POST** `/todos`

#### 请求体

```json

{

"title": "项目会议准备",

"description": "准备季度项目汇报材料",

"dueDate": "2025-04-01T14:00:00Z"

}` ``#### 响应 (201 Created)```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "项目会议准备",

"status": "pending",

"dueDate": "2025-04-01T14:00:00Z",

"createdAt": "2025-03-28T15:00:00Z"

}

` ` `

---

**GET** `/todos/{id}`

#### 响应示例

```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "项目会议准备",

"description": "准备季度项目汇报材料",

"status": "pending",

"dueDate": "2025-04-01T14:00:00Z",

"createdAt": "2025-03-28T15:00:00Z",

"updatedAt": "2025-03-28T15:00:00Z"

}` ``

---### 4. 更新Todo信息**PATCH**`/todos/{id}`#### 请求体 (部分更新)```json

{

"title": "更新后的会议准备",

"status": "completed"

}

` ` `

#### 响应

```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "更新后的会议准备",

"status": "completed",

"updatedAt": "2025-03-28T16:00:00Z"

}` ``

---### 5. 删除Todo**DELETE**`/todos/{id}`#### 响应 (204 No Content)---### 6. 批量更新状态**POST**`/todos/batch-update`#### 请求体```json

{

"ids": ["id1", "id2"],

"status": "completed"

}

` ` `

#### 响应

```json

{

"updatedCount": 2

}` ``

---## 错误处理| 状态码 | 描述                  |

|--------|-----------------------|

| 400    | 请求参数验证失败      |

| 401    | 未授权访问            |

| 404    | 资源不存在            |

| 429    | 请求频率限制          |

| 500    | 服务器内部错误        |

错误响应示例：```json

{

"error": {

"code": "INVALID_DUE_DATE",

"message": "截止日期不能早于当前时间"

}

}

` ` `标记分享51006这道实操题考察的是Prompt 工程能力和对 RESTful 规范的理解，核心思路是把 Schema 喂给 AI，再通过结构化 Prompt 引导它生成标准 CRUD 代码。整个操作流程分 3 步：1）先把 API 文档里的 Schema 提取出来，比如一个用户表有 id、name、email、created_at 这些字段2）构造一个精准的 Prompt，明确告诉 AI 要用什么框架、遵循什么规范、返回什么格式3）拿到生成的代码后快速 review，重点看路由设计、参数校验、异常处理这几块假设 Schema 是这样的：▼json复制代码{"User":{"id":"long, 主键","name":"string, 必填, 最大50字符","email":"string, 必填, 邮箱格式","created_at":"datetime, 自动生成"}}给 AI 的 Prompt 可以这样写：▼text复制代码基于以下 Schema 生成 Spring Boot 的 RESTful CRUD 接口：-框架：Spring Boot 3.x + Spring Data JPA-规范：严格遵循 RESTful，GET 用于查询，POST 用于创建，PUT 用于全量更新，DELETE 用于删除-响应格式：统一包装成 {code, message, data} 结构-要求：包含参数校验注解、异常处理Schema:

{粘贴上面的 JSON}AI 生成的 Controller 核心代码大概长这样：▼java复制代码@RestController@RequestMapping("/api/users")publicclassUserController{@AutowiredprivateUserService userService;@GetMapping("/{id}")publicResult<User>getById(@PathVariableLong id){returnResult.success(userService.findById(id));

}@PostMappingpublicResult<User>create(@Valid@RequestBodyUserCreateDTO dto){returnResult.success(userService.create(dto));

}@PutMapping("/{id}")publicResult<User>update(@PathVariableLong id,@Valid@RequestBodyUserUpdateDTO dto){returnResult.success(userService.update(id, dto));

}@DeleteMapping("/{id}")publicResult<Void>delete(@PathVariableLong id){

userService.delete(id);returnResult.success(null);

}

}拿到代码后重点检查这几个地方：路由是不是用了复数名词、HTTP 方法用得对不对、有没有加@Valid做参数校验。

Prompt 优化技巧很多人用 AI 生成代码效果不好，问题往往出在 Prompt 太模糊。AI 不是人，它猜不到你想要 Spring Boot 还是 Express，猜不到你们公司用的是驼峰还是下划线命名。一个高质量的 Prompt 要包含 4 个要素：1）技术栈版本，比如 Spring Boot 3.2、JDK 17、MyBatis Plus 3.52）编码规范，比如 RESTful 风格、统一响应体结构、驼峰命名3）完整上下文，Schema 要全贴上去，字段类型、约束条件一个都不能少4）反例约束，告诉 AI 不要干什么，比如"不要用 Lombok"、"不要用 XML 配置"生成代码的 Review 重点AI 生成的代码不能直接用，至少要检查这几个地方：1）安全性漏洞，有没有 SQL 注入风险、有没有做权限校验2）异常处理是不是完善，空指针、资源不存在这些边界情况覆盖了没有3）事务边界对不对，涉及多表操作的有没有加@Transactional4）日志是不是规范，关键操作有没有打日志，日志级别用得对不对不同 AI 工具的差异现在市面上 AI 编程工具很多，Cursor、GitHub Copilot、通义灵码、CodeGeeX 各有特点：工具强项弱项Cursor上下文理解强，能读懂整个项目收费，国内网络不稳定Copilot补全速度快，和 IDE 集成好对中文注释理解一般通义灵码中文支持好，免费额度多复杂逻辑生成质量不如前两者CodeGeeX完全免费，国产模型偶尔会生成过时 API面试现场实操建议15 分钟时间很紧，建议这样分配：1）前 3 分钟，快速阅读 Schema，理解业务含义，想清楚要生成哪些接口2）中间 8 分钟，写 Prompt、喂给 AI、拿到代码、快速调整明显问题3）最后 4 分钟，给面试官讲解代码结构和设计决策，展示你的工程思维关键是要表现出你不是在无脑用 AI，而是知道 AI 生成的东西哪里可能有坑、怎么 review、怎么改进。

- **提问**：如果 AI 生成的代码有明显的安全漏洞，你会怎么处理？回答：拿到代码第一件事就是扫一遍安全问题。如果发现有 SQL 拼接这种明显漏洞，直接手动改成参数化查询。如果是鉴权没做，补上@PreAuthorize或者自定义拦截器。改完之后会反向给 AI 一个反馈，告诉它下次要注意这个点，后续生成的代码质量会提升。- **提问**：RESTful 规范里 PUT 和 PATCH 有什么区别，生成代码时要怎么选？
- **回答**：PUT 是全量更新，客户端得把所有字段都传过来，没传的字段会被置空。PATCH 是部分更新，只更新传了的字段。实际项目里 PATCH 用得更多，因为前端很少会一次性改全部字段。生成代码时如果是编辑场景，优先用 PATCH 加一个非空校验逻辑。- **提问**：如果时间来不及，AI 生成的代码只来得及做部分修改，你会优先改哪里？
- **回答**：优先级是安全 > 正确性 > 规范性。第一改安全漏洞，比如 SQL 注入、越权访问。第二改逻辑错误，比如空指针、边界条件没处理。第三才是代码风格、命名规范这些。规范性的问题不影响功能，面试完再改也行。

Prompt 优化技巧生成代码的 Review 重点不同 AI 工具的差异面试现场实操建议

提问：如果 AI 生成的代码有明显的安全漏洞，你会怎么处理？提问：RESTful 规范里 PUT 和 PATCH 有什么区别，生成代码时要怎么选？提问：如果时间来不及，AI 生成的代码只来得及做部分修改，你会优先改哪里？热门面试题目榜更多说说 Java 中 HashMap 的原理？9130Java 中的序列化和反序列化是什么？6255MySQL 索引的最左前缀匹配原则是什么？5662Java 中 ConcurrentHashMap 1.7 和 1.8 之间有哪些区别？5067Java 中有哪些集合类？请简单介绍4854MySQL 的索引类型有哪些？4845详细描述一条 SQL 语句在 MySQL 中的执行过程。4218什么是 RAG？RAG 的主要流程是什么？4151MySQL 的存储引擎有哪些？它们之间有什么区别？4092数据库的脏读、不可重复读和幻读分别是什么？3900推荐教程更多AI 超级智能体亿级流量点赞系统教程智能协同云图库项目教程预览用户交流一起刷题学习、求职交流、反馈建议、获取更新通知面试鸭《用户协议》《隐私政策》友情链接编程导航老鱼简历代码小抄剪切助手联系我们商务合作站长：程序员鱼皮关注我们扫码关注面试鸭公众号

---

> 来源: 现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑.mhtml

## 

## 关键点

- # 现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑
现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑VIP中等大模型为方便拷贝至编辑器，以下文档以 Markdown 源码进行展示▼markdown复制代码# TodoList API 文档 (v1.0)## 基础信息-**Base URL**:`https://api.example.com/v1`-**数据格式**: JSON-认证方式: Bearer Token (需在Header中添加`Authorization: Bearer <token>`)

---## 数据结构 Schema### Todo 对象| 字段名       | 类型    | 必填 | 描述                     |

|--------------|---------|------|--------------------------|

|`id`| string  | 是   | 唯一标识符 (UUIDv4)      |

|`title`| string  | 是   | 任务标题 (1-100字符)     |

|`description`| string  | 否   | 任务描述 (可选)          |

|`status`| enum    | 是   |`pending`/`completed`|

|`dueDate`| string  | 否   | 截止日期 (ISO8601格式)   |

|`createdAt`| string  | 是   | 创建时间 (ISO8601格式)   |

|`updatedAt`| string  | 是   | 最后更新时间 (ISO8601)   |

---## API 接口列表### 1. 获取Todo列表**GET**`/todos`#### 参数| 参数名     | 类型    | 默认值 | 描述                     |

|------------|---------|--------|--------------------------|

|`status`| string  | -      | 过滤状态 (`pending/completed`) |

|`page`| integer | 1      | 分页页码                 |

|`limit`| integer | 20     | 每页数量 (最大100)       |#### 响应示例```json

{

"total": 45,

"page": 1,

"limit": 20,

"items": [

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "购买食材",

"status": "pending",

"dueDate": "2025-03-30T09:00:00Z",

"createdAt": "2025-03-28T14:30:00Z"

}

]

}

` ` `

---

**POST** `/todos`

#### 请求体

```json

{

"title": "项目会议准备",

"description": "准备季度项目汇报材料",

"dueDate": "2025-04-01T14:00:00Z"

}` ``#### 响应 (201 Created)```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "项目会议准备",

"status": "pending",

"dueDate": "2025-04-01T14:00:00Z",

"createdAt": "2025-03-28T15:00:00Z"

}

` ` `

---

**GET** `/todos/{id}`

#### 响应示例

```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "项目会议准备",

"description": "准备季度项目汇报材料",

"status": "pending",

"dueDate": "2025-04-01T14:00:00Z",

"createdAt": "2025-03-28T15:00:00Z",

"updatedAt": "2025-03-28T15:00:00Z"

}` ``

---### 4. 更新Todo信息**PATCH**`/todos/{id}`#### 请求体 (部分更新)```json

{

"title": "更新后的会议准备",

"status": "completed"

}

` ` `

#### 响应

```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "更新后的会议准备",

"status": "completed",

"updatedAt": "2025-03-28T16:00:00Z"

}` ``

---### 5. 删除Todo**DELETE**`/todos/{id}`#### 响应 (204 No Content)---### 6. 批量更新状态**POST**`/todos/batch-update`#### 请求体```json

{

"ids": ["id1", "id2"],

"status": "completed"

}

` ` `

#### 响应

```json

{

"updatedCount": 2

}` ``

---## 错误处理| 状态码 | 描述                  |

|--------|-----------------------|

| 400    | 请求参数验证失败      |

| 401    | 未授权访问            |

| 404    | 资源不存在            |

| 429    | 请求频率限制          |

| 500    | 服务器内部错误        |

错误响应示例：```json

{

"error": {

"code": "INVALID_DUE_DATE",

"message": "截止日期不能早于当前时间"

}

}

` ` `标记分享51006这道实操题考察的是Prompt 工程能力和对 RESTful 规范的理解，核心思路是把 Schema 喂给 AI，再通过结构化 Prompt 引导它生成标准 CRUD 代码。
- 整个操作流程分 3 步：1）先把 API 文档里的 Schema 提取出来，比如一个用户表有 id、name、email、created_at 这些字段2）构造一个精准的 Prompt，明确告诉 AI 要用什么框架、遵循什么规范、返回什么格式3）拿到生成的代码后快速 review，重点看路由设计、参数校验、异常处理这几块假设 Schema 是这样的：▼json复制代码{"User":{"id":"long, 主键","name":"string, 必填, 最大50字符","email":"string, 必填, 邮箱格式","created_at":"datetime, 自动生成"}}给 AI 的 Prompt 可以这样写：▼text复制代码基于以下 Schema 生成 Spring Boot 的 RESTful CRUD 接口：-框架：Spring Boot 3.x + Spring Data JPA-规范：严格遵循 RESTful，GET 用于查询，POST 用于创建，PUT 用于全量更新，DELETE 用于删除-响应格式：统一包装成 {code, message, data} 结构-要求：包含参数校验注解、异常处理Schema:

{粘贴上面的 JSON}AI 生成的 Controller 核心代码大概长这样：▼java复制代码@RestController@RequestMapping("/api/users")publicclassUserController{@AutowiredprivateUserService userService;@GetMapping("/{id}")publicResult<User>getById(@PathVariableLong id){returnResult.success(userService.findById(id));

}@PostMappingpublicResult<User>create(@Valid@RequestBodyUserCreateDTO dto){returnResult.success(userService.create(dto));

}@PutMapping("/{id}")publicResult<User>update(@PathVariableLong id,@Valid@RequestBodyUserUpdateDTO dto){returnResult.success(userService.update(id, dto));

}@DeleteMapping("/{id}")publicResult<Void>delete(@PathVariableLong id){

userService.delete(id);returnResult.success(null);

}

}拿到代码后重点检查这几个地方：路由是不是用了复数名词、HTTP 方法用得对不对、有没有加@Valid做参数校验。
- 

Prompt 优化技巧很多人用 AI 生成代码效果不好，问题往往出在 Prompt 太模糊。
- AI 不是人，它猜不到你想要 Spring Boot 还是 Express，猜不到你们公司用的是驼峰还是下划线命名。
- 一个高质量的 Prompt 要包含 4 个要素：1）技术栈版本，比如 Spring Boot 3.2、JDK 17、MyBatis Plus 3.52）编码规范，比如 RESTful 风格、统一响应体结构、驼峰命名3）完整上下文，Schema 要全贴上去，字段类型、约束条件一个都不能少4）反例约束，告诉 AI 不要干什么，比如"不要用 Lombok"、"不要用 XML 配置"生成代码的 Review 重点AI 生成的代码不能直接用，至少要检查这几个地方：1）安全性漏洞，有没有 SQL 注入风险、有没有做权限校验2）异常处理是不是完善，空指针、资源不存在这些边界情况覆盖了没有3）事务边界对不对，涉及多表操作的有没有加@Transactional4）日志是不是规范，关键操作有没有打日志，日志级别用得对不对不同 AI 工具的差异现在市面上 AI 编程工具很多，Cursor、GitHub Copilot、通义灵码、CodeGeeX 各有特点：工具强项弱项Cursor上下文理解强，能读懂整个项目收费，国内网络不稳定Copilot补全速度快，和 IDE 集成好对中文注释理解一般通义灵码中文支持好，免费额度多复杂逻辑生成质量不如前两者CodeGeeX完全免费，国产模型偶尔会生成过时 API面试现场实操建议15 分钟时间很紧，建议这样分配：1）前 3 分钟，快速阅读 Schema，理解业务含义，想清楚要生成哪些接口2）中间 8 分钟，写 Prompt、喂给 AI、拿到代码、快速调整明显问题3）最后 4 分钟，给面试官讲解代码结构和设计决策，展示你的工程思维关键是要表现出你不是在无脑用 AI，而是知道 AI 生成的东西哪里可能有坑、怎么 review、怎么改进。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑
现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑VIP中等大模型为方便拷贝至编辑器，以下文档以 Markdown 源码进行展示▼markdown复制代码# TodoList API 文档 (v1.0)## 基础信息-**Base URL**:`https://api.example.com/v1`-**数据格式**: JSON-认证方式: Bearer Token (需在Header中添加`Authorization: Bearer <token>`)

---## 数据结构 Schema### Todo 对象| 字段名       | 类型    | 必填 | 描述                     |

|--------------|---------|------|--------------------------|

|`id`| string  | 是   | 唯一标识符 (UUIDv4)      |

|`title`| string  | 是   | 任务标题 (1-100字符)     |

|`description`| string  | 否   | 任务描述 (可选)          |

|`status`| enum    | 是   |`pending`/`completed`|

|`dueDate`| string  | 否   | 截止日期 (ISO8601格式)   |

|`createdAt`| string  | 是   | 创建时间 (ISO8601格式)   |

|`updatedAt`| string  | 是   | 最后更新时间 (ISO8601)   |

---## API 接口列表### 1. 获取Todo列表**GET**`/todos`#### 参数| 参数名     | 类型    | 默认值 | 描述                     |

|------------|---------|--------|--------------------------|

|`status`| string  | -      | 过滤状态 (`pending/completed`) |

|`page`| integer | 1      | 分页页码                 |

|`limit`| integer | 20     | 每页数量 (最大100)       |#### 响应示例```json

{

"total": 45,

"page": 1,

"limit": 20,

"items": [

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "购买食材",

"status": "pending",

"dueDate": "2025-03-30T09:00:00Z",

"createdAt": "2025-03-28T14:30:00Z"

}

]

}

` ` `

---

**POST** `/todos`

#### 请求体

```json

{

"title": "项目会议准备",

"description": "准备季度项目汇报材料",

"dueDate": "2025-04-01T14:00:00Z"

}` ``#### 响应 (201 Created)```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "项目会议准备",

"status": "pending",

"dueDate": "2025-04-01T14:00:00Z",

"createdAt": "2025-03-28T15:00:00Z"

}

` ` `

---

**GET** `/todos/{id}`

#### 响应示例

```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "项目会议准备",

"description": "准备季度项目汇报材料",

"status": "pending",

"dueDate": "2025-04-01T14:00:00Z",

"createdAt": "2025-03-28T15:00:00Z",

"updatedAt": "2025-03-28T15:00:00Z"

}` ``

---### 4. 更新Todo信息**PATCH**`/todos/{id}`#### 请求体 (部分更新)```json

{

"title": "更新后的会议准备",

"status": "completed"

}

` ` `

#### 响应

```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "更新后的会议准备",

"status": "completed",

"updatedAt": "2025-03-28T16:00:00Z"

}` ``

---### 5. 删除Todo**DELETE**`/todos/{id}`#### 响应 (204 No Content)---### 6. 批量更新状态**POST**`/todos/batch-update`#### 请求体```json

{

"ids": ["id1", "id2"],

"status": "completed"

}

` ` `

#### 响应

```json

{

"updatedCount": 2

}` ``

---## 错误处理| 状态码 | 描述                  |

|--------|-----------------------|

| 400    | 请求参数验证失败      |

| 401    | 未授权访问            |

| 404    | 资源不存在            |

| 429    | 请求频率限制          |

| 500    | 服务器内部错误        |

错误响应示例：```json

{

"error": {

"code": "INVALID_DUE_DATE",

"message": "截止日期不能早于当前时间"

}

}

` ` `标记分享51006这道实操题考察的是Prompt 工程能力和对 RESTful 规范的理解，核心思路是把 Schema 喂给 AI，再通过结构化 Prompt 引导它生成标准 CRUD 代码。整个操作流程分 3 步：1）先把 API 文档里的 Schema 提取出来，比如一个用户表有 id、name、email、created_at 这些字段2）构造一个精准的 Prompt，明确告诉 AI 要用什么框架、遵循什么规范、返回什么格式3）拿到生成的代码后快速 review，重点看路由设计、参数校验、异常处理这几块假设 Schema 是这样的：▼json复制代码{"User":{"id":"long, 主键","name":"string, 必填, 最大50字符","email":"string, 必填, 邮箱格式","created_at":"datetime, 自动生成"}}给 AI 的 Prompt 可以这样写：▼text复制代码基于以下 Schema 生成 Spring Boot 的 RESTful CRUD 接口：-框架：Spring Boot 3.x + Spring Data JPA-规范：严格遵循 RESTful，GET 用于查询，POST 用于创建，PUT 用于全量更新，DELETE 用于删除-响应格式：统一包装成 {code, message, data} 结构-要求：包含参数校验注解、异常处理Schema:

{粘贴上面的 JSON}AI 生成的 Controller 核心代码大概长这样：▼java复制代码@RestController@RequestMapping("/api/users")publicclassUserController{@AutowiredprivateUserService userService;@GetMapping("/{id}")publicResult<User>getById(@PathVariableLong id){returnResult.success(userService.findById(id));

}@PostMappingpublicResult<User>create(@Valid@RequestBodyUserCreateDTO dto){returnResult.success(userService.create(dto));

}@PutMapping("/{id}")publicResult<User>update(@PathVariableLong id,@Valid@RequestBodyUserUpdateDTO dto){returnResult.success(userService.update(id, dto));

}@DeleteMapping("/{id}")publicResult<Void>delete(@PathVariableLong id){

userService.delete(id);returnResult.success(null);

}

}拿到代码后重点检查这几个地方：路由是不是用了复数名词、HTTP 方法用得对不对、有没有加@Valid做参数校验。

Prompt 优化技巧很多人用 AI 生成代码效果不好，问题往往出在 Prompt 太模糊。AI 不是人，它猜不到你想要 Spring Boot 还是 Express，猜不到你们公司用的是驼峰还是下划线命名。一个高质量的 Prompt 要包含 4 个要素：1）技术栈版本，比如 Spring Boot 3.2、JDK 17、MyBatis Plus 3.52）编码规范，比如 RESTful 风格、统一响应体结构、驼峰命名3）完整上下文，Schema 要全贴上去，字段类型、约束条件一个都不能少4）反例约束，告诉 AI 不要干什么，比如"不要用 Lombok"、"不要用 XML 配置"生成代码的 Review 重点AI 生成的代码不能直接用，至少要检查这几个地方：1）安全性漏洞，有没有 SQL 注入风险、有没有做权限校验2）异常处理是不是完善，空指针、资源不存在这些边界情况覆盖了没有3）事务边界对不对，涉及多表操作的有没有加@Transactional4）日志是不是规范，关键操作有没有打日志，日志级别用得对不对不同 AI 工具的差异现在市面上 AI 编程工具很多，Cursor、GitHub Copilot、通义灵码、CodeGeeX 各有特点：工具强项弱项Cursor上下文理解强，能读懂整个项目收费，国内网络不稳定Copilot补全速度快，和 IDE 集成好对中文注释理解一般通义灵码中文支持好，免费额度多复杂逻辑生成质量不如前两者CodeGeeX完全免费，国产模型偶尔会生成过时 API面试现场实操建议15 分钟时间很紧，建议这样分配：1）前 3 分钟，快速阅读 Schema，理解业务含义，想清楚要生成哪些接口2）中间 8 分钟，写 Prompt、喂给 AI、拿到代码、快速调整明显问题3）最后 4 分钟，给面试官讲解代码结构和设计决策，展示你的工程思维关键是要表现出你不是在无脑用 AI，而是知道 AI 生成的东西哪里可能有坑、怎么 review、怎么改进。

- **提问**：如果 AI 生成的代码有明显的安全漏洞，你会怎么处理？回答：拿到代码第一件事就是扫一遍安全问题。如果发现有 SQL 拼接这种明显漏洞，直接手动改成参数化查询。如果是鉴权没做，补上@PreAuthorize或者自定义拦截器。改完之后会反向给 AI 一个反馈，告诉它下次要注意这个点，后续生成的代码质量会提升。- **提问**：RESTful 规范里 PUT 和 PATCH 有什么区别，生成代码时要怎么选？
- **回答**：PUT 是全量更新，客户端得把所有字段都传过来，没传的字段会被置空。PATCH 是部分更新，只更新传了的字段。实际项目里 PATCH 用得更多，因为前端很少会一次性改全部字段。生成代码时如果是编辑场景，优先用 PATCH 加一个非空校验逻辑。- **提问**：如果时间来不及，AI 生成的代码只来得及做部分修改，你会优先改哪里？
- **回答**：优先级是安全 > 正确性 > 规范性。第一改安全漏洞，比如 SQL 注入、越权访问。第二改逻辑错误，比如空指针、边界条件没处理。第三才是代码风格、命名规范这些。规范性的问题不影响功能，面试完再改也行。

Prompt 优化技巧生成代码的 Review 重点不同 AI 工具的差异面试现场实操建议

提问：如果 AI 生成的代码有明显的安全漏洞，你会怎么处理？提问：RESTful 规范里 PUT 和 PATCH 有什么区别，生成代码时要怎么选？提问：如果时间来不及，AI 生成的代码只来得及做部分修改，你会优先改哪里？热门面试题目榜更多说说 Java 中 HashMap 的原理？9130Java 中的序列化和反序列化是什么？6255MySQL 索引的最左前缀匹配原则是什么？5662Java 中 ConcurrentHashMap 1.7 和 1.8 之间有哪些区别？5067Java 中有哪些集合类？请简单介绍4854MySQL 的索引类型有哪些？4845详细描述一条 SQL 语句在 MySQL 中的执行过程。4218什么是 RAG？RAG 的主要流程是什么？4151MySQL 的存储引擎有哪些？它们之间有什么区别？4092数据库的脏读、不可重复读和幻读分别是什么？3900推荐教程更多AI 超级智能体亿级流量点赞系统教程智能协同云图库项目教程预览用户交流一起刷题学习、求职交流、反馈建议、获取更新通知面试鸭《用户协议》《隐私政策》友情链接编程导航老鱼简历代码小抄剪切助手联系我们商务合作站长：程序员鱼皮关注我们扫码关注面试鸭公众号

设计智能客服系统时，如何通过知识库构建解决长尾问题？请描述具体实现步骤当大模型API响应延迟超过1秒时，前端可以采取哪些优化策略保证用户体验？上次浏览：2026-03-16 15:08:14使用LangChain时，如何实现多路召回结果的动态权重分配？上次浏览：2026-03-16 15:09:02当大模型上下文窗口扩展到100万token时，哪些现有业务场景可能发生质变？当发现RAG系统召回结果与用户query意图不匹配时，有哪些可能的改进方向？使用LangChain实现RAG系统时，如何处理PDF文档中的表格数据召回问题？现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑参数高效微调（PEFT）如何减少计算成本？冻结层在微调中的作用是什么？为什么需要混合精度训练？上次浏览：2026-03-16 15:09:27模型输出重复和幻觉如何微调解决？上次浏览：2026-03-16 15:10:0511345. 现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑VIP中等大模型为方便拷贝至编辑器，以下文档以 Markdown 源码进行展示▼markdown复制代码# TodoList API 文档 (v1.0)## 基础信息-**Base URL**:`https://api.example.com/v1`-**数据格式**: JSON-认证方式: Bearer Token (需在Header中添加`Authorization: Bearer <token>`)

---## 数据结构 Schema### Todo 对象| 字段名       | 类型    | 必填 | 描述                     |

|--------------|---------|------|--------------------------|

|`id`| string  | 是   | 唯一标识符 (UUIDv4)      |

|`title`| string  | 是   | 任务标题 (1-100字符)     |

|`description`| string  | 否   | 任务描述 (可选)          |

|`status`| enum    | 是   |`pending`/`completed`|

|`dueDate`| string  | 否   | 截止日期 (ISO8601格式)   |

|`createdAt`| string  | 是   | 创建时间 (ISO8601格式)   |

|`updatedAt`| string  | 是   | 最后更新时间 (ISO8601)   |

---## API 接口列表### 1. 获取Todo列表**GET**`/todos`#### 参数| 参数名     | 类型    | 默认值 | 描述                     |

|------------|---------|--------|--------------------------|

|`status`| string  | -      | 过滤状态 (`pending/completed`) |

|`page`| integer | 1      | 分页页码                 |

|`limit`| integer | 20     | 每页数量 (最大100)       |#### 响应示例```json

{

"total": 45,

"page": 1,

"limit": 20,

"items": [

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "购买食材",

"status": "pending",

"dueDate": "2025-03-30T09:00:00Z",

"createdAt": "2025-03-28T14:30:00Z"

}

]

}

` ` `

---

**POST** `/todos`

#### 请求体

```json

{

"title": "项目会议准备",

"description": "准备季度项目汇报材料",

"dueDate": "2025-04-01T14:00:00Z"

}` ``#### 响应 (201 Created)```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "项目会议准备",

"status": "pending",

"dueDate": "2025-04-01T14:00:00Z",

"createdAt": "2025-03-28T15:00:00Z"

}

` ` `

---

**GET** `/todos/{id}`

#### 响应示例

```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "项目会议准备",

"description": "准备季度项目汇报材料",

"status": "pending",

"dueDate": "2025-04-01T14:00:00Z",

"createdAt": "2025-03-28T15:00:00Z",

"updatedAt": "2025-03-28T15:00:00Z"

}` ``

---### 4. 更新Todo信息**PATCH**`/todos/{id}`#### 请求体 (部分更新)```json

{

"title": "更新后的会议准备",

"status": "completed"

}

` ` `

#### 响应

```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "更新后的会议准备",

"status": "completed",

"updatedAt": "2025-03-28T16:00:00Z"

}` ``

---### 5. 删除Todo**DELETE**`/todos/{id}`#### 响应 (204 No Content)---### 6. 批量更新状态**POST**`/todos/batch-update`#### 请求体```json

{

"ids": ["id1", "id2"],

"status": "completed"

}

` ` `

#### 响应

```json

{

"updatedCount": 2

}` ``

---## 错误处理| 状态码 | 描述                  |

|--------|-----------------------|

| 400    | 请求参数验证失败      |

| 401    | 未授权访问            |

| 404    | 资源不存在            |

| 429    | 请求频率限制          |

| 500    | 服务器内部错误        |

错误响应示例：```json

{

"error": {

"code": "INVALID_DUE_DATE",

"message": "截止日期不能早于当前时间"

}

}

` ` `标记分享51006这道实操题考察的是Prompt 工程能力和对 RESTful 规范的理解，核心思路是把 Schema 喂给 AI，再通过结构化 Prompt 引导它生成标准 CRUD 代码。整个操作流程分 3 步：1）先把 API 文档里的 Schema 提取出来，比如一个用户表有 id、name、email、created_at 这些字段2）构造一个精准的 Prompt，明确告诉 AI 要用什么框架、遵循什么规范、返回什么格式3）拿到生成的代码后快速 review，重点看路由设计、参数校验、异常处理这几块假设 Schema 是这样的：▼json复制代码{"User":{"id":"long, 主键","name":"string, 必填, 最大50字符","email":"string, 必填, 邮箱格式","created_at":"datetime, 自动生成"}}给 AI 的 Prompt 可以这样写：▼text复制代码基于以下 Schema 生成 Spring Boot 的 RESTful CRUD 接口：-框架：Spring Boot 3.x + Spring Data JPA-规范：严格遵循 RESTful，GET 用于查询，POST 用于创建，PUT 用于全量更新，DELETE 用于删除-响应格式：统一包装成 {code, message, data} 结构-要求：包含参数校验注解、异常处理Schema:

{粘贴上面的 JSON}AI 生成的 Controller 核心代码大概长这样：▼java复制代码@RestController@RequestMapping("/api/users")publicclassUserController{@AutowiredprivateUserService userService;@GetMapping("/{id}")publicResult<User>getById(@PathVariableLong id){returnResult.success(userService.findById(id));

}@PostMappingpublicResult<User>create(@Valid@RequestBodyUserCreateDTO dto){returnResult.success(userService.create(dto));

}@PutMapping("/{id}")publicResult<User>update(@PathVariableLong id,@Valid@RequestBodyUserUpdateDTO dto){returnResult.success(userService.update(id, dto));

}@DeleteMapping("/{id}")publicResult<Void>delete(@PathVariableLong id){

userService.delete(id);returnResult.success(null);

}

}拿到代码后重点检查这几个地方：路由是不是用了复数名词、HTTP 方法用得对不对、有没有加@Valid做参数校验。

Prompt 优化技巧很多人用 AI 生成代码效果不好，问题往往出在 Prompt 太模糊。AI 不是人，它猜不到你想要 Spring Boot 还是 Express，猜不到你们公司用的是驼峰还是下划线命名。一个高质量的 Prompt 要包含 4 个要素：1）技术栈版本，比如 Spring Boot 3.2、JDK 17、MyBatis Plus 3.52）编码规范，比如 RESTful 风格、统一响应体结构、驼峰命名3）完整上下文，Schema 要全贴上去，字段类型、约束条件一个都不能少4）反例约束，告诉 AI 不要干什么，比如"不要用 Lombok"、"不要用 XML 配置"生成代码的 Review 重点AI 生成的代码不能直接用，至少要检查这几个地方：1）安全性漏洞，有没有 SQL 注入风险、有没有做权限校验2）异常处理是不是完善，空指针、资源不存在这些边界情况覆盖了没有3）事务边界对不对，涉及多表操作的有没有加@Transactional4）日志是不是规范，关键操作有没有打日志，日志级别用得对不对不同 AI 工具的差异现在市面上 AI 编程工具很多，Cursor、GitHub Copilot、通义灵码、CodeGeeX 各有特点：工具强项弱项Cursor上下文理解强，能读懂整个项目收费，国内网络不稳定Copilot补全速度快，和 IDE 集成好对中文注释理解一般通义灵码中文支持好，免费额度多复杂逻辑生成质量不如前两者CodeGeeX完全免费，国产模型偶尔会生成过时 API面试现场实操建议15 分钟时间很紧，建议这样分配：1）前 3 分钟，快速阅读 Schema，理解业务含义，想清楚要生成哪些接口2）中间 8 分钟，写 Prompt、喂给 AI、拿到代码、快速调整明显问题3）最后 4 分钟，给面试官讲解代码结构和设计决策，展示你的工程思维关键是要表现出你不是在无脑用 AI，而是知道 AI 生成的东西哪里可能有坑、怎么 review、怎么改进。

- **提问**：如果 AI 生成的代码有明显的安全漏洞，你会怎么处理？回答：拿到代码第一件事就是扫一遍安全问题。如果发现有 SQL 拼接这种明显漏洞，直接手动改成参数化查询。如果是鉴权没做，补上@PreAuthorize或者自定义拦截器。改完之后会反向给 AI 一个反馈，告诉它下次要注意这个点，后续生成的代码质量会提升。- **提问**：RESTful 规范里 PUT 和 PATCH 有什么区别，生成代码时要怎么选？
- **回答**：PUT 是全量更新，客户端得把所有字段都传过来，没传的字段会被置空。PATCH 是部分更新，只更新传了的字段。实际项目里 PATCH 用得更多，因为前端很少会一次性改全部字段。生成代码时如果是编辑场景，优先用 PATCH 加一个非空校验逻辑。- **提问**：如果时间来不及，AI 生成的代码只来得及做部分修改，你会优先改哪里？
- **回答**：优先级是安全 > 正确性 > 规范性。第一改安全漏洞，比如 SQL 注入、越权访问。第二改逻辑错误，比如空指针、边界条件没处理。第三才是代码风格、命名规范这些。规范性的问题不影响功能，面试完再改也行。

Prompt 优化技巧生成代码的 Review 重点不同 AI 工具的差异面试现场实操建议

提问：如果 AI 生成的代码有明显的安全漏洞，你会怎么处理？提问：RESTful 规范里 PUT 和 PATCH 有什么区别，生成代码时要怎么选？提问：如果时间来不及，AI 生成的代码只来得及做部分修改，你会优先改哪里？热门面试题目榜更多说说 Java 中 HashMap 的原理？9130Java 中的序列化和反序列化是什么？6255MySQL 索引的最左前缀匹配原则是什么？5662Java 中 ConcurrentHashMap 1.7 和 1.8 之间有哪些区别？5067Java 中有哪些集合类？请简单介绍4854MySQL 的索引类型有哪些？4845详细描述一条 SQL 语句在 MySQL 中的执行过程。4218什么是 RAG？RAG 的主要流程是什么？4151MySQL 的存储引擎有哪些？它们之间有什么区别？4092数据库的脏读、不可重复读和幻读分别是什么？3900推荐教程更多AI 超级智能体亿级流量点赞系统教程智能协同云图库项目教程预览用户交流一起刷题学习、求职交流、反馈建议、获取更新通知面试鸭《用户协议》《隐私政策》友情链接编程导航老鱼简历代码小抄剪切助手联系我们商务合作站长：程序员鱼皮关注我们扫码关注面试鸭公众号

---

> 来源: 现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑.mhtml

- # 现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑
现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑VIP中等大模型为方便拷贝至编辑器，以下文档以 Markdown 源码进行展示▼markdown复制代码# TodoList API 文档 (v1.0)## 基础信息-**Base URL**:`https://api.example.com/v1`-**数据格式**: JSON-认证方式: Bearer Token (需在Header中添加`Authorization: Bearer <token>`)

---## 数据结构 Schema### Todo 对象| 字段名       | 类型    | 必填 | 描述                     |

|--------------|---------|------|--------------------------|

|`id`| string  | 是   | 唯一标识符 (UUIDv4)      |

|`title`| string  | 是   | 任务标题 (1-100字符)     |

|`description`| string  | 否   | 任务描述 (可选)          |

|`status`| enum    | 是   |`pending`/`completed`|

|`dueDate`| string  | 否   | 截止日期 (ISO8601格式)   |

|`createdAt`| string  | 是   | 创建时间 (ISO8601格式)   |

|`updatedAt`| string  | 是   | 最后更新时间 (ISO8601)   |

---## API 接口列表### 1. 获取Todo列表**GET**`/todos`#### 参数| 参数名     | 类型    | 默认值 | 描述                     |

|------------|---------|--------|--------------------------|

|`status`| string  | -      | 过滤状态 (`pending/completed`) |

|`page`| integer | 1      | 分页页码                 |

|`limit`| integer | 20     | 每页数量 (最大100)       |#### 响应示例```json

{

"total": 45,

"page": 1,

"limit": 20,

"items": [

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "购买食材",

"status": "pending",

"dueDate": "2025-03-30T09:00:00Z",

"createdAt": "2025-03-28T14:30:00Z"

}

]

}

` ` `

---

**POST** `/todos`

#### 请求体

```json

{

"title": "项目会议准备",

"description": "准备季度项目汇报材料",

"dueDate": "2025-04-01T14:00:00Z"

}` ``#### 响应 (201 Created)```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "项目会议准备",

"status": "pending",

"dueDate": "2025-04-01T14:00:00Z",

"createdAt": "2025-03-28T15:00:00Z"

}

` ` `

---

**GET** `/todos/{id}`

#### 响应示例

```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "项目会议准备",

"description": "准备季度项目汇报材料",

"status": "pending",

"dueDate": "2025-04-01T14:00:00Z",

"createdAt": "2025-03-28T15:00:00Z",

"updatedAt": "2025-03-28T15:00:00Z"

}` ``

---### 4. 更新Todo信息**PATCH**`/todos/{id}`#### 请求体 (部分更新)```json

{

"title": "更新后的会议准备",

"status": "completed"

}

` ` `

#### 响应

```json

{

"id": "550e8400-e29b-41d4-a716-446655440000",

"title": "更新后的会议准备",

"status": "completed",

"updatedAt": "2025-03-28T16:00:00Z"

}` ``

---### 5. 删除Todo**DELETE**`/todos/{id}`#### 响应 (204 No Content)---### 6. 批量更新状态**POST**`/todos/batch-update`#### 请求体```json

{

"ids": ["id1", "id2"],

"status": "completed"

}

` ` `

#### 响应

```json

{

"updatedCount": 2

}` ``

---## 错误处理| 状态码 | 描述                  |

|--------|-----------------------|

| 400    | 请求参数验证失败      |

| 401    | 未授权访问            |

| 404    | 资源不存在            |

| 429    | 请求频率限制          |

| 500    | 服务器内部错误        |

错误响应示例：```json

{

"error": {

"code": "INVALID_DUE_DATE",

"message": "截止日期不能早于当前时间"

}

}

` ` `标记分享51006这道实操题考察的是Prompt 工程能力和对 RESTful 规范的理解，核心思路是把 Schema 喂给 AI，再通过结构化 Prompt 引导它生成标准 CRUD 代码。
- - 整个操作流程分 3 步：1）先把 API 文档里的 Schema 提取出来，比如一个用户表有 id、name、email、created_at 这些字段2）构造一个精准的 Prompt，明确告诉 AI 要用什么框架、遵循什么规范、返回什么格式3）拿到生成的代码后快速 review，重点看路由设计、参数校验、异常处理这几块假设 Schema 是这样的：▼json复制代码{"User":{"id":"long, 主键","name":"string, 必填, 最大50字符","email":"string, 必填, 邮箱格式","created_at":"datetime, 自动生成"}}给 AI 的 Prompt 可以这样写：▼text复制代码基于以下 Schema 生成 Spring Boot 的 RESTful CRUD 接口：-框架：Spring Boot 3.x + Spring Data JPA-规范：严格遵循 RESTful，GET 用于查询，POST 用于创建，PUT 用于全量更新，DELETE 用于删除-响应格式：统一包装成 {code, message, data} 结构-要求：包含参数校验注解、异常处理Schema:

{粘贴上面的 JSON}AI 生成的 Controller 核心代码大概长这样：▼java复制代码@RestController@RequestMapping("/api/users")publicclassUserController{@AutowiredprivateUserService userService;@GetMapping("/{id}")publicResult<User>getById(@PathVariableLong id){returnResult.success(userService.findById(id));

}@PostMappingpublicResult<User>create(@Valid@RequestBodyUserCreateDTO dto){returnResult.success(userService.create(dto));

}@PutMapping("/{id}")publicResult<User>update(@PathVariableLong id,@Valid@RequestBodyUserUpdateDTO dto){returnResult.success(userService.update(id, dto));

}@DeleteMapping("/{id}")publicResult<Void>delete(@PathVariableLong id){

userService.delete(id);returnResult.success(null);

}

}拿到代码后重点检查这几个地方：路由是不是用了复数名词、HTTP 方法用得对不对、有没有加@Valid做参数校验。
- - 

Prompt 优化技巧很多人用 AI 生成代码效果不好，问题往往出在 Prompt 太模糊。
- - AI 不是人，它猜不到你想要 Spring Boot 还是 Express，猜不到你们公司用的是驼峰还是下划线命名。
- - 一个高质量的 Prompt 要包含 4 个要素：1）技术栈版本，比如 Spring Boot 3.2、JDK 17、MyBatis Plus 3.52）编码规范，比如 RESTful 风格、统一响应体结构、驼峰命名3）完整上下文，Schema 要全贴上去，字段类型、约束条件一个都不能少4）反例约束，告诉 AI 不要干什么，比如"不要用 Lombok"、"不要用 XML 配置"生成代码的 Review 重点AI 生成的代码不能直接用，至少要检查这几个地方：1）安全性漏洞，有没有 SQL 注入风险、有没有做权限校验2）异常处理是不是完善，空指针、资源不存在这些边界情况覆盖了没有3）事务边界对不对，涉及多表操作的有没有加@Transactional4）日志是不是规范，关键操作有没有打日志，日志级别用得对不对不同 AI 工具的差异现在市面上 AI 编程工具很多，Cursor、GitHub Copilot、通义灵码、CodeGeeX 各有特点：工具强项弱项Cursor上下文理解强，能读懂整个项目收费，国内网络不稳定Copilot补全速度快，和 IDE 集成好对中文注释理解一般通义灵码中文支持好，免费额度多复杂逻辑生成质量不如前两者CodeGeeX完全免费，国产模型偶尔会生成过时 API面试现场实操建议15 分钟时间很紧，建议这样分配：1）前 3 分钟，快速阅读 Schema，理解业务含义，想清楚要生成哪些接口2）中间 8 分钟，写 Prompt、喂给 AI、拿到代码、快速调整明显问题3）最后 4 分钟，给面试官讲解代码结构和设计决策，展示你的工程思维关键是要表现出你不是在无脑用 AI，而是知道 AI 生成的东西哪里可能有坑、怎么 review、怎么改进。

- 本文已做格式统一与噪声清理，保留原始语义。
- 15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑
- # 现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑
- 11345. 现场实操：给定一个包含数据Schema的API文档，请使用AI工具在15分钟内生成符合RESTful规范的CRUD接口代码，并解释关键实现逻辑VIP中等大模型为方便拷贝至编辑器，以下文档以 Markdown 源码进行展示▼markdown复制代码# TodoList API 文档 (v1.0)## 基础信息-**Base URL**:`https://api.example.com/v1`-**数据格式**: JSON-认证方式: Bearer Token (需在Header中添加`Authorization: Bearer <token>`)
- ---## 数据结构 Schema### Todo 对象| 字段名       | 类型    | 必填 | 描述                     |
- |--------------|---------|------|--------------------------|

- 本文已做格式统一与噪声清理，保留原始语义。
