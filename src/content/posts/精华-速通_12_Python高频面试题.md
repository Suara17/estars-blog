---
title: '🚀 速通 · Python 高频面试题'
published: 2026-06-16
description: '不是让你精通Python所有细节，而是能回答面试中最常考的20个问题，同时展示出你写的是「工程代码」而不是「脚本代码」。'
category: '求职作战室'
tags: ['求职作战室', '整理版']
draft: false
lang: zh-CN
---# 🚀 速通 · Python 高频面试题

---

## 🎯 你要达到什么水平

**不是让你精通Python所有细节，而是能回答面试中最常考的20个问题，同时展示出你写的是「工程代码」而不是「脚本代码」。**

---

## 📦 高频面试题速览

| 类别 | 问题数 | 优先级 |
|:----|:-----:|:-----:|
| 基础语法与数据结构 | 10 | ⭐⭐⭐⭐⭐ |
| 面向对象与魔法方法 | 5 | ⭐⭐⭐⭐ |
| 并发与异步 | 3 | ⭐⭐⭐ |
| 工程实践 | 2 | ⭐⭐⭐⭐ |

---

## 🔵 基础语法与数据结构

### Q1：列表和元组的区别？

**答案：**
```
列表（list）可变，元组（tuple）不可变。
列表用 []，元组用 ()。
列表支持增删改，元组创建后不能修改。
性能上元组略快，因为不可变所以可作为字典的键。
```

**面试官追问：「那set和frozenset呢？」**
```
set可变，frozenset不可变。
set不能作为字典的键，frozenset可以。
```

---

### Q2：字典和列表的底层实现？

**答案：**
```
列表底层是动态数组（连续内存），插入/删除O(n)，随机访问O(1)。
字典底层是哈希表（hash table），查找/插入/删除平均O(1)，
但需要处理哈希冲突（Python用开放寻址法）。
字典的key必须是可哈希的（不可变类型）。
```

**面试官追问：「为什么Python3.7+字典是有序的？」**
```
Python3.6开始字典底层使用紧凑的哈希表实现（结合数组+索引），
实际会保持插入顺序。Python3.7正式将有序作为语言特性。
```

---

### Q3：可变对象与不可变对象？函数传参是值传递还是引用传递？

**答案：**
```
不可变对象：int、float、str、tuple、frozenset
可变对象：list、dict、set、自定义类实例

Python函数传参是「对象引用传递」：
- 函数内部修改可变对象会影响外部
- 函数内部对不可变对象重新赋值不会影响外部（因为创建了新对象）
```

**例子：**
```python
def append_to(element, target=[]):  # 默认参数是可变对象
    target.append(element)
    return target

print(append_to(1))  # [1]
print(append_to(2))  # [1, 2]  ← 默认参数被记住了！
```
**正确写法：** `def append_to(element, target=None):` 内部再初始化。

---

### Q4：深拷贝和浅拷贝的区别？

**答案：**
```python
import copy

a = [1, 2, [3, 4]]
b = copy.copy(a)      # 浅拷贝：只拷贝外层，内层list还是引用
c = copy.deepcopy(a)  # 深拷贝：递归拷贝所有层

a[2][0] = 99
print(b[2][0])  # 99（浅拷贝受影响）
print(c[2][0])  # 3（深拷贝不受影响）
```

---

### Q5：装饰器是什么？写一个计时装饰器

**答案：**
```python
import time
from functools import wraps

def timer(func):
    @wraps(func)   # 保留原函数的元信息
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.2f}s")
        return result
    return wrapper

@timer
def slow_func():
    time.sleep(1)

# 面试常考：带参数的装饰器怎么写？
def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
```

---

### Q6：生成器与迭代器的区别？yield关键字的作用？

**答案：**
```
迭代器：实现了__iter__和__next__方法的对象。
生成器：用yield关键字的函数，返回生成器对象，是迭代器的一种。

yield让函数变成生成器，每次调用next()执行到yield暂停并返回值，
下次调用next()从断点继续执行。

好处：惰性求值，节省内存（处理大文件、无限序列时特别有用）。
```

示例：
```python
def read_large_file(file_path):
    """逐行读取大文件，不会一次性加载到内存"""
    with open(file_path) as f:
        for line in f:
            yield line.strip()
```

---

### Q7：`__init__`和`__new__`的区别？

**答案：**
```
__new__：静态方法，负责创建实例（分配内存），返回实例对象
__init__：实例方法，负责初始化实例（设置属性），无返回值

调用顺序：__new__ → __init__
通常不需要重写__new__，除非要实现单例模式或不可变类型。
```

---

