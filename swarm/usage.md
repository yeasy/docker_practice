## 使用
在使用 swarm 管理集群前，需要把集群中所有的节点的 docker daemon 的监听方式更改为 `0.0.0.0:2375`。

可以有两种方式达到这个目的，第一种是在启动docker daemon的时候指定
```sh
sudo docker -H 0.0.0.0:2375&
```

第二种方式是直接修改 Docker 的配置文件(Ubuntu 上是 `/etc/default/docker`，其他版本的 Linux 上略有不同)

在文件的最后添加下面这句代码：
```sh
DOCKER_OPTS="-H 0.0.0.0:2375 -H unix:///var/run/docker.sock"
```


需要注意的是，一定要在所有希望被 Swarm 管理的节点上进行的。修改之后要重启 Docker
```sh
sudo service docker restart
```

Docker 集群管理需要使用服务发现(Discovery service backend)功能，Swarm支持以下的几种方式：DockerHub 提供的服务发现功能，本地的文件，etcd，counsel，zookeeper 和 IP 列表，本文会详细讲解前两种方式，其他的用法都是大同小异的。

先说一下本次试验的环境，本次试验包括三台机器，IP地址分别为192.168.1.84,192.168.1.83和192.168.1.124.利用这三台机器组成一个docker集群，其中83这台机器同时充当swarm manager节点。

### 使用 DockerHub 提供的服务发现功能

#### 创建集群 token

在上面三台机器中的任何一台机器上面执行 `swarm create` 命令来获取一个集群标志。这条命令执行完毕后，Swarm 会前往 DockerHub 上内置的发现服务中获取一个全球唯一的 token，用来标识要管理的集群。
```sh
sudo docker run --rm swarm create
```

我们在84这台机器上执行这条命令，输出如下：
```sh
rio@084:~$ sudo docker run --rm swarm create
b7625e5a7a2dc7f8c4faacf2b510078e
```

可以看到我们返回的 token 是 `b7625e5a7a2dc7f8c4faacf2b510078e`，每次返回的结果都是不一样的。这个 token 一定要记住，后面的操作都会用到这个 token。

#### 加入集群

在所有要加入集群的节点上面执行 `swarm join` 命令，表示要把这台机器加入这个集群当中。在本次试验中，就是要在 83、84 和 124 这三台机器上执行下面的这条命令：
```sh
sudo docker run -d swarm join --addr=ip_address:2375 token://token_id
```
其中的 ip_address 换成执行这条命令的机器的 IP，token_id 换成上一步执行 `swarm create` 返回的 token。

在83这台机器上面的执行结果如下：
```sh
rio@083:~$ sudo docker run -d swarm join --addr=192.168.1.83:2375 token://b7625e5a7a2dc7f8c4faacf2b510078e
3b3d9da603d7c121588f796eab723458af5938606282787fcbb03b6f1ac2000b
```
这条命令通过 `-d` 参数启动了一个容器，使得83这台机器加入到集群。如果这个容器被停止或者被删除，83这台机器就会从集群中消失。

#### 启动swarm manager
因为我们要使用 83 这台机器充当 swarm 管理节点，所以需要在83这台机器上面执行 `swarm manage` 命令：
```sh
sudo docker run -d -p 2376:2375 swarm manage token://b7625e5a7a2dc7f8c4faacf2b510078e
```
执行结果如下：
```sh
rio@083:~$ sudo docker run -d -p 2376:2375 swarm manage token://b7625e5a7a2dc7f8c4faacf2b510078e
83de3e9149b7a0ef49916d1dbe073e44e8c31c2fcbe98d962a4f85380ef25f76
```
这条命令如果执行成功会返回已经启动的 Swarm 的容器的 ID，此时整个集群已经启动起来了。

现在通过 `docker ps` 命令来看下有没有启动成功。
```sh
rio@083:~$ sudo docker ps
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS                    NAMES
83de3e9149b7        swarm:latest        "/swarm manage token   4 minutes ago       Up 4 minutes        0.0.0.0:2376->2375/tcp   stupefied_stallman
```
可以看到，Swarm 已经成功启动。
在执行 `Swarm manage` 这条命令的时候，有几点需要注意的：

* 这条命令需要在充当 swarm 管理者的机器上执行
* Swarm 要以 daemon 的形式执行
* 映射的端口可以使任意的除了 2375 以外的并且是未被占用的端口，但一定不能是 2375 这个端口，因为 2375 已经被 Docker 本身给占用了。

