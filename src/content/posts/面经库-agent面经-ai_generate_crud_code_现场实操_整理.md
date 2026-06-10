---
title: "面经库｜AI Generate CRUD Code 现场实操 整理"
published: 2026-06-10
description: "# AI_Generate_CRUD_Code_现场实操 ## 问题 AI_Generate_CRUD_Code_现场实操 ## 标准回答 # 现场实操：给定数据Schema生成符合RESTful规范的CRUD接口代码 这是一道典型的现场实"
tags: ["面经", "面经库", "agent面经"]
category: "面经整理"
draft: false
lang: zh-CN
pinned: false
comment: true
---

# AI_Generate_CRUD_Code_现场实操
## 问题
AI_Generate_CRUD_Code_现场实操

## 标准回答

# 现场实操：给定数据Schema生成符合RESTful规范的CRUD接口代码

这是一道典型的现场实操题，考察候选人利用AI工具快速生成后端代码的能力？
在15分钟内完成，需要遵循以下步骤：

**操作流程**：
**理解Schema**：提取数据模型定义（字段、类型、约束、关系）
**设计RESTful端点**：
- `GET /resources` - 列表查询（支持分页、过滤、排序）
- `POST /resources` - 创建资源
- `GET /resources/{id}` - 获取单个资源
- `PUT /resources/{id}` - 全量更新
- `PATCH /resources/{id}` - 部分更新
- `DELETE /resources/{id}` - 删除资源
**生成代码**：使用AI工具（如Copilot、ChatGPT）输出控制器、服务层、数据访问层代码
**解释关键逻辑**：验证、错误处理、状态码选择、数据一致性

**关键实现逻辑要点**：
- **数据验证**：使用DTO + 校验注解（如`@Valid`、`@NotNull`、`@Size`）
- **错误处理**：全局异常处理器返回标准错误格式（如`{“code”: 400, “message”: “...”}`）
- **RESTful状态码**：
- 201 Created（POST成功）
- 200 OK（GET/PUT/PATCH成功）
- 204 No Content（DELETE成功）
- 404 Not Found（资源不存在）
- **分页规范**：使用`page`、`size`参数，返回`{“data”: [], “total”: 100, “page”: 1, “size”: 20}`

---

## 扩展知识

### 1. 常用框架示例（Spring Boot）
```java
// Controller示例
@RestController
@RequestMapping("/api/users")
public class UserController {
@GetMapping
public Page<UserDTO> list(@PageableDefault Pageable pageable) { ... }

@PostMapping
@ResponseStatus(HttpStatus.CREATED)
public UserDTO create(@Valid @RequestBody UserCreateDTO dto) { ... }

@GetMapping("/{id}")
public UserDTO get(@PathVariable Long id) { ... }

@PutMapping("/{id}")
public UserDTO update(@PathVariable Long id, @Valid @RequestBody UserUpdateDTO dto) { ... }

@DeleteMapping("/{id}")
@ResponseStatus(HttpStatus.NO_CONTENT)
public void delete(@PathVariable Long id) { ... }
}
```

### 2. 数据验证的错误响应
- 使用`@Valid`触发校验，`MethodArgumentNotValidException`处理
- 返回格式：`{“field”: “email”, “message”: “邮箱格式不正确”}`

### 3. AI生成代码的技巧
- **明确约束**：在prompt中包含Schema定义、技术栈（如Spring Boot 3 + JPA）、代码风格要求
- **分步生成**：先生成实体类，再生成Repository、Service、Controller
- **人工修正**：检查生成的业务逻辑是否正确，补充遗漏的验证规则

---

## 面试官追问

### Q1：如果Schema包含嵌套对象或数组，RESTful API怎么设计？
**A**：使用子资源端点，如`POST /users/{userId}/orders`。或者将嵌套对象序列化为JSON字段，在单个请求中包含完整结构。通常推荐前者保持语义清晰。

### Q2：如何处理并发更新冲突？
**A**：乐观锁方案：在表中增加`version`字段，更新时检查版本号。若版本不匹配返回409 Conflict。AI生成代码时可要求添加`@Version`注解（JPA）。

### Q3：AI生成的代码可能存在SQL注入风险，怎么防范？
**A**：强制要求使用参数化查询（如JPA、MyBatis的`#{}`），禁止字符串拼接SQL。可在prompt中明确“使用防SQL注入写法”，并在代码审查时重点检查。

### Q4：15分钟内如果AI生成代码有bug，面试官会如何评判？
**A**：更看重思路和解决问题的过程。你能识别出bug的位置、解释原因并提出修正方案，比完美无bug的代码更重要。建议先输出核心结构，再逐步完善验证逻辑。

---

## 总结

本题考察AI辅助编程能力与RESTful规范掌握程度。关键在于：快速理解Schema、设计规范接口、生成可运行的代码骨架，并能解释验证、错误处理、并发控制等

## 关键点

。AI工具是辅助，候选人的设计思路和问题排查能力才是评分核心。

## 

- # 现场实操：给定数据Schema生成符合RESTful规范的CRUD接口代码

这是一道典型的现场实操题，考察候选人利用AI工具快速生成后端代码的能力。
- 在15分钟内完成，需要遵循以下步骤：

**操作流程**：
**理解Schema**：提取数据模型定义（字段、类型、约束、关系）
**设计RESTful端点**：
- `GET /resources` - 列表查询（支持分页、过滤、排序）
- `POST /resources` - 创建资源
- `GET /resources/{id}` - 获取单个资源
- `PUT /resources/{id}` - 全量更新
- `PATCH /resources/{id}` - 部分更新
- `DELETE /resources/{id}` - 删除资源
**生成代码**：使用AI工具（如Copilot、ChatGPT）输出控制器、服务层、数据访问层代码
**解释关键逻辑**：验证、错误处理、状态码选择、数据一致性

