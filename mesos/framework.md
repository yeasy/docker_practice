## 常见应用框架

应用框架是实际干活的，可以理解为 Mesos 之上跑的 `应用`。应用框架注册到 Mesos master 服务上即可使用。

用户大部分时候，只需要跟应用框架打交道。因此，选择合适的应用框架十分关键。

Mesos 目前支持的应用框架分为四大类：长期运行任务（以及 PaaS）、大数据处理、批量调度、数据存储。

随着 Mesos 自身的发展，越来越多的框架开始支持 Mesos，下面总结了目前常用的一些框架。

### 长期运行的服务

#### [Aurora](http://aurora.incubator.apache.org)
项目维护地址在 http://aurora.incubator.apache.org 。

利用 mesos 调度安排的任务，保证任务一直在运行。

提供 REST 接口，客户端和 webUI（8081 端口）

#### [Marathon](https://github.com/mesosphere/marathon)
项目维护地址在 https://github.com/mesosphere/marathon 。

一个私有 PaaS 平台，保证运行的应用不被中断。

如果任务停止了，会自动重启一个新的相同任务。

支持任务为任意 bash 命令，以及容器。

提供 REST 接口，客户端和 webUI（8080 端口）

#### [Singularity](https://github.com/HubSpot/Singularity)
项目维护地址在 https://github.com/HubSpot/Singularity 。

一个私有 PaaS 平台。

调度器，运行长期的任务和一次性任务。

提供 REST 接口，客户端和 webUI（7099、8080 端口），支持容器。

### 大数据处理
#### [Cray Chapel](https://github.com/nqn/mesos-chapel)
项目维护地址在 https://github.com/nqn/mesos-chapel 。

支持 Chapel 并行编程语言的运行框架。

#### [Dpark](https://github.com/douban/dpark)
项目维护地址在 https://github.com/douban/dpark 。

Spark 的 Python 实现。

#### [Hadoop](https://github.com/mesos/hadoop)
项目维护地址在 https://github.com/mesos/hadoop 。

经典的 map-reduce 模型的实现。

#### [Spark](http://spark.incubator.apache.org)
项目维护地址在 http://spark.incubator.apache.org 。

跟 Hadoop 类似，但处理迭代类型任务会更好的使用内存做中间状态缓存，速度要快一些。

#### [Storm](https://github.com/mesosphere/storm-mesos)
项目维护地址在 https://github.com/mesosphere/storm-mesos 。

分布式流计算，可以实时处理数据流。

### 批量调度
#### [Chronos](https://github.com/airbnb/chronos)
项目维护地址在 https://github.com/airbnb/chronos 。

Cron 的分布式实现，负责任务调度，支持容错。

#### [Jenkins](https://github.com/jenkinsci/mesos-plugin)
项目维护地址在 https://github.com/jenkinsci/mesos-plugin 。

大名鼎鼎的 CI 引擎。使用 mesos-jenkins 插件，可以将 jenkins 的任务被 Mesos 集群来动态调度执行。

#### JobServer
项目维护地址在 http://www.grandlogic.com/content/html_docs/jobserver.html 。

基于 Java 的调度任务和数据处理引擎。

#### GoDocker
项目维护地址在 https://bitbucket.org/osallou/go-docker 。

基于 Docker 容器的集群维护工具。提供用户接口，除了支持 Mesos，还支持 Kubernetes、Swarm 等。

### 数据存储
#### [Cassandra](https://github.com/mesosphere/cassandra-mesos)
项目维护地址在 https://github.com/mesosphere/cassandra-mesos 。

高性能的分布式数据库。可扩展性很好，支持高可用。

#### [ElasticSearch](https://github.com/mesosphere/elasticsearch-mesos)
项目维护地址在 https://github.com/mesosphere/elasticsearch-mesos 。

功能十分强大的分布式数据搜索引擎。

一方面通过分布式集群实现可靠的数据库，一方面提供灵活的 API，对数据进行整合和分析。ElasticSearch + LogStash + Kibana 目前合成为 ELK 工具栈。

#### Hypertable
项目维护地址在 https://code.google.com/p/hypertable 。

高性能的分布式数据库，支持结构化或者非结构化的数据存储。

#### Tachyon
项目维护地址在 http://tachyon-project.org/ 。

内存为中心的分布式存储系统，利用内存访问的高速提供高性能。
