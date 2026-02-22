## 3.11 本章小结

Docker 支持在多种平台上安装和使用，选择合适的安装方式是顺利使用 Docker 的第一步。

| 平台 | 推荐方式 | 说明 |
|------|---------|------|
| **Ubuntu/Debian** | 官方 APT 仓库 | 最完善的支持，推荐首选 |
| **CentOS/Fedora** | 官方 YUM/DNF 仓库 | 注意关闭 SELinux 或配置策略 |
| **macOS** | Docker Desktop | 图形化安装，包含 Compose 和 Kubernetes |
| **Windows 10/11** | Docker Desktop (WSL 2) | 需启用 WSL 2 后端 |
| **Raspberry Pi** | 官方安装脚本 | 支持 ARM 架构 |
| **离线环境** | 二进制包安装 | 适用于无法联网的服务器 |

### 3.11.1 安装后验证

安装完成后，运行以下命令验证 Docker 是否正常工作：

```bash
$ docker version
$ docker run --rm hello-world
```

### 3.11.2 延伸阅读

- [镜像加速器](3.9_mirror.md)：解决国内拉取镜像慢的问题
- [开启实验特性](3.10_experimental.md)：使用最新功能
- [Docker Hub](../06_repository/6.1_dockerhub.md)：官方镜像仓库
