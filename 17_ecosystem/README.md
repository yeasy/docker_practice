# 第十七章 容器其他生态

> **版本说明**：本章介绍的工具和运行时（Podman、Buildah、Skopeo、containerd、Kata Containers、gVisor、WasmEdge 等）都保持活跃的开发。建议：
> - 查阅各项目官方文档获取最新版本
> - 在生产环境使用前验证版本兼容性
> - 关注官方发布说明了解重大变更

本章将介绍 Docker 和 Kubernetes 之外的容器生态技术。

同时，Docker 自身的生态也在向云构建、AI 本地推理和企业级桌面安全扩展。当前需要额外关注：

* **Docker Model Runner**：在 Docker Desktop / Docker Engine 中管理、运行和服务本地 AI 模型，支持 OpenAI 与 Ollama 兼容 API，并可将 GGUF、Safetensors 等模型文件作为 OCI Artifact 管理。
* **Docker Build Cloud**：通过远程 BuildKit 和共享构建缓存加速本地与 CI 构建，适合多平台镜像和团队共享缓存场景。
* **Docker Offload**：把容器构建和运行卸载到云端，适合 VDI、受限本机或不支持嵌套虚拟化的开发环境。
* **Hardened Docker Desktop / Enhanced Container Isolation (ECI)**：通过更强的命名空间隔离、敏感挂载保护和系统调用限制降低桌面容器逃逸风险。

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
