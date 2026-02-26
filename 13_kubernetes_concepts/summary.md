## 本章小结

Kubernetes 是当前最主流的容器编排平台，其声明式管理模型和丰富的 API 为大规模容器化应用提供了坚实的基础。

| 概念 | 要点 |
|------|------|
| **Pod** | 最小调度单位，包含一组共享网络和存储的容器 |
| **Deployment** | 管理 Pod 副本集，支持滚动更新和回滚 |
| **Service** | 为 Pod 提供稳定的网络访问入口和负载均衡 |
| **Namespace** | 资源隔离和多租户支持 |
| **ConfigMap/Secret** | 配置与敏感信息的管理 |
| **Master 节点** | 运行 API Server、Scheduler、Controller Manager |
| **Worker 节点** | 运行 kubelet、kube-proxy 和容器运行时 |

### 13.6.1 延伸阅读

- [部署 Kubernetes](../14_kubernetes_setup/README.md)：搭建 Kubernetes 集群
- [Etcd](../15_etcd/README.md)：Kubernetes 使用的分布式存储
- [底层实现](../12_implementation/README.md)：容器技术原理
