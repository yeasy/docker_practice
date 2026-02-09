## CMD 容器启动命令

### 什么是 CMD

`CMD` 指令用于指定容器启动时默认执行的命令。它定义了容器的"主进程"。

> **核心概念**：容器的生命周期 = 主进程的生命周期。CMD 指定的命令就是这个主进程。

---

### 语法格式

CMD 有三种格式：

| 格式 | 语法 | 推荐程度 |
|------|------|---------|
| **exec 格式**| `CMD ["可执行文件", "参数1", "参数2"]` | ✅**推荐** |
| **shell 格式** | `CMD 命令 参数1 参数2` | ⚠️ 简单场景 |
| **参数格式** | `CMD ["参数1", "参数2"]` | 配合 ENTRYPOINT |

#### exec 格式（推荐）

具体内容如下：

```docker
CMD ["nginx", "-g", "daemon off;"]
CMD ["python", "app.py"]
CMD ["node", "server.js"]
```

**优点**：
- 直接执行指定程序，是容器的 PID 1
- 正确接收信号（如 SIGTERM）
- 无需 shell 解析

#### shell 格式

具体内容如下：

```docker
CMD echo "Hello World"
CMD nginx -g "daemon off;"
```

**实际执行**：会被包装为 `sh -c`

```docker
## 你写的

CMD echo $HOME

## 实际执行的

CMD ["sh", "-c", "echo $HOME"]
```

**优点**：可以使用环境变量、管道等 shell 特性
**缺点**：主进程是 sh，信号无法正确传递给应用

---

### exec 格式 vs shell 格式

| 特性 | exec 格式 | shell 格式 |
|------|----------|-----------|
| 主进程 | 指定的程序 | `/bin/sh` |
| 信号传递 | ✅ 正确 | ❌ 无法传递 |
| 环境变量 | ❌ 需要 shell 包装 | ✅ 自动解析 |
| 推荐使用 | ✅ 大多数场景 | 需要 shell 特性时 |

#### 信号传递问题示例

具体内容如下：

```docker
## ❌ shell 格式：docker stop 会超时

CMD node server.js
## 实际是 sh -c "node server.js"

## SIGTERM 发给 sh，不会传递给 node

## ✅ exec 格式：docker stop 正常工作

CMD ["node", "server.js"]
## SIGTERM 直接发给 node

具体内容如下：

```

---

### 运行时覆盖 CMD

`docker run` 后的命令会覆盖 Dockerfile 中的 CMD：

```bash
## ubuntu 默认 CMD 是 /bin/bash

$ docker run -it ubuntu        # 进入 bash
$ docker run ubuntu cat /etc/os-release  # 覆盖为 cat 命令
```

```
Dockerfile:              docker run 命令:
CMD ["/bin/bash"]   +    cat /etc/os-release
        │                        │
        └───────► 被覆盖 ◄───────┘
                    ↓
           执行: cat /etc/os-release
```

---

### 经典错误：容器立即退出

#### 错误示例

具体内容如下：

```docker
## ❌ 容器启动后立即退出

CMD service nginx start
```

#### 原因分析

具体内容如下：

```
1. CMD service nginx start
   ↓ 被转换为
2. CMD ["sh", "-c", "service nginx start"]
   ↓
3. sh 启动，执行 service 命令
   ↓
4. service 命令将 nginx 放到后台
   ↓
5. service 命令结束，sh 退出
   ↓
6. 容器主进程（sh）退出 → 容器停止
```

#### 正确做法

具体内容如下：

```docker
## ✅ 让 nginx 在前台运行

CMD ["nginx", "-g", "daemon off;"]
```

---

### CMD vs ENTRYPOINT

| 指令 | 用途 | 运行时行为 |
|------|------|-----------|
| **CMD**| 默认命令 | `docker run` 参数会**覆盖**它 |
| **ENTRYPOINT**| 入口点 | `docker run` 参数会**追加**到它后面 |

#### 单独使用 CMD

具体内容如下：

```docker
## Dockerfile

CMD ["curl", "-s", "http://example.com"]
```

```bash
$ docker run myimage              # 执行默认命令
$ docker run myimage curl -v ...  # 完全覆盖
```

#### 搭配 ENTRYPOINT

具体内容如下：

```docker
## Dockerfile

ENTRYPOINT ["curl", "-s"]
CMD ["http://example.com"]
```

```bash
$ docker run myimage              # curl -s http://example.com
$ docker run myimage http://other.com  # curl -s http://other.com（参数覆盖）
```

详见 [ENTRYPOINT 入口点](entrypoint.md) 章节。

---

### 最佳实践

#### 1. 优先使用 exec 格式

具体内容如下：

```docker
## ✅ 推荐

CMD ["python", "app.py"]

## ⚠️ 仅在需要 shell 特性时使用

CMD ["sh", "-c", "echo $PATH && python app.py"]
```

#### 2. 确保应用在前台运行

具体内容如下：

```docker
## ✅ 前台运行

CMD ["nginx", "-g", "daemon off;"]
CMD ["apache2ctl", "-D", "FOREGROUND"]
CMD ["java", "-jar", "app.jar"]

## ❌ 不要使用后台服务命令

CMD service nginx start
CMD systemctl start nginx
```

#### 3. 使用双引号

具体内容如下：

```docker
## ✅ 正确：双引号

CMD ["node", "server.js"]

## ❌ 错误：单引号（JSON 不支持）

CMD ['node', 'server.js']
```

#### 4. 配合 ENTRYPOINT 使用

具体内容如下：

```docker
## 用于可配置参数的场景

ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8080"]

## 运行时可以覆盖端口

$ docker run myapp --port 9000
```

---

### 常见问题

#### Q: CMD 可以写多个吗？

不可以。多个 CMD 只有最后一个生效：

```docker
CMD ["echo", "first"]
CMD ["echo", "second"]  # 只有这个生效
```

#### Q: 如何在 CMD 中使用环境变量？

具体内容如下：

```docker
## 方法1：使用 shell 格式

CMD echo "Port is $PORT"

## 方法2：显式使用 sh -c

CMD ["sh", "-c", "echo Port is $PORT"]
```

#### Q: 为什么我的容器不响应 Ctrl+C？

可能是使用了 shell 格式，信号被 sh 吃掉了：

```docker
## ❌ 信号无法传递

CMD python app.py

## ✅ 信号正确传递

CMD ["python", "app.py"]
```

---

### 本章小结

| 要点 | 说明 |
|------|------|
| **作用** | 指定容器启动时的默认命令 |
| **推荐格式** | exec 格式 `CMD ["程序", "参数"]` |
| **覆盖方式** | `docker run image 新命令` |
| **与 ENTRYPOINT** | CMD 作为 ENTRYPOINT 的默认参数 |
| **核心原则** | 应用必须在前台运行 |

### 延伸阅读

- [ENTRYPOINT 入口点](entrypoint.md)：固定的启动命令
- [后台运行](../../05_container/5.2_daemon.md)：容器前台/后台概念
- [最佳实践](../../15_appendix/15.1_best_practices.md)：Dockerfile 编写指南
