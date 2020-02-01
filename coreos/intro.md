# Fedora CoreOS 介绍

[Fedora CoreOS](https://getfedora.org/coreos/) 是一个自动更新的，最小的，整体的，以容器为中心的操作系统，不仅适用于集群，而且可独立运行，并针对运行 Kubernetes 进行了优化。它旨在结合 CoreOS Container Linux 和 Fedora Atomic Host 的优点，将 Container Linux 中的 [Ignition](https://github.com/coreos/ignition) 与 [rpm-ostree](https://github.com/coreos/rpm-ostree) 和 Project Atomic 中的 SELinux 强化等技术相集成。其目标是提供最佳的容器主机，以安全，大规模地运行容器化的工作负载。

## FCOS 特性

### 一个最小化操作系统

FCOS 被设计成一个基于容器的最小化的现代操作系统。它比现有的 Linux 安装平均节省 40% 的 RAM（大约 114M ）并允许从 PXE 或 iPXE 非常快速的启动。

### 系统初始化

Ignition 是一种配置实用程序，可读取配置文件（JSON 格式）并根据该配置配置 FCOS 系统。可配置的组件包括存储，文件系统，systemd 和用户。

Ignition 在系统首次启动期间（在 initramfs 中）仅运行一次。由于 Ignition 在启动过程中的早期运行，因此它可以在用户空间开始启动之前重新对磁盘分区，格式化文件系统，创建用户并写入文件。当 systemd 启动时，systemd 服务已被写入磁盘，从而加快了启动时间。

### 自动更新

FCOS 使用 rpm-ostree 系统进行事务性升级。无需像 yum 升级那样升级单个软件包，而是 rpm-ostree 将 OS 升级作为一个原子单元进行。新的 OS 部署在升级期间进行，并在下次重新引导时生效。如果升级出现问题，则一次回滚和重新启动会使系统返回到先前的状态。确保了系统升级对群集容量的影响降到最小。

### 容器工具

对于诸如构建，复制和其他管理容器的任务，FCOS 用一组兼容的容器工具代替了 **Docker CLI** 工具。**podman CLI** 工具支持许多容器运行时功能，例如运行，启动，停止，列出和删除容器和镜像。**skopeo CLI** 工具可以复制，认证和签名镜像。您可以使用 **crictl CLI** 工具来处理 CRI-O 容器引擎中的容器和镜像。

## 参考文档

* [官方文档](https://docs.fedoraproject.org/en-US/fedora-coreos/)
* [openshift 官方文档](https://docs.openshift.com/container-platform/4.3/architecture/architecture-rhcos.html)
