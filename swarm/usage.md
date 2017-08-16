## 使用 Swarm
前面演示了基于 consul 服务发现后端来配置一个本地 Swarm 集群。其中，consul 也可以被替换为 etcd、zookeeper 等。

另外一个更方便的方式是直接使用 DockerHub 提供的免费服务发现后端。

下面使用这种方式来演示 Swarm 的主要操作，包括：

* create：创建一个集群；
* list：列出集群中的节点；
* manage：管理一个集群；
* join：让节点加入到某个集群。

注意，使用 DockerHub 的服务发现后端，需要各个节点能通过公网访问到 DockerHub 的服务接口。

### 创建集群 id

在任意一台安装了 Swarm 的机器上执行 `swarm create` 命令来在 DockerHub 服务上进行注册。

Swarm 会通过服务发现后端（此处为 DockerHub 提供）来获取一个唯一的由数字和字母组成的 token，用来标识要管理的集群。

```sh
$ docker run --rm swarm create
946d65606f7c2f49766e4dddac5b4365
```

注意返回的字符串，这是集群的唯一 id，加入集群的各个节点将需要这个信息。

### 配置集群节点

在所有要加入集群的普通节点上面执行 `swarm join` 命令，表示把这台机器加入指定集群当中。

例如某台机器 IP 地址为 `192.168.0.2`，将其加入我们刚创建的 `946d65606f7c2f49766e4dddac5b4365` 集群，则可以通过：

```sh
$ docker run --rm swarm join --addr=192.168.0.2:2375 token://946d65606f7c2f49766e4dddac5b4365
time="2015-12-09T08:59:43Z" level=info msg="Registering on the discovery service every 20s..." addr="192.168.0.2:2375" discovery="token://946d65606f7c2f49766e4dddac5b4365"
...
```

*注：其中 `--addr` 指定的 IP 地址信息将被发送给服务发现后端，用以区分集群不同的节点。manager 服务必须要通过这个地址可以访问到该节点。*

通过控制台可以看到，上述命令执行后，默认每隔 20 秒（可以通过 `--heartbeat` 选项指定），会输出一条心跳信息。对于发现服务后端来说，默认如果超过 60 秒（可以通过 `--ttl` 选项指定）没有收到心跳信息，则将节点从列表中删除。

如果不希望看到输出日志信息，则可以用 `-d` 选项替换 `--rm` 选项，让服务后台执行。

执行 `swarm join` 命令实际上是通过 agent 把自己的信息注册到发现服务上，因此，此时对于后端的发现服务来说，已经可以看到有若干节点注册上来了。那么，如何管理和使用这些节点呢，这就得需要 Swarm 的 manager 服务了。


### 配置管理节点
配置管理节点需要通过 `swarm manage` 命令，该命令将启动 manager 服务，默认监听到 `2375` 端口，所有对集群的管理可以通过该服务接口进行。

读者可能注意到，manager 服务默认监听的端口跟 Docker 服务监听端口是一样的，这是为了兼容其它基于 Docker 的服务，可以无缝地切换到 Swarm 平台上来。

仍然在节点 `192.168.0.2` 进行操作。由于我们是采用 Docker 容器形式启动 manager 服务，本地的 `2375` 端口已经被 Docker Daemon 占用。我们将 manager 服务监听端口映射到本地一个空闲的 `12375` 端口。

```sh
$ docker run -d -p 12375:2375 swarm manage token://946d65606f7c2f49766e4dddac5b4365
1e1ca8c4117b6b7271efc693f9685b4e907d8dc95324350392b21e94b3cffd18
```

可以通过 `docker ps` 命令来查看启动的 swarm manager 服务容器。

```sh
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                     NAMES
1e1ca8c4117b        swarm               "/swarm manage token:"   11 seconds ago      Up 10 seconds       0.0.0.0:12375->2375/tcp   jovial_rosalind
```

命令如果执行成功会返回刚启动的 Swarm 容器的 ID，此时一个简单的 Swarm 集群就已经搭建起来了，包括一个普通节点和一个管理节点。

### 查看集群节点列表

集群启动成功以后，用户可以在任何一台节点上使用 `swarm list` 命令查看集群中的节点列表。例如

```sh
$ docker run --rm swarm list token://946d65606f7c2f49766e4dddac5b4365
192.168.0.2:2375
```
显示正是之前用 `swarm join` 命令加入集群的节点的地址。

