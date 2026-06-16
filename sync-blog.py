#!/usr/bin/env python3
"""
博客新增文章同步脚本
扫描源目录 → 对比已发布文章 → 添加 frontmatter → git commit + push
可直接运行：python3 /workspace/小万工作间/estars-blog/sync-blog.py
如需更新扫描目录，修改下方 SOURCES 列表即可。
"""
import os
import re
import hashlib
import subprocess
import sys
from datetime import date, datetime

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
    # 3. 求职作战室/整理版
    {
        "path": f"{BASE}/求职作战室/整理版",
        "prefix": "求职作战室-整理版",
        "category": "求职作战室",
        "tags": ["求职作战室", "整理版"],
        "exclude": [],
        "subdir": True,
    },
]

# ============================================================
# 要删除的旧博文前缀（后续不再同步的目录）
# ============================================================
CLEANUP_PREFIXES = [
    "外部精选-",
    "求职作战室-岗位情报-",
    "求职作战室-面经-",
    "求职作战室-简历材料-",
    "求职作战室-基础题库-",
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
    """从文件前几行提取简短描述（120字内，去掉markdown标记和引号）"""
    lines = content.split("\n")
    desc = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("---") or line.startswith("#") or line.startswith(">") or line.startswith("|"):
            continue
        if line.startswith("name:") or line.startswith("description:"):
            continue
        clean = re.sub(r'[#*_\[\]`>|\\]', '', line).strip()
        if clean:
            desc = clean[:120]
            break
    desc = desc.replace("'", "").replace('"', "").strip()
    if not desc:
        desc = "博客同步文章"
    return desc


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


def is_modified_today(filepath: str) -> bool:
    """检查文件的修改日期是否是今天"""
    mtime = os.path.getmtime(filepath)
    return datetime.fromtimestamp(mtime).date() == date.today()


def strip_old_frontmatter(content: str) -> str:
    """如果已有 frontmatter（---...---），去掉它"""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content


def is_content_unchanged(post_path: str, body: str) -> bool:
    """检查 posts 目录中已存在的文件，去掉 frontmatter 后与当前正文是否一致"""
    if not os.path.isfile(post_path):
        return False
    with open(post_path, "r", encoding="utf-8") as f:
        existing = f.read()
    existing_body = strip_old_frontmatter(existing)
    return existing_body.strip() == body.strip()


def cleanup_removed_posts():
    """删除不再同步的旧博文（匹配 CLEANUP_PREFIXES）"""
    deleted = 0
    if not os.path.isdir(POSTS_DIR):
        return deleted
    for fname in sorted(os.listdir(POSTS_DIR)):
        if not fname.endswith(".md"):
            continue
        for prefix in CLEANUP_PREFIXES:
            if fname.startswith(prefix):
                os.remove(os.path.join(POSTS_DIR, fname))
                print(f"  🗑️ 删除: {fname}")
                deleted += 1
                break
    return deleted


def main():
    new_files = []
    deleted = []

    # 第一步：清理不再同步的旧博文
    print("🔍 检查需要删除的旧博文...")
    if os.path.isdir(POSTS_DIR):
        for fname in sorted(os.listdir(POSTS_DIR)):
            if not fname.endswith(".md"):
                continue
            for prefix in CLEANUP_PREFIXES:
                if fname.startswith(prefix):
                    os.remove(os.path.join(POSTS_DIR, fname))
                    print(f"  🗑️ 删除: {fname}")
                    deleted.append(fname)
                    break
    print(f"📊 删除统计: {len(deleted)} 篇")
    print()

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
                    src_file = os.path.join(root, fname)
                    if not is_modified_today(src_file):
                        continue
                    with open(src_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    title = extract_title(content, fname)
                    desc = extract_description(content)
                    body = strip_old_frontmatter(content)
                    post_path = os.path.join(POSTS_DIR, post_name)
                    if is_content_unchanged(post_path, body):
                        print(f"  ⏭️ 跳过: {post_name} (内容无变化)")
                        continue
                    full = build_frontmatter(title, src["category"], src["tags"], desc) + body
                    with open(post_path, "w", encoding="utf-8") as f:
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
                src_file = os.path.join(src_path, fname)
                if not is_modified_today(src_file):
                    continue
                with open(src_file, "r", encoding="utf-8") as f:
                    content = f.read()
                title = extract_title(content, fname)
                desc = extract_description(content)
                body = strip_old_frontmatter(content)
                post_path = os.path.join(POSTS_DIR, post_name)
                if is_content_unchanged(post_path, body):
                    print(f"  ⏭️ 跳过: {post_name} (内容无变化)")
                    continue
                full = build_frontmatter(title, src["category"], src["tags"], desc) + body
                with open(post_path, "w", encoding="utf-8") as f:
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
        # 使用列表形式直接传给 subprocess，避免 shell 拆分参数
        r = subprocess.run(cmd, capture_output=True, text=True)
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
