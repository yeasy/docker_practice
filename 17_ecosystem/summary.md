## 本章小结

Docker 并非容器生态的唯一选择，了解其他工具有助于根据场景做出合适的技术选型。

| 项目 | 定位 | 特点 |
|------|------|------|
| **Fedora CoreOS** | 容器化操作系统 | 自动更新、不可变基础设施、专为运行容器设计 |
| **Podman** | 容器管理引擎 | 无守护进程、兼容 Docker CLI、支持 Rootless 模式、支持原生 Pod |
| **Buildah** | 镜像构建工具 | Daemonless 工作模式、灵活的脚本化构建能力 |
| **Skopeo** | 镜像仓库管理 | 无需拉取即可检查远端镜像、跨仓库/格式无缝迁移镜像 |
| **containerd** | 核心底层运行时 | 稳定高效、符合 CRI 规范、是 Docker 的基石之一 |
| **安全容器** | 强隔离沙箱运行 | 利用轻量级虚拟机 (Kata) 或用户态内核 (gVisor) 防止越狱，极其安全 |
| **Wasm** | 新型工作负载 | 体积极小、冷启动超快且具备跨平台及高度特征化沙盒能力的后端架构新方向 |

### Podman vs Docker

两者的主要区别：

| 对比项 | Docker | Podman |
|--------|--------|--------|
| **守护进程** | 需要 dockerd | 无需守护进程 |
| **权限** | 默认需要 root | 原生支持 Rootless |
| **CLI 兼容** | - | 与 Docker 命令兼容 |
| **Pod 支持** | 不支持 | 原生支持 Pod 概念 |
| **Compose** | docker compose | podman-compose 或兼容模式 |

### 延伸阅读

- [底层实现](../12_implementation/README.md)：容器技术的内核基础
- [安全](../18_security/README.md)：容器安全实践
