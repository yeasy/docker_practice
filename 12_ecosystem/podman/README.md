# podman

[`podman`](https://github.com/containers/podman) 是一个无守护进程、与 Docker 命令高度兼容的下一代 Linux 容器工具。它由 Red Hat 开发，旨在提供一个更安全的容器运行环境。

## Podman vs Docker

| 特性 | Docker | Podman |
| :--- | :--- | :--- |
| **架构** | C/S 架构，依赖守护进程 (`dockerd`) | 无守护进程 (Daemonless) |
| **权限** | 默认需要 root 权限 (虽有 Rootless 模式) | 默认支持 Rootless (非 root 用户运行) |
| **生态** | 完整的生态系统 (Compose, Swarm) | 专注单机容器，配合 Kubernetes 使用 |
| **镜像构建** | `docker build` | `podman build` 或 `buildah` |

## 安装

### CentOS / RHEL

```bash
$ sudo yum -y install podman
```

### macOS

macOS 上需要安装 Podman Desktop 或通过 Homebrew 安装：

```bash
$ brew install podman
$ podman machine init
$ podman machine start
```

## 使用

`podman` 的命令行几乎与 `docker` 完全兼容，大多数情况下，你只需将 `docker` 替换为 `podman` 即可。

### 运行容器

```bash
# $ docker run -d -p 80:80 nginx:alpine

$ podman run -d -p 80:80 nginx:alpine
```

### 列出容器

```bash
$ podman ps
```

### 构建镜像

```bash
$ podman build -t myimage .
```

## Pods 的概念

与 Docker 不同，Podman 支持 "Pod" 的概念（类似于 Kubernetes 的 Pod），允许你在同一个网络命名空间中运行多个容器。

```bash
# 创建一个 Pod
$ podman pod create --name mypod -p 8080:80

# 在 Pod 中运行容器
$ podman run -d --pod mypod --name webbing nginx
```

## 迁移到 Podman

如果你习惯使用 `docker` 命令，可以简单地设置别名：

$ alias docker=podman
```

## 进阶用法

### Systemd 集成

Podman 可以生成 systemd 单元文件，让容器像普通系统服务一样管理。

```bash
# 创建容器
$ podman run -d --name myweb -p 8080:80 nginx

# 生成 systemd 文件
$ podman generate systemd --name myweb --files --new

# 启用并启动服务
$ systemctl --user enable --now container-myweb.service
```

### Podman Compose

虽然 Podman 兼容 Docker Compose，但在某些场景下你可能需要明确使用 `podman-compose`。

```bash
$ pip3 install podman-compose
$ podman-compose up -d
```

## 参考

* [Podman 官方网站](https://podman.io/)
* [Podman GitHub 仓库](https://github.com/containers/podman)
