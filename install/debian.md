## Debian 安装 Docker CE

### 准备工作

#### 系统要求

Docker CE 支持以下版本的 [Debian](https://www.debian.org/intro/about) 操作系统：

* Debian 9 Stretch
* Debian 8 Jessie
* Debian 7 Wheezy

Docker CE 可以安装在 64 位的 x86 平台或 ARM 平台上（如[树莓派](https://www.raspberrypi.org/)）。


#### 卸载旧版本

旧版本的 Docker 称为 `docker` 或者 `docker-engine`，使用以下命令卸载旧版本：

```bash
$ sudo apt-get remove docker docker-engine docker.io
```

#### Debian 7 Wheezy

Debian 7 的内核默认为 3.2，为了满足 Docker CE 的需求，应该安装 [`backports`](https://backports.debian.org/Instructions/) 的内核。

### 使用 APT 源安装

由于官方源使用 HTTPS 以确保软件下载过程中不被篡改。因此，我们首先需要添加使用 HTTPS 传输的软件包以及 CA 证书。

Debian 8 Jessie 或者 Debian 9 Stretch 使用以下命令:

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

Debian 7 Wheezy 使用以下命令：

```bash
$ sudo apt-get update

$ sudo apt-get install \
     apt-transport-https \
     ca-certificates \
     curl \
     lsb-release \
     python-software-properties

```

鉴于国内网络问题，强烈建议使用国内源，下面先介绍国内源的使用。

#### 国内源

为了确认所下载软件包的合法性，需要添加软件源的 GPG 密钥。

```bash
$ curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/debian/gpg | sudo apt-key add -
```

然后，我们需要向 `source.list` 中添加 Docker CE 软件源：

```bash
$ sudo add-apt-repository \
   "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/debian \
   $(lsb_release -cs) \
   stable"
```

>以上命令会添加 稳定 版本的 Docker CE APT 镜像源，如果需要最新版本的 Docker CE 请将 stable 改为 edge 或者 test 。从 Docker 17.06 开始，edge test 版本的 APT 镜像源也会包含稳定版本的 Docker CE

#### 官方源

```bash
$ curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
```

Debian 7 需要进行额外的操作：

编辑 `/etc/apt/sources.list` 将 deb-src 一行删除或者使用 # 注释。

```bash
deb-src [arch=amd64] https://download.docker.com/linux/debian wheezy stable
```

#### 安装 Docker CE

更新 apt 软件包缓存，并安装 `docker-ce`。

```bash
$ sudo apt-get update

$ sudo apt-get install docker-ce
```

### 使用脚本自动安装

在测试或开发环境中 Docker 官方为了简化安装流程，提供了一套便捷的安装脚本，Debian 系统上可以使用这套脚本安装：

```bash
$ curl -fsSL get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh --mirror Aliyun
```

执行这个命令后，脚本就会自动的将一切准备工作做好，并且把 Docker CE 的 edge 版本安装在系统中。

### 树莓派安装 Docker CE

基本和上述步骤相同，添加 apt 源时请使用如下命令：

```bash
$ sudo add-apt-repository \
    "deb [arch=armhf] https://mirrors.aliyun.com/docker-ce/linux/debian \
    $(lsb_release -cs) \
    stable"
```

ARM 平台不能使用 x86 镜像，查看树莓派可使用镜像请访问 [arm32v7](https://hub.docker.com/u/arm32v7/)。

### 启动 Docker CE

```bash
$ sudo systemctl enable docker
$ sudo systemctl start docker
```
Debian 7 Wheezy 请使用以下命令启动

```bash
$ sudo service docker start
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

### 镜像加速

鉴于国内网络问题，后续拉取 Docker 镜像十分缓慢，强烈建议安装 Docker 之后配置 [国内镜像加速](/install/mirror.html)。

### 参考文档

* [Docker 官方 Debian 安装文档](https://docs.docker.com/engine/installation/linux/docker-ce/debian/)
* [阿里云 Docker CE 安装镜像帮助](https://yq.aliyun.com/articles/110806)
