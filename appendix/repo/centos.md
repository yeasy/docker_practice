## CentOS

### 基本信息

[CentOS](https://en.wikipedia.org/wiki/CentOS) 是流行的 Linux 发行版，其软件包大多跟 RedHat 系列保持一致。

> ⚠️ **重要提示**：CentOS 8 已于 2021 年 12 月 31 日停止维护 (EOL)，CentOS 7 也已于 2024 年 6 月 30 日 **完全结束支持**。Docker Hub 上的 CentOS 官方镜像 **已停止更新** 且存在未修复的安全漏洞。
>
> 2026 年了，对于任何新项目，**强烈建议** 使用以下生产级替代方案：
> - [Rocky Linux](https://hub.docker.com/_/rockylinux)：CentOS 原创始人发起的社区驱动项目，目前主流为 Rocky Linux 9。
> - [AlmaLinux](https://hub.docker.com/_/almalinux)：由 CloudLinux 支持的企业级发行版，提供长期支持。
> - [CentOS Stream](https://hub.docker.com/r/centos/centos)：RHEL 的上游开发分支 (适合开发测试，不建议用于生产环境)。

该仓库位于 `https://hub.docker.com/_/centos`，提供了 CentOS 从 5 ~ 8 各个版本的镜像 (仅作为历史归档，不再更新)。

### 使用方法

使用 Rocky Linux 9 替代 (**推荐**)：

```bash
$ docker run --name rocky -it rockylinux:9 bash
```

使用旧版 CentOS 7 (**仅用于维护旧项目，不推荐**)：

```bash
$ docker run --name centos -it centos:7 bash
```

### Dockerfile

请到 https://github.com/docker-library/docs/tree/master/centos 查看。
