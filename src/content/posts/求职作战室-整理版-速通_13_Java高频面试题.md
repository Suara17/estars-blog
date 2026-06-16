---
title: '🚀 速通 · Java 高频面试题'
published: 2026-06-16
description: '能回答Java基础核心问题，尤其是面向对象、集合框架、JVM基础。'
category: '求职作战室'
tags: ['求职作战室', '整理版']
draft: false
lang: zh-CN
---# 🚀 速通 · Java 高频面试题

---

## 🎯 你要达到什么水平

**能回答Java基础核心问题，尤其是面向对象、集合框架、JVM基础。**
部分AI岗位要求Java（如字节跳动、中软才信等），不需要精通，但不能一问三不知。

---

## 📦 高频面试题速览

| 类别 | 问题数 | 优先级 |
|:----|:-----:|:-----:|
| 面向对象基础 | 5 | ⭐⭐⭐⭐⭐ |
| 集合框架 | 4 | ⭐⭐⭐⭐⭐ |
| JVM基础 | 3 | ⭐⭐⭐⭐ |
| 多线程 | 3 | ⭐⭐⭐⭐ |
| Java8+新特性 | 2 | ⭐⭐⭐ |

---

## 🔵 面向对象基础

### Q1：面向对象的四大特性？

```
1. 封装：隐藏内部实现，对外暴露接口
2. 继承：子类继承父类的属性和方法
3. 多态：同一方法在不同对象上有不同表现（重写/接口实现）
4. 抽象：抽象类和接口，定义规范不实现细节
```

**常问：「重载（Overload）和重写（Override）的区别？」**
```
重载：同一个类中，方法名相同，参数列表不同，编译时多态
重写：子类重新定义父类的方法，运行时多态
```

---

### Q2：`==`和`equals()`的区别？

**答案：**
```
== ：比较基本类型的值，或引用类型的地址是否相同
equals()：Object中的默认实现是==，但String、Integer等类重写了它，
          改为比较内容是否相等

String a = new String("hello");
String b = new String("hello");
a == b        // false（不同对象）
a.equals(b)   // true（内容相同）
```

---

### Q3：String、StringBuilder、StringBuffer的区别？

```
String：不可变，每次修改创建新对象，线程安全（因为不可变）
StringBuilder：可变，非线程安全，性能最高（单线程推荐）
StringBuffer：可变，线程安全（方法有synchronized），性能略低
```

---

### Q4：final关键字的作用？

```
- final class：不能被继承
- final method：不能被重写
- final variable：值不能被修改（基本类型值不变，引用类型地址不变）
- final参数：方法内不能修改参数引用
```

---

### Q5：抽象类和接口的区别？

| 特性 | 抽象类 | 接口 |
|:----|:------|:----|
| 关键字 | abstract class | interface |
| 方法实现 | 可以有抽象方法和具体方法 | 默认方法（default）、静态方法、抽象方法 |
| 构造方法 | 可以有 | 不能有 |
| 成员变量 | 任何类型 | public static final（常量） |
| 继承 | 单继承 | 多实现 |

**Java8+接口可以有default和static方法，接口越来越像抽象类。**

---

## 🟡 集合框架

### Q6：ArrayList和LinkedList的区别？

```
ArrayList底层是数组，LinkedList底层是双向链表。

ArrayList：
- 随机访问O(1)
- 插入/删除O(n)（需移动元素）
- 内存连续，缓存友好

LinkedList：
- 随机访问O(n)（需遍历）
- 头尾插入/删除O(1)
- 内存不连续，占用更多空间（存储前后指针）
```

**场景：频繁随机访问用ArrayList，频繁插入删除用LinkedList。**

---

### Q7：HashMap的底层实现？JDK1.8前后的变化？

```
JDK1.8之前：数组+链表（头插法）
JDK1.8之后：数组+链表+红黑树（尾插法）

核心参数：
- 初始容量：16
- 负载因子：0.75
- 树化阈值：链表长度≥8且数组长度≥64时转为红黑树
- 退化阈值：红黑树节点≤6时转回链表

put流程：
  计算key的hash → 定位数组索引 → 若空直接插入 → 
  若不空，遍历链表/红黑树 → 找到相同key覆盖，
  否则新增 → 检查是否超过阈值，触发resize
```

**为什么链表转红黑树的阈值是8？**
```
基于泊松分布，在随机hash下，链表长度达到8的概率极低（约0.00000006），
所以8是时间和空间的折中选择。
```

---

### Q8：ConcurrentHashMap的实现原理？

