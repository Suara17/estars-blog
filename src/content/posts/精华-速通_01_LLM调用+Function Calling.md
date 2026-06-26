---
title: '🚀 速通 · LLM API调用 + Function Calling'
published: 2026-06-16
description: '做一个能联网查天气并回答的聊天机器人：'
category: '求职作战室'
tags: ['求职作战室', '整理版']
draft: false
lang: zh-CN
---# 🚀 速通 · LLM API调用 + Function Calling

---

## 🎯 你要做到什么级别的小Demo

做一个**能联网查天气并回答的聊天机器人**：

```
用户问："北京今天多少度？"
你的程序会：
  1. 识别用户想查询天气 → 触发 get_weather 函数
  2. 调用外部天气API获取实时数据
  3. 把结果交给LLM，生成自然语言回答
  4. 返回："北京今天25°C，多云，适合出门~"
```

**为什么是这个Demo：** 它覆盖了LLM调用 + Function Calling + 工具集成 + 流式输出，是Agent的最小闭环。面试官一听就懂，一眼就能看出你掌握了核心。

---

## 📄 核心代码框架（逐行解释）

```python
# ===== 第1步：导入库 & 配置 =====
import json
import requests
from openai import OpenAI

client = OpenAI(
    api_key="sk-your-key",   # 换成你的API Key
    base_url="https://api.openai.com/v1"   # 也可换成国产模型地址
)

# ===== 第2步：定义工具（Tool Schema） =====
# 这是Function Calling的核心：告诉LLM有哪些函数可以调用，参数是什么

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的当前天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名，如'北京'、'上海'"
                    }
                },
                "required": ["city"]
            }
        }
    }
]
# 解释：LLM看到这个schema，当用户问天气时，它会返回一个function call请求，
# 而不是直接回答。我们拦截这个请求，调用真实API，再把结果送给LLM生成回答。

# ===== 第3步：实现工具函数（真实逻辑） =====
def get_weather(city: str) -> str:
    """调用一个免费天气API（示例用wttr.in，不需要key）"""
    url = f"https://wttr.in/{city}?format=%C+%t"
    resp = requests.get(url, timeout=5)
    return resp.text.strip()
    # 返回例如："☀️ +25°C"

# ===== 第4步：核心循环——处理Function Call =====
def chat_with_function_calling(user_message: str) -> str:
    # 4a. 先发消息给LLM
    messages = [
        {"role": "system", "content": "你是一个友好的助手，可以使用工具查询天气。"},
        {"role": "user", "content": user_message}
    ]
    response = client.chat.completions.create(
        model="gpt-4o",           # 或者用国产模型
        messages=messages,
        tools=tools,              # 把工具定义传给模型
        tool_choice="auto"        # 让模型自己决定是否调用工具
    )
    # response 里可能包含直接回答，也可能包含 tool_calls

    # 4b. 检查是否有函数调用请求
    assistant_message = response.choices[0].message
    if assistant_message.tool_calls:
        # 有工具调用 → 执行函数
        for tool_call in assistant_message.tool_calls:
            if tool_call.function.name == "get_weather":
                # 解析参数
                args = json.loads(tool_call.function.arguments)
                city = args.get("city")
                # 调用真实函数
                weather_result = get_weather(city)
                # 把函数执行结果追加到对话中
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": weather_result
                })
        # 4c. 把带有工具结果的完整对话再发给LLM生成最终回答
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return final_response.choices[0].message.content
    else:
        # 没有工具调用，直接返回模型的回答
        return assistant_message.content

# ===== 第5步：跑起来 =====
if __name__ == "__main__":
    while True:
        user_input = input("你：")
        if user_input.lower() in ["quit", "exit"]:
            break
        answer = chat_with_function_calling(user_input)
        print(f"助手：{answer}\n")
```

**代码就这么点，核心思想就三步：**
1. 定义工具（schema）给LLM看
2. LLM判断需要调用工具时，返回`tool_calls`而不是文字
3. 你执行函数，把结果塞回对话，再让LLM生成最终回答

---

## ❓ 面试官最爱问的3个问题

| 问题 | 满分回答要点 |
|:----|:-----------|
| **1. Function Calling 的原理是什么？** | LLM输出一个特殊的JSON结构（`tool_calls`），包含函数名和参数，由开发者执行真正的函数后再将结果送回给LLM。它不是LLM直接调用函数，而是**请求调用**。 |
| **2. 如果函数调用超时或出错，你怎么处理？** | 加try-except，超时重试，或返回一个错误提示说"暂时查不到，请稍后再试"。也可以设计fallback：比如天气API失败就返回缓存数据。 |
| **3. 多个工具同时被调用怎么处理？** | 模型可能一次请求调用多个函数。遍历`tool_calls`依次执行，收集所有结果，再把全部结果一起送回LLM。注意有些函数有依赖关系时，需要按顺序执行。 |

---

**⏱ 练熟这个Demo预计时间：** 半天（API Key + 写代码 + 调试）
**有了它你能在面试中展示：** LLM API调用、Function Calling完整流程、错误处理思路、工具集成能力。
