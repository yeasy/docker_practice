## Swarm 中的过滤器

Swarm 的调度器可以按照指定调度策略自动分配容器到节点。但有些时候希望能对这些分配加以干预。比如说，让 IO 敏感的容器分配到安装了 SSD 的节点上；让计算敏感的容器分配到 CPU 核数多的机器上；让网络敏感的容器分配到高带宽的机房；让某些容器尽量放同一个节点……。

这可以通过过滤器（filter）来实现，目前支持 `Constraint`、`Affinity`、`Port`、`Dependency`、`Health` 等五种过滤器。

### Constraint 过滤器
Constraint 过滤器是绑定到节点的键值对，相当于给节点添加标签。

可在启动 Docker 服务的时候指定，例如指定某个节点颜色为 `red`。

```bash
$ docker daemon --label color=red -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock
```

同样的，可以写在 Docker 服务的配置文件里面（以 Ubuntu 14.04 为例，是 `/etc/default/docker`）。

```bash
DOCKER_OPTS="--label color=red -H 0.0.0.0:2375 -H unix:///var/run/docker.sock"
```

使用 Swarm 启动容器的时候，采用 `-e constarint:key=value` 的形式，可以过滤选择出匹配条件的节点。

例如，我们将 `192.168.0.2` 节点打上红色标签，`192.168.0.3` 节点打上绿色标签。

然后，分别启动两个容器，指定使用过滤器分别为红色和绿色。

```bash
$ docker -H 192.168.0.2:12375 run -d -e constraint:color==red ubuntu:14.04 ping 127.0.0.1
252ffb48e64e9858c72241f5eedf6a3e4571b1ad926faf091db3e26672370f64
$ docker -H 192.168.0.2:12375 run -d -e constraint:color==green ubuntu:14.04 ping 127.0.0.1
3d6f8d7af8583416b17061d038545240c9e5c3be7067935d3ef2fbddce4b8136
```

*注：指定标签中间是两个等号*

查看它们将被分配到指定节点上。

```bash
$ docker -H 192.168.0.2:12375 ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                         NAMES
252ffb48e64e        ubuntu:14.04        "ping 127.0.0.1"         1 minutes ago       Up 1 minutes                            Host-2/sick_galileo
3d6f8d7af858        ubuntu:14.04        "ping 127.0.0.1"         2 minutes ago       Up 2 minutes                            Host-3/compassionate_ritchie
```

另外，Docker 内置了一些常见的过滤器，包括 `node`、`storagedriver`、`executiondriver`、`kernelversion`、`operatingsystem` 等。这些值可以通过 `docker info` 命令查看。

例如，目前集群中各个节点的信息为：

```bash
$ docker -H 192.168.0.2:12375 info
Containers: 5
Images: 39
Role: primary
Strategy: spread
Filters: health, port, dependency, affinity, constraint
Nodes: 2
 Host-2: 192.168.0.2:2375
  └ Containers: 4
  └ Reserved CPUs: 0 / 4
  └ Reserved Memory: 1 GiB / 4.053 GiB
  └ Labels: color=red, executiondriver=native-0.2, kernelversion=3.16.0-43-generic, operatingsystem=Ubuntu 14.04.3 LTS, storagedriver=aufs
 Host-3: 192.168.0.3:2375
  └ Containers: 1
  └ Reserved CPUs: 0 / 8
  └ Reserved Memory: 0 B / 16.46 GiB
  └ Labels: color=green, executiondriver=native-0.2, kernelversion=3.16.0-30-generic, operatingsystem=Ubuntu 14.04.3 LTS, storagedriver=aufs
CPUs: 12
Total Memory: 20.51 GiB
Name: 946d65606f7c
```

### Affinity 过滤器
Affinity 过滤器允许用户在启动一个容器的时候，让它分配到某个已有容器的节点上。

例如，下面我们将启动一个 nginx 容器，让它分配到已经运行某个 ubuntu 容器的节点上。

在 Constraint 过滤器的示例中，我们分别启动了两个 ubuntu 容器 `sick_galileo` 和 `compassionate_ritchie`，分别在 Host-2 和 Host-3 上。

现在启动一个 nginx 容器，让它跟容器 `sick_galileo` 放在一起，都放到 Host-2 节点上。可以通过 `-e affinity:container==<name or id>` 参数来实现。

```bash
$ docker -H 192.168.0.2:12375 run -d -e affinity:container==sick_galileo nginx
```

然后启动一个 redis 容器，让它跟容器 `compassionate_ritchie` 放在一起，都放到 Host-3 节点上。

```bash
$ docker -H 192.168.0.2:12375 run -d -e affinity:container==compassionate_ritchie redis
```

查看所有容器运行情况。

```bash
$ docker -H 192.168.0.2:12375 ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                         NAMES
0a32f15aa8ee        redis               "/entrypoint.sh redis"   2 seconds ago       Up 1 seconds        6379/tcp                  Host-3/awesome_darwin
d2b9a53e67d5        nginx               "nginx -g 'daemon off"   29 seconds ago      Up 28 seconds       80/tcp, 443/tcp               Host-2/fervent_wilson
252ffb48e64e        ubuntu:14.04        "ping 127.0.0.1"         2 minutes ago       Up 2 minutes                            Host-2/sick_galileo
3d6f8d7af858        ubuntu:14.04        "ping 127.0.0.1"         3 minutes ago       Up 3 minutes                            Host-3/compassionate_ritchie
```

### 其它过滤器
其它过滤器的使用方法也是大同小异，例如通过 `-e affinity:image==<name or id>` 来选择拥有指定镜像的节点；通过 `-e affinity:label_name==value` 来选择拥有指定标签的容器所允许的节点。

此外，当容器端口需要映射到宿主机指定端口号的时候，Swarm 也会自动分配容器到指定宿主机端口可用的节点。

当不同容器之间存在数据卷或链接依赖的时候，Swarm 会分配这些容器到同一个节点上。
