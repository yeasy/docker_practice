# 第十一章 Docker Compose

`Docker Compose` 是 Docker 官方编排 (Orchestration) 项目之一，负责快速的部署分布式应用。

> ⚠️ **重要提示：Compose V1 已停止支持**
>
> 早期基于 Python 编写的 Compose V1（命令为 `docker-compose`）已于 2023 年中正式停止支持。现已全面升级为基于 Go 编写的 Compose V2，作为 Docker CLI 的官方插件提供（命令为 `docker compose`，中间为空格）。本书强烈推荐且后续章节均以 V2 为核心标准进行讲解。

## Docker Compose 解决什么问题？

在学习 Compose 之前，笔者想强调它的真正价值。假设你正在开发一个微服务应用——前端、后端、数据库三个服务。如果你用 Docker 容器分别运行它们，你会遇到这些问题：

1. **启动顺序**：需要先启数据库，再启后端，最后启前端
2. **网络连接**：三个容器需要能彼此通信
3. **卷挂载**：本地代码需要映射到容器内
4. **环境变量**：每个服务的配置需要逐个设置

使用 `docker run` 逐个启动的话，需要记住 3 条复杂的命令。而 **Docker Compose 的核心价值就是用一个 YAML 文件来定义整个应用**，然后一条命令 `docker compose up` 启动所有服务。这是 Compose 被广泛采用的原因——它极大地简化了本地开发和测试的复杂性。

**谁应该学 Compose？** 任何使用 Docker 进行本地开发的人，以及需要快速部署多容器应用的团队。

本章将介绍 `Compose` 项目情况以及安装和使用。

* [简介](11.1_introduction.md)
* [安装与卸载](11.2_install.md)
* [使用](11.3_usage.md)
* [命令说明](11.4_commands.md)
* [Compose 模板文件](11.5_compose_file.md)
* [实战 Django](11.6_django.md)
* [实战 Rails](11.7_rails.md)
* [实战 WordPress](11.8_wordpress.md)
* [实战 LNMP](11.9_lnmp.md)
