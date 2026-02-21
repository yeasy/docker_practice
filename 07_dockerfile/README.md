# 第七章 Dockerfile 指令详解

本节涵盖了相关内容与详细描述，主要探讨以下几个方面：

## 什么是 Dockerfile

Dockerfile 是一个文本文件，其內包含了一条条的**指令 (Instruction)**，每一条指令构建一层，therefore 每一条指令的内容，就是描述该层应当如何构建。

在[第四章](../04_image/README.md)中，我们通过 `docker commit` 学习了镜像的构成。但是，手动 `commit` 只能作为临时修补，并不适合作为生产环境镜像的构建方式。

使用 Dockerfile 构建镜像有以下优势：

*   **自动化**：可以通过 `docker build` 命令自动构建镜像。
*   **可重复性**：由于 Dockerfile 是文本文件，可以确保每次构建的结果一致。
*   **版本控制**：Dockerfile 可以纳入版本控制系统 (如 Git)，便于追踪变更。
*   **透明性**：任何人都可以通过阅读 Dockerfile 了解镜像的构建过程。

## Dockerfile 基本结构

Dockerfile 一般分为四部分：基础镜像信息、维护者信息、镜像操作指令和容器启动时执行指令。

### 概述

总体概述了以下内容。

### 指令详解

本章将详细讲解 Dockerfile 中的各个指令：

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
*   [RUN 执行命令](7.1_run.md)

此外，我们还将介绍 Dockerfile 的最佳实践和常见问题。

*   [参考文档](7.16_references.md)

## 使用 Dockerfile 构建镜像

构建镜像的基本命令格式为：

```bash
docker build [选项] <上下文路径/URL/->
```

例如，在 Dockerfile 所在目录执行：

```bash
docker build -t my-image:v1 .
```

更多关于 `docker build` 的用法，我们在实战中会结合具体指令进行演示。
