# 常见问题总结

## 镜像相关

### 如何批量清理临时镜像文件？

答：可以使用 `docker image prune` 命令。

### 如何查看镜像支持的环境变量？

答：可以使用 `docker run IMAGE env` 命令。

### 本地的镜像文件都存放在哪里？

答：与 Docker 相关的本地资源默认存放在 `/var/lib/docker/` 目录下，以 `aufs` 文件系统为例，其中 `container` 目录存放容器信息，`graph` 目录存放镜像信息，`aufs` 目录下存放具体的镜像层文件。

### 构建 Docker 镜像应该遵循哪些原则？

答：整体原则上，尽量保持镜像功能的明确和内容的精简，要点包括

* 尽量选取满足需求但较小的基础系统镜像，例如大部分时候可以选择 debian:wheezy 或 debian:jessie 镜像，仅有不足百兆大小；

* 清理编译生成文件、安装包的缓存等临时文件；

* 安装各个软件时候要指定准确的版本号，并避免引入不需要的依赖；

* 从安全角度考虑，应用要尽量使用系统的库和依赖；

* 如果安装应用时候需要配置一些特殊的环境变量，在安装后要还原不需要保持的变量值；

* 使用 Dockerfile 创建镜像时候要添加 .dockerignore 文件或使用干净的工作目录。

更多内容请查看 [Dockerfile 最佳实践](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)

### 碰到网络问题，无法 pull 镜像，命令行指定 http_proxy 无效？

答：在 Docker 配置文件中添加 `export http_proxy="http://<PROXY_HOST>:<PROXY_PORT>"`，之后重启 Docker 服务即可。

## 容器相关

### 容器退出后，通过 docker container ls 命令查看不到，数据会丢失么？

答：容器退出后会处于终止（exited）状态，此时可以通过 `docker container ls -a` 查看。其中的数据也不会丢失，还可以通过 `docker start` 命令来启动它。只有删除掉容器才会清除所有数据。

### 如何停止所有正在运行的容器？

答：可以使用 `docker stop $(docker container ls -q)` 命令。

### 如何批量清理已经停止的容器？

答：可以使用 `docker container prune` 命令。

### 如何获取某个容器的 PID 信息？

答：可以使用 `docker inspect --format '{{ .State.Pid }}' <CONTAINER ID or NAME>` 命令。

### 如何获取某个容器的 IP 地址？

答：可以使用 `docker inspect --format '{{ .NetworkSettings.IPAddress }}' <CONTAINER ID or NAME>` 命令

### 如何给容器指定一个固定 IP 地址，而不是每次重启容器 IP 地址都会变？

答：使用以下命令启动容器可以使容器 IP 固定不变

```bash
$ docker network create -d bridge --subnet 172.25.0.0/16 my-net

$ docker run --network=my-net --ip=172.25.3.3 -itd --name=my-container busybox
```

### 如何临时退出一个正在交互的容器的终端，而不终止它？

答：按 `Ctrl-p Ctrl-q`。如果按 `Ctrl-c` 往往会让容器内应用进程终止，进而会终止容器。

### 使用 `docker port` 命令映射容器的端口时，系统报错“Error: No public port '80' published for xxx”？

答：

* 创建镜像时 `Dockerfile` 要通过 `EXPOSE` 指定正确的开放端口；

* 容器启动时指定 `PublishAllPort = true`。

### 可以在一个容器中同时运行多个应用进程么？

答：一般并不推荐在同一个容器内运行多个应用进程。如果有类似需求，可以通过一些额外的进程管理机制，比如 `supervisord` 来管理所运行的进程。可以参考 https://docs.docker.com/engine/admin/multi-service_container/ 。

### 如何控制容器占用系统资源（CPU、内存）的份额？

答：在使用 `docker create` 命令创建容器或使用 `docker run` 创建并启动容器的时候，可以使用 -c|--cpu-shares[=0] 参数来调整容器使用 CPU 的权重；使用 -m|--memory[=MEMORY] 参数来调整容器使用内存的大小。

## 仓库相关

### 仓库（Repository）、注册服务器（Registry）、注册索引（Index） 有何关系？

首先，仓库是存放一组关联镜像的集合，比如同一个应用的不同版本的镜像。

注册服务器是存放实际的镜像文件的地方。注册索引则负责维护用户的账号、权限、搜索、标签等的管理。因此，注册服务器利用注册索引来实现认证等管理。

## 配置相关

### Docker 的配置文件放在哪里，如何修改配置？

答：使用 `upstart` 的系统（如 Ubuntu 14.04）的配置文件在 `/etc/default/docker`，使用 `systemd` 的系统（如 Ubuntu 16.04、Centos 等）的配置文件在 `/etc/docker/daemon.json`。


### 如何更改 Docker 的默认存储位置？

答：Docker 的默认存储位置是 `/var/lib/docker`，如果希望将 Docker 的本地文件存储到其他分区，可以使用 Linux 软连接的方式来完成，或者在启动 daemon 时通过 `-g` 参数指定，或者修改配置文件 `/etc/docker/daemon.json` 的 "data-root" 项 。可以使用 `docker system info | grep "Root Dir"` 查看当前使用的存储位置。

例如，如下操作将默认存储位置迁移到 /storage/docker。

