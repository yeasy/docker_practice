## 本章小结

本章详细介绍了 Dockerfile 的所有核心指令，以下是各指令要点的速查表。

| 指令 | 作用 | 关键要点 |
|------|------|---------|
| **FROM** | 指定基础镜像 | 必须是第一条指令 |
| **RUN** | 在新层执行命令 | 合并命令、清理缓存以减小体积 |
| **COPY** | 复制文件 | 优先使用，支持 `--from` |
| **ADD** | 更高级的复制 | 自动解压 tar，不推荐用于下载 |
| **CMD** | 容器启动默认命令 | 可被 `docker run` 参数覆盖 |
| **ENTRYPOINT** | 容器入口点 | 固定启动命令，CMD 作为默认参数 |
| **ENV** | 设置环境变量 | 构建时 + 运行时均生效 |
| **ARG** | 构建参数 | 仅构建时生效，FROM 后需重新声明 |
| **VOLUME** | 定义匿名卷 | VOLUME 之后的修改会丢失 |
| **EXPOSE** | 声明端口 | 仅文档作用，不自动映射 |
| **WORKDIR** | 指定工作目录 | 替代 `RUN cd`，目录不存在会自动创建 |
| **USER** | 指定运行用户 | 用户必须已存在，推荐 gosu |
| **HEALTHCHECK** | 健康检查 | 支持 starting/healthy/unhealthy 状态 |
| **ONBUILD** | 延迟执行指令 | 只继承一次，不可级联 |
| **LABEL** | 添加元数据 | 推荐 OCI 标准标签，替代 MAINTAINER |
| **SHELL** | 更改默认 shell | 推荐 `["/bin/bash", "-o", "pipefail", "-c"]` |

### 延伸阅读

- [使用 Dockerfile 定制镜像](../04_image/4.5_build.md)：Dockerfile 入门
- [多阶段构建](7.17_multistage_builds.md)：优化镜像大小
- [Dockerfile 最佳实践](../appendix/best_practices.md)：编写指南
- [安全](../18_security/README.md)：容器安全实践
- [Compose 模板文件](../11_compose/11.5_compose_file.md)：Compose 中的配置
---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/docker_practice/issues) 或 [PR](https://github.com/yeasy/docker_practice/pulls)。
