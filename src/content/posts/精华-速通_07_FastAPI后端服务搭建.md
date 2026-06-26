---
title: '🚀 速通 · FastAPI 后端服务搭建'
published: 2026-06-16
description: '做一个能把Agent包装成API服务的后端接口：'
category: '求职作战室'
tags: ['求职作战室', '整理版']
draft: false
lang: zh-CN
---# 🚀 速通 · FastAPI 后端服务搭建

---

## 🎯 你要做到什么级别的小Demo

做一个**能把Agent包装成API服务的后端接口**：

```
你用FastAPI搭建一个后端服务，提供以下API：
1. POST /chat —— 接收用户消息，调用你的Agent，返回流式回答
2. GET /history/{session_id} —— 查看某次对话历史
3. POST /upload —— 上传PDF文档，自动走RAG流程存入向量库
4. GET /health —— 健康检查

用Docker部署，有Swagger文档。
```

**为什么是这个Demo：** AI应用最终都要以API形式提供服务，FastAPI是当前AI项目后端的事实标准。面试官看到你不仅会写Agent，还能把它包装成生产级的API服务，会认为你有**工程化交付能力**——这正是企业最想要的。

---

## 📄 核心代码框架（逐行解释）

```python
# ===== 项目结构 =====
# .
# ├── main.py          # 入口文件
# ├── routers/         # 路由模块
# │   ├── chat.py
# │   ├── history.py
# │   └── upload.py
# ├── models/          # 数据模型
# │   └── schemas.py
# ├── services/        # 业务逻辑
# │   └── agent.py
# └── requirements.txt

# ===== main.py —— 应用入口 =====
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 创建应用实例
app = FastAPI(
    title="AI Agent API",
    description="提供Agent对话、文档上传、历史查询等功能",
    version="1.0.0"
)

# 跨域配置（前后端分离必备）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # 生产环境要严格限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
from routers import chat, history, upload
app.include_router(chat.router, prefix="/api/v1")
app.include_router(history.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "AI Agent API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
# 解释：uvicorn是ASGI服务器，reload=True开发时改代码自动重启

# ===== routers/chat.py —— 对话接口（最核心） =====
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.agent import run_agent

router = APIRouter()

# 请求体模型（Pydantic自动校验）
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    stream: bool = False

class ChatResponse(BaseModel):
    answer: str
    session_id: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer, session_id = await run_agent(
            message=request.message,
            session_id=request.session_id
        )
        return ChatResponse(answer=answer, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# 解释：APIRouter把路由模块化，Pydantic自动做请求校验和文档生成
# async/await让接口在调用LLM时不会阻塞其他请求

# ===== services/agent.py —— Agent逻辑封装 =====
from langgraph.graph import StateGraph, END
# ...（你的Agent代码，见速通03）

async def run_agent(message: str, session_id: str = None):
    """包装Agent调用为异步函数"""
    # 这里是同步代码的话，用run_in_executor避免阻塞事件循环
    import asyncio
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda: agent.invoke({
        "messages": [{"role": "user", "content": message}]
    }))
    return result["final_answer"], session_id

# ===== services/upload.py —— 文件上传 =====
from fastapi import UploadFile, File
import shutil
from pathlib import Path

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 保存文件
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 触发RAG索引更新（见RAG速通文档）
    # await index_document(file_path)
    
    return {"filename": file.filename, "status": "indexed"}
# 解释：UploadFile是FastAPI对文件上传的内置支持
```

### Docker部署配置

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
      - ./chroma_db:/app/chroma_db
  # redis: 可选，用于缓存和会话管理
```

---

## ❓ 面试官最爱问的3个问题

| 问题 | 满分回答要点 |
|:----|:-----------|
| **1. FastAPI和Flask有什么区别？为什么选FastAPI？** | FastAPI是**异步**框架，天然支持async/await，调用LLM等IO操作时不阻塞事件循环；自动生成**OpenAPI文档**（Swagger）；基于**Pydantic**做请求校验，类型安全；性能接近Go/Node.js。Flask是同步的，适合简单项目，但高并发场景需要额外配置异步支持。AI项目密集调用外部API，FastAPI是更合适的选择。 |
| **2. 你的API在高并发下怎么保证稳定性？** | ① **异步非阻塞** — FastAPI本身异步，配合uvicorn的worker多进程 ② **限流** — 用slowapi或自定义中间件对每个用户做rate limit ③ **缓存** — 对相同请求结果用Redis缓存（LLM调用结果、Embedding结果）④ **熔断** — 调用LLM API失败时回退备用模型或返回缓存结果 ⑤ **健康检查** — /health接口配合k8s探针自动重启。 |
| **3. 怎么处理LLM调用的超时和错误？** | ① 给httpx/requests设置timeout（通常30-60s）② **重试机制**（retry：第一次失败后等1s重试，最多3次）③ **降级**（主模型超时切备用模型，如gpt-4o→gpt-4o-mini）④ **流式输出**（stream=True让用户尽早看到内容，即使后续中断也不至于白屏）⑤ **最终兜底**：所有模型都失败，返回友好提示并记录日志。 |

---

**⏱ 练熟时间：** 1天（已有Python基础）
**面试杀伤力：** ⭐⭐⭐⭐ 体现工程化交付能力，让面试官觉得你不只是会写脚本。
