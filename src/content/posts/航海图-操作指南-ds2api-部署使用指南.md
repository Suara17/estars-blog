---
title: "DS2API 部署使用指南"
published: 2026-06-10
description: "# ds2api 部署使用指南 > 将 DeepSeek Web 对话能力转换为 OpenAI、Claude、Gemini 兼容 API 的中间件。 > 项目地址：https://github.com/CJackHwang/ds2api （"
tags: ["航海图", "操作指南"]
category: "航海图"
draft: false
lang: zh-CN
pinned: false
comment: true
---

# ds2api 部署使用指南

> 将 DeepSeek Web 对话能力转换为 OpenAI、Claude、Gemini 兼容 API 的中间件。
> 项目地址：https://github.com/CJackHwang/ds2api （v4.6.1，已归档只读）

---

## 一、项目简介

ds2api 是一个用 **Go** 编写的 DeepSeek Web → OpenAI 兼容 API 代理。它通过模拟 DeepSeek 网页端的对话流程，把网页能力转为标准 API 接口，支持：

- OpenAI `/v1/chat/completions`（含流式响应）
- Claude `/v1/messages`
- Gemini `/v1beta/models/.../generateContent`
- WebUI 管理台（React 前端）

**与 qoder-cn-proxy 的区别：** qoder-cn-proxy 调用的是 Qoder CN 官方 API（需要 PAT Token）；ds2api 模拟的是 DeepSeek **网页端**对话（需要 DeepSeek 账号密码）。

---

## 二、部署环境要求

| 项目 | 要求 |
|------|------|
| 操作系统 | Alpine Linux（proot 环境） |
| Go | >= 1.26.0（Alpine 自带的 1.23 不够） |
| 架构 | ARM64（手机 CPU） |
| DeepSeek 账号 | 邮箱+密码 或 手机号+密码 |

---

## 三、部署步骤

### 1. 安装 Go 1.26.0

Alpine 自带的 Go 1.23 版本太低，需要手动安装 Go 1.26：

```bash
# 用 Python 下载并解压（比 curl 在 proot 中更稳定）
python3 -c "
import urllib.request, tarfile
url = 'https://dl.google.com/go/go1.26.0.linux-arm64.tar.gz'
out = '/tmp/go1.26.0.linux-arm64.tar.gz'
print('下载 Go 1.26.0...')
req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.0'})
data = urllib.request.urlopen(req, timeout=600)
with open(out, 'wb') as f:
    total = 0
    while True:
        chunk = data.read(1048576)
        if not chunk: break
        f.write(chunk)
        total += len(chunk)
print(f'下载完成: {total/1048576:.1f} MB')
print('解压...')
with tarfile.open(out, 'r:gz') as tar:
    tar.extractall('/usr/local')
print('完成')
"

# 验证
/usr/local/go/bin/go version
# → go version go1.26.0 linux/arm64
```

> **注意：** `dl.google.com` 在 proot 环境中 TLS 连接比 `go.dev` 更稳定。如果下载失败，多试几次或换网络。

### 2. 获取源码

```bash
cd /workspace

# 方式 A：Git 克隆（可能遇到 TLS 错误）
git clone https://github.com/CJackHwang/ds2api.git

# 方式 B：下载 Release 源码包（更可靠）
curl -L -o ds2api-v4.6.1.tar.gz "https://github.com/CJackHwang/ds2api/archive/refs/tags/v4.6.1.tar.gz"
tar xzf ds2api-v4.6.1.tar.gz
mv ds2api-4.6.1 ds2api
rm ds2api-v4.6.1.tar.gz
```

### 3. 编译

```bash
export PATH="/usr/local/go/bin:$PATH"
cd /workspace/ds2api

# 使用 goproxy.cn 国内镜像加速依赖下载
GONOSUMCHECK=* GONOSUMDB=* GOPROXY=https://goproxy.cn,direct \
  go build -o ds2api ./cmd/ds2api
```

编译成功后生成 `/workspace/ds2api/ds2api`（约 25MB，ARM64 ELF）。

### 4. 配置

复制示例配置并编辑：

```bash
cp config.example.json config.json
```

编辑 `config.json`，关键字段：

```jsonc
{
  "keys": ["你的API密钥"],           // 客户端调用时用的 API Key
  "api_keys": [
    {
      "key": "你的API密钥",
      "name": "主 API Key",
      "remark": "本地使用"
    }
  ],
  "accounts": [
    {
      "name": "主账号",
      "email": "你的DeepSeek邮箱",
      "password": "你的DeepSeek密码"
      // 或用手机号登录：
      // "phone": "你的手机号",
      // "phone_code": "国际区号如+86"
    }
  ],
  "model_aliases": {
    "gpt-4o": "deepseek-v4-flash",
    "gpt-5.5": "deepseek-v4-flash",
    "o3": "deepseek-v4-pro"
  }
  // ... 其他配置保持默认即可
}
```

