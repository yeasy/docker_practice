## 简介
Swarm 是 Docker公司官方在 2014 年 12月初发布的一套管理 Docker 集群的工具。它将一群 Docker 宿主机变成一个单一的，虚拟的主机。

Swarm 使用标准的 Docker API 接口作为其前端访问入口，换言之，各种形式的 Docker 工具比如 Dokku,Compose,Krane,Deis,docker-py,Docker 本身等都可以很容易的与 Swarm 进行集成。

![Swarm 结构图](../images/swarm.png)

在使用swarm管理docker集群时，会有一个swarm manager以及若干的swarm node，swarm manager上运行swarm daemon，用户只需要跟swarm manager通信，然后swarm manager再根据discovery service的信息选择一个swarm node来运行container。

值得注意的是swarm daemon只是一个任务调度器(scheduler)和路由器(router),它本身不运行容器，它只接受 Docker client 发送过来的请求，调度合适的 swarm node 来运行container。这意味着，即使 swarm daemon 由于某些原因挂掉了，已经运行起来的容器也不会有任何影响。


有以下两点需要注意：

* 集群中的每台节点上面的 Docker 的版本都不能小于1.4
* 为了让 swarm manager 能够跟每台 swarm node 进行通信，集群中的每台节点的 Docker daemon 都必须监听同一个网络接口。