集群启动成功以后，现在我们可以在任何一台节点上使用 `swarm list` 命令查看集群中的节点了，本实验在 124 这台机器上执行 `swarm list` 命令：
```sh
rio@124:~$ sudo docker run --rm swarm list token://b7625e5a7a2dc7f8c4faacf2b510078e
192.168.1.84:2375
192.168.1.124:2375
192.168.1.83:2375
```
输出结果列出的IP地址正是我们使用 `swarm join` 命令加入集群的机器的IP地址。

现在我们可以在任何一台安装了 Docker 的机器上面通过命令(命令中要指明swarm manager机器的IP地址)来在集群中运行container了。
本次试验，我们在 192.168.1.85 这台机器上使用 `docker info` 命令来查看集群中的节点的信息。

其中 info 也可以换成其他的 Docker 支持的命令。
```sh
rio@085:~$ sudo docker -H 192.168.1.83:2376 info
Containers: 8
Strategy: spread
Filters: affinity, health, constraint, port, dependency
Nodes: 2
 sclu083: 192.168.1.83:2375
  └ Containers: 1
  └ Reserved CPUs: 0 / 2
  └ Reserved Memory: 0 B / 4.054 GiB
 sclu084: 192.168.1.84:2375
  └ Containers: 7
  └ Reserved CPUs: 0 / 2
  └ Reserved Memory: 0 B / 4.053 GiB
```
结果输出显示这个集群中只有两个节点，IP地址分别是 192.168.1.83 和 192.168.1.84，结果不对呀，我们明明把三台机器加入了这个集群，还有 124 这一台机器呢？
经过排查，发现是忘了修改 124 这台机器上面改 docker daemon 的监听方式，只要按照上面的步骤修改写 docker daemon 的监听方式就可以了。

在使用这个方法的时候，使用swarm create可能会因为网络的原因会出现类似于下面的这个问题：
```sh
rio@227:~$ sudo docker run --rm swarm create
[sudo] password for rio:
time="2015-05-19T12:59:26Z" level=fatal msg="Post https://discovery-stage.hub.docker.com/v1/clusters: dial tcp: i/o timeout"
```

### 使用文件

第二种方法相对于第一种方法要简单得多，也不会出现类似于上面的问题。

第一步：在 swarm 管理节点上新建一个文件，把要加入集群的机器 IP 地址和端口号写入文件中，本次试验就是要在83这台机器上面操作：
```sh
rio@083:~$ echo 192.168.1.83:2375 >> cluster
rio@083:~$ echo 192.168.1.84:2375 >> cluster
rio@083:~$ echo 192.168.1.124:2375 >> cluster
rio@083:~$ cat cluster
192.168.1.83:2375
192.168.1.84:2375
192.168.1.124:2375
```

第二步：在083这台机器上面执行 `swarm manage` 这条命令：
```sh
rio@083:~$ sudo docker run -d -p 2376:2375 -v $(pwd)/cluster:/tmp/cluster swarm manage file:///tmp/cluster
364af1f25b776f99927b8ae26ca8db5a6fe8ab8cc1e4629a5a68b48951f598ad
```
使用`docker ps`来查看有没有启动成功：
```sh
rio@083:~$ sudo docker ps
CONTAINER ID        IMAGE               COMMAND                CREATED              STATUS              PORTS                    NAMES
364af1f25b77        swarm:latest        "/swarm manage file:   About a minute ago   Up About a minute   0.0.0.0:2376->2375/tcp   happy_euclid
```
可以看到，此时整个集群已经启动成功。

在使用这条命令的时候需要注意的是注意：这里一定要使用-v命令，因为cluster文件是在本机上面，启动的容器默认是访问不到的，所以要通过-v命令共享。

接下来的就可以在任何一台安装了docker的机器上面通过命令使用集群，同样的，在85这台机器上执行docker info命令查看集群的节点信息：
```sh
rio@s085:~$ sudo docker -H 192.168.1.83:2376 info
Containers: 9
Strategy: spread
Filters: affinity, health, constraint, port, dependency
Nodes: 3
 atsgxxx: 192.168.1.227:2375
  └ Containers: 0
  └ Reserved CPUs: 0 / 4
  └ Reserved Memory: 0 B / 2.052 GiB
 sclu083: 192.168.1.83:2375
  └ Containers: 2
  └ Reserved CPUs: 0 / 2
  └ Reserved Memory: 0 B / 4.054 GiB
 sclu084: 192.168.1.84:2375
  └ Containers: 7
  └ Reserved CPUs: 0 / 2
  └ Reserved Memory: 0 B / 4.053 GiB
```
