# 第十七章 容器其它生态

> **版本说明**：本章介绍的工具和运行时（Podman、Buildah、Skopeo、containerd、Kata Containers、gVisor、WasmEdge 等）都保持活跃的开发。建议：
> - 查阅各项目官方文档获取最新版本
> - 在生产环境使用前验证版本兼容性
> - 关注官方发布说明了解重大变更

本章将介绍 Docker 和 Kubernetes 之外的容器生态技术。

## 本章内容

* [Fedora CoreOS 简介](17.1_coreos_intro.md)
  * 专为容器化工作负载设计的操作系统。

* [Fedora CoreOS 安装与配置](17.2_coreos_install.md)
  * CoreOS 的安装方式与基本配置。

* [Podman](17.3_podman.md)
  * 兼容 Docker CLI 的下一代无守护进程容器引擎。

* [Buildah](17.4_buildah.md)
  * 无需守护进程的 OCI 容器镜像构建工具。

* [Skopeo](17.5_skopeo.md)
  * 远程检查和管理容器镜像的利器。

* [containerd](17.6_containerd.md)
  * 作为现代容器生态基石的核心容器运行时。

* [安全容器运行时](17.7_secure_runtime.md)
  * 通过提供更强隔离性来保证安全的技术方案（如 Kata Containers、gVisor）。

* [WebAssembly](17.8_wasm.md)
  * 一种极具潜力的轻量级跨平台二进制指令格式。
