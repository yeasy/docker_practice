## 使用其它服务发现后端

Swarm 目前可以支持多种服务发现后端，这些后端功能上都是一致的，即维护属于某个集群的节点的信息。不同方案并无优劣之分，在实际使用时候，可以结合自身需求和环境限制进行选择，甚至自己定制其它方案。

使用中可以通过不同的路径来选择特定的服务发现后端机制。

* `token://<token>`：使用 DockerHub 提供的服务，适用于可以访问公网情况；
* `file://path/to/file`：使用本地文件，需要手动管理；
* `consul://<ip>/<path>`：使用 consul 服务，私有环境推荐；
* `etcd://<ip1>,<ip2>/<path>`：使用 etcd 服务，私有环境推荐；
* `zk://<ip1>,<ip2>/<path>`：使用 zookeeper 服务，私有环境推荐；
* `[nodes://]<ip1>,<ip2>`：手动指定集群中节点的地址，方便进行服务测试。

### 使用文件

使用本地文件的方式十分简单，就是讲所有属于某个集群的节点的 Docker daemon 信息写入一个文件中，然后让 manager 从这个文件中直接读取相关信息。

首先，在 Swarm 管理节点（`192.168.0.2`）上新建一个文件，把要加入集群的机器的 Docker daemon 信息写入文件：

```sh
$ tee /tmp/cluster_info <<-'EOF'
192.168.0.2:2375
192.168.0.3:2375
EOF
```

然后，本地执行 `swarm manage` 命令，并指定服务发现机制为本地文件，注意因为是容器方式运行 manager，需要将本地文件挂载到容器内。

```sh
$ docker run -d -p 12375:2375 -v /tmp/cluster_info:/tmp/cluster_info swarm manage file:///tmp/cluster_info
```

接下来就可以通过使用 Swarm 服务来进行管理了，例如使用 info 查看所有节点的信息。

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
Name: e71eb5f1d48b
```

### 其它发现服务后端
其它服务发现后端的使用方法，也是大同小异，不同之处在于使用 Swarm 命令时指定的路径格式不同。

例如，对于前面介绍的 consul 服务后端来说。

快速部署一个 consul 服务的命令为：

```sh
$ docker run -d -p 8500:8500 --name=consul progrium/consul -server -bootstrap
```

之后创建 Swarm 的管理服务，指定使用 consul 服务，管理端口监听在本地的 4000 端口。

```sh
$ docker run -d -p 4000:4000 swarm manage -H :4000 --replication --advertise <manager_ip>:4000 consul://<consul_ip>:8500
```

Swarm 节点注册时候命令格式类似于：

```sh
$ swarm join --advertise=<node_ip:2375> consul://<consul_addr>/<optional path prefix>
```

对于 etcd 服务后端来说，节点注册时候命令格式类似于：

```sh
$ swarm join --addr=<node_addr:2375> etcd://<etcd_addr1>,<etcd_addr2>/<optional path prefix>
```
启动管理服务时候，格式类似于：

```sh
$ swarm manage -H tcp://<manager_ip>:4000 etcd://<etcd_addr1>,<etcd_addr2>/<optional path prefix>
```

### 地址和端口的范围匹配
对于基于文件，以及手动指定节点信息两种服务发现后端机制来说，其中地址和端口域可以支持指定一个范围，以一次性指定多个地址。
例如：

* `192.168.0.[2:10]:2375` 代表 `192.168.0.2:2375` -- `192.168.0.10:2375` 一共 9 个地址；
* `192.168.0.2:[2:9]375` 代表 `192.168.0.2:2375` -- `192.168.0.2:9375` 一共 8 个地址。