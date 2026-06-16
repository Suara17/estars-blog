---
title: '🚀 速通 · MCP协议（模型上下文协议）'
published: 2026-06-16
description: '做一个基于MCP协议的天气查询工具服务器：'
category: '求职作战室'
tags: ['求职作战室', '整理版']
draft: false
lang: zh-CN
---# 🚀 速通 · MCP协议（模型上下文协议）

---

## 🎯 你要做到什么级别的小Demo

做一个**基于MCP协议的天气查询工具服务器**：

```
你运行一个MCP服务器，然后让Claude Desktop（或其他MCP客户端）连接它。
用户在Claude里输入："北京今天天气怎么样？"
Claude会通过MCP协议调用你的服务器 → 返回实时天气 → Claude展示给用户。

整个过程，你不需要写Function Calling的复杂逻辑，
只需要按照MCP规范暴露一个工具接口。
```

**为什么是这个Demo：** MCP是2026年新兴的**标准化工具调用协议**，被称为"AI界的USB-C"。懂的人极少，你在面试中聊MCP，面试官会觉得你技术视野领先。而且它确实是未来趋势——OpenAI、Anthropic、各大云厂商都在推。

---

## 📄 核心代码框架（逐行解释）

```python
# ===== 使用MCP官方Python SDK实现 =====

# 第0步：安装
# pip install mcp httpx

# ===== 第1步：导入MCP SDK核心 =====
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# 解释：MCP Server的核心是暴露工具（Tools）给AI客户端调用
# 与Function Calling不同，MCP是标准化的协议层，任何支持的客户端都能用

# ===== 第2步：创建一个服务器实例 =====
server = Server("weather-server")

# ===== 第3步：定义工具列表（类似Function Calling的Schema） =====
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """告诉客户端：我这个服务器提供什么工具"""
    return [
        types.Tool(
            name="get_weather",
            description="查询指定城市的当前天气",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名，例如'北京'、'上海'、'广州'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位，默认为celsius"
                    }
                },
                "required": ["city"]
            }
        )
    ]
# 解释：@server.list_tools() 装饰器定义了这个MCP服务器提供了哪些工具
# inputSchema和Function Calling的parameters结构几乎一样

# ===== 第4步：实现工具的执行逻辑 =====
@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict
) -> list[types.TextContent]:
    """当客户端调用某个工具时，这个函数会被触发"""
    
    if name == "get_weather":
        city = arguments.get("city", "北京")
        unit = arguments.get("unit", "celsius")
        
        # 实际调用天气API（这里用模拟数据）
        result = f"{city}的天气：晴天，25°C"
        
        # 返回结果（必须用TextContent包装）
        return [types.TextContent(type="text", text=result)]
    
    # 如果调用了不存在的工具
    raise ValueError(f"未知工具: {name}")
# 解释：@server.call_tool() 是工具的实际执行入口
# name是工具名，arguments是LLM解析出的参数
# 必须返回 types.TextContent 列表

# ===== 第5步：启动服务器 =====
async def main():
    """使用stdio传输协议运行MCP服务器"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="weather-server",
                server_version="0.1.0"
            )
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
# 解释：stdio_server表示通过标准输入输出和客户端通信
# Claude Desktop等客户端会启动这个进程，通过stdio交互
```

### 用MCP Client测试你的服务器

```python
# 这是一个简单的MCP Client，用来测试你的Server
import asyncio
from mcp.client.stdio import stdio_client

async def test():
    async with stdio_client(["python", "weather_server.py"]) as (read, write):
        # 发送请求获取工具列表
        # 完整实现略，可以用mcp库的client高层API
        print("MCP Server已启动，可通过Claude Desktop连接")

asyncio.run(test())
```

---

## 🧠 MCP和Function Calling的核心区别（面试高频考点）

```diff
- Function Calling：
  - OpenAI/Anthropic各自定义自己的格式
  - 只能在对应的LLM下使用
  - 每次接入新工具都要重新写调用逻辑
  - 是API层面的功能

+ MCP协议：
+ 统一标准，任何模型/客户端都能用
+ Server提供工具、Resources、Prompts三种能力
+ 一次开发，到处可用（Claude、Cursor、VS Code都能连）
+ 是协议层面的标准（类比HTTP协议）
+ 支持热插拔、权限控制、远程连接
```

**一句话总结：** Function Calling是LLM厂商给你的接口规范，MCP是**整个行业统一的工具调用协议**。后者是大趋势。

---

## ❓ 面试官最爱问的3个问题

| 问题 | 满分回答要点 |
|:----|:-----------|
| **1. MCP解决了什么问题？为什么需要它？** | 在MCP之前，每个LLM接入外部工具都要写适配代码：OpenAI的Function Calling一套格式、Claude一套、国产模型又一套。相当于每个设备都要自己的充电器。**MCP统一了工具调用的协议标准**：工具开发者只需要按MCP规范写一个Server，任何支持MCP的客户端（Claude、Cursor、VS Code、甚至你自建的应用）都可以直接使用，无需重复适配。 |
| **2. MCP的三种核心能力是什么？** | **① Tools（工具）**：可被LLM调用的函数，类似Function Calling ② **Resources（资源）**：LLM可以读取的数据（文件、数据库、API数据），类似RAG中的上下文获取 ③ **Prompts（提示模板）**：预定义的提示词模板，用户可以直接使用。实际开发中最常用的是Tools。 |
| **3. MCP Server有哪几种传输方式？** | **① stdio（标准输入输出）**：Client启动Server进程，通过命令行管道通信（最简单，适合本地） ② **SSE（Server-Sent Events）**：通过HTTP通信，支持远程连接（适合生产环境）。如果Server在远程服务器，Client通过HTTP连接，Server通过SSE流式推送结果。 |

---

**⏱ 练熟时间：** 半天（理解概念 + 跑通Demo）
**面试杀伤力：** ⭐⭐⭐⭐⭐ **核弹级**——懂MCP的候选人比例不到5%，你只要提一嘴"MCP协议"，面试官就会觉得你技术视野领先同行一大截。

**进阶建议：** 把MCP和你前面做的天气查询、搜索工具集成，做成一个"统一的MCP工具服务器"，然后面试时说："我把所有工具都封装成了MCP Server，任何MCP客户端都能直接使用"——就这一句话，面试官得记你一笔。
