## CentOS/Fedora

### CentOS 系统简介

`CentOS` 和 `Fedora` 都是基于 `Redhat` 的常见 Linux 分支。`CentOS` 是目前企业级服务器的常用操作系统；`Fedora` 则主要面向个人桌面用户。

![CentOS 操作系统](_images/centos-logo.png)

CentOS（Community Enterprise Operating System，中文意思是：社区企业操作系统），它是基于 `Red Hat Enterprise Linux` 源代码编译而成。由于 `CentOS` 与 `Redhat Linux` 源于相同的代码基础，所以很多成本敏感且需要高稳定性的公司就使用 `CentOS` 来替代商业版 `Red Hat Enterprise Linux`。`CentOS` 自身不包含闭源软件。

#### 使用 CentOS 官方镜像

首先使用 `docker search` 命令来搜索标星至少为 `25` 的 `CentOS` 相关镜像。

```bash
$ docker search -f stars=25 centos
NAME      DESCRIPTION      STARS     OFFICIAL   AUTOMATED
centos    The official...  2543      [OK]
jdeathe/centos-ssh         27                   [OK]
```

使用 `docker run` 直接运行最新的 `CentOS` 镜像，并登录 `bash`。

```bash
$ docker run -it centos bash
Unable to find image 'centos:latest' locally
latest: Pulling from library/centos
3d8673bd162a: Pull complete
Digest: sha256:a66ffcb73930584413de83311ca11a4cb4938c9b2521d331026dad970c19adf4
Status: Downloaded newer image for centos:latest
[root@43eb3b194d48 /]# cat /etc/redhat-release
CentOS Linux release 7.2.1511 (Core)
```

### Fedora 系统简介

![Fedora 操作系统](_images/fedora-logo.png)

`Fedora` 由 `Fedora Project` 社区开发，红帽公司赞助的 `Linux` 发行版。它的目标是创建一套新颖、多功能并且自由和开源的操作系统。`Fedora` 的功能对于用户而言，它是一套功能完备的，可以更新的免费操作系统，而对赞助商 `Red Hat` 而言，它是许多新技术的测试平台。被认为可用的技术最终会加入到 `Red Hat Enterprise Linux` 中。

#### 使用 Fedora 官方镜像

首先使用 `docker search` 命令来搜索标星至少为 `2` 的 `Fedora` 相关镜像，结果如下。

```bash
$ docker search -f stars=2 fedora
NAME                     DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
fedora                   Official Docker builds of Fedora                433       [OK]
dockingbay/fedora-rust   Trusted build of Rust programming language...   3                    [OK]
gluster/gluster-fedora   Official GlusterFS image [ Fedora 21 + Glu...   3                    [OK]
startx/fedora            Simple container used for all startx based...   2                    [OK]
```

使用 `docker run` 命令直接运行 `Fedora` 官方镜像，并登录 `bash`。

```bash
$ docker run -it fedora bash
Unable to find image 'fedora:latest' locally
latest: Pulling from library/fedora
2bf01635e2a0: Pull complete
Digest: sha256:64a02df6aac27d1200c2572fe4b9949f1970d05f74d367ce4af994ba5dc3669e
Status: Downloaded newer image for fedora:latest
[root@196ca341419b /]# cat /etc/redhat-release
Fedora release 24 (Twenty Four)
```

### 相关资源

* `Fedora` 官网：https://getfedora.org/
* `Fedora` 官方仓库：https://github.com/fedora-infra
* `Fedora` 官方镜像：https://hub.docker.com/_/fedora/
* `Fedora` 官方镜像仓库：https://github.com/fedora-cloud/docker-brew-fedora
* `CentOS` 官网：https://www.centos.org
* `CentOS` 官方仓库：https://github.com/CentOS
* `CentOS` 官方镜像：https://hub.docker.com/_/centos/
* `CentOS` 官方镜像仓库：https://github.com/CentOS/CentOS-Dockerfiles
