# 第十四章 部署 Kubernetes

目前，Kubernetes 支持在多种环境下使用，包括本地主机 (Ubuntu、Debian、CentOS、Fedora 等)、云服务 ([腾讯云](https://cloud.tencent.com/act/cps/redirect?redirect=10058&cps_key=3a5255852d5db99dcd5da4c72f05df61)、[阿里云](https://www.aliyun.com/product/kubernetes?source=5176.11533457&userCode=8lx5zmtu&type=copy)、[百度云](https://cloud.baidu.com/product/cce.html)等)。

你可以使用以下几种方式部署 Kubernetes，接下来的小节会对各种方式进行详细介绍。

* [使用 kubeadm 部署 (CRI 使用 containerd)](14.1_kubeadm.md)
  * Kubernetes 也支持 CRI-O 等符合 CRI 的运行时；本文以 containerd 为主线。
* [使用 kubeadm 部署 (使用 Docker)](14.2_kubeadm-docker.md)
* [在 Docker Desktop 使用](14.3_docker-desktop.md)
* [Kind - Kubernetes IN Docker](14.4_kind.md)
* [K3s - 轻量级 Kubernetes](14.5_k3s.md)
* [一步步部署 Kubernetes 集群](14.6_systemd.md)
* [部署 Dashboard](14.7_dashboard.md)
* [Kubernetes 命令行 kubectl](14.8_kubectl.md)

除了上述方式，企业生产环境中还有两个常见的部署工具值得关注：

* **[KubeKey](https://github.com/kubesphere/kubekey)**：KubeSphere 社区开源的集群部署工具（CNCF 认证），支持一条命令从裸机部署到高可用集群，内置对 containerd 和多 Linux 发行版的适配，适合需要快速搭建私有化 Kubernetes 的团队。
* **[RKE2](https://docs.rke2.io/)**：SUSE Rancher 出品的安全加固型 Kubernetes 发行版，默认启用 CIS 基准合规、SELinux 支持和 etcd 自动快照，适合对安全审计有严格要求的企业场景。
