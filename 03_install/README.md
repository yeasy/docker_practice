# 第三章 安装 Docker

Docker Engine 主要提供 `stable` 和 `test` 两个更新频道；`test.docker.com` 对应测试频道，适合预发布验证，不建议直接用于生产环境。

官方网站上有各种环境下的[安装指南](https://docs.docker.com/get-docker/)，这里主要介绍 Docker 在 `Linux`、`Windows 10/11` 和 `macOS` 上的安装。

## 安装方式选择指南

在开始安装前，笔者建议你根据以下决策树选择最合适的安装方式：

### 生产环境 vs 开发环境

**生产环境**（服务器部署）：

- 优先使用**官方 APT/YUM 源安装**（Ubuntu、Debian、Fedora、CentOS）
- 优势：获得官方安全更新、长期技术支持、版本管理清晰
- 安装步骤稍多一些，但这种“麻烦”是值得的——它为你的生产系统争取了稳定性和可维护性

**开发环境**（本地开发机、测试服务器）：

- 使用**脚本自动安装**或**包管理器直接安装**
- 如果你想快速上手，官方脚本（`get.docker.com`）是最便捷的选择
- 国内用户注意：这一步一定要选对镜像源，否则网络卡顿会严重影响体验

### 国内用户的网络优化建议

值得注意的是，国内直接访问 Docker 官方源速度较慢，建议：

- **安装过程**：使用阿里云、腾讯云等国内镜像源
- **镜像拉取**：安装完成后配置 Docker 镜像加速器（详见 [3.9 镜像加速器](3.9_mirror.md)），这一步对日常开发的体验提升最明显

### 特殊场景

- **Raspberry Pi/ARM 平台**：见 [3.5 Raspberry Pi](3.5_raspberry-pi.md)
- **离线环境**：见 [3.6 Linux 离线安装](3.6_offline.md)
- **macOS/Windows**：Docker Desktop 是官方推荐的一站式解决方案
- **需要实验特性**：见 [3.10 开启实验特性](3.10_experimental.md)

## 详细安装指南

* [Ubuntu](3.1_ubuntu.md)
* [Debian](3.2_debian.md)
* [Fedora](3.3_fedora.md)
* [CentOS](3.4_centos.md)
* [Raspberry Pi](3.5_raspberry-pi.md)
* [Linux 离线安装](3.6_offline.md)
* [macOS](3.7_mac.md)
* [Windows 10/11](3.8_windows.md)
* [镜像加速器](3.9_mirror.md)
* [开启实验特性](3.10_experimental.md)
