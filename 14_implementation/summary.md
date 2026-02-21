## 本章小结

| Namespace | 隔离内容 | 一句话说明 |
|-----------|---------|-----------|
| PID | 进程 ID | 容器有自己的进程树 |
| NET | 网络 | 容器有自己的 IP 和端口 |
| MNT | 文件系统 | 容器有自己的根目录 |
| UTS | 主机名 | 容器有自己的 hostname |
| IPC | 进程间通信 | 容器间 IPC 隔离 |
| USER | 用户 ID | 容器 root ≠ 宿主机 root |

### 延伸阅读

- [控制组 (Cgroups)](14.3_cgroups.md)：资源限制机制
- [联合文件系统](14.4_ufs.md)：分层存储的实现
- [安全](../11_ops/security/README.md)：容器安全实践
- [Linux Namespace 官方文档](https://man7.org/linux/man-pages/man7/namespaces.7.html)

| 资源 | 限制参数 | 示例 |
|------|---------|------|
| **内存** | `-m` | `-m 512m` |
| **CPU 核心数** | `--cpus` | `--cpus=1.5` |
| **CPU 绑定** | `--cpuset-cpus` | `--cpuset-cpus="0,1"` |
| **磁盘 I/O** | `--device-write-bps` | `--device-write-bps /dev/sda:10mb` |
| **进程数** | `--pids-limit` | `--pids-limit=100` |

### 延伸阅读

- [命名空间](14.2_namespace.md)：资源隔离
- [安全](../11_ops/security/README.md)：容器安全概述
- [Docker Stats](../05_container/README.md)：监控容器资源

| 概念 | 说明 |
|------|------|
| **UnionFS** | 将多层目录联合挂载为一个文件系统 |
| **Copy-on-Write** | 写时复制，修改时才复制到可写层 |
| **overlay2** | Docker 默认推荐的存储驱动 |
| **分层好处** | 镜像复用、快速构建、快速启动 |

### 延伸阅读

- [镜像](../02_basic_concept/2.1_image.md)：理解镜像分层
- [容器](../02_basic_concept/2.2_container.md)：容器存储层
- [构建镜像](../04_image/4.5_build.md)：Dockerfile 层的创建
