## 简介

随着容器技术的普及，目前主流的云计算服务商都提供了成熟的容器服务。与容器相关的云计算服务主要分为以下几种类型：

### 1。容器编排托管服务

这是目前最主流的形式。云厂商托管 Kubernetes 的控制平面 (Master 节点)，用户只需管理工作节点 (Worker Node)。
* **优势**：降低了 Kubernetes 集群的维护成本，高可用性由厂商保证。
* **典型服务**：AWS EKS，Azure AKS，Google GKE，阿里云 ACK，腾讯云 TKE。

### 2。容器实例服务

这一类服务通常被称为 CaaS (Container as a Service)。用户无需管理底层服务器 (EC2/CVM)，只需提供镜像和配置即可运行容器。
* **优势**：极致的弹性，按秒计费，零运维。
* **典型服务**：AWS Fargate，Azure Container Instances，Google Cloud Run，阿里云 ECI。

### 3。镜像仓库服务

提供安全、可靠的私有 Docker 镜像存储服务，通常与云厂商的 CI/CD 流水线深度集成。
* **典型服务**：AWS ECR，Azure ACR，Google GCR/GAR，阿里云 ACR。

本章将介绍如何在几个主流云平台上使用 Docker 和 Kubernetes 服务。
