# 第七章 Dockerfile 指令详解

## 什么是 Dockerfile

Dockerfile 是一个文本文件，其内包含了一条条的 **指令 (Instruction)**，每一条指令构建一层，因此每一条指令的内容，就是描述该层应当如何构建。

在[第四章](../04_image/README.md)中，我们通过 `docker commit` 学习了镜像的构成。但是，手动 `commit` 只能作为临时修补，并不适合作为生产环境镜像的构建方式。

使用 Dockerfile 构建镜像有以下优势：

*   **自动化**：可以通过 `docker build` 命令自动构建镜像。
*   **可重复性**：由于 Dockerfile 是文本文件，可以确保每次构建的结果一致。
*   **版本控制**：Dockerfile 可以纳入版本控制系统 (如 Git)，便于追踪变更。
*   **透明性**：任何人都可以通过阅读 Dockerfile 了解镜像的构建过程。

## Dockerfile 编写哲学

在深入每个指令的细节之前，笔者想强调一个至关重要的原则：**Dockerfile 不是脚本，而是镜像的“设计图”**。这个区别决定了你如何思考每条指令的作用。

相比编写 Bash 脚本的思维（“按顺序执行这些命令”），Dockerfile 的思维应该是（“这一层镜像应该如何构建，下一层如何分层”）。这个思维转变会影响你的决策：

- **合并命令**：一个 `RUN apt-get update && apt-get install ...` 应该写在一起，而不是分开成多个 `RUN` 指令，因为它们是同一个“层”的逻辑
- **选择合适的指令**：`COPY` vs `ADD`、`CMD` vs `ENTRYPOINT` 这些选择不是随意的，而是根据镜像分层的语义来决定的
- **优化镜像大小**：最后才清理缓存、删除临时文件，让这些“瘦身”操作在同一层完成

这个章节将详细介绍各个指令。在学习指令语法时，请始终思考：“这个指令为什么要以这样的方式工作？如果我是 Docker，我应该如何设计它？”

## Dockerfile 基本结构

Dockerfile 一般分为四部分：基础镜像信息、维护者信息、镜像操作指令和容器启动时执行指令。

### 指令详解

本章将详细讲解 Dockerfile 中的各个指令：

*   [RUN 执行命令](7.1_run.md)
*   [COPY 复制文件](7.2_copy.md)
*   [ADD 更高级的复制文件](7.3_add.md)
*   [CMD 容器启动命令](7.4_cmd.md)
*   [ENTRYPOINT 入口点](7.5_entrypoint.md)
*   [ENV 设置环境变量](7.6_env.md)
*   [ARG 构建参数](7.7_arg.md)
*   [VOLUME 定义匿名卷](7.8_volume.md)
*   [EXPOSE 暴露端口](7.9_expose.md)
*   [WORKDIR 指定工作目录](7.10_workdir.md)
*   [USER 指定当前用户](7.11_user.md)
*   [HEALTHCHECK 健康检查](7.12_healthcheck.md)
*   [ONBUILD 为他人作嫁衣裳](7.13_onbuild.md)
*   [LABEL 为镜像添加元数据](7.14_label.md)
*   [SHELL 指令](7.15_shell.md)

### 高级特性

本章还将介绍 Dockerfile 的高级特性：

*   [多阶段构建](7.17_multistage_builds.md)
*   [多阶段构建实战：Laravel 应用](7.18_multistage_builds_laravel.md)

### 参考与最佳实践

此外，我们还将介绍 Dockerfile 的最佳实践和常见问题。

*   [参考文档](7.16_references.md)

## 使用 Dockerfile 构建镜像

构建镜像的基本命令格式为：

```bash
docker build [选项] <上下文路径/URL/->
```
例如，在 Dockerfile 所在目录执行：

```bash
docker build -t my-image:1.0 .
```

### 关于版本号最佳实践

本章中的 Dockerfile 示例使用的基础镜像标签遵循以下原则：

- **通用标签**（如 `ubuntu:24.04`、`alpine`、`nginx`）：保持原样，无需修改
- **基础镜像版本号**（如 `node:20`、`python:3.12`）：使用主或次版本号而非完整版本号（patch），这样可以自动获取最新的补丁版本，确保获得安全更新
- **避免**：不建议使用 `latest` 标签和完整的 patch 版本号（如 `20.10.0`）作为基础镜像，因为这会导致构建的不可重现性或安全风险

读者在使用这些示例时，应根据实际生产环境需求选择合适的版本号。

更多关于 `docker build` 的用法，我们在实战中会结合具体指令进行演示。