我们在另外一台节点 `192.168.0.3` 上同样使用 `swarm join` 命令新加入一个节点：
```sh
$docker run --rm swarm join --addr=192.168.0.3:2375 token://946d65606f7c2f49766e4dddac5b4365
time="2015-12-10T02:05:34Z" level=info msg="Registering on the discovery service every 20s..." addr="192.168.0.3:2375" discovery="token://946d65606f7c2f49766e4dddac5b4365"
...
```

再次使用 `swarm list` 命令查看集群中的节点列表信息，可以看到新加入的节点：

```sh
$ docker run --rm swarm list token://946d65606f7c2f49766e4dddac5b4365
192.168.0.3:2375
192.168.0.2:2375
```

### 使用集群服务
那么，怎么使用 Swarm 提供的服务呢？

实际上，所有 Docker 客户端可以继续使用，只要指定使用 Swarm manager 服务的监听地址即可。

例如，manager 服务监听的地址为 `192.168.0.2:12375`，则可以通过指定 `-H 192.168.0.2:12375` 选项来继续使用 Docker 客户端，执行任意 Docker 命令，例如 `ps`、`info`、`run` 等等。

在任意节点上使用 `docker run` 来启动若干容器，例如

```sh
$docker -H 192.168.0.2:12375:12375 run -d ubuntu ping 127.0.0.1
4c9bccbf86fb6e2243da58c1b15e9378fac362783a663426bbe7058eea84de46
```

使用 `ps` 命令查看集群中正在运行的容器。

```sh
$ docker -H 192.168.0.2:12375 ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                         NAMES
4c9bccbf86fb        ubuntu              "ping 127.0.0.1"         About a minute ago   Up About a minute                       clever_wright
730061a3801a        registry:latest     "docker-registry"        2 minutes ago        Up 2 minutes         192.168.0.2:5000->5000/tcp   Host-1/registry_registry_1
72d99f24a06f        redis:3.0           "/entrypoint.sh redis"   2 minutes ago        Up 2 minutes         6379/tcp                      Host-1/registry_redis_1,Host-1/registry_registry_1/redis,Host-1/registry_registry_1/redis_1,Host-1/registry_registry_1/registry_redis_1
```

输出结果中显示目前集群中正在运行的容器（注意不包括 Swarm manager 服务容器），可以在不同节点上使用 `docker ps` 查看本地容器，发现这些容器实际上可能运行在集群中多个节点上（被 Swarm 调度策略进行分配）。

使用 info 查看所有节点的信息。

```sh
$ docker -H 192.168.0.2:12375 info
Containers: 18
Images: 36
Role: primary
Strategy: spread
Filters: health, port, dependency, affinity, constraint
Nodes: 2
 Host-1: 192.168.0.2:2375
  └ Containers: 15
  └ Reserved CPUs: 0 / 4
  └ Reserved Memory: 1 GiB / 4.053 GiB
  └ Labels: executiondriver=native-0.2, kernelversion=3.16.0-43-generic, operatingsystem=Ubuntu 14.04.3 LTS, storagedriver=aufs
 Host-2: 192.168.0.3:2375
  └ Containers: 3
  └ Reserved CPUs: 0 / 8
  └ Reserved Memory: 0 B / 16.46 GiB
  └ Labels: executiondriver=native-0.2, kernelversion=3.16.0-30-generic, operatingsystem=Ubuntu 14.04.3 LTS, storagedriver=aufs
CPUs: 12
Total Memory: 20.51 GiB
Name: 1e1ca8c4117b
```
结果输出显示这个集群目前只有两个节点，地址分别是 `192.168.0.2` 和 `192.168.0.3`。

类似的，也可以通过 Compose 模板来启动多个服务。不过请注意，要想让服务分布到多个 Swarm 节点上，需要采用版本 2 的写法。

### 使用网络
Swarm 为了支持跨主机的网络，默认采用了 `overlay` 网络类型，实现上通过 vxlan 来构建联通整个 Swarm 集群的网络。

首先，在集群中所有节点上，添加配置 Docker daemon 选项：

```
--cluster-store=<DISCOVERY_HOST:PORT> --cluster-advertise=<DOCKER_DAEMON_HOST:PORT>
```

以 consul 服务为例，可能类似：

```sh
--cluster-store=consul://<consul 服务地址>:8500 --cluster-advertise=192.168.0.3:2375
```

之后重启 Docker 服务。

首先，创建一个网络。

```sh
$ docker -H 192.168.0.2:12375 network create swarm_network
```

查看网络，将看到一个 overlay 类型的网络。

```sh
$ docker -H 192.168.0.2:12375 network ls
NETWORK ID          NAME                DRIVER
6edf2d16ec97        swarm_network       overlay
```

此时，所有添加到这个网络上的容器将自动被分配到集群中的节点上，并且彼此联通。
