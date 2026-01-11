# 网络配置

当 Docker 启动时，会自动在主机上创建一个 `docker0` 虚拟网桥，实际上是 Linux 的一个 bridge，可以理解为一个软件交换机。它会在挂载到它的网口之间进行转发。

同时，Docker 随机分配一个本地未占用的私有网段（在 [RFC1918](https://datatracker.ietf.org/doc/html/rfc1918) 中定义）中的一个地址给 `docker0` 接口。比如典型的 `172.17.42.1`，掩码为 `255.255.0.0`。此后启动的容器内的网口也会自动分配一个同一网段（`172.17.0.0/16`）的地址。

当创建一个 Docker 容器的时候，同时会创建了一对 `veth pair` 接口（当数据包发送到一个接口时，另外一个接口也可以收到相同的数据包）。这对接口一端在容器内，即 `eth0`；另一端在本地并被挂载到 `docker0` 网桥，名称以 `veth` 开头（例如 `vethAQI2QT`）。通过这种方式，主机可以跟容器通信，容器之间也可以相互通信。Docker 就创建了在主机和所有容器之间一个虚拟共享网络。

![Docker 网络](./_images/network.png)

## 用户自定义网络

虽然默认的 `bridge` 网络可以满足大部分需求，但为了更好地隔离容器、或满足特定的网络需求，我们推荐使用用户自定义网络。

用户可以创建 `bridge`、`overlay` 或 `macvlan` 等不同类型的自定义网络。

### 创建一个自定义 bridge 网络

```bash
$ docker network create my-net
```

### 连接容器到自定义网络

在启动容器时，可以使用 `--network` 选项来指定网络。

```bash
$ docker run -it --rm --name busybox1 --network my-net busybox sh
$ docker run -it --rm --name busybox2 --network my-net busybox sh
```

在 `busybox1` 的终端中，可以 `ping` 通 `busybox2`。

```bash
/ # ping busybox2
PING busybox2 (172.19.0.3): 56 data bytes
64 bytes from 172.19.0.3: seq=0 ttl=64 time=0.083 ms
```

### 容器互联的废弃与替代

在 Docker 的早期版本中，`--link` 选项被用来连接容器。然而，这个功能现在已经被废弃，并且不推荐在生产环境中使用。

**注意：`--link` 是一个遗留功能。它可能会在未来的版本中被移除。我们强烈建议使用用户自定义网络来连接多个容器。**

使用自定义网络，容器之间可以通过容器名直接进行通信，这比使用 `--link` 更加灵活和强大。

接下来的部分将介绍 Docker 的一些高级网络配置，包括 DNS 配置和端口映射等内容。
