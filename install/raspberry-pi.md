## 树莓派卡片电脑安装 Docker CE

>警告：切勿在没有配置 Docker APT 源的情况下直接使用 apt 命令安装 Docker.

### 系统要求

Docker CE 不仅支持 `x86_64` 架构的计算机，同时也支持 `ARM` 架构的计算机，本小节内容以树莓派单片电脑为例讲解 `ARM` 架构安装 Docker CE。

Docker CE 支持以下版本的 [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) 操作系统：

* Raspbian Stretch

* Raspbian Jessie

*注：* `Raspbian` 是树莓派基金会为树莓派卡片电脑设计的 Linux 发行版，其基于 Debian。

### 使用 APT 安装

由于 apt 源使用 HTTPS 以确保软件下载过程中不被篡改。因此，我们首先需要添加使用 HTTPS 传输的软件包以及 CA 证书。

```bash
$ sudo apt-get update

$ sudo apt-get install \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg2 \
     lsb-release \
     software-properties-common
```

鉴于国内网络问题，强烈建议使用国内源，官方源请在注释中查看。

为了确认所下载软件包的合法性，需要添加软件源的 GPG 密钥。

```bash
$ curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/raspbian/gpg | sudo apt-key add -


# 官方源
# $ curl -fsSL https://download.docker.com/linux/raspbian/gpg | sudo apt-key add -
```

然后，我们需要向 `source.list` 中添加 Docker CE 软件源：

```bash
$ sudo add-apt-repository \
    "deb [arch=armhf] https://mirrors.ustc.edu.cn/docker-ce/linux/raspbian \
    $(lsb_release -cs) \
    stable"


# 官方源
# $ sudo add-apt-repository \
#    "deb [arch=armhf] https://download.docker.com/linux/raspbian \
#    $(lsb_release -cs) \
#    stable"    
```

>以上命令会添加稳定版本的 Docker CE APT 源，如果需要最新版本的 Docker CE 请将 stable 改为 edge 或者 test。从 Docker 17.06 开始，edge test 版本的 APT 源也会包含稳定版本的 Docker CE。

#### 安装 Docker CE

更新 apt 软件包缓存，并安装 `docker-ce`。

```bash
$ sudo apt-get update

$ sudo apt-get install docker-ce
```

### 使用脚本自动安装

在测试或开发环境中 Docker 官方为了简化安装流程，提供了一套便捷的安装脚本，Raspbian 系统上可以使用这套脚本安装：

```bash
$ curl -fsSL get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh --mirror Aliyun
```

执行这个命令后，脚本就会自动的将一切准备工作做好，并且把 Docker CE 的 Edge 版本安装在系统中。

### 启动 Docker CE

```bash
$ sudo systemctl enable docker
$ sudo systemctl start docker
```

### 建立 docker 用户组

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

### 测试 Docker 是否安装正确

```bash
$ docker run arm32v7/hello-world

Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
ca4f61b1923c: Pull complete
Digest: sha256:be0cd392e45be79ffeffa6b05338b98ebb16c87b255f48e297ec7f98e123905c
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
 https://cloud.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/
```

若能正常输出以上信息，则说明安装成功。

*注意：* ARM 平台不能使用 `x86` 镜像，查看 Raspbian 可使用镜像请访问 [arm32v7](https://hub.docker.com/u/arm32v7/)。

### 镜像加速

鉴于国内网络问题，后续拉取 Docker 镜像十分缓慢，强烈建议安装 Docker 之后配置 [国内镜像加速](mirror.md)。