### 5. 启动

```bash
cd /workspace/ds2api
./ds2api
```

启动后监听 `http://0.0.0.0:8080`（端口见启动日志）。

**首次启动注意：** 如果提示 `[webui] static files missing, running npm build`，说明 WebUI 前端静态文件未构建，会自动尝试用 npm 构建。如不需要 WebUI，可忽略此提示。

**后台运行（保活）：**

```bash
nohup ./ds2api > /workspace/ds2api/ds2api.log 2>&1 &
```

或使用 Omnibot 的终端持久会话运行。

---

## 四、API 使用

### 基本信息

| 配置项 | 值 |
|--------|-----|
| API Base URL | `http://127.0.0.1:8080`（手机 App 用 localhost） |
| API Key | config.json 中设置的 key |
| 默认模型 | `deepseek-v4-flash`（可通过 model_aliases 映射） |

### 支持的端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/chat/completions` | OpenAI 聊天补全（支持流式） |
| POST | `/v1/messages` | Claude 消息格式 |
| POST | `/v1beta/models/.../generateContent` | Gemini 格式 |
| GET | `/v1/models` | 列出可用模型 |
| GET | `/` | WebUI 管理台 |

### 请求示例

**OpenAI 格式（流式）：**

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Authorization: Bearer 你的API密钥" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4-flash",
    "messages": [{"role": "user", "content": "你好"}],
    "stream": true
  }'
```

**非流式：**

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Authorization: Bearer 你的API密钥" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4-flash",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

### 客户端配置

在 ChatGPT 兼容客户端（如 ChatBox、NextChat 等）中：

- **API 类型：** OpenAI Compatible
- **API Base URL：** `http://127.0.0.1:8080`
- **API Key：** config.json 中设置的 key
- **Model：** `deepseek-v4-flash` 或 `deepseek-v4-pro`

---

## 五、可用模型

| 模型名 | 别名 | 说明 |
|--------|------|------|
| `deepseek-v4-flash` | `gpt-4o`, `gpt-5.5` | 快速模型，适合日常对话 |
| `deepseek-v4-pro` | `o3`, `gpt-5.3-codex` | 高级模型，适合复杂推理 |

可通过 `model_aliases` 字段自定义别名映射。

---

## 六、目录结构

```
/workspace/ds2api/
├── ds2api              # 编译后的二进制
├── config.json         # 运行配置（需手动创建）
├── config.example.json # 配置示例
├── cmd/ds2api/main.go  # 入口代码
├── api/                # API 路由
├── app/                # 应用逻辑
├── internal/           # 内部包
├── webui/              # React 前端
├── start.mjs           # Node.js 启动菜单脚本
├── go.mod              # Go 模块定义
└── go.sum              # Go 依赖校验
```

---

## 七、常见问题

### Q: 启动报错 TLS 连接失败？
A: DeepSeek 需要通过网络访问其 Web 服务。确保手机网络正常。

### Q: 编译时 `go: go.mod requires go >= 1.26.0`？
A: Alpine 自带的 Go 版本太低（1.23）。需要手动安装 Go 1.26（见步骤 1）。

### Q: `GOTOOLCHAIN=auto` 下载 Go 时 Segmentation fault？
A: proot 环境下 Go 自动工具链下载不稳定。改用手动下载 tar.gz 包安装。

### Q: Git clone 报 TLS 错误？
A: 改用下载 Release 源码包的方式获取代码（方式 B）。

### Q: 与 qoder-cn-proxy 有什么区别？
A: **qoder-cn-proxy** 调用 Qoder CN 官方 API，需要 PAT Token。**ds2api** 模拟 DeepSeek 网页端对话，需要 DeepSeek 账号密码。两者是不同的 API 代理方案。

### Q: 手机浏览器访问 127.0.0.1:8080 超时？
A: 在手机浏览器中用 `http://127.0.0.1:8080`（不要用局域网 IP）。

---

## 八、技术架构

```
客户端 (OpenAI/Claude/Gemini 格式请求)
  ↓
ds2api (Go 后端, 端口 8080)
  ↓ 模拟 DeepSeek Web 协议
DeepSeek Web 服务
  ↓
返回响应 → 转为标准 API 格式返回给客户端
```

ds2api 本质上是一个 **Web 协议适配层**，把 DeepSeek 的网页对话协议转换为标准的 OpenAI/Claude/Gemini API 格式，让任何兼容的客户端都能使用 DeepSeek 的能力。
