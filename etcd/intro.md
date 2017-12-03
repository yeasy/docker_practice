## 什么是 etcd

![](_images/etcd_logo.png)

`etcd` 是 `CoreOS` 团队于 2013 年 6 月发起的开源项目，它的目标是构建一个高可用的分布式键值（`key-value`）数据库，基于 `Go` 语言实现。我们知道，在分布式系统中，各种服务的配置信息的管理分享，服务的发现是一个很基本同时也是很重要的问题。`CoreOS` 项目就希望基于 `etcd` 来解决这一问题。

`etcd` 目前在 [github.com/coreos/etcd](https://github.com/coreos/etcd) 进行维护。

受到 [Apache ZooKeeper](http://zookeeper.apache.org/) 项目和 [doozer](https://github.com/ha/doozerd) 项目的启发，`etcd` 在设计的时候重点考虑了下面四个要素：

* 简单：具有定义良好、面向用户的 `API` ([gRPC](https://github.com/grpc/grpc))

* 安全：支持 `HTTPS` 方式的访问

* 快速：支持并发 `10 k/s` 的写操作

* 可靠：支持分布式结构，基于 `Raft` 的一致性算法

*Apache ZooKeeper 是一套知名的分布式系统中进行同步和一致性管理的工具。*

*doozer 是一个一致性分布式数据库。*

*[Raft](https://raft.github.io/) 是一套通过选举主节点来实现分布式系统一致性的算法，相比于大名鼎鼎的 Paxos 算法，它的过程更容易被人理解，由 Stanford 大学的 Diego Ongaro 和 John Ousterhout 提出。更多细节可以参考 [raftconsensus.github.io](http://raftconsensus.github.io)。*

一般情况下，用户使用 `etcd` 可以在多个节点上启动多个实例，并添加它们为一个集群。同一个集群中的 `etcd` 实例将会保持彼此信息的一致性。
