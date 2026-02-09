## ARG 构建参数

### 基本语法

具体内容如下：

```docker
ARG <参数名>[=<默认值>]
```

`ARG` 指令定义构建时的变量，可以在 `docker build` 时通过 `--build-arg` 传入。

---

### ARG vs ENV

| 特性 | ARG | ENV |
|------|-----|-----|
| **生效时间** | 仅构建时 | 构建时 + 运行时 |
| **持久性** | 构建后消失 | 写入镜像 |
| **覆盖方式** | `docker build --build-arg` | `docker run -e` |
| **适用场景** | 构建参数（版本号等） | 应用配置 |
| **可见性** | `docker history` 可见 | `docker inspect` 可见 |

```
构建时                         运行时
├─ ARG VERSION=1.0             │ （ARG 已消失）
├─ ENV APP_ENV=prod            │ APP_ENV=prod（仍存在）
└─ RUN echo $VERSION           │
```

> ⚠️ **安全提示**：不要用 ARG 传递密码等敏感信息，`docker history` 可以查看所有 ARG 值。

---

### 基本用法

#### 定义和使用

具体内容如下：

```docker
## 定义有默认值的 ARG

ARG NODE_VERSION=20

## 使用 ARG

FROM node:${NODE_VERSION}-alpine
RUN echo "Using Node.js $NODE_VERSION"
```

#### 构建时覆盖

运行以下命令：

```bash
## 使用默认值

$ docker build -t myapp .

## 覆盖默认值

$ docker build --build-arg NODE_VERSION=18 -t myapp .
```

---

### ARG 的作用域

#### FROM 之前的 ARG

具体内容如下：

```docker
## FROM 之前的 ARG 只能用于 FROM 指令

ARG REGISTRY=docker.io
ARG IMAGE_NAME=node

FROM ${REGISTRY}/${IMAGE_NAME}:20

## ❌ 这里无法使用上面的 ARG

RUN echo $REGISTRY  # 输出空
```

#### FROM 之后重新声明

具体内容如下：

```docker
ARG NODE_VERSION=20

FROM node:${NODE_VERSION}-alpine

## 需要再次声明才能使用

ARG NODE_VERSION
RUN echo "Node version: $NODE_VERSION"
```

#### 多阶段构建中的 ARG

具体内容如下：

```docker
ARG BASE_VERSION=alpine

FROM node:20-${BASE_VERSION} AS builder
## 需要重新声明

ARG NODE_VERSION=20
RUN echo "Building with Node $NODE_VERSION"

FROM node:20-${BASE_VERSION}
## 每个阶段都需要重新声明

ARG NODE_VERSION=20
RUN echo "Running with Node $NODE_VERSION"
```

---

### 常见使用场景

#### 1. 控制基础镜像版本

具体内容如下：

```docker
ARG ALPINE_VERSION=3.19
FROM alpine:${ALPINE_VERSION}
```

```bash
$ docker build --build-arg ALPINE_VERSION=3.18 .
```

#### 2. 设置软件版本

具体内容如下：

```docker
ARG NGINX_VERSION=1.25.0

RUN curl -fsSL https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz | tar -xz
```

#### 3. 配置构建环境

具体内容如下：

```docker
ARG BUILD_ENV=production
ARG ENABLE_DEBUG=false

RUN if [ "$ENABLE_DEBUG" = "true" ]; then \
        npm install --include=dev; \
    else \
        npm install --production; \
    fi
```

#### 4. 配置私有仓库

具体内容如下：

```docker
ARG NPM_TOKEN

RUN echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > ~/.npmrc && \
    npm install && \
    rm ~/.npmrc
```

```bash
## 构建时传入 token

$ docker build --build-arg NPM_TOKEN=xxx .
```

---

### 将 ARG 传递给 ENV

如果需要在运行时使用 ARG 的值：

```docker
ARG VERSION=1.0.0

## 将 ARG 传递给 ENV

ENV APP_VERSION=$VERSION

## 运行时可用

CMD echo "App version: $APP_VERSION"
```

---

### 预定义 ARG

Docker 提供了一些预定义的 ARG，无需声明即可使用：

| ARG | 说明 |
|-----|------|
| `HTTP_PROXY` | HTTP 代理 |
| `HTTPS_PROXY` | HTTPS 代理 |
| `NO_PROXY` | 不使用代理的地址 |
| `FTP_PROXY` | FTP 代理 |

```bash
## 构建时使用代理

$ docker build --build-arg HTTP_PROXY=http://proxy:8080 .
```

---

### 最佳实践

#### 1. 为 ARG 提供合理默认值

具体内容如下：

```docker
## ✅ 好：有默认值

ARG NODE_VERSION=20

## ⚠️ 需要每次传入

ARG NODE_VERSION
```

#### 2. 不要用 ARG 存储敏感信息

具体内容如下：

```docker
## ❌ 错误：密码会被记录在镜像历史中

ARG DB_PASSWORD
RUN echo "password=$DB_PASSWORD" > /app/.env

## ✅ 正确：使用 secrets 或运行时环境变量

具体内容如下：

```

#### 3. 使用 ARG 提高构建灵活性

具体内容如下：

```docker
ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}

## 可以构建不同基础镜像的版本

## docker build --build-arg BASE_IMAGE=python:3.11-alpine .

具体内容如下：

```

---

### 本章小结

| 要点 | 说明 |
|------|------|
| **作用** | 定义构建时变量 |
| **语法** | `ARG NAME=value` |
| **覆盖** | `docker build --build-arg NAME=value` |
| **作用域** | FROM 之后需要重新声明 |
| **vs ENV** | ARG 仅构建时，ENV 构建+运行时 |
| **安全** | 不要存储敏感信息 |

### 延伸阅读

- [ENV 设置环境变量](env.md)：运行时环境变量
- [FROM 指令](../../04_image/4.5_build.md)：基础镜像指定
- [多阶段构建](../multistage-builds.md)：复杂构建场景
