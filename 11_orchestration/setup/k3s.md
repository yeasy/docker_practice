## K3s - 轻量级 Kubernetes

[K3s](https://k3s.io/) 是一个轻量级的 Kubernetes 发行版，由 Rancher Labs 开发。它专为边缘计算、物联网、CI、ARM 等资源受限的环境设计。K3s 被打包为单个二进制文件，只有不到 100MB，但通过了 CNCF 的一致性测试。

### 核心特性

*   **轻量级**：移除过时的、非必须的 Kubernetes 功能（如传统的云提供商插件），使用 SQLite 作为默认数据存储（也支持 Etcd/MySQL/Postgres）。
*   **单一二进制**：所有组件（API Server, Controller Manager, Scheduler, Kubelet, Kube-proxy）打包在一个进程中运行。
*   **开箱即用**：内置 Helm Controller、Traefik Ingress controller、ServiceLB、Local-Path-Provisioner。
*   **安全**：默认启用安全配置，基于 TLS 通信。

### 安装

K3s 的安装非常简单，官方提供了便捷的安装脚本。

#### 脚本安装（Linux）

K3s 提供了极为便捷的安装脚本：

```bash
curl -sfL https://get.k3s.io | sh -
```

安装完成后，K3s 会自动启动并配置好 `systemd` 服务。

#### 查看状态

运行以下命令：

```bash
sudo k3s kubectl get nodes
```

输出类似：
```
NAME          STATUS   ROLES                  AGE   VERSION
k3s-master    Ready    control-plane,master   1m    v1.28.2+k3s1
```

### 快速使用

K3s 内置了 `kubectl` 命令（通过 `k3s kubectl` 调用），为了方便，通常会建立别名或配置 `KUBECONFIG`。

```bash
## 读取 K3s 的配置文件

export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

## 现在可以直接使用 kubectl

kubectl get pods -A
```

### 清理卸载

运行以下命令：

```bash
/usr/local/bin/k3s-uninstall.sh
```
