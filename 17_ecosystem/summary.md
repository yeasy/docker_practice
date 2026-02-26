## 本章小结

Docker 并非容器生态的唯一选择，了解其他工具有助于根据场景做出合适的技术选型。

| 项目 | 定位 | 特点 |
|------|------|------|
| **Fedora CoreOS** | 容器化操作系统 | 自动更新、不可变基础设施、专为运行容器设计 |
| **Podman** | 容器引擎 | 无守护进程、兼容 Docker CLI、支持 Rootless 模式 |

### 17.4.1 Podman vs Docker

两者的主要区别：

| 对比项 | Docker | Podman |
|--------|--------|--------|
| **守护进程** | 需要 dockerd | 无需守护进程 |
| **权限** | 默认需要 root | 原生支持 Rootless |
| **CLI 兼容** | - | 与 Docker 命令兼容 |
| **Pod 支持** | 不支持 | 原生支持 Pod 概念 |
| **Compose** | docker compose | podman-compose 或兼容模式 |

### 17.4.2 延伸阅读

- [底层实现](../12_implementation/README.md)：容器技术的内核基础
- [安全](../18_security/README.md)：容器安全实践
