# Fedora 安装 Docker CE

>警告：切勿在没有配置 Docker dnf 源的情况下直接使用 dnf 命令安装 Docker.

## 准备工作

### 系统要求

Docker CE 支持以下版本的 [Fedora](https://getfedora.org/) 操作系统：

* 30
* 31

### 卸载旧版本

旧版本的 Docker 称为 `docker` 或者 `docker-engine`，使用以下命令卸载旧版本：

```bash
$ sudo dnf remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
```

## 使用 dnf 安装

执行以下命令安装依赖包：

```bash
$ sudo dnf -y install dnf-plugins-core
```

鉴于国内网络问题，强烈建议使用国内源，官方源请在注释中查看。

执行下面的命令添加 `dnf` 软件源：

```bash
$ sudo dnf config-manager \
    --add-repo \
    https://mirrors.ustc.edu.cn/docker-ce/linux/fedora/docker-ce.repo

$ sudo sed -i 's/download.docker.com/mirrors.ustc.edu.cn\/docker-ce/g' /etc/yum.repos.d/docker-ce.repo

# 官方源
# $ sudo dnf config-manager \
#    --add-repo \
#    https://download.docker.com/linux/fedora/docker-ce.repo
```

如果需要测试版本的 Docker CE 请使用以下命令：

```bash
$ sudo dnf config-manager --set-enabled docker-ce-test
```

你也可以禁用测试版本的 Docker CE

```bash
$ sudo dnf config-manager --set-disabled docker-ce-test
```

### 安装 Docker CE

更新 `dnf` 软件源缓存，并安装 `docker-ce`。

```bash
$ sudo dnf update
$ sudo dnf install docker-ce
```

你也可以使用以下命令安装指定版本的 Docker

```bash
$ dnf list docker-ce  --showduplicates | sort -r

docker-ce.x86_64          18.06.1.ce-3.fc28                     docker-ce-stable

$ sudo dnf -y install docker-ce-18.06.1.ce
```

由于 Fedora 31 默认启用了 **Cgroupv2**，暂时 Docker 与 Cgroupv2 不兼容，请执行以下命令切换到 **Cgroupv1** 并重启计算机:

```bash
$ sudo grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=0"
```

## 使用脚本自动安装

在测试或开发环境中 Docker 官方为了简化安装流程，提供了一套便捷的安装脚本，Debian 系统上可以使用这套脚本安装，另外可以通过 `--mirror` 选项使用国内源进行安装：

```bash
$ curl -fsSL get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh --mirror Aliyun
# $ sudo sh get-docker.sh --mirror AzureChinaCloud
```

执行这个命令后，脚本就会自动的将一切准备工作做好，并且把 Docker CE 最新稳定(stable)版本安装在系统中。

## 启动 Docker CE

```bash
$ sudo systemctl enable docker
$ sudo systemctl start docker
```

## 建立 docker 用户组

默认情况下，`docker` 命令会使用 [Unix socket](https://en.wikipedia.org/wiki/Unix_domain_socket) 与 Docker 引擎通讯。而只有 `root` 用户和 `docker` 组的用户才可以访问 Docker 引擎的 Unix socket。出于安全考虑，一般 Linux 系统上不会直接使用 `root` 用户。因此，更好地做法是将需要使用 `docker` 的用户加入 `docker` 用户组。

建立 `docker` 组：

```bash
$ sudo groupadd docker
```

将当前用户加入 `docker` 组：

```bash
$ sudo usermod -aG docker $USER
```

退出当前终端并重新登录，进行如下测试。

## 测试 Docker 是否安装正确

```bash
$ docker run hello-world

Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
d1725b59e92d: Pull complete
Digest: sha256:0add3ace90ecb4adbf7777e9aacf18357296e799f81cabc9fde470971e499788
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

若能正常输出以上信息，则说明安装成功。

## 镜像加速

如果在使用过程中发现拉取 Docker 镜像十分缓慢，可以配置 Docker [国内镜像加速](mirror.md)。

## 参考文档

* [Docker 官方 Fedora 安装文档](https://docs.docker.com/install/linux/docker-ce/fedora)。