### Q8：`is`和`==`的区别？

**答案：**
```
== 比较值是否相等（调用__eq__方法）
is 比较内存地址是否相同（是否是同一个对象）

a = [1, 2, 3]
b = [1, 2, 3]
a == b  # True（值相等）
a is b  # False（不同对象）

c = None
c is None  # True（None是单例）
```

---

### Q9：with语句的上下文管理器是怎么工作的？

**答案：**
```python
class FileManager:
    def __enter__(self):
        print("进入with块")
        return self  # 返回给as变量
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("退出with块，清理资源")
        # 返回True可抑制异常

with FileManager() as f:
    print("执行中")
```

也可以用`contextlib.contextmanager`装饰器：
```python
from contextlib import contextmanager
@contextmanager
def file_manager(filename):
    print("打开文件")
    yield
    print("关闭文件")
```

---

### Q10：GIL是什么？对Python并发有什么影响？

**答案：**
```
GIL（Global Interpreter Lock）是CPython的全局解释器锁，
保证同一时刻只有一个线程执行Python字节码。

影响：
- CPU密集型任务：多线程无法利用多核，用多进程（multiprocessing）
- IO密集型任务：多线程仍然有效（IO等待时释放GIL）
- 可以用asyncio、C扩展（如numpy）绕过GIL

Python 3.12+改进了GIL，但尚未完全移除。
```

---

## 🟡 面向对象与魔法方法

### Q11：类变量和实例变量的区别？

```python
class Dog:
    species = "犬科"      # 类变量
    def __init__(self, name):
        self.name = name  # 实例变量

a = Dog("旺财")
b = Dog("来福")
print(a.species)  # 犬科
Dog.species = "哺乳动物"
print(a.species)  # 哺乳动物（类变量被改了）
a.species = "狗"  # 创建了实例变量，不影响类变量
print(b.species)  # 哺乳动物
```

---

### Q12：`@staticmethod`和`@classmethod`的区别？

```python
class A:
    @staticmethod
    def static_method():
        """不依赖类和实例，就是个普通函数"""
        return "static"
    
    @classmethod
    def class_method(cls):
        """依赖类本身，可以访问类变量"""
        return cls.__name__

# staticmethod：通过类或实例调用，没有自动传参
# classmethod：自动传入类作为第一个参数
```

---

## 🟠 并发与异步

### Q13：多线程、多进程、异步有什么区别？分别适用什么场景？

| 方式 | 特点 | 适用场景 |
|:----|:----|:-------|
| **多线程**（threading） | 共享内存，受GIL限制 | IO密集型（文件/网络/数据库） |
| **多进程**（multiprocessing） | 独立内存，无GIL | CPU密集型（计算/图像处理） |
| **异步**（asyncio） | 单线程协作式调度 | 高IO并发（Web服务器/爬虫） |

---

### Q14：asyncio的基本用法？

```python
import asyncio

async def fetch_data(url):
    print(f"开始下载 {url}")
    await asyncio.sleep(1)  # 模拟IO等待
    return f"{url} 的数据"

async def main():
    tasks = [fetch_data(f"page{i}") for i in range(3)]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())  # 3个任务并发执行，总共约1秒
```

---

## 🔴 工程实践

### Q15：Python中如何管理依赖和环境？

```
- 环境隔离：venv / conda / poetry
- 依赖管理：pip freeze > requirements.txt / poetry.lock
- Python版本管理：pyenv
- 推荐现代方案：poetry（依赖管理+打包+发布一体）
```

### Q16：类型提示（Type Hints）有什么用？

```python
def add(a: int, b: int) -> int:
    return a + b

from typing import List, Optional, Dict
def process(items: List[str]) -> Optional[Dict[str, int]]:
    if not items:
        return None
    return {item: len(item) for item in items}
```

**作用：** 代码可读性提升、IDE自动补全、静态类型检查（mypy）、减少bug。

---

## ⚡ 速通建议

```
Python面试准备的核心不在于背语法，而在于：

1. 理解语言特性背后的设计哲学（为什么这样设计）
2. 会写工程级代码（类型提示、装饰器、上下文管理器）
3. 能说清楚GIL、可变不可变、深浅拷贝等底层机制

建议刷题：
- LeetCode用Python刷50道Easy/Medium（熟悉常用数据结构和API）
- 手写常见装饰器、生成器、上下文管理器
- 能解释你项目中的每一行Python代码为什么这么写
```

---

**⏱ 准备时间：** 2天（1天刷题+1天过面试题）
**面试杀伤力：** ⭐⭐⭐⭐ Python基础是入场券，答得好给面试官留下「基本功扎实」的印象
