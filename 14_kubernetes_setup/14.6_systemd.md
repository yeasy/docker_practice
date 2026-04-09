## 14.6 一步步部署 Kubernetes 集群

### 14.6.1 概述

部署 Kubernetes 集群涉及多个组件的安装和配置，包括 Master 节点和 Worker 节点。本章介绍如何使用 systemd 管理这些服务的生命周期。

### 14.6.2 Kubernetes 主要组件

#### Master 节点组件

- **kube-apiserver**：API 服务器，Kubernetes 集群的中心
- **kube-controller-manager**：控制器管理器
- **kube-scheduler**：调度器，负责 Pod 调度
- **etcd**：分布式键值存储，存储集群数据

#### Worker 节点组件

- **kubelet**：节点代理，管理容器生命周期
- **kube-proxy**：网络代理，处理服务网络
- **Container Runtime**：容器运行时（Docker、containerd 等）

### 14.6.3 使用 systemd 管理 Kubernetes 服务

#### 服务单元文件

为了让 systemd 管理 Kubernetes 服务，需要创建相应的 `.service` 文件，例如：

```text
/etc/systemd/system/kubelet.service
/etc/systemd/system/kube-proxy.service
/etc/systemd/system/kube-apiserver.service
```

#### 常用命令

```bash
# 启动服务
sudo systemctl start kubelet

# 停止服务
sudo systemctl stop kubelet

# 重启服务
sudo systemctl restart kubelet

# 查看服务状态
sudo systemctl status kubelet

# 设置开机自启
sudo systemctl enable kubelet
```

如果希望查看更完整的 systemd 部署案例，可以参考 `opsnull/follow-me-install-kubernetes-cluster` 这类社区项目，再结合本章前文的 kubeadm 与组件配置说明理解整体流程。

### 14.6.4 推荐学习路径

1. 理解 Kubernetes 架构和各组件的作用
2. 准备所需的系统环境（Linux 主机、网络配置等）
3. 按步骤安装各个 Kubernetes 组件
4. 配置 systemd 服务单元文件
5. 验证集群健康状态
