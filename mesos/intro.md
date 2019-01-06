## 简介
Mesos 最初由 UC Berkeley 的 AMP 实验室于 2009 年发起，遵循 Apache 协议，目前已经成立了 Mesosphere 公司进行运营。Mesos 可以将整个数据中心的资源（包括 CPU、内存、存储、网络等）进行抽象和调度，使得多个应用同时运行在集群中分享资源，并无需关心资源的物理分布情况。

如果把数据中心中的集群资源看做一台服务器，那么 Mesos 要做的事情，其实就是今天操作系统内核的职责：抽象资源 + 调度任务。Mesos 项目是 Mesosphere 公司 Datacenter Operating System (DCOS) 产品的核心部件。

Mesos 项目主要由 C++ 语言编写，项目官方地址为 [https://mesos.apache.org](https://mesos.apache.org)，代码仍在快速演化中，已经发布了正式版 1.0.0 版本。

Mesos 拥有许多引人注目的特性，包括：
* 支持数万个节点的大规模场景（Apple、Twitter、eBay 等公司实践）；
* 支持多种应用框架，包括 Marathon、Singularity、Aurora 等；
* 支持 HA（基于 ZooKeeper 实现）；
* 支持 Docker、LXC 等容器机制进行任务隔离；
* 提供了多个流行语言的 API，包括 Python、Java、C++ 等；
* 自带了简洁易用的 WebUI，方便用户直接进行操作。

值得注意的是，Mesos 自身只是一个资源抽象的平台，要使用它往往需要结合运行其上的分布式应用（在 Mesos 中被称作框架，framework），比如 Hadoop、Spark 等可以进行分布式计算的大数据处理应用；比如 Marathon 可以实现 PaaS，快速部署应用并自动保持运行；比如 ElasticSearch 可以索引海量数据，提供灵活的整合和查询能力……

大部分时候，用户只需要跟这些框架打交道即可，完全无需关心底下的资源调度情况，因为 Mesos 已经自动帮你实现了。这大大方便了上层应用的开发和运维。

当然，用户也可以基于 Mesos 打造自己的分布式应用框架。
