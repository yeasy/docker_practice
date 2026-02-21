## 本章小结

| 概念 | 要点 |
|------|------|
| **镜像是什么** | 只读的应用模板，包含运行所需的一切 |
| **分层存储** | 多层叠加，共享基础层，节省空间 |
| **只读特性** | 构建后不可修改，保证一致性 |
| **层的陷阱** | 删除操作只是标记，不减小体积 |

理解了镜像，接下来让我们学习[容器](2.2_container.md)——镜像的运行实例。

### 延伸阅读

- [获取镜像](../04_image/4.1_pull.md)：从 Registry 下载镜像
- [使用 Dockerfile 定制镜像](../04_image/4.5_build.md)：创建自己的镜像
- [Dockerfile 最佳实践](../16_appendix/16.1_best_practices.md)：构建高质量镜像的技巧
- [底层实现 - 联合文件系统](../14_implementation/14.4_ufs.md)：深入理解分层存储的技术原理

| 概念 | 要点 |
|------|------|
| **容器是什么** | 镜像的运行实例，本质是隔离的进程 |
| **容器 vs 虚拟机** | 共享内核，更轻量，但隔离性较弱 |
| **存储层** | 可写层随容器删除而消失 |
| **数据持久化** | 使用 Volume 或 Bind Mount |
| **生命周期** | 与主进程（PID 1）绑定 |

理解了镜像和容器，接下来让我们学习[仓库](2.3_repository.md)——存储和分发镜像的服务。

### 延伸阅读

- [启动容器](../05_container/5.1_run.md)：详细的容器启动选项
- [后台运行](../05_container/5.2_daemon.md)：理解容器为什么会 “立即退出”
- [进入容器](../05_container/5.4_attach_exec.md)：如何操作运行中的容器
- [数据管理](../08_data_network/README.md)：Volume 和数据持久化详解

| 概念 | 要点 |
|------|------|
| **Registry** | 存储和分发镜像的服务 |
| **仓库（Repository）** | 同一软件的镜像集合 |
| **标签（Tag）** | 版本标识，默认为 latest |
| **Docker Hub** | 默认的公共 Registry |
| **私有 Registry** | 企业内部使用，推荐 Harbor |

现在你已经了解了 Docker 的三个核心概念：[镜像](2.1_image.md)、[容器](2.2_container.md)和仓库。接下来，让我们开始[安装 Docker](../03_install/README.md)，动手实践！

### 延伸阅读

- [Docker Hub](../06_repository/6.1_dockerhub.md)：Docker Hub 的详细使用
- [私有仓库](../06_repository/6.2_registry.md)：搭建私有 Registry
- [私有仓库高级配置](../06_repository/6.3_registry_auth.md)：认证、TLS 配置
- [镜像加速器](../03_install/3.9_mirror.md)：配置镜像加速
