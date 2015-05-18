## 简介
swarm是Docker公司官方在2014年12月初发布的一套较为简单的工具，用来管理Docker集群，它将一群Docker宿主机变成一个单一的，虚拟的主机。Swarm使用标准的Docker API接口作为其前端访问入口，换言之，各种形式的Docker工具比如Dokku,Compose,Krane,Deis,docker-py,docker本身等都可以很容易的与swarm进行集成。

![swarm结构图](file:///C:/Users/RIO/Desktop/12.png)

在使用swarm管理docker集群时，会有一个swarm manager以及若干的swarm node，swarm manager上运行swarm daemon，用户只需要跟swarm manager通信，然后swarm manager再根据discovery service的信息选择一个swarm node来运行container。值得注意的是swarm daemon只是一个任务调度器(scheduler)和路由器(router),它本身不运行container，它只接受docker client发送过来的请求，调度合适的swarm node来运行container。这意味着，即使swarm daemon由于某些原因挂掉了，已经运行起来的container也不会有任何影响。
有以下两点需要注意：

1. 集群中的每台节点上面的docker的版本都不能小于1.4
2. 为了让swarm manager能够跟每台swarm node进行通信，集群中的每台节点的docker daemon都必须监听同一个网络接口
