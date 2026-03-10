## 本章小结

本章介绍了 Docker 容器的启动、停止、进入和删除等核心操作。

| 操作 | 命令 | 说明 |
|------|------|------|
| 新建并运行 | `docker run` | 最常用的启动方式 |
| 交互式启动 | `docker run -it` | 用于调试或临时操作 |
| 后台运行 | `docker run -d` | 用于服务类应用 |
| 启动已停止的容器 | `docker start` | 重用已有容器 |
| 优雅停止 | `docker stop` | 先 SIGTERM，超时后 SIGKILL |
| 强制停止 | `docker kill` | 直接 SIGKILL |
| 重启 | `docker restart` | 停止后立即启动 |
| 停止全部 | `docker stop $(docker ps -q)` | 停止所有运行中容器 |
| 进入容器调试 | `docker exec -it 容器名 bash` | 推荐方式 |
| 执行单条命令 | `docker exec 容器名 命令` | 不进入交互模式 |
| 查看主进程输出 | `docker attach 容器名` | 慎用，退出可能停止容器 |
| 删除已停止容器 | `docker rm 容器名` | 需先停止 |
| 强制删除运行中容器 | `docker rm -f 容器名` | 直接删除 |
| 删除容器及匿名卷 | `docker rm -v 容器名` | 同时清理匿名卷 |
| 清理所有已停止容器 | `docker container prune` | 批量清理 |

### 延伸阅读

- [后台运行](5.2_daemon.md)：理解 `-d` 参数和容器生命周期
- [进入容器](5.4_attach_exec.md)：操作运行中的容器
- [网络配置](../09_network/README.md)：理解端口映射的原理
- [数据管理](../08_data/README.md)：数据持久化方案
- [删除镜像](../04_image/4.3_rm.md)：清理镜像
- [数据卷](../08_data/8.1_volume.md)：数据卷管理
---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/docker_practice/issues) 或 [PR](https://github.com/yeasy/docker_practice/pulls)。
