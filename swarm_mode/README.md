# Swarm mode

Docker 1.12 [Swarm mode](https://docs.docker.com/engine/swarm/) 已经内嵌入 Docker 引擎，成为了 docker 子命令 `docker swarm`。请注意与旧的 `Docker Swarm` 区分开来。

`Swarm mode` 内置 kv 存储功能，提供了众多的新特性，比如：具有容错能力的去中心化设计、内置服务发现、负载均衡、路由网格、动态伸缩、滚动更新、安全传输等。

> **定位说明**：Swarm mode 适合小型团队和简单的容器编排场景，具有学习成本低、配置简单的优势。对于大规模生产部署、复杂的微服务架构，建议使用 [Kubernetes](../kubernetes/README.md)，它拥有更丰富的生态系统和更强大的扩展能力。
