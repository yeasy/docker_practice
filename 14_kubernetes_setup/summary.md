## 14.9 本章小结

部署 Kubernetes 集群有多种方式，应根据使用场景选择合适的方案。

| 部署方式 | 适用场景 | 特点 |
|---------|---------|------|
| **kubeadm** | 生产环境 | 官方推荐的集群部署工具 |
| **Docker Desktop** | 本地开发 | 一键启用，开箱即用 |
| **Kind** | CI/CD 测试 | Kubernetes IN Docker，快速创建集群 |
| **K3s** | 边缘计算/IoT | 轻量级，资源占用少 |
| **手动部署** | 学习原理 | 逐步配置每个组件，加深理解 |

### 14.9.1 延伸阅读

- [容器编排基础](../13_kubernetes_concepts/README.md)：Kubernetes 核心概念
- [Dashboard](dashboard.md)：部署可视化管理界面
- [kubectl](kubectl.md)：命令行工具使用指南
