# [CentOS](https://hub.docker.com/_/centos)

## 基本信息

[CentOS](https://en.wikipedia.org/wiki/CentOS) 是流行的 Linux 发行版，其软件包大多跟 RedHat 系列保持一致。

> ⚠️ **重要提示**：CentOS 8 已于 2021 年 12 月 31 日停止维护（EOL），CentOS 7 将于 2024 年 6 月 30 日结束支持。Docker Hub 上的 CentOS 官方镜像**已停止更新**。
>
> 对于新项目，建议使用以下替代方案：
> - [Rocky Linux](https://hub.docker.com/_/rockylinux)：CentOS 创始人发起的社区驱动项目
> - [AlmaLinux](https://hub.docker.com/_/almalinux)：由 CloudLinux 支持的企业级发行版
> - [CentOS Stream](https://hub.docker.com/r/centos/centos)：RHEL 的上游开发分支

该仓库位于 `https://hub.docker.com/_/centos`，提供了 CentOS 从 5 ~ 8 各个版本的镜像（仅供参考，不再更新）。

## 使用方法

使用 Rocky Linux 替代（推荐）：

```bash
$ docker run --name rocky -it rockylinux:9 bash
```

使用旧版 CentOS 7（仅用于遗留系统）：

```bash
$ docker run --name centos -it centos:7 bash
```

## Dockerfile

请到 https://github.com/docker-library/docs/tree/master/centos 查看。
