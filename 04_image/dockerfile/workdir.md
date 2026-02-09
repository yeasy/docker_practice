## WORKDIR 指定工作目录

### 基本语法

具体内容如下：

```docker
WORKDIR <工作目录路径>
```

`WORKDIR` 指定后续指令的工作目录。如果目录不存在，Docker 会自动创建。

---

### 基本用法

具体内容如下：

```docker
WORKDIR /app

RUN pwd          # 输出 /app
RUN echo "hello" > world.txt    # 创建 /app/world.txt
COPY . .         # 复制到 /app/
```

---

### 为什么需要 WORKDIR

#### 常见错误

具体内容如下：

```docker
## ❌ 错误：cd 在下一个 RUN 中无效

RUN cd /app
RUN echo "hello" > world.txt    # 文件在根目录！
```

#### 原因分析

具体内容如下：

```
RUN cd /app
    ↓
启动容器 → cd /app（仅内存变化）→ 提交镜像层 → 容器销毁
                                   │
                                   ↓ 工作目录未改变！
RUN echo "hello" > world.txt
    ↓
启动新容器（工作目录在 /）→ 创建 /world.txt
```

每个 RUN 都在新容器中执行，**前一个 RUN 的内存状态（包括工作目录）不会保留**。

#### 正确做法

具体内容如下：

```docker
## ✅ 正确：使用 WORKDIR

WORKDIR /app
RUN echo "hello" > world.txt    # 创建 /app/world.txt
```

---

### 相对路径

WORKDIR 支持相对路径，基于上一个 WORKDIR：

```docker
WORKDIR /a
WORKDIR b
WORKDIR c

RUN pwd    # 输出 /a/b/c
```

---

### 使用环境变量

具体内容如下：

```docker
ENV APP_HOME=/app
WORKDIR $APP_HOME

RUN pwd    # 输出 /app
```

---

### 多阶段构建中的 WORKDIR

具体内容如下：

```docker
## 构建阶段

FROM node:20 AS builder
WORKDIR /build
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

## 生产阶段

FROM nginx:alpine
WORKDIR /usr/share/nginx/html
COPY --from=builder /build/dist .
```

---

### 最佳实践

#### 1. 尽早设置 WORKDIR

具体内容如下：

```docker
FROM node:20
WORKDIR /app    # 尽早设置

COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "server.js"]
```

#### 2. 使用绝对路径

具体内容如下：

```docker
## ✅ 推荐：绝对路径，意图明确

WORKDIR /app

## ⚠️ 避免：相对路径可能造成混淆

WORKDIR app
```

#### 3. 不要用 RUN cd

具体内容如下：

```docker
## ❌ 避免

RUN cd /app && echo "hello" > world.txt

## ✅ 推荐

WORKDIR /app
RUN echo "hello" > world.txt
```

#### 4. 适时重置 WORKDIR

具体内容如下：

```docker
WORKDIR /app
## ... 应用相关操作 ...

WORKDIR /data
## ... 数据相关操作 ...

具体内容如下：

```

---

### 与其他指令的关系

| 指令 | WORKDIR 的影响 |
|------|---------------|
| `RUN` | 在 WORKDIR 中执行命令 |
| `CMD` | 在 WORKDIR 中启动 |
| `ENTRYPOINT` | 在 WORKDIR 中启动 |
| `COPY` | 相对目标路径基于 WORKDIR |
| `ADD` | 相对目标路径基于 WORKDIR |

```docker
WORKDIR /app

RUN pwd                    # /app
COPY . .                   # 复制到 /app
CMD ["./start.sh"]         # /app/start.sh
```

---

### 运行时覆盖

使用 `-w` 参数覆盖工作目录：

```bash
$ docker run -w /tmp myimage pwd
/tmp
```

---

### 本章小结

| 要点 | 说明 |
|------|------|
| **作用** | 设置后续指令的工作目录 |
| **语法** | `WORKDIR /path` |
| **自动创建** | 目录不存在会自动创建 |
| **持久性** | 影响后续所有指令，直到下次 WORKDIR |
| **不要用** | `RUN cd /path`（无效） |

### 延伸阅读

- [COPY 复制文件](copy.md)：文件复制
- [RUN 执行命令](../../04_image/4.5_build.md)：执行构建命令
- [最佳实践](../../15_appendix/15.1_best_practices.md)：Dockerfile 编写指南
