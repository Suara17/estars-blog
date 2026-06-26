---
title: "归藏技能（Guizang Social Card Skill）小红书卡片制作流程"
published: 2026-06-11
description: "## 概述 使用 `guizang-social-card-skill`（已安装于 `/workspace/.omnibot/skills/guizang-social-card-skill/`）为文章生成小红书 ## 前置条件 ⚠️ 注意：Pexels 的图片 ID 随机，具体 URL 需从页面元素中提取。"
category: "航海图"
tags: ["航海图", "操作指南", "小红书", "卡片制作", "Guizang"]
draft: false
lang: zh-CN
---

# 归藏技能（Guizang Social Card Skill）小红书卡片制作流程

## 概述

使用 `guizang-social-card-skill`（已安装于 `/workspace/.omnibot/skills/guizang-social-card-skill/`）为文章生成小红书 3:4 图文卡片（1080×1440px）。本流程记录以"OpenClaw工作原理解析.md"为素材的完整制作经验。

## 前置条件

- 技能已安装：`skills_list | grep guizang` 确认存在
- 系统已装中文字体：`wqy-zenhei`（文泉驿正黑），位于 `/usr/share/fonts/wqy-zenhei/`
- Chromium 浏览器：`/usr/bin/chromium-browser`
- Node.js + Puppeteer 用于渲染输出 PNG

## 完整工作流

### Step 1：读取技能参考文件

```bash
# 技能 SKILL.md 位于
/workspace/.omnibot/skills/guizang-social-card-skill/SKILL.md

# 关键参考文件
references/style-system.md       # 风格系统（Swiss / Editorial 两种模式）
references/layout-recipes.md     # 布局食谱
references/theme-presets.md      # 主题色板（Ink Classic / IKB Blue 等）
references/components.md         # 组件规范（字体、间距、圆角等）
references/platform-specs.md     # 平台规格（小红书 1080×1440, 3:4）
references/production-workflow.md # 生产工作流
assets/template-swiss-card.html   # Swiss 风格 HTML 模板
assets/template-editorial-card.html # 杂志风格 HTML 模板
```

### Step 2：规划卡片内容与风格

**小红书规格**：1080×1440px（3:4），导出 PNG

**推荐风格**：
- **Swiss International**：科技、工程、AI 类文章（IKB Blue 强调色 #002FA7）
- **Editorial Magazine x E-ink**：文艺、人文、生活类文章
- **手绘可爱风（Doodle）**：需要自定义 CSS，参考本指南的"手绘风改造"部分

### Step 3：配置素材图片

**三种方案**：
- A. 用户自行提供截图/照片（推荐最自然）
- B. 从 Pexels/Unsplash 找免费素材图
- C. AI 生成插画

**B 方案操作**（以 Pexels 为例）：

```bash
# 1. 在 Pexels 搜索科技/AI 相关图片
# 2. 打开图片详情页，通过 find_elements 找到下载链接
# 3. 用 wget 下载到 assets/ 目录
cd /workspace/social-card-openclaw/assets
wget -O robot-hand-blue.jpg "https://images.pexels.com/photos/8386437/pexels-photo-8386437.jpeg?cs=srgb&dl=pexels-tara-winstead-8386437.jpg&fm=jpg"
```

> ⚠️ 注意：Pexels 的图片 ID 随机，具体 URL 需从页面元素中提取。

### Step 4：编写 HTML 卡片

#### 项目目录结构

```
social-card-<slug>/
├── index.html       # 所有卡片帧的 HTML
├── render.cjs       # Puppeteer 渲染脚本
├── assets/          # 素材图片
└── output/          # 输出 PNG
```

#### HTML 结构要点

- 每个卡片帧为一个 `<section>` 或 `<div>`，用 `id` 区分
- 设置 `width: 1080px; height: 1440px;` 匹配小红书规格
- 文字和关键内容保持在安全区内（上下左右留 60-90px 边距）
- 字体优先使用系统 WenQuanYi Zen Hei，避免 Google Fonts 加载失败

#### 字体配置

```css
@font-face {
  font-family: 'WQ';
  src: local('WenQuanYi Zen Hei'), local('文泉驿正黑');
}
body {
  font-family: 'WQ', 'Noto Sans SC', sans-serif;
}
```

> ⚠️ 务必使用 `@font-face` 引用本地中文字体，防止 Chromium 脱机渲染时无法加载 Google Fonts 导致乱码或空白。

### Step 5：渲染为 PNG

#### 方式 A：Puppeteer（推荐）

安装依赖：
```bash
cd social-card-<slug>/
npm init -y
npm install puppeteer
```

渲染脚本 `render.cjs`：
```javascript
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: '/usr/bin/chromium-browser',
    args: ['--no-sandbox', '--disable-gpu', '--disable-software-rasterizer'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1440 });

  // 关键：添加 cache-busting 参数避免 Chromium 缓存旧文件
  const ts = Date.now();
  await page.goto('file://' + path.resolve(__dirname, 'index.html') + '?_=' + ts, {
    waitUntil: 'networkidle0', timeout: 30000
  });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 3000)); // 等字体和图片加载完成

  // 截取整个视口或特定元素
  await page.screenshot({ path: 'output.png', type: 'png' });

  // 或截取特定元素
  const el = await page.$('.frame');
  if (el) await el.screenshot({ path: 'output/result.png', type: 'png' });

  await browser.close();
})();
```

