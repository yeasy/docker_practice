## 本章小结

etcd 是 Kubernetes 的核心存储组件，为分布式系统提供可靠的键值存储和服务发现能力。

| 概念 | 要点 |
|------|------|
| **定位** | 分布式键值存储系统，用于配置管理和服务发现 |
| **协议** | 基于 Raft 一致性算法，保证数据强一致 |
| **API** | 提供 gRPC 和 HTTP API |
| **集群** | 建议使用奇数节点 (3 或 5 个) 部署 |
| **etcdctl** | 命令行管理工具，支持 put/get/del/watch 等操作 |
| **安全** | 支持 TLS 加密通信和 RBAC 访问控制 |

### 15.5.1 延伸阅读

- [容器编排基础](../13_kubernetes_concepts/README.md)：Kubernetes 如何使用 etcd
- [部署 Kubernetes](../14_kubernetes_setup/README.md)：在集群中部署 etcd
