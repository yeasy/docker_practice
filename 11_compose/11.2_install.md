## 11.2 安装与卸载

`Compose` 是 Docker 官方的开源项目，负责实现本地或单机多容器应用的快速编排。跨主机集群编排应使用 Swarm、Kubernetes 或云厂商托管服务。

当前的 Compose 以 `docker compose` 子命令的形式提供。Docker Desktop 在 macOS、Windows 和 Linux 上默认包含它；如果你已经在 Linux 上单独安装了 Docker Engine 和 Docker CLI，也可以再安装 Compose CLI 插件。

### 11.2.1 Linux

在 Linux 上，默认建议通过 Docker 官方软件仓库安装 Compose CLI 插件，这样可以随系统包管理器更新。

Ubuntu / Debian：

```bash
$ sudo apt-get update
$ sudo apt-get install docker-compose-plugin
```

Fedora / CentOS / RHEL 兼容发行版：

```bash
$ sudo dnf install docker-compose-plugin
```

如果是离线环境、需要锁定特定版本，或包管理器暂不覆盖你的架构，可以从 Docker 官方发布页手工安装。手工安装不会自动更新；下载 URL 中的版本号和架构（如 `x86_64`、`aarch64`）需要按目标机器替换。

```bash
$ DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
$ mkdir -p $DOCKER_CONFIG/cli-plugins
$ curl -SL https://github.com/docker/compose/releases/download/v5.1.2/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
$ chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```

### 11.2.2 测试安装

```bash
$ docker compose version
Docker Compose version v5.x.x
```

### 11.2.3 卸载

如果是仓库方式安装，使用包管理器卸载；如果是二进制包方式安装，删除二进制文件即可。

```bash
$ sudo apt-get remove docker-compose-plugin
# 或
$ sudo dnf remove docker-compose-plugin

$ rm $DOCKER_CONFIG/cli-plugins/docker-compose
```
