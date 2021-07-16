# 创建 Swarm 集群

阅读 [基本概念](overview.md) 一节我们知道 `Swarm` 集群由 **管理节点** 和 **工作节点** 组成。本节我们来创建一个包含一个管理节点和两个工作节点的最小 `Swarm` 集群。

## 初始化集群

在已经安装好 Docker 的主机上执行如下命令：

```bash
$ docker swarm init --advertise-addr 192.168.99.100
Swarm initialized: current node (dxn1zf6l61qsb1josjja83ngz) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

如果你的 Docker 主机有多个网卡，拥有多个 IP，必须使用 `--advertise-addr` 指定 IP。

> 执行 `docker swarm init` 命令的节点自动成为管理节点。

## 增加工作节点

上一步我们初始化了一个 `Swarm` 集群，拥有了一个管理节点，下面我们继续在两个 Docker 主机中分别执行如下命令，创建工作节点并加入到集群中。

```bash
$ docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377

This node joined a swarm as a worker.
```

## 查看集群

经过上边的两步，我们已经拥有了一个最小的 `Swarm` 集群，包含一个管理节点和两个工作节点。

在管理节点使用 `docker node ls` 查看集群。

```bash
$ docker node ls
ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
03g1y59jwfg7cf99w4lt0f662    worker2   Ready   Active
9j68exjopxe7wfl6yuxml7a7j    worker1   Ready   Active
dxn1zf6l61qsb1josjja83ngz *  manager   Ready   Active        Leader
```
