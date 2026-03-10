## 本章小结

本章深入介绍了 Docker 的底层实现，包括命名空间、控制组和联合文件系统三大核心技术。

| 技术 | 作用 | 要点 |
|------|------|------|
| **Namespace** | 资源隔离 | PID、NET、MNT、UTS、IPC、USER 六种命名空间 |
| **Cgroups** | 资源限制 | 限制 CPU、内存、磁盘 I/O、进程数 |
| **Union FS** | 分层存储 | overlay2 为推荐驱动，支持 Copy-on-Write |

| Namespace | 隔离内容 | 一句话说明 |
|-----------|---------|-----------| 
| PID | 进程 ID | 容器有自己的进程树 |
| NET | 网络 | 容器有自己的 IP 和端口 |
| MNT | 文件系统 | 容器有自己的根目录 |
| UTS | 主机名 | 容器有自己的 hostname |
| IPC | 进程间通信 | 容器间 IPC 隔离 |
| USER | 用户 ID | 容器 root ≠ 宿主机 root |

| 资源 | 限制参数 | 示例 |
|------|---------|------|
| **内存** | `-m` | `-m 512m` |
| **CPU 核心数** | `--cpus` | `--cpus=1.5` |
| **CPU 绑定** | `--cpuset-cpus` | `--cpuset-cpus="0,1"` |
| **磁盘 I/O** | `--device-write-bps` | `--device-write-bps /dev/sda:10mb` |
| **进程数** | `--pids-limit` | `--pids-limit=100` |

### 延伸阅读

- [命名空间](12.2_namespace.md)：资源隔离机制详解
- [控制组 (Cgroups)](12.3_cgroups.md)：资源限制机制
- [联合文件系统](12.4_ufs.md)：分层存储的实现
- [安全](../18_security/README.md)：容器安全实践
- [镜像](../02_basic_concept/2.1_image.md)：理解镜像分层
- [容器](../02_basic_concept/2.2_container.md)：容器存储层
- [构建镜像](../04_image/4.5_build.md)：Dockerfile 层的创建
---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/docker_practice/issues) 或 [PR](https://github.com/yeasy/docker_practice/pulls)。
