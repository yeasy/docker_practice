## 安装 Swarm
Swarm 安装有几种方式，可以基于 Docker Machine 来进行安装，也可以手动配置。为了能更容易理解 Swarm 的组件和更灵活的进行管理，推荐使用手动配置方式。

对于 Docker 1.12+ 版本，Swarm 相关命令已经原生嵌入到了 Docker engine 的支持，对于较低版本的 Docker，需要额外进行配置。

### 下载镜像
Docker 官方已经提供了 Swarm 镜像使用，需要在所有被 Swarm 管理的 Docker 主机上下载该镜像。

```sh
$ docker pull swarm
```

可以使用下面的命令来查看 Swarm 版本，验证是否成功下载 Swarm 镜像。

```sh
$ docker run --rm swarm -v
swarm version 1.2.2 (34e3da3)
```

### 配置节点
Docker 主机在加入 Swarm 集群前，需要进行一些简单配置，添加 Docker daemon 的网络监听。

例如，在启动 Docker daemon 的时候通过 `-H` 参数：

```sh
$ sudo docker daemon -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock
```

*注：Docker 1.8.0 版本之前不支持 daemon 命令，可以用 -d 代替。*

如果是通过服务方式启动，则需要修改服务的配置文件。

以 Ubuntu 14.04 为例，配置文件为 `/etc/default/docker`（其他版本的 Linux 上略有不同）。

在文件的最后添加：

```sh
DOCKER_OPTS="$DOCKER_OPTS -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock"
```

### 启动集群
Docker 集群管理需要使用服务发现（Service Discover）功能，Swarm 支持以下的几种方式：DockerHub、本地文件、etcd、consul、zookeeper 和手动指定节点 IP 地址信息等。

除了手动指定外，这些方法原理上都是通过维护一套数据库机制，来管理集群中注册节点的 Docker daemon 的访问信息。

本地配置集群推荐使用 consul 作为服务发现后端。利用社区提供的 Docker 镜像，整个过程只需要三步即可完成。

#### 启动 Consul 服务后端
启动 consuconsull 服务容器，映射到主机的 8500 端口。

```sh
$ docker run -d -p 8500:8500 --name=consul progrium/consul -server -bootstrap
```

获取到本地主机的地址作为 consul 的服务地址：`<consul_ip>:8500`。

#### 启动管理节点
首先，启动一个主管理节点，映射到主机的 4000 端口，并获取所在主机地址为 `<manager0_ip>`。其中 4000 端口是 Swarm 管理器的默认监听端口，用户也可以指定映射为其它端口。

```sh
$ docker run -d -p 4000:4000 swarm manage -H :4000 --replication --advertise <manager0_ip>:4000 consul://<consul_ip>:8500
```

为了提高高可用性，用户也可以启动从管理节点。假定获取所在主机地址为 `<manager1_ip>`。

```sh
$ docker run -d swarm manage -H :4000 --replication --advertise <manager1_ip>:4000 consul://<consul_ip>:8500
```

#### 启动工作节点
需要在每个工作节点上启动 agent 服务。

获取节点的主机地址为 `<node_ip>`，并指定前面获取到的 consul 服务地址。

```sh
$ docker run -d swarm join --advertise=<node_ip>:2375 consul://<consul_ip>:8500
```

节点启动后，用户可以指定 Docker 服务地址为 `<manager0_ip>:4000>` 来测试各种 Docker 命令，可以看到整个 Swarm 集群就像一个虚拟的 Docker 主机一样正常工作。

由于 Swarm 实际上是通过 agent 调用了本地的 Docker daemon 来运行容器，当 Swarm 集群服务出现故障时，无法接受新的请求，但已经运行起来的容器将不会受到影响。
