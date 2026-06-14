#!/usr/bin/env python3
"""
博客新增文章同步脚本
扫描源目录 → 对比已发布文章 → 添加 frontmatter → git commit + push
可直接运行：python3 /workspace/小万工作间/estars-blog/sync-blog.py
如需更新扫描目录，修改下方 SOURCES 列表即可。
"""
import os
import re
import subprocess
import sys
from datetime import date

BASE = "/workspace/小万工作间"
POSTS_DIR = f"{BASE}/estars-blog/src/content/posts"
TODAY = date.today().isoformat()

# ============================================================
# 要扫描的源目录定义（增删改这里即可）
# ============================================================
SOURCES = [
    # 1. 航海图/操作指南
    {
        "path": f"{BASE}/航海图/操作指南",
        "prefix": "航海图-操作指南",
        "category": "航海图",
        "tags": ["航海图", "操作指南"],
        "exclude": ["estars-blog博客站维护指南.md"],
        "subdir": False,
    },
    # 2. 工程现场/实战.经验
    {
        "path": f"{BASE}/工程现场/实战.经验",
        "prefix": "工程现场-实战.经验",
        "category": "工程现场",
        "tags": ["工程现场", "实战", "经验"],
        "exclude": [],
        "subdir": False,
    },
    # 3. 求职作战室/面经（含子目录递归）
    {
        "path": f"{BASE}/求职作战室/面经",
        "prefix": "求职作战室-面经",
        "category": "求职作战室",
        "tags": ["求职作战室", "面经"],
        "exclude": [],
        "subdir": True,
    },
    # 4. 外部精选/L站精选
    {
        "path": f"{BASE}/外部精选/L站精选",
        "prefix": "外部精选",
        "category": "外部精选",
        "tags": ["外部精选", "L站精选", "LINUX DO"],
        "exclude": [],
        "subdir": False,
    },
    # 5. 外部精选/公众号精选
    {
        "path": f"{BASE}/外部精选/公众号精选",
        "prefix": "外部精选",
        "category": "外部精选",
        "tags": ["外部精选", "公众号精选"],
        "exclude": [],
        "subdir": False,
    },
    # 6. 外部精选/小红书精选
    {
        "path": f"{BASE}/外部精选/小红书精选",
        "prefix": "外部精选-小红书精选",
        "category": "外部精选",
        "tags": ["外部精选", "小红书精选"],
        "exclude": ["README.md"],
        "subdir": False,
    },
    # 7. 求职作战室/岗位情报
    {
        "path": f"{BASE}/求职作战室/岗位情报",
        "prefix": "求职作战室-岗位情报",
        "category": "求职作战室",
        "tags": ["求职作战室", "岗位情报"],
        "exclude": [],
        "subdir": False,
    },
]


def extract_title(content: str, fname: str) -> str:
    """从 H1、frontmatter name 或文件名提取标题"""
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("# ") and len(line) > 2:
            return line[2:].strip()
    m = re.search(r'^name:\s*(.+)', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return os.path.splitext(fname)[0]


def extract_description(content: str) -> str:
    """从文件前几行提取简短描述（200字内）"""
    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("---") or line.startswith("#") or line.startswith(">") or line.startswith("|"):
            continue
        if line.startswith("name:") or line.startswith("description:"):
            continue
        return line[:197] + "..." if len(line) > 200 else line
    return ""


def build_frontmatter(title: str, category: str, tags: list, description: str) -> str:
    # 单引号包裹 + 去引号，避免 YAML 解析问题
    desc_clean = description.replace("'", "").replace('"', "").strip()[:120]
    title_clean = title.replace("'", "''")
    return f"""---
title: '{title_clean}'
published: {TODAY}
description: '{desc_clean}'
category: '{category}'
tags: {tags}
draft: false
lang: zh-CN
---"""


def strip_old_frontmatter(content: str) -> str:
    """如果已有 frontmatter（---...---），去掉它"""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content


def main():
    # 加载已发布文件集合
    published = set()
    if os.path.exists(POSTS_DIR):
        for f in os.listdir(POSTS_DIR):
            if f.endswith(".md"):
                published.add(f)

    new_files = []

    for src in SOURCES:
        src_path = src["path"]
        if not os.path.isdir(src_path):
            print(f"  ⚠️ 目录不存在: {src_path}")
            continue

        if src["subdir"]:
            # 递归子目录
            for root, dirs, files in os.walk(src_path):
                for fname in sorted(files):
                    if not fname.endswith(".md"):
                        continue
                    rel_dir = os.path.relpath(root, src_path)
                    if rel_dir == ".":
                        post_name = f"{src['prefix']}-{fname}"
                    else:
                        post_name = f"{src['prefix']}-{rel_dir}-{fname}"
                    if post_name in published:
                        continue
                    src_file = os.path.join(root, fname)
                    with open(src_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    title = extract_title(content, fname)
                    desc = extract_description(content)
                    body = strip_old_frontmatter(content)
                    full = build_frontmatter(title, src["category"], src["tags"], desc) + body
                    with open(os.path.join(POSTS_DIR, post_name), "w", encoding="utf-8") as f:
                        f.write(full)
                    print(f"  📝 新增: {post_name}")
                    new_files.append(post_name)
        else:
            # 只读直接子文件
            for fname in sorted(os.listdir(src_path)):
                if not fname.endswith(".md"):
                    continue
                if fname in src["exclude"]:
                    continue
                post_name = f"{src['prefix']}-{fname}"
                if post_name in published:
                    continue
                src_file = os.path.join(src_path, fname)
                with open(src_file, "r", encoding="utf-8") as f:
                    content = f.read()
                title = extract_title(content, fname)
                desc = extract_description(content)
                body = strip_old_frontmatter(content)
                full = build_frontmatter(title, src["category"], src["tags"], desc) + body
                with open(os.path.join(POSTS_DIR, post_name), "w", encoding="utf-8") as f:
                    f.write(full)
                print(f"  📝 新增: {post_name}")
                new_files.append(post_name)

    total = len(new_files)
    print(f"\n{'='*40}")
    print(f"📊 统计: 新增 {total} 篇")
    if total == 0:
        print("✅ 没有新增文章，跳过 git 操作")
        return

    # Git 提交
    print("\n🔄 提交到 Git...")
    git_dir = f"{BASE}/estars-blog"
    cmds = [
        ["git", "-C", git_dir, "add", "-A"],
        ["git", "-C", git_dir, "commit", "-m", f"feat: 博客同步 {TODAY}"],
        ["env", "GIT_SSL_NO_VERIFY=1", "git", "-C", git_dir, "push", "origin", "main"],
    ]
    for cmd in cmds:
        r = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)
        print(r.stdout)
        if r.returncode != 0:
            if "nothing to commit" in r.stdout or "nothing to commit" in r.stderr:
                print("✅ 没有变化，跳过推送")
                return
            if "Everything up-to-date" in r.stdout:
                print("✅ 远程已最新")
                return
            print(f"❌ 失败: {r.stderr}")
            sys.exit(1)

    print(f"\n🎉 博客同步完成！新增 {total} 篇，已推送到 GitHub → Cloudflare Pages 自动部署")


if __name__ == "__main__":
    main()
