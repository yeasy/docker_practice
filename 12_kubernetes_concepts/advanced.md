## 12.4 Kubernetes 高级特性

掌握了 Kubernetes 的核心概念 (Pod，Service，Deployment) 后，我们需要了解更多高级特性以构建生产级应用。

### 12.4.1 Helm - 包管理工具

[Helm](https://helm.sh/) 被称为 Kubernetes 的包管理器 (类似于 Linux 的 apt/yum)。它将一组 Kubernetes 资源定义文件打包为一个 **Chart**。

*   **安装应用**：`helm install my-release bitnami/mysql`
*   **版本管理**：轻松回滚应用的发布版本。
*   **模板化**：支持复杂的应用部署逻辑配置。

### 12.4.2 Ingress - 服务的入口

Service 虽然提供了负载均衡，但通常是 4 层 (TCP/UDP)。**Ingress** 提供了 7 层 (HTTP/HTTPS) 路由能力，充当集群的网关。

*   **域名路由**：基于 Host 将请求转发不同服务 (api.example.com -> api-svc，web.example.com -> web-svc)。
*   **路径路由**：基于 Path 将请求转发 (/api -> api-svc， / -> web-svc)。
*   **SSL/TLS**：集中管理证书。

常见的 Ingress Controller 有 Nginx Ingress Controller，Traefik，Istio Gateway 等。

### 12.4.3 Persistent Volume 与 StorageClass

容器内的文件是临时的。对于有状态应用 (如数据库)，需要持久化存储。

*   **PVC (Persistent Volume Claim)**：用户申请存储的声明。
*   **PV (Persistent Volume)**：实际的存储资源 (NFS，AWS EBS，Ceph 等)。
*   **StorageClass**：定义存储类，支持动态创建 PV。

### 12.4.4 Horizontal Pod Autoscaling

HPA 根据 CPU 利用率或其他指标 (如内存、自定义指标) 自动扩缩 Deployment 或 ReplicaSet 中的 Pod 数量。

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-apache
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

### 12.4.5 ConfigMap 与 Secret

*   **ConfigMap**：存储非机密的配置数据 (配置文件、环境变量)。
*   **Secret**：存储机密数据 (密码、Token、证书)，在 Etcd 中加密存储。

通过将配置与镜像分离，保证了容器的可移植性。