运行：
```bash
node render.cjs
```

#### 方式 B：Chromium 命令行截图

```bash
chromium-browser --headless --no-sandbox --disable-gpu \
  --screenshot=output.png --window-size=1080,1440 \
  "file://$(pwd)/index.html?_=$(date +%s)"
```

> ⚠️ 此方式在 Alpine proot 环境中偶有截图内容为空的 bug，优先使用 Puppeteer。

### Step 6：预览与迭代

用 `file_read` 预览生成的 PNG：

```
file_read("path/to/output.png")
```

## 手绘可爱风格实现（Doodle Style）

### 风格特征

- 暖色调纸纹背景（#fcf6eb / #faf3e8）
- SVG 手绘装饰元素：云朵、星星、爱心、波浪线
- 拟人手绘感边框（虚线、波纹线）
- 柔和 pastel 配色：粉色 #ffb5c2、蓝色 #b5d8f7、黄色 #f9d56e
- 圆角、松散的手绘图标（纯 SVG 绘制）
- 无科技感图片，用 SVG 可爱插画代替

### 手绘装饰 SVG 示例

```svg
<!-- 云朵 -->
<path d="M28 62 Q10 50 16 33 Q10 16 28 14 Q32 -2 56 4 Q72 -4 90 8 Q108 0 116 20 Q128 26 120 45 Q126 56 108 62 Q88 68 66 58 Q44 68 28 62Z" fill="#f0e0c8" stroke="#d4c4a8" stroke-width="2.5"/>

<!-- 星星 -->
<path d="M16 2 L19 12 L30 12 L21 19 L24 30 L16 23 L8 30 L11 19 L2 12 L13 12Z" fill="#f9d56e" stroke="#e8b84a" stroke-width="2"/>

<!-- 手绘分割线 -->
<path d="M10 13 Q40 6 70 12 Q100 18 130 10 Q160 4 190 14 Q220 22 250 9 Q280 2 295 14 Q310 18 320 12" stroke="#e0b896" stroke-width="3" fill="none" stroke-linecap="round"/>
```

### 手机阅读字体大小经验值（1080px 画幅）

| 元素 | 字号 | 说明 |
|------|------|------|
| 主标题 | 76-84px | 加粗，控制 1-2 行 |
| 标签/小标题 | 26-30px | 点缀性文字 |
| 步骤标题 | 36-40px | 流程图的每一步 |
| 步骤描述 | 30-34px | 正文说明文字，行高 1.5 |
| 底部备注 | 24-26px | 装饰性文字 |

### 流程卡片布局

使用垂直时间线布局：

```
[步骤1图标] 步骤1标题
             步骤1描述文字
     |  (手绘竖线连接)
[步骤2图标] 步骤2标题
             步骤2描述文字
     |
[步骤3图标] 步骤3标题
             步骤3描述文字
```

每个步骤由 `item` 容器实现：
- `icn`（固定宽度 76-90px，SVG 图标）
- `tx`（弹性宽度，`tit` + `desc`）
- 竖线用绝对定位 `step-line` 或伪元素

## 常见问题 & 解决方案

### 1. 修改 HTML 后渲染图片无变化

**原因**：Chromium 会缓存 `file://` URL 的内容，即使文件已更新。

**解决方案**：在 URL 后添加随机查询参数（cache-busting）：

```javascript
const ts = Date.now();
await page.goto('file://.../index.html?_=' + ts, ...);
```

或使用全新的文件名/目录路径，彻底避免缓存。

### 2. 汉字渲染为方块或乱码

**原因**：系统缺少中文字体，或 Google Fonts 在离线环境无法加载。

**解决方案**：
- 使用本地字体：`@font-face { src: local('WenQuanYi Zen Hei'), local('文泉驿正黑'); }`
- 不要依赖 `@import url(https://fonts.googleapis.com/...)` 加载中文字体
- 验证字体可用：`fc-list :lang=zh`

### 3. Chromium 截图内容空白

**可能原因**：
- `--screenshot` 参数与文件路径配合问题
- 字体加载超时

**解决方案**：改用 Puppeteer + `waitForSelector` + `document.fonts.ready` 确保完整加载。

### 4. Puppeteer 找不到 Chromium

```bash
# 指定系统预装的 Chromium
executablePath: '/usr/bin/chromium-browser'
```

## 技术栈速查

| 工具 | 用途 | 路径 |
|------|------|------|
| guizang-social-card-skill | 卡片设计规范与模板 | `/workspace/.omnibot/skills/guizang-social-card-skill/` |
| Chromium | 无头渲染引擎 | `/usr/bin/chromium-browser` |
| Puppeteer | Node.js 截图控制 | `node_modules/puppeteer` |
| WenQuanYi | 中文字体 | `/usr/share/fonts/wqy-zenihi/wqy-zenhei.ttc` |
| Node.js | 运行渲染脚本 | `/usr/bin/node` (v22) |
| Python HTTP server | 本地调试用（可选） | `python3 -m http.server` |

## 本次实践产出

- 最终卡片：`/workspace/cute-card/output.png`（1080×1440 可爱手绘风）
- HTML 源码：`/workspace/cute-card/index.html`
- 渲染脚本：`/workspace/cute-card/render.cjs`
- 文章原文：`/workspace/小万工作间/工程现场/实战.经验/OpenClaw工作原理解析.md`
