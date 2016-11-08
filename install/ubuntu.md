## Ubuntu 系列安装 Docker

### 系统要求

Docker 支持以下版本的 Ubuntu 操作系统：

* Ubuntu Xenial 16.04 (LTS)
* Ubuntu Trusty 14.04 (LTS)
* Ubuntu Precise 12.04 (LTS)

*注：Ubuntu 发行版中，LTS（Long-Term-Support）长期支持版本，会获得 5 年的升级维护支持，这样的版本会更稳定，因此在生产环境中推荐使用 LTS 版本。*

Docker 目前支持的 Ubuntu 版本最低为 12.04 LTS，但从稳定性上考虑，推荐使用 14.04 LTS 或更高的版本。

Docker 需要安装在 64 位的 x86 平台或 ARM 平台上（如[树莓派](https://www.raspberrypi.org/)），并且要求内核版本不低于 3.10。但实际上内核越新越好，过低的内核版本可能会出现部分功能无法使用，或者不稳定。

用户可以通过如下命令检查自己的内核版本详细信息：

```sh
$ uname -a
Linux device 4.4.0-45-generic #66~14.04.1-Ubuntu SMP Wed Oct 19 15:05:38 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
```

或者

```sh
$ cat /proc/version
Linux version 4.4.0-45-generic (buildd@lcy01-08) (gcc version 4.8.4 (Ubuntu 4.8.4-2ubuntu1~14.04.3) ) #66~14.04.1-Ubuntu SMP Wed Oct 19 15:05:38 UTC 2016
```

#### 升级内核

如果内核版本过低，可以用下面的命令升级系统内核。

##### Ubuntu 12.04 LTS

```sh
sudo apt-get install -y --install-recommends linux-generic-lts-trusty
```

##### Ubuntu 14.04 LTS

```sh
sudo apt-get install -y --install-recommends linux-generic-lts-xenial
```

升级完内核后不要忘记了重启以生效。

```sh
sudo reboot
```

### 使用脚本自动安装

Docker 官方为了简化安装流程，提供了一套安装脚本，Ubuntu 系统上可以使用这套脚本安装：

```sh
curl -sSL https://get.docker.com/ | sh
```

执行这个命令后，脚本就会自动的将一切准备工作做好，并且把 Docker 安装在系统中。

不过，由于伟大的墙的原因，在国内使用这个脚本可能会出现某些下载出现错误的情况。国内的一些云服务商提供了这个脚本的修改版本，使其使用国内的 Docker 软件源镜像安装，这样就避免了墙的干扰。

#### 阿里云的安装脚本

```sh
curl -sSL http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh -
```

#### DaoCloud 的安装脚本

```sh
curl -sSL https://get.daocloud.io/docker | sh
```

### 手动安装

#### 安装所需的软件包

##### 可选内核模块

从 Ubuntu 14.04 开始，一部分内核模块移到了可选内核模块包(`linux-image-extra-*`)，以减少内核软件包的体积。正常安装的系统应该会包含可选内核模块包，而一些裁剪后的系统可能会将其精简掉。`AUFS` 内核驱动属于可选内核模块的一部分，作为推荐的 Docker 存储层驱动，一般建议安装可选内核模块包以使用 `AUFS`。

如果系统没有安装可选内核模块的话，可以执行下面的命令来安装可选内核模块包：

```sh
$ sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual
```

##### 12.04 LTS 图形界面

在 Ubuntu 12.04 桌面环境下，需要一些额外的软件包，可以用下面的命令安装。

```sh
$ sudo apt-get install xserver-xorg-lts-trusty libgl1-mesa-glx-lts-trusty
```

#### 添加 APT 镜像源

虽然 Ubuntu 系统软件源中有 Docker，名为 `docker.io`，但是不应该使用系统源中的这个版本，它的版本太旧。我们需要使用 Docker 官方提供的软件源，因此，我们需要添加 APT 软件源。

首先，我们需要确保 APT 使用 HTTPS，以及 CA 证书更新到最新。官方源使用的是 HTTPS，从而确保软件下载过程中不被篡改。

*国内的一些软件源镜像（比如[阿里云](http://mirrors.aliyun.com/docker-engine/)）不是太在意系统安全上的细节，可能依旧使用不安全的 HTTP，对于这些源可以不执行这一步。*

```sh
$ sudo apt-get update
$ sudo apt-get install apt-transport-https ca-certificates
```

为了确认所下载软件包的合法性，需要添加 Docker 官方软件源的 GPG 密钥。

```sh
$ sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
```

然后，我们需要向 `source.list` 中添加 Docker 软件源，下表列出了不同的 Ubuntu 版本对应的 APT 源。

|     Ubuntu 版本      |                            REPO                              |
|---------------------|--------------------------------------------------------------|
| Precise 12.04 (LTS) | `deb https://apt.dockerproject.org/repo ubuntu-precise main` |
| Trusty 14.04 (LTS)  | `deb https://apt.dockerproject.org/repo ubuntu-trusty main`  |
| Xenial 16.04 (LTS)  | `deb https://apt.dockerproject.org/repo ubuntu-xenial main`  |

用下面的命令将 APT 源添加到 `source.list`（将其中的 `<REPO>` 替换为上表的值）：

```sh
$ echo "<REPO>" | sudo tee /etc/apt/sources.list.d/docker.list
```

添加成功后，更新 apt 软件包缓存。

```sh
$ sudo apt-get update
```

#### 安装 Docker

在一切准备就绪后，就可以安装最新版本的 Docker 了，软件包名称为 `docker-engine`。

```sh
$ sudo apt-get install docker-engine
```

如果系统中存在旧版本的 Docker （`lxc-docker`），会提示是否先删除，选择是即可。

#### 启动 Docker 引擎

##### Ubuntu 12.04/14.04

```sh
$ sudo service docker start
```

##### Ubuntu 16.04

```sh
$ sudo systemctl enable docker
$ sudo systemctl start docker
```

#### 建立 docker 用户组

默认情况下，`docker` 命令会使用 [Unix socket](https://en.wikipedia.org/wiki/Unix_domain_socket) 与 Docker 引擎通讯。而只有 `root` 用户和 `docker` 组的用户才可以访问 Docker 引擎的 Unix socket。出于安全考虑，一般 Linux 系统上不会直接使用 `root` 用户。因此，更好地做法是将需要使用 `docker` 的用户加入 `docker` 用户组。

建立 `docker` 组：

```sh
$ sudo groupadd docker
```

将当前用户加入 `docker` 组：

```sh
$ sudo usermod -aG docker $USER
```

#### 配置 GRUB 引导参数

在 Docker 使用期间，或者在 `docker info` 信息中，可能会看到下面的警告信息：

```sh
WARNING: Your kernel does not support cgroup swap limit. WARNING: Your
kernel does not support swap limit capabilities. Limitation discarded.
```

如警告信息所说，这些内核功能没有启用，因此如果需要使用这些功能，需要启用这些功能。因此需要修改 GRUB 的配置文件 ` /etc/default/grub`，添加下面这个配置：

```sh
GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"
```

然后不要忘记了更新 GRUB

```sh
$ sudo update-grub
```

### 参考文档

参见 [Docker官方配置文档](https://docs.docker.com/engine/installation/linux/ubuntulinux/)。