```
JDK1.7：分段锁（Segment）+ 多次hash
JDK1.8：CAS + synchronized + 红黑树

JDK1.8核心：
- 数组+链表+红黑树（和HashMap一样）
- 并发安全通过CAS和synchronized实现（锁住数组的单个桶）
- 读操作不加锁（volatile保证可见性）
- 扩容时多线程协助迁移
```

---

### Q9：HashSet和TreeSet的区别？

```
HashSet：底层HashMap，无序，O(1)，元素需实现hashCode()和equals()
TreeSet：底层TreeMap（红黑树），有序（默认自然顺序或Comparator），O(log n)
```

---

## 🟠 JVM基础

### Q10：JVM内存区域（运行时数据区）？

```
线程私有：
  - 程序计数器：当前线程执行的字节码行号
  - 虚拟机栈：局部变量表、操作数栈、方法出口
  - 本地方法栈：native方法

线程共享：
  - 堆：对象实例、数组（GC主要区域）
  - 方法区（元空间）：类信息、常量、静态变量、JIT编译代码
```

---

### Q11：GC（垃圾回收）的基本算法？

```
1. 标记-清除：标记存活对象→清除未标记的，产生碎片
2. 标记-复制：将内存分为两块，存活对象复制到另一块，整块清除
3. 标记-整理：标记存活对象→向一端移动→清理边界外

分代收集：
  - 新生代：标记-复制（Eden→Survivor）
  - 老年代：标记-整理/标记-清除
```

---

### Q12：类加载机制（双亲委派模型）？

```
启动类加载器（Bootstrap ClassLoader）：加载JAVA_HOME/lib
扩展类加载器（Extension ClassLoader）：加载JAVA_HOME/lib/ext
应用程序类加载器（App ClassLoader）：加载classpath

双亲委派：一个类加载器收到请求后，先交给父加载器加载，
父加载器不能加载时才自己加载。保证核心类不被篡改。
```

---

## 🔴 多线程

### Q13：synchronized和Lock的区别？

```
synchronized：关键字，自动获取释放锁，支持锁升级（偏向→轻量→重量）
Lock：接口，需手动lock/unlock，更灵活（可中断、可超时、可尝试）

使用Lock的场景：
- 需要尝试获取锁（tryLock）
- 需要可中断的锁
- 需要公平锁
- 需要多个条件变量（Condition）
```

---

### Q14：volatile关键字的作用？

```
保证可见性：对volatile变量的写会立即刷新到主存，读从主存读
防止指令重排序：禁止JIT和CPU对volatile变量周围的指令重排

不保证原子性：i++操作仍然不是线程安全的（需要synchronized或AtomicInteger）
```

---

### Q15：线程池的核心参数？

```java
ThreadPoolExecutor(int corePoolSize,      // 核心线程数
                   int maximumPoolSize,   // 最大线程数
                   long keepAliveTime,    // 空闲线程存活时间
                   TimeUnit unit,
                   BlockingQueue<Runnable> workQueue, // 任务队列
                   ThreadFactory threadFactory,
                   RejectedExecutionHandler handler) // 拒绝策略
```

**拒绝策略：**
```
AbortPolicy：抛出异常（默认）
CallerRunsPolicy：由调用线程执行
DiscardPolicy：丢弃任务
DiscardOldestPolicy：丢弃队列中最老的任务
```

---

## ⚡ Java8+ 新特性

### Q16：Lambda表达式和Stream API？

```java
// Lambda
list.forEach(item -> System.out.println(item));

// Stream
list.stream()
    .filter(s -> s.startsWith("A"))
    .map(String::toUpperCase)
    .sorted()
    .collect(Collectors.toList());
```

### Q17：Optional怎么用？

```java
// 避免空指针
Optional<String> opt = Optional.ofNullable(getName());
String result = opt.orElse("默认值");
opt.ifPresent(System.out::println);
```

---

## ⚡ 速通建议

```
Java准备策略（针对AI岗）：
1. 重点：面向对象、HashMap/ConcurrentHashMap、JVM内存区
2. 理解：多线程基础（synchronized、volatile、线程池）
3. 了解：Java8+新特性（Lambda、Stream看代码能懂就行）

不要求深入到源码级别，但要知道核心原理和常见问题。
最好能用「和Python对比」的方式回答，展示多语言视野。
```

---

**⏱ 准备时间：** 1-2天（如果你完全零基础可能需要更长，但AI岗问Java不会太深）
**面试杀伤力：** ⭐⭐⭐ 对AI岗来说是加分项，能体现出后端功底
