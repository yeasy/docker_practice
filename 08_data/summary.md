## 本章小结

本章介绍了 Docker 的三种数据管理方式：数据卷 (Volume)、绑定挂载 (Bind Mount) 和 tmpfs 挂载。

| 方式 | 特点 | 适用场景 |
|------|------|---------|
| **数据卷 (Volume)** | Docker 管理，生命周期独立于容器 | 数据库、应用数据（推荐生产环境） |
| **绑定挂载 (Bind Mount)** | 挂载宿主机目录，更灵活 | 开发环境、配置文件、日志 |
| **tmpfs 挂载** | 仅存储在内存中，容器停止即消失 | 临时敏感数据、高速缓存 |

| 操作 | 命令 |
|------|------|
| 创建数据卷 | `docker volume create name` |
| 列出数据卷 | `docker volume ls` |
| 查看详情 | `docker volume inspect name` |
| 删除数据卷 | `docker volume rm name` |
| 清理未用 | `docker volume prune` |
| 挂载数据卷 | `-v name:/path` 或 `--mount source=name,target=/path` |

### 延伸阅读

- [数据卷](8.1_volume.md)：Docker 管理的持久化存储
- [绑定挂载](8.2_bind-mounts.md)：挂载宿主机目录
- [tmpfs 挂载](8.3_tmpfs.md)：内存中的临时存储
- [存储驱动](../12_implementation/12.4_ufs.md)：Docker 存储的底层原理
- [Compose 数据管理](../11_compose/11.5_compose_file.md)：Compose 中的挂载配置
---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/docker_practice/issues) 或 [PR](https://github.com/yeasy/docker_practice/pulls)。
