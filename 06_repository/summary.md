## 本章小结

本章介绍了 Docker Hub 的使用、私有仓库的搭建以及 Nexus 3 等企业级方案。

| 功能 | 说明 |
|------|------|
| **官方镜像** | 优先使用的基础镜像 |
| **拉取限制** | 匿名 100 次/6h，登录 200 次/6h |
| **安全** | 推荐开启 2FA 并使用 Access Token |
| **自动化** | 支持 Webhooks 和自动构建 |

### 延伸阅读

- [私有仓库](6.2_registry.md)：搭建自己的 Registry
- [镜像加速器](../03_install/3.9_mirror.md)：加速下载
---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/docker_practice/issues) 或 [PR](https://github.com/yeasy/docker_practice/pulls)。
