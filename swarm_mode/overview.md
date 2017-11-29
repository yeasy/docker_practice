## 基本概念

`Swarm` 是使用 [`SwarmKit`](https://github.com/docker/swarmkit/) 构建的 Docker 引擎内置（原生）的集群管理和编排工具。

 使用 `Swarm` 集群之前需要了解以下几个概念。

### 节点

运行 Docker 的主机可以主动初始化一个 `Swarm` 集群或者加入一个已存在的 `Swarm` 集群，这样这个运行 Docker 的主机就成为一个 `Swarm` 集群的节点 (`node`) 。

节点分为管理 (`manager`) 节点和工作 (`worker`) 节点。

管理节点用于 `Swarm` 集群的管理，`docker swarm` 命令基本只能在管理节点执行（节点退出集群命令 `docker swarm leave` 可以在工作节点执行）。一个 `Swarm` 集群可以有多个管理节点，但只有一个管理节点可以成为 `leader`，`leader` 通过 `raft` 协议实现。

工作节点是任务执行节点，管理节点将服务 (`service`) 下发至工作节点执行。管理节点默认也作为工作节点。你也可以通过配置让服务只运行在管理节点。

来自 Docker 官网的这张图片形象的展示了集群中管理节点与工作节点的关系。

![](https://docs.docker.com/engine/swarm/images/swarm-diagram.png)

### 服务和任务

任务 （`Task`）是 `Swarm` 中的最小的调度单位，目前来说就是一个单一的容器。

服务 （`Services`） 是指一组任务的集合，服务定义了任务的属性。服务有两种模式：

* `replicated services` 按照一定规则在各个工作节点上运行指定个数的任务。

* `global services` 每个工作节点上运行一个任务

两种模式通过 `docker service create` 的 `--mode` 参数指定。

来自 Docker 官网的这张图片形象的展示了容器、任务、服务的关系。

![](https://docs.docker.com/engine/swarm/images/services-diagram.png)
