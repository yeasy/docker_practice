# 附录一：常见问题与错误速查

更多错误排查条目见 [常见错误处理](errors.md)。

## 镜像相关

### 如何批量清理临时镜像文件？

答：可以使用 `docker image prune` 命令。

### 如何查看镜像支持的环境变量？

答：可以使用 `docker run IMAGE env` 命令。

### 本地的镜像文件都存放在哪里？

答：在 Linux 上，全新安装的 Docker Engine 29 及以后版本默认使用 containerd 镜像存储。独立运行的 containerd 默认将镜像内容和容器快照保存在 `/var/lib/containerd`，卷和 Docker 配置等数据仍保存在 `/var/lib/docker`。沿用经典 `overlay2` 驱动的安装将镜像层保存在 Docker 数据目录下的 `overlay2/`。具体路径取决于后端和配置，详见 [Docker 数据目录](https://docs.docker.com/engine/daemon/#daemon-data-directory)。

### 构建 Docker 镜像应该遵循哪些原则？

答：整体原则上，尽量保持镜像功能的明确和内容的精简，要点包括

* 尽量选取满足需求但较小的基础系统镜像，例如大部分时候可以选择 `alpine` 镜像，仅有不足六兆大小；
* 清理编译生成文件、安装包的缓存等临时文件；
* 安装各个软件时候要指定准确的版本号，并避免引入不需要的依赖；
* 从安全角度考虑，应用要尽量使用系统的库和依赖；
* 如果安装应用时候需要配置一些特殊的环境变量，在安装后要还原不需要保持的变量值；
* 使用 Dockerfile 创建镜像时候要添加 .dockerignore 文件或使用干净的工作目录。

更多内容请查看 [Dockerfile 最佳实践](../best_practices.md)

### 碰到网络问题，无法 pull 镜像，命令行指定 http\_proxy 无效？

答：先区分代理要作用在哪一层。Docker daemon 拉取镜像时，推荐在 `daemon.json` 的 `proxies` 字段或 systemd drop-in 中配置 `HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY`，然后重启 Docker 服务。Docker CLI、构建过程和容器内应用的代理应分别使用 `~/.docker/config.json`、`--build-arg` 或 `docker run --env` 配置；不要把 `export http_proxy=...` 当作 `daemon.json` 内容写入。

## 容器相关

### 容器退出后，通过 docker container ls 命令查看不到，数据会丢失么？

答：容器退出后会处于终止 (exited) 状态，此时可以通过 `docker container ls -a` 查看。其中的数据也不会丢失，还可以通过 `docker start` 命令来启动它。只有删除掉容器才会清除所有数据。

### 如何停止所有正在运行的容器？

答：可以使用 `docker stop $(docker container ls -q)` 命令。

### 如何批量清理已经停止的容器？

答：可以使用 `docker container prune` 命令。

### 如何获取某个容器的 PID 信息？

答：可以使用

```bash
docker inspect --format '{{ .State.Pid }}' <CONTAINER ID or NAME>
```

### 如何获取某个容器的 IP 地址？

答：可以使用

```bash
docker inspect --format '{{ .NetworkSettings.IPAddress }}' <CONTAINER ID or NAME>
```

### 如何给容器指定一个固定 IP 地址，而不是每次重启容器 IP 地址都会变？

答：使用以下命令启动容器可以使容器 IP 固定不变

```bash
$ docker network create -d bridge --subnet 172.25.0.0/16 my-net

$ docker run --network=my-net --ip=172.25.3.3 -itd --name=my-container busybox
```

这个固定 IP 主要用于同一 Docker daemon 内的容器间通信。Docker Desktop 上不要依赖宿主机直接访问 Linux 容器 IP；宿主机访问容器服务仍应使用端口映射或 `host.docker.internal` 等机制。

### 如何临时退出一个正在交互的容器的终端，而不终止它？

答：按 `Ctrl-p Ctrl-q`。如果按 `Ctrl-c` 往往会让容器内应用进程终止，进而会终止容器。

### 使用 `docker port` 命令映射容器的端口时，系统报错 “Error：No public port ‘80’ published for xxx”？

答：

* 创建容器时用 `-p HOST_PORT:CONTAINER_PORT` 或 `--publish` 显式发布端口，例如 `docker run -p 8080:80 nginx`；
* 只想把镜像声明的 `EXPOSE` 端口随机发布到宿主机端口时，用 `-P` / `--publish-all`，之后通过 `docker ps` 查看实际端口；
* `Dockerfile` 中的 `EXPOSE` 只是镜像元数据，不会自动发布端口。

### 可以在一个容器中同时运行多个应用进程么？

答：一般并不推荐在同一个容器内运行多个应用进程。如果有类似需求，可以通过一些额外的进程管理机制，比如 `supervisord` 来管理所运行的进程。可以参考 [Docker 官方说明](https://docs.docker.com/engine/containers/multi-service_container/)。

### 如何控制容器占用 CPU、内存等系统资源的份额？

答：在使用 `docker create` 命令创建容器或使用 `docker run` 创建并启动容器的时候，可以使用 -c|--cpu-shares\[=0] 参数来调整容器使用 CPU 的权重；使用 -m|--memory\[=MEMORY] 参数来调整容器使用内存的大小。

## 仓库相关

### 仓库、注册服务器、注册索引有何关系？

首先，仓库是存放一组关联镜像的集合，比如同一个应用的不同版本的镜像。

注册服务器是存放实际的镜像文件的地方。注册索引则负责维护用户的账号、权限、搜索、标签等的管理。因此，注册服务器利用注册索引来实现认证等管理。

## 配置相关

### Docker 的配置文件放在哪里，如何修改配置？

答：使用 `systemd` 的系统（如 Ubuntu 22.04+、Debian 12+、Rocky/Alma/CentOS Stream 9+）的配置文件在 `/etc/docker/daemon.json`。

### 如何更改 Docker 的默认存储位置？

答：在 Linux 上，运行 `docker info --format '{{.DockerRootDir}}'` 可查看 Docker 的数据目录。可通过 `/etc/docker/daemon.json` 的 `data-root` 指定新位置。使用独立的 containerd 镜像存储时，还需单独设置 containerd 的 `root`。配置新路径前先备份原数据；修改路径本身不会搬迁已有数据。详见 [Docker 数据目录配置](https://docs.docker.com/engine/daemon/#configure-the-data-directory-location)。

### 使用内存和 swap 限制启动容器时候报内核不支持警告？

答：如果遇到 `WARNING: Your kernel does not support cgroup swap limit` 等警告，这是因为系统默认没有开启对内存和 swap 使用的统计功能，引入该功能会带来性能的下降。要开启该功能，可以采取如下操作：

* 编辑 `/etc/default/grub` 文件（Ubuntu 系统为例），配置 `GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"`
* 更新 grub：`$ sudo update-grub`
* 重启系统，即可。

## Docker 与虚拟化

### Docker 与 LXC 有何不同？

答：LXC 利用 Linux 上相关技术实现了容器。Docker 则在如下的几个方面进行了改进：

* 移植性：通过抽象容器配置，容器可以实现从一个平台移植到另一个平台；
* 镜像系统：基于 OverlayFS 的镜像系统为容器的分发带来了很多的便利，同时共同的镜像层只需要存储一份，实现高效率的存储；
* 版本管理：类似于 Git 的版本管理理念，用户可以更方便的创建、管理镜像文件；
* 仓库系统：仓库系统大大降低了镜像的分发和管理的成本；
* 周边工具：各种现有工具（配置管理、云平台）对 Docker 的支持，以及基于 Docker 的 PaaS、CI 等系统，让 Docker 的应用更加方便和多样化。

### Docker 与 Vagrant 有何不同？

答：Docker 将应用及其依赖打包为镜像，并在容器中运行。Vagrant 用配置文件描述开发机器，可以通过虚拟机提供程序创建整套客户操作系统。

### 开发环境中 Docker 和 Vagrant 该如何选择？

答：若要让团队复用同一套应用服务，可用 Docker Compose 描述服务，并在 macOS 或 Windows 上用 [Docker Desktop](https://docs.docker.com/desktop/) 运行 Linux 容器。若需要测试特定内核、系统启动过程或整台虚拟机的配置，可用 Vagrant 管理相应的虚拟机。

## 其他

### Docker 能在非 Linux 平台上运行么？比如 Windows 或 macOS

答：完全可以。安装方法请查看[安装 Docker](../../03_install/README.md) 一节

### 如何将一台宿主主机的 Docker 环境迁移到另外一台宿主主机？

答：在新主机上用原部署配置重新创建服务，重新拉取镜像，并备份、恢复数据卷和绑定挂载中的应用数据。对运行中的数据库，先制作一致性备份。仅复制 `/var/lib/docker` 会遗漏绑定挂载和独立 containerd 数据目录中的内容。

### 如何进入 Docker 容器的网络命名空间？

答：在运行 Docker Engine 的 Linux 主机上，可以通过容器主进程的 PID 找到其网络命名空间。下例为它注册一个临时名称，查看网络接口后移除名称。先将 `container_id` 设为运行中容器的名称或 ID。

```bash
$ pid=$(docker inspect --format='{{.State.Pid}}' "$container_id")
$ sudo ip netns attach "docker-$pid" "$pid"
$ sudo ip netns exec "docker-$pid" ip address show
$ sudo ip netns delete "docker-$pid"
```

### 如何获取容器绑定到本地哪个 veth 接口上？

答：Docker 容器启动后，会通过 veth 接口对连接到本地网桥，veth 接口命名跟容器命名毫无关系，十分难以找到对应关系。

最简单的一种方式是通过查看接口的索引号，在容器中执行 `ip a` 命令，查看到本地接口最前面的接口索引号，如 `205`，将此值加上 1，即 `206`，然后在本地主机执行 `ip a` 命令，查找接口索引号为 `206` 的接口，两者即为连接的 veth 接口对。
