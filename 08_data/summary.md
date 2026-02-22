## 8.5 本章小结

相关信息如下表：

| 要点 | 说明 |
|------|------|
| **作用** | 将宿主机目录挂载到容器 |
| **语法** | `-v /宿主机:/容器` 或 `--mount type=bind,...` |
| **只读** | 添加 `readonly` 或 `:ro` |
| **适用场景** | 开发环境、配置文件、日志 |
| **vs Volume** | Bind 更灵活，Volume 更适合生产 |

### 8.5.1 延伸阅读

- [数据卷](volume.md)：Docker 管理的持久化存储
- [tmpfs 挂载](tmpfs.md)：内存临时存储
- [Compose 数据管理](../11_compose/11.5_compose_file.md)：Compose 中的挂载配置

| 操作 | 命令 |
|------|------|
| 创建数据卷 | `docker volume create name` |
| 列出数据卷 | `docker volume ls` |
| 查看详情 | `docker volume inspect name` |
| 删除数据卷 | `docker volume rm name` |
| 清理未用 | `docker volume prune` |
| 挂载数据卷 | `-v name:/path` 或 `--mount source=name,target=/path` |

### 8.5.2 延伸阅读

- [绑定挂载](bind-mounts.md)：挂载宿主机目录
- [tmpfs 挂载](tmpfs.md)：内存中的临时存储
- [存储驱动](../12_implementation/12.4_ufs.md)：Docker 存储的底层原理