```sh
[root@s26 ~]# df -h
Filesystem                    Size  Used Avail Use% Mounted on
/dev/mapper/VolGroup-lv_root   50G  5.3G   42G  12% /
tmpfs                          48G  228K   48G   1% /dev/shm
/dev/sda1                     485M   40M  420M   9% /boot
/dev/mapper/VolGroup-lv_home  222G  188M  210G   1% /home
/dev/sdb2                     2.7T  323G  2.3T  13% /storage
[root@s26 ~]# service docker stop
[root@s26 ~]# cd /var/lib/
[root@s26 lib]# mv docker /storage/
[root@s26 lib]# ln -s /storage/docker/ docker
[root@s26 lib]# ls -la docker
lrwxrwxrwx. 1 root root 15 11月 17 13:43 docker -> /storage/docker
[root@s26 lib]# service docker start
```

### 使用内存和 swap 限制启动容器时候报警告："WARNING: Your kernel does not support cgroup swap limit. WARNING: Your kernel does not support swap limit capabilities. Limitation discarded."？

答：这是因为系统默认没有开启对内存和 swap 使用的统计功能，引入该功能会带来性能的下降。要开启该功能，可以采取如下操作：

* 编辑 `/etc/default/grub` 文件（Ubuntu 系统为例），配置 `GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"`

* 更新 grub：`$ sudo update-grub`

* 重启系统，即可。

## Docker 与虚拟化

### Docker 与 LXC（Linux Container）有何不同？

答：LXC 利用 Linux 上相关技术实现了容器。Docker 则在如下的几个方面进行了改进：
* 移植性：通过抽象容器配置，容器可以实现从一个平台移植到另一个平台；
* 镜像系统：基于 AUFS 的镜像系统为容器的分发带来了很多的便利，同时共同的镜像层只需要存储一份，实现高效率的存储；
* 版本管理：类似于Git的版本管理理念，用户可以更方便的创建、管理镜像文件；
* 仓库系统：仓库系统大大降低了镜像的分发和管理的成本；
* 周边工具：各种现有工具（配置管理、云平台）对 Docker 的支持，以及基于 Docker的 PaaS、CI 等系统，让 Docker 的应用更加方便和多样化。

### Docker 与 Vagrant 有何不同？

答：两者的定位完全不同。

* Vagrant 类似 Boot2Docker（一款运行 Docker 的最小内核），是一套虚拟机的管理环境。Vagrant 可以在多种系统上和虚拟机软件中运行，可以在 Windows，Mac 等非 Linux 平台上为 Docker 提供支持，自身具有较好的包装性和移植性。

* 原生的 Docker 自身只能运行在 Linux 平台上，但启动和运行的性能都比虚拟机要快，往往更适合快速开发和部署应用的场景。

简单说：Vagrant 适合用来管理虚拟机，而 Docker 适合用来管理应用环境。

### 开发环境中 Docker 和 Vagrant 该如何选择？

答：Docker 不是虚拟机，而是进程隔离，对于资源的消耗很少，但是目前需要 Linux 环境支持。Vagrant 是虚拟机上做的封装，虚拟机本身会消耗资源。

如果本地使用的 Linux 环境，推荐都使用 Docker。

如果本地使用的是 macOS 或者 Windows 环境，那就需要开虚拟机，单一开发环境下 Vagrant 更简单；多环境开发下推荐在 Vagrant 里面再使用 Docker 进行环境隔离。

## 其它

### Docker 能在非 Linux 平台（比如 Windows 或 macOS ）上运行么？

答：完全可以。安装方法请查看 [安装 Docker](../../install/) 一节

### 如何将一台宿主主机的 Docker 环境迁移到另外一台宿主主机？

答：停止 Docker 服务。将整个 Docker 存储文件夹复制到另外一台宿主主机，然后调整另外一台宿主主机的配置即可。

### 如何进入 Docker 容器的网络命名空间？

答：Docker 在创建容器后，删除了宿主主机上 `/var/run/netns` 目录中的相关的网络命名空间文件。因此，在宿主主机上是无法看到或访问容器的网络命名空间的。

用户可以通过如下方法来手动恢复它。

首先，使用下面的命令查看容器进程信息，比如这里的 1234。

```bash
$ docker inspect --format='{{. State.Pid}} ' $container_id
1234
```

接下来，在 `/proc` 目录下，把对应的网络命名空间文件链接到 `/var/run/netns` 目录。

```bash
$ sudo ln -s /proc/1234/ns/net /var/run/netns/
```

然后，在宿主主机上就可以看到容器的网络命名空间信息。例如

```bash
$ sudo ip netns show
1234
```

此时，用户可以通过正常的系统命令来查看或操作容器的命名空间了。例如修改容器的 IP 地址信息为 `172.17.0.100/16`。

```bash
$ sudo ip netns exec 1234 ifconfig eth0 172.17.0.100/16
```

### 如何获取容器绑定到本地那个 veth 接口上？

答：Docker 容器启动后，会通过 veth 接口对连接到本地网桥，veth 接口命名跟容器命名毫无关系，十分难以找到对应关系。

最简单的一种方式是通过查看接口的索引号，在容器中执行 `ip a` 命令，查看到本地接口最前面的接口索引号，如 `205`，将此值加上 1，即 `206`，然后在本地主机执行 `ip a` 命令，查找接口索引号为 `206` 的接口，两者即为连接的 veth 接口对。
