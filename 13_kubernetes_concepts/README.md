# 第十三章 容器编排基础

`Kubernetes` 是 Google 发起的开源容器编排系统，它支持多种云平台与私有数据中心。

`Kubernetes` 负责对容器工作负载进行调度与编排，其目的是让用户通过集群声明式地管理应用，而无需手动干预每个容器的生命周期细节。

Kubernetes 的最小调度单位是 `Pod`。一个 `Pod` 由一组紧密协作的容器构成，它们共享网络命名空间、IP 以及部分存储资源，也可以根据需要对 Pod 进行端口映射。

如果你已经熟悉 Docker，可以用以下对照来理解 Kubernetes 的核心概念：Docker 中的"容器"对应 Kubernetes 的 `Pod`（一个或多个容器的组合）；`docker-compose.yml` 的角色类似于 Kubernetes 的 `Deployment` + `Service` 声明；`docker run` 的端口映射和网络配置，在 Kubernetes 中由 `Service` 和 `Ingress` 接管。掌握这些映射关系，有助于从单机 Docker 平滑过渡到集群编排。

本章将分为 5 节介绍 `Kubernetes`：

* [简介](13.1_intro.md)
* [基本概念](13.2_concepts.md)
* [架构设计](13.3_design.md)
* [高级特性](13.4_advanced.md)
* [实战练习](13.5_practice.md)
