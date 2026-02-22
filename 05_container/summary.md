## 5.7 本章小结

相关信息如下表：

| 操作 | 命令 | 说明 |
|------|------|------|
| 新建并运行 | `docker run` | 最常用的启动方式 |
| 交互式启动 | `docker run -it` | 用于调试或临时操作 |
| 后台运行 | `docker run -d` | 用于服务类应用 |
| 启动已停止的容器 | `docker start` | 重用已有容器 |

### 5.7.1 延伸阅读

- [后台运行](5.2_daemon.md)：理解 `-d` 参数和容器生命周期
- [进入容器](5.4_attach_exec.md)：操作运行中的容器
- [网络配置](../08_data_network/network/README.md)：理解端口映射的原理
- [数据管理](../08_data_network/README.md)：数据持久化方案

| 操作 | 命令 | 说明 |
|------|------|------|
| 优雅停止 | `docker stop` | 先 SIGTERM，超时后 SIGKILL |
| 强制停止 | `docker kill` | 直接 SIGKILL |
| 重新启动 | `docker start` | 启动已停止的容器 |
| 重启 | `docker restart` | 停止后立即启动 |
| 停止全部 | `docker stop $(docker ps -q)` | 停止所有运行中容器 |

### 5.7.2 延伸阅读

- [启动容器](../05_container/5.1_run.md)：容器启动详解
- [删除容器](5.6_rm.md)：清理容器
- [容器日志](5.2_daemon.md)：排查停止原因

| 需求 | 推荐命令 |
|------|---------|
| 进入容器调试 | `docker exec -it 容器名 bash` |
| 执行单条命令 | `docker exec 容器名 命令` |
| 查看主进程输出 | `docker attach 容器名` (慎用)|

### 5.7.3 延伸阅读

- [后台运行](5.2_daemon.md)：理解容器主进程
- [查看容器](5.1_run.md)：列出和过滤容器
- [容器日志](5.2_daemon.md)：查看容器输出

| 操作 | 命令 |
|------|------|
| 删除已停止容器 | `docker rm 容器名` |
| 强制删除运行中容器 | `docker rm -f 容器名` |
| 删除容器及匿名卷 | `docker rm -v 容器名` |
| 清理所有已停止容器 | `docker container prune` |
| 删除所有容器 | `docker rm -f $(docker ps -aq)` |

### 5.7.4 延伸阅读

- [终止容器](5.3_stop.md)：优雅停止容器
- [删除镜像](../04_image/4.3_rm.md)：清理镜像
- [数据卷](../08_data_network/data/volume.md)：数据卷管理
