## 本章小结

| 要点 | 说明 |
|------|------|
| **作用** | 设置后续指令的工作目录 |
| **语法** | `WORKDIR /path` |
| **自动创建** | 目录不存在会自动创建 |
| **持久性** | 影响后续所有指令，直到下次 WORKDIR |
| **不要用** | `RUN cd /path`（无效） |

### 延伸阅读

- [COPY 复制文件](7.2_copy.md)：文件复制
- [RUN 执行命令](../04_image/4.5_build.md)：执行构建命令
- [最佳实践](../16_appendix/16.1_best_practices.md)：Dockerfile 编写指南

| 要点 | 说明 |
|------|------|
| **作用** | 切换后续指令的执行用户 |
| **语法** | `USER username` 或 `USER UID:GID` |
| **前提** | 用户必须已存在 |
| **运行时覆盖** | `docker run -u` |
| **切换工具** | 使用 gosu，不用 su/sudo |

### 延伸阅读

- [安全](../11_ops/security/README.md)：容器安全实践
- [ENTRYPOINT](7.5_entrypoint.md)：入口脚本中的用户切换
- [最佳实践](../16_appendix/16.1_best_practices.md)：Dockerfile 安全

| 要点 | 说明 |
|------|------|
| **作用** | 检测容器应用是否真实可用 |
| **命令** | `HEALTHCHECK [选项] CMD command` |
| **状态** | starting, healthy, unhealthy |
| **Compose** | 支持 `condition: service_healthy` 依赖 |
| **注意** | 避免副作用，节省资源 |

### 延伸阅读

- [CMD 容器启动命令](7.4_cmd.md)：启动主进程
- [Compose 模板文件](../10_compose/10.5_compose_file.md)：Compose 中的健康检查
- [Docker 调试](../16_appendix/16.2_debug.md)：容器排障

| 要点 | 说明 |
|------|------|
| **作用** | 定义在子镜像构建时执行的指令 |
| **语法** | `ONBUILD INSTRUCTION` |
| **适用** | 基础架构镜像（Node, Python, Go 等） |
| **限制** | 只继承一次，不可级联 |
| **规范** | 建议使用 `-onbuild` 标签后缀 |

### 延伸阅读

- [COPY 指令](7.2_copy.md)：文件复制
- [Dockerfile 最佳实践](../16_appendix/16.1_best_practices.md)：基础镜像设计

| 要点 | 说明 |
|------|------|
| **作用** | 添加 key-value 元数据 |
| **语法** | `LABEL k=v k=v ...` |
| **规范** | 推荐使用 OCI 标准标签 |
| **弃用** | 不要再使用 `MAINTAINER` |
| **查看** | `docker inspect` |

### 延伸阅读

