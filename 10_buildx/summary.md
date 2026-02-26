## 本章小结

Docker Buildx 是 Docker 构建系统的重要进化，提供了高效、安全且支持多平台的镜像构建能力。

| 概念 | 要点 |
|------|------|
| **BuildKit** | 下一代构建引擎，Docker 23.0+ 默认启用 |
| **缓存挂载** | `RUN --mount=type=cache` 加速依赖安装 |
| **Secret 挂载** | `RUN --mount=type=secret` 安全传递密钥 |
| **buildx build** | 替代 `docker build`，支持更多构建功能 |
| **多架构构建** | `--platform` 参数一键构建多种架构镜像 |
| **Manifest List** | 多架构镜像的索引文件 |
| **SBOM** | 通过 `--sbom=true` 生成软件物料清单 |

### 10.4.1 延伸阅读

- [Dockerfile 指令详解](../07_dockerfile/README.md)：Dockerfile 编写基础
- [多阶段构建](../07_dockerfile/7.17_multistage_builds.md)：优化镜像体积
- [Dockerfile 最佳实践](../appendix/best_practices.md)：编写高效 Dockerfile
