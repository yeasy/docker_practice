## 本章小结

Docker Compose 是管理多容器应用的利器，通过 YAML 文件声明式地定义服务、网络和数据卷。

| 概念 | 要点 |
|------|------|
| **核心概念** | 服务 (service) 和项目 (project) |
| **配置文件** | `compose.yaml` (推荐) 或 `docker-compose.yml` |
| **版本** | Compose V2 为 Go 编写的 CLI 插件，通过 `docker compose` 使用 |
| **启动** | `docker compose up -d` 启动所有服务 |
| **停止** | `docker compose down` 停止并移除容器 |
| **查看状态** | `docker compose ps` 查看服务状态 |
| **查看日志** | `docker compose logs` 查看服务日志 |
| **模板文件** | 支持 `services`、`networks`、`volumes` 等顶级配置 |

### 11.10.1 延伸阅读

- [Compose 模板文件](11.5_compose_file.md)：详细模板语法参考
- [Compose 命令说明](11.4_commands.md)：完整命令列表
- [网络配置](../09_network/README.md)：Docker 网络基础
- [数据管理](../08_data/README.md)：数据卷管理
