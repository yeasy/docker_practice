## Debian操作系统安装Docker

### 系统要求

Docker 支持以下版本的 [Debian](https://www.debian.org/intro/about) 操作系统：

* Debian testing stretch (64-bit)
* Debian 8 Jessie (64-bit)
* Debian 7 Wheezy (64-bit)（*必须启用 backports*)

Docker 需要安装在 64 位的 x86 平台或 ARM 平台上（如[树莓派](https://www.raspberrypi.org/)），并且要求内核版本不低于 3.10。但实际上内核越新越好，过低的内核版本可能会出现部分功能无法使用，或者不稳定。

用户可以通过如下命令检查自己的内核版本详细信息：

```bash
$ uname -a
Linux debian-512mb-nyc3-01 3.16.0-0.bpo.4-amd64 #1 SMP Debian 3.16.36-1+deb8u2~bpo70+1 (2016-10-19) x86_64 GNU/Linux
```

#### 升级内核

##### Debian 7 Wheezy

Debian 7 的内核默认为 3.2，为了满足 Docker 的需求，应该安装 `backports` 的内核。

执行下面的命令添加 `backports` 源：

```bash
$ echo "deb http://http.debian.net/debian wheezy-backports main" | sudo tee /etc/apt/sources.list.d/backports.list
```

升级到 `backports` 内核：

```bash
$ sudo apt-get update
$ sudo apt-get -t wheezy-backports install linux-image-amd64
```

##### Debian 8 Jessie

Debian 8 的内核默认为 3.16，满足基本的 Docker 运行条件。但是如果打算使用 `overlay2` 存储层驱动，或某些功能不够稳定希望升级到较新版本的内核，可以添加 `backports` 源，升级到新版本的内核。

执行下面的命令添加 `backports` 源：

```bash
$ echo "deb http://http.debian.net/debian jessie-backports main" | sudo tee /etc/apt/sources.list.d/backports.list
```

升级到 `backports` 内核：

```bash
$ sudo apt-get update
$ sudo apt-get -t jessie-backports install linux-image-amd64
```

需要注意的是，升级到 `backports` 的内核之后，会因为 `AUFS` 内核模块不可用，而使用默认的 `devicemapper` 驱动，并且配置为 `loop-lvm`，这是不推荐的。因此，不要忘记安装 Docker 后，配置 `overlay2` 存储层驱动。

##### 配置 GRUB 引导参数

在 Docker 使用期间，或者在 `docker info` 信息中，可能会看到下面的警告信息：

```bash
WARNING: No memory limit support
WARNING: No swap limit support
WARNING: No oom kill disable support
```

如果需要这些功能，就需要修改 GRUB 的配置文件 ` /etc/default/grub`，在 `GRUB_CMDLINE_LINUX` 中添加内核引导参数 `cgroup_enable=memory swapaccount=1`。

然后不要忘记了更新 GRUB，并重启：

```bash
$ sudo update-grub
$ sudo reboot
```

### 使用脚本自动安装

Docker 官方为了简化安装流程，提供了一套安装脚本，Debian 系统上可以使用这套脚本安装：

```bash
curl -sSL https://get.docker.com/ | sh
```

执行这个命令后，脚本就会自动的将一切准备工作做好，并且把 Docker 安装在系统中。

不过，由于伟大的墙的原因，在国内使用这个脚本可能会出现某些下载出现错误的情况。国内的一些云服务商提供了这个脚本的修改版本，使其使用国内的 Docker 软件源镜像安装，这样就避免了墙的干扰。

#### 阿里云的安装脚本

```bash
curl -sSL http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh -
```

#### DaoCloud 的安装脚本

```bash
curl -sSL https://get.daocloud.io/docker | sh
```

### 手动安装

#### 添加 APT 镜像源

由于官方源使用 HTTPS 以确保软件下载过程中不被篡改。因此，我们首先需要添加使用 HTTPS 传输的软件包以及 CA 证书。

*国内的一些软件源镜像（比如[阿里云](http://mirrors.aliyun.com/docker-engine/)）不是太在意系统安全上的细节，可能依旧使用不安全的 HTTP，对于这些源可以不执行这一步。*

```bash
$ sudo apt-get update
$ sudo apt-get install apt-transport-https ca-certificates
```

为了确认所下载软件包的合法性，需要添加 Docker 官方软件源的 GPG 密钥。

```bash
$ sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
```

然后，我们需要向 `source.list` 中添加 Docker 软件源，下表列出了不同的 Debian 版本对应的 APT 源。

|     Debian 版本      |                            REPO                              |
|---------------------|--------------------------------------------------------------|
|   Debian 7 Wheezy   | `deb https://apt.dockerproject.org/repo debian-wheezy main`  |
|   Debian 8 Jessie   | `deb https://apt.dockerproject.org/repo debian-jessie main`  |
| Debian Stretch/Sid  | `deb https://apt.dockerproject.org/repo debian-stretch main` |

用下面的命令将 APT 源添加到 `source.list`（将其中的 `<REPO>` 替换为上表的值）：

```bash
$ echo "<REPO>" | sudo tee /etc/apt/sources.list.d/docker.list
```

添加成功后，更新 apt 软件包缓存。

```bash
$ sudo apt-get update
```

#### 安装 Docker

在一切准备就绪后，就可以安装最新版本的 Docker 了，软件包名称为 `docker-engine`。

```bash
$ sudo apt-get install docker-engine
```

如果系统中存在旧版本的 Docker （`lxc-docker`, `docker.io`），会提示是否先删除，选择是即可。

#### 启动 Docker 引擎

##### Debian 7 Wheezy

```bash
$ sudo service docker start
```

##### Debian 8 Jessie/Stretch

```bash
$ sudo systemctl enable docker
$ sudo systemctl start docker
```

#### 建立 docker 用户组

默认情况下，`docker` 命令会使用 [Unix socket](https://en.wikipedia.org/wiki/Unix_domain_socket) 与 Docker 引擎通讯。而只有 `root` 用户和 `docker` 组的用户才可以访问 Docker 引擎的 Unix socket。出于安全考虑，一般 Linux 系统上不会直接使用 `root` 用户。因此，更好地做法是将需要使用 `docker` 的用户加入 `docker` 用户组。

建立 `docker` 组：

```bash
$ sudo groupadd docker
```

将当前用户加入 `docker` 组：

```bash
$ sudo usermod -aG docker $USER
```



### 参考文档

参见 [Docker 官方 Debian 安装文档](https://docs.docker.com/engine/installation/linux/debian/)。