**关键实现逻辑要点**：
- **数据验证**：使用DTO + 校验注解（如`@Valid`、`@NotNull`、`@Size`）
- **错误处理**：全局异常处理器返回标准错误格式（如`{“code”: 400, “message”: “...”}`）
- **RESTful状态码**：
- 201 Created（POST成功）
- 200 OK（GET/PUT/PATCH成功）
- 204 No Content（DELETE成功）
- 404 Not Found（资源不存在）
- **分页规范**：使用`page`、`size`参数，返回`{“data”: [], “total”: 100, “page”: 1, “size”: 20}`

---

```java
// Controller示例
@RestController
@RequestMapping("/api/users")
public class UserController {
@GetMapping
public Page<UserDTO> list(@PageableDefault Pageable pageable) { ... }

@PostMapping
@ResponseStatus(HttpStatus.CREATED)
public UserDTO create(@Valid @RequestBody UserCreateDTO dto) { ... }

@GetMapping("/{id}")
public UserDTO get(@PathVariable Long id) { ... }

@PutMapping("/{id}")
public UserDTO update(@PathVariable Long id, @Valid @RequestBody UserUpdateDTO dto) { ... }

@DeleteMapping("/{id}")
@ResponseStatus(HttpStatus.NO_CONTENT)
public void delete(@PathVariable Long id) { ... }
}
```

- 使用`@Valid`触发校验，`MethodArgumentNotValidException`处理
- 返回格式：`{“field”: “email”, “message”: “邮箱格式不正确”}`

- **明确约束**：在prompt中包含Schema定义、技术栈（如Spring Boot 3 + JPA）、代码风格要求
- **分步生成**：先生成实体类，再生成Repository、Service、Controller
- **人工修正**：检查生成的业务逻辑是否正确，补充遗漏的验证规则

---

- **A**：使用子资源端点，如`POST /users/{userId}/orders`。
- 或者将嵌套对象序列化为JSON字段，在单个请求中包含完整结构。
- 通常推荐前者保持语义清晰。

## 备注

- 本文已做格式统一与噪声清理，保留原始语义。
- ## 问题

AI_Generate_CRUD_Code_现场实操

这是一道典型的现场实操题，考察候选人利用AI工具快速生成后端代码的能力。在15分钟内完成，需要遵循以下步骤：

**操作流程**：
**理解Schema**：提取数据模型定义（字段、类型、约束、关系）
**设计RESTful端点**：
- `GET /resources` - 列表查询（支持分页、过滤、排序）
- `POST /resources` - 创建资源
- `GET /resources/{id}` - 获取单个资源
- `PUT /resources/{id}` - 全量更新
- `PATCH /resources/{id}` - 部分更新
- `DELETE /resources/{id}` - 删除资源
**生成代码**：使用AI工具（如Copilot、ChatGPT）输出控制器、服务层、数据访问层代码
**解释关键逻辑**：验证、错误处理、状态码选择、数据一致性

**关键实现逻辑要点**：
- **数据验证**：使用DTO + 校验注解（如`@Valid`、`@NotNull`、`@Size`）
- **错误处理**：全局异常处理器返回标准错误格式（如`{“code”: 400, “message”: “...”}`）
- **RESTful状态码**：
- 201 Created（POST成功）
- 200 OK（GET/PUT/PATCH成功）
- 204 No Content（DELETE成功）
- 404 Not Found（资源不存在）
- **分页规范**：使用`page`、`size`参数，返回`{“data”: [], “total”: 100, “page”: 1, “size”: 20}`

---

```java
// Controller示例
@RestController
@RequestMapping("/api/users")
public class UserController {
@GetMapping
public Page<UserDTO> list(@PageableDefault Pageable pageable) { ... }

@PostMapping
@ResponseStatus(HttpStatus.CREATED)
public UserDTO create(@Valid @RequestBody UserCreateDTO dto) { ... }

@GetMapping("/{id}")
public UserDTO get(@PathVariable Long id) { ... }

@PutMapping("/{id}")
public UserDTO update(@PathVariable Long id, @Valid @RequestBody UserUpdateDTO dto) { ... }

@DeleteMapping("/{id}")
@ResponseStatus(HttpStatus.NO_CONTENT)
public void delete(@PathVariable Long id) { ... }
}
```

- 使用`@Valid`触发校验，`MethodArgumentNotValidException`处理
- 返回格式：`{“field”: “email”, “message”: “邮箱格式不正确”}`

- **明确约束**：在prompt中包含Schema定义、技术栈（如Spring Boot 3 + JPA）、代码风格要求
- **分步生成**：先生成实体类，再生成Repository、Service、Controller
- **人工修正**：检查生成的业务逻辑是否正确，补充遗漏的验证规则

---

- **A**：使用子资源端点，如`POST /users/{userId}/orders`。或者将嵌套对象序列化为JSON字段，在单个请求中包含完整结构。通常推荐前者保持语义清晰。
- ### Q2：如何处理并发更新冲突？
- **A**：乐观锁方案：在表中增加`version`字段，更新时检查版本号。若版本不匹配返回409 Conflict。AI生成代码时可要求添加`@Version`注解（JPA）。
- ### Q3：AI生成的代码可能存在SQL注入风险，怎么防范？

- 本文已做格式统一与噪声清理，保留原始语义。
- 在15分钟内完成，需要遵循以下步骤：
- 1. **理解Schema**：提取数据模型定义（字段、类型、约束、关系）
- 2. **设计RESTful端点**：
- - `GET /resources` - 列表查询（支持分页、过滤、排序）
- - `POST /resources` - 创建资源

- 本文已做格式统一与噪声清理，保留原始语义。