- [OCI 标签规范](https://github.com/opencontainers/image-spec/blob/main/annotations.md)
- [Dockerfile 最佳实践](../16_appendix/16.1_best_practices.md)

| 要点 | 说明 |
|------|------|
| **作用** | 更改 RUN/CMD/ENTRYPOINT 的默认 shell |
| **Linux 默认** | `["/bin/sh", "-c"]` |
| **Windows 默认** | `["cmd", "/S", "/C"]` |
| **推荐用法** | `SHELL ["/bin/bash", "-o", "pipefail", "-c"]` |
| **影响范围** | 后续所有使用 shell 格式的指令 |

### 延伸阅读

- [RUN 指令](../04_image/4.5_build.md)：执行命令
- [Dockerfile 最佳实践](../16_appendix/16.1_best_practices.md)：错误处理与调试

| 要点 | 说明 |
|------|------|
| **作用** | 在新层执行命令 |
| **原则** | 合并命令，清理缓存 |
| **格式** | Shell (常用) vs Exec |
| **陷阱** | `cd` 不持久，环境变量不持久 |
| **进阶** | 使用 Cache Mount 加速构建 |

### 延伸阅读

- [CMD 容器启动命令](7.4_cmd.md)：容器启动时的命令
- [WORKDIR 指定工作目录](7.10_workdir.md)：改变目录
- [Dockerfile 最佳实践](../16_appendix/16.1_best_practices.md)

| 操作 | 示例 |
|------|------|
| 复制文件 | `COPY app.js /app/` |
| 复制多个文件 | `COPY *.json /app/` |
| 复制目录内容 | `COPY src/ /app/src/` |
| 修改所有者 | `COPY --chown=node:node . /app/` |
| 从构建阶段复制 | `COPY --from=builder /app/dist ./` |

### 延伸阅读

- [ADD 指令](7.3_add.md)：复制和解压
- [WORKDIR 指令](7.10_workdir.md)：设置工作目录
- [多阶段构建](7.17_multistage_builds.md)：优化镜像大小
- [最佳实践](../16_appendix/16.1_best_practices.md)：Dockerfile 编写指南

| 场景 | 推荐指令 |
|------|---------|
| 复制普通文件 | `COPY` |
| 复制目录 | `COPY` |
| 自动解压 tar | `ADD` |
| 从 URL 下载 | `RUN curl` |
| 保持 tar 不解压 | `COPY` |

### 延伸阅读

- [COPY 复制文件](7.2_copy.md)：基本复制操作
- [多阶段构建](7.17_multistage_builds.md)：减少镜像体积
- [最佳实践](../16_appendix/16.1_best_practices.md)：Dockerfile 编写指南

| 要点 | 说明 |
|------|------|
| **作用** | 指定容器启动时的默认命令 |
| **推荐格式** | exec 格式 `CMD ["程序", "参数"]` |
| **覆盖方式** | `docker run image 新命令` |
| **与 ENTRYPOINT** | CMD 作为 ENTRYPOINT 的默认参数 |
| **核心原则** | 应用必须在前台运行 |

### 延伸阅读

- [ENTRYPOINT 入口点](7.5_entrypoint.md)：固定的启动命令
- [后台运行](../05_container/5.2_daemon.md)：容器前台/后台概念
- [最佳实践](../16_appendix/16.1_best_practices.md)：Dockerfile 编写指南

| ENTRYPOINT | CMD | 适用场景 |
|------------|-----|---------|
| ✓ | ✗ | 镜像作为固定命令使用 |
| ✗ | ✓ | 简单的默认命令 |
| ✓ | ✓ | **推荐**：固定命令 + 可配置参数 |

### 延伸阅读

- [CMD 容器启动命令](7.4_cmd.md)：默认命令
- [最佳实践](../16_appendix/16.1_best_practices.md)：启动命令设计
- [后台运行](../05_container/5.2_daemon.md)：前台/后台概念

| 要点 | 说明 |
|------|------|
| **语法** | `ENV KEY=value` |
| **作用范围** | 构建时 + 运行时 |
| **覆盖方式** | `docker run -e KEY=value` |
| **与 ARG** | ARG 仅构建时，ENV 持久化到运行时 |
| **安全** | 不要存储敏感信息 |

### 延伸阅读

- [ARG 构建参数](7.7_arg.md)：构建时变量
- [Compose 环境变量](../10_compose/10.5_compose_file.md)：Compose 中的环境变量
- [最佳实践](../16_appendix/16.1_best_practices.md)：Dockerfile 编写指南

| 要点 | 说明 |
|------|------|
| **作用** | 定义构建时变量 |
| **语法** | `ARG NAME=value` |
| **覆盖** | `docker build --build-arg NAME=value` |
| **作用域** | FROM 之后需要重新声明 |
| **vs ENV** | ARG 仅构建时，ENV 构建+运行时 |
| **安全** | 不要存储敏感信息 |

### 延伸阅读

- [ENV 设置环境变量](7.6_env.md)：运行时环境变量
- [FROM 指令](../04_image/4.5_build.md)：基础镜像指定
- [多阶段构建](7.17_multistage_builds.md)：复杂构建场景

| 要点 | 说明 |
|------|------|
| **作用** | 创建挂载点，标记为外部卷 |
| **语法** | `VOLUME /path` |
| **默认行为** | 自动创建匿名卷 |
| **覆盖方式** | `docker run -v name:/path` |
| **注意** | VOLUME 之后的修改会丢失 |

### 延伸阅读

- [数据卷](../08_data_network/data/volume.md)：卷的管理和使用
- [挂载主机目录](../08_data_network/data/bind-mounts.md)：Bind Mount
- [Compose 数据管理](../10_compose/10.5_compose_file.md)：Compose 中的卷配置

| 要点 | 说明 |
|------|------|
| **作用** | 声明容器提供服务的端口（文档） |
| **不会** | 自动映射端口或开放外部访问 |
| **配合** | `docker run -P` 自动映射 |
| **外部访问** | 需要 `-p 宿主机端口:容器端口` |
| **语法** | `EXPOSE 80` 或 `EXPOSE 80/tcp` |

### 延伸阅读

- [网络配置](../08_data_network/network/README.md)：Docker 网络详解
- [端口映射](../08_data_network/network/port_mapping.md)：-p 参数详解
- [Compose 端口](../10_compose/10.5_compose_file.md)：Compose 中的端口配置
