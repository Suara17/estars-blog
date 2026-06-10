---
title: "机器人指南｜Qoder cn proxy 部署指南"
published: 2026-06-10
description: "qoder-cn-proxy 部署指南适用场景在 Android 手机上用 Alpine Linux 运行 qoder-cn-proxy，把手机变成 Qoder CN API 的本地代理，供手机 App、浏览器或 OpenAI 兼容客户端使"
tags: ["机器人指南"]
category: "机器人指南"
draft: false
lang: zh-CN
pinned: false
comment: true
---

qoder-cn-proxy 部署指南适用场景在 Android 手机上用 Alpine Linux 运行 qoder-cn-proxy，把手机变成 Qoder CN API 的本地代理，供手机 App、浏览器或 OpenAI 兼容客户端使用。前置要求•Node.js v18+（推荐 v22）•Qoder CN CLI：npm install -g @qoder-ai/qoder-cli-cn•Qoder CN PAT Token：从 https://qoder.cn/settings/tokens 获取部署步骤1. 克隆项目cd /workspace
git clone https://github.com/avaritiachaos/qoder-cn-proxy.git
cd qoder-cn-proxy2. 配置 Tokencp .env.example .env编辑 .env，填入 PAT：QODER_CN_PAT=你的PAT3. 安装依赖npm install --silent4. 启动服务cd /workspace/qoder-cn-proxy
export PATH="/root/.npm-global/bin:$PATH"
node clean/server.js默认监听 http://0.0.0.0:3000，启动后输出：Qoder CN clean proxy listening on http://0.0.0.0:30005. 保活用持久化终端会话运行，或放后台：nohup node clean/server.js > /workspace/qoder-cn-proxy/proxy.log 2>&1 &客户端使用配置项值API Base URLhttp://手机局域网IP:3000（如 http://192.168.10.251:3000）API Key任意值或留空Modelqoder-cn、auto、qwen3.7-max、deepseek-v4 等可用端点方法路径说明GET/服务状态GET/health健康检查GET/v1/models列出模型POST/v1/chat/completionsOpenAI 聊天补全（支持流式）POST/v1/messagesAnthropic 消息格式测试验证# 服务状态
curl http://127.0.0.1:3000/
→ {"ok":true,"name":"qoder-cn-proxy","mode":"clean"}

聊天补全
curl http://127.0.0.1:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"auto","messages":[{"role":"user","content":"你好"}]}'注意事项•服务监听 0.0.0.0:3000，未配置 HTTPS•首次启动会自动下载 Qoder CN runner（约 200MB），确保网络畅通•Android App 用 http://127.0.0.1:3000 访问，外部设备用局域网 IP
