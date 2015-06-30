## Mesos 常见框架

framework 是实际干活的，可以理解为 mesos 上跑的 `应用`，需要注册到 master 上。

### 长期运行的服务

#### [Aurora](http://aurora.incubator.apache.org/)
利用 mesos 调度安排的任务，保证任务一直在运行。

提供 REST 接口，客户端和 webUI（8081 端口）

#### [Marathon](https://github.com/mesosphere/marathon)
一个 PaaS 平台。

保证任务一直在运行。如果停止了，会自动重启一个新的任务。

支持任务为任意 bash 命令，以及容器。

提供 REST 接口，客户端和 webUI（8080 端口）

#### [Singularity](https://github.com/HubSpot/Singularity)
一个 PaaS 平台。

调度器，运行长期的任务和一次性任务。

提供 REST 接口，客户端和 webUI（7099、8080 端口），支持容器。

### 大数据处理
#### [Cray Chapel](https://github.com/nqn/mesos-chapel)
支持 Chapel 并行编程语言的运行框架。

#### [Dpark](https://github.com/douban/dpark)
Spark 的 Python 实现。

#### [Hadoop](https://github.com/mesos/hadoop)
经典的 map-reduce 模型的实现。

#### [Spark](http://spark.incubator.apache.org/)
跟 Hadoop 类似，但处理迭代类型任务会更好的使用内存做中间状态缓存，速度要快一些。

#### [Storm](https://github.com/mesosphere/storm-mesos)
分布式流计算，可以实时处理数据流。

### 批量调度
#### [Chronos](https://github.com/airbnb/chronos)
Cron 的分布式实现，负责任务调度。

#### [Jenkins](https://github.com/jenkinsci/mesos-plugin)
大名鼎鼎的 CI 引擎。使用 mesos-jenkins 插件，可以将 jenkins 的任务被 mesos 来动态调度执行。

#### [ElasticSearch](https://github.com/mesosphere/elasticsearch-mesos)
功能十分强大的分布式数据搜索引擎。

### 数据存储
#### [Cassandra](https://github.com/mesosphere/cassandra-mesos)
高性能分布式数据库。
