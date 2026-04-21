## 本章小结

本章介绍了 Docker 的三个核心概念：镜像、容器和仓库。

| 概念 | 要点 |
|------|------|
| **镜像是什么** | 只读的应用模板，包含运行所需的一切 |
| **分层存储** | 多层叠加，共享基础层，节省空间 |
| **只读特性** | 构建后不可修改，保证一致性 |
| **层的陷阱** | 删除操作只是标记，不减小体积 |
| **容器是什么** | 镜像的运行实例，本质是隔离的进程 |
| **容器 vs 虚拟机** | 共享内核，更轻量，但隔离性较弱 |
| **存储层** | 可写层随容器删除而消失 |
| **数据持久化** | 使用 Volume 或 Bind Mount |
| **生命周期** | 与主进程 (PID 1) 绑定 |
| **Registry** | 存储和分发镜像的服务 |
| **仓库 (Repository)** | 同一软件的镜像集合 |
| **标签 (Tag)** | 版本标识，默认为 latest |
| **Docker Hub** | 默认的公共 Registry |
| **私有 Registry** | 企业内部使用，推荐 Harbor |

现在你已经了解了 Docker 的三个核心概念：[镜像](2.1_image.md)、[容器](2.2_container.md) 和仓库。接下来，让我们开始 [安装 Docker](../03_install/README.md)，动手实践！
---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/docker_practice/issues) 或 [PR](https://github.com/yeasy/docker_practice/pulls)。
