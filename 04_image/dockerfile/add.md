# ADD 更高级的复制文件

## 基本语法

```docker
ADD [选项] <源路径>... <目标路径>
ADD [选项] ["<源路径>", ... "<目标路径>"]
```

`ADD` 在 `COPY` 基础上增加了两个功能：
1. 自动解压 tar 压缩包
2. 支持从 URL 下载文件（不推荐）

---

## ADD vs COPY

| 特性 | COPY | ADD |
|------|------|-----|
| 复制本地文件 | ✅ | ✅ |
| 自动解压 tar | ❌ | ✅ |
| 支持 URL | ❌ | ✅（不推荐） |
| 行为可预测性 | ✅ 高 | ⚠️ 低 |
| 推荐程度 | ✅ **优先使用** | 仅解压场景 |

> 笔者建议：除非需要自动解压 tar 文件，否则始终使用 COPY。明确的行为比隐式的魔法更好。

---

## 自动解压功能

### 基本用法

```docker
# 自动解压 tar.gz 到目标目录
ADD app.tar.gz /app/
```

ADD 会识别并解压以下格式：
- `.tar`
- `.tar.gz` / `.tgz`
- `.tar.bz2` / `.tbz2`
- `.tar.xz` / `.txz`

### 实际应用

官方基础镜像通常使用 ADD 解压根文件系统：

```docker
FROM scratch
ADD ubuntu-noble-core-cloudimg-amd64-root.tar.gz /
```

### 解压过程

```
ADD app.tar.gz /app/
        │
        ├─ 识别 .tar.gz 格式
        ├─ 自动解压
        └─ 内容放入 /app/

app.tar.gz 包含：        /app/ 目录结果：
├── src/                 ├── src/
│   └── main.py          │   └── main.py
└── config.json          └── config.json
```

---

## URL 下载功能（不推荐）

### 基本用法

```docker
# 从 URL 下载文件
ADD https://example.com/app.zip /app/app.zip
```

### 为什么不推荐

| 问题 | 说明 |
|------|------|
| 权限固定 | 下载的文件权限为 600，通常需要额外 RUN 修改 |
| 不会解压 | URL 下载的压缩包不会自动解压 |
| 缓存问题 | URL 内容变化时不会重新下载 |
| 层数增加 | 需要额外 RUN 清理 |

### 推荐替代方案

```docker
# ❌ 不推荐：使用 ADD 下载
ADD https://example.com/app.tar.gz /tmp/
RUN tar -xzf /tmp/app.tar.gz -C /app && rm /tmp/app.tar.gz

# ✅ 推荐：使用 RUN + curl
RUN curl -fsSL https://example.com/app.tar.gz | tar -xz -C /app
```

优势：
- 一条 RUN 完成下载、解压、清理
- 减少镜像层数
- 更清晰的构建意图

---

## 修改文件所有者

```docker
ADD --chown=node:node app.tar.gz /app/
ADD --chown=1000:1000 files/ /app/
```

---

## 何时使用 ADD

### ✅ 适合使用 ADD

```docker
# 解压本地 tar 文件
FROM scratch
ADD rootfs.tar.gz /

# 解压应用包
ADD dist.tar.gz /app/
```

### ❌ 不适合使用 ADD

```docker
# 复制普通文件（用 COPY）
ADD package.json /app/          # ❌
COPY package.json /app/         # ✅

# 下载文件（用 RUN + curl）
ADD https://example.com/file /  # ❌
RUN curl -fsSL ... -o /file     # ✅

# 需要保留 tar 不解压（用 COPY）
ADD archive.tar.gz /archives/   # ❌ 会解压
COPY archive.tar.gz /archives/  # ✅ 保持原样
```

---

## 缓存行为

ADD 可能导致构建缓存失效：

```docker
# 如果 app.tar.gz 内容变化，此层及后续层都需重建
ADD app.tar.gz /app/
RUN npm install
```

**优化建议**：

```docker
# 先复制依赖文件
COPY package*.json /app/
RUN npm install

# 再添加应用代码
ADD app.tar.gz /app/
```

---

## 最佳实践

### 1. 默认使用 COPY

```docker
# ✅ 大多数场景使用 COPY
COPY . /app/
```

### 2. 仅在需要解压时使用 ADD

```docker
# ✅ 自动解压场景
ADD app.tar.gz /app/
```

### 3. 不要用 ADD 下载文件

```docker
# ❌ 避免
ADD https://example.com/file.tar.gz /tmp/

# ✅ 推荐
RUN curl -fsSL https://example.com/file.tar.gz | tar -xz -C /app
```

### 4. 解压后清理

```docker
# 如果需要控制解压过程
COPY app.tar.gz /tmp/
RUN tar -xzf /tmp/app.tar.gz -C /app && \
    rm /tmp/app.tar.gz
```

---

## 本章小结

| 场景 | 推荐指令 |
|------|---------|
| 复制普通文件 | `COPY` |
| 复制目录 | `COPY` |
| 自动解压 tar | `ADD` |
| 从 URL 下载 | `RUN curl` |
| 保持 tar 不解压 | `COPY` |

## 延伸阅读

- [COPY 复制文件](copy.md)：基本复制操作
- [多阶段构建](../multistage-builds.md)：减少镜像体积
- [最佳实践](../../15_appendix/best_practices.md)：Dockerfile 编写指南
