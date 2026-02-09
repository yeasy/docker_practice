## Kubernetes 简介

Kubernetes 简介 示意图如下：

![](../_images/kubernetes_logo.png)

### 什么是 Kubernetes

Kubernetes（常简称为 K8s）是 Google 开源的容器编排引擎。如果说 Docker 解决了"如何打包和运送集装箱"的问题，那么 Kubernetes 解决的就是"如何管理海量集装箱的调度、运行和维护"的问题。

它不仅仅是一个编排系统，更是一个**云原生应用操作系统**。

> **名字由来**：Kubernetes 在希腊语中意为"舵手"或"飞行员"。K8s 是因为 k 和 s 之间有 8 个字母。

---

### 为什么需要 Kubernetes

当我们在单机运行几个容器时，Docker Compose 就足够了。但在生产环境中，我们需要面对：

- **多主机调度**：容器应该运行在哪台机器上？
- **自动恢复**：容器崩溃了怎么办？节点挂了怎么办？
- **服务发现**：容器 IP 变了，其他服务怎么找到它？
- **负载均衡**：流量大了，如何分发给多个副本？
- **滚动更新**：如何不中断服务升级应用？

Kubernetes 完美解决了这些问题。

---

### 核心概念

#### Pod（豆荚）

Kubernetes 的最小调度单位。一个 Pod 可以包含一个或多个紧密协作的容器（共享网络和存储）。就像豌豆荚里的豌豆一样。

#### Node（节点）

运行 Pod 的物理机或虚拟机。

#### Deployment（部署）

定义应用的期望状态（如：需要 3 个副本，镜像版本为 v1）。K8s 会持续确保当前状态符合期望状态。

#### Service（服务）

定义一组 Pod 的访问策略。提供稳定的 Cluster IP 和 DNS 名称，负责负载均衡。

#### Namespace（命名空间）

用于多租户资源隔离。

---

### Docker 用户如何过渡

如果你已经熟悉 Docker，学习 K8s 会很容易：

| Docker 概念 | Kubernetes 概念 | 说明 |
|------------|----------------|------|
| Container  | Pod            | K8s 增加了一层 Pod 包装 |
| Volume     | PersistentVolume | K8s 的存储更加抽象和强大 |
| Network    | Service/Ingress| K8s 的网络模型更扁平 |
| Compose    | Deployment + Service | 声明式配置的理念是一致的 |

---

### 架构

Kubernetes 也是 C/S 架构，由 **Master (控制平面)**和**Worker (工作节点)** 组成：

- **Control Plane**：负责决策（API Server, Scheduler, Controller Manager, etcd）
- **Worker Node**：负责干活（Kubelet, Kube-proxy, Container Runtime）

---

### 学习建议

Kubernetes 的学习曲线较陡峭。建议的学习路径：
1. **理解基本概念**：Pod, Deployment, Service
2. **动手实践**：使用 Minikube 或 Kind 在本地搭建集群
3. **部署应用**：编写 YAML 部署一个无状态应用
4. **深入原理**：网络模型、存储机制、调度算法

---

### 延伸阅读

- [Minikube 安装](../kubernetes/setup/README.md)：本地体验 K8s
- [Kubernetes 官网](https://kubernetes.io/)：官方文档
