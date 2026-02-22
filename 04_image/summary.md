## 4.8 本章小结

相关信息如下表：

| 操作 | 命令 |
|------|------|
| 拉取镜像 | `docker pull 镜像名:标签` |
| 拉取所有标签 | `docker pull -a 镜像名` |
| 指定平台 | `docker pull --platform linux/amd64 镜像名` |
| 用摘要拉取 | `docker pull 镜像名@sha256:...` |

### 4.8.1 延伸阅读

- [列出镜像](4.2_list.md)：查看本地镜像
- [删除镜像](4.3_rm.md)：清理本地镜像
- [镜像加速器](../03_install/3.9_mirror.md)：加速镜像下载
- [Docker Hub](../06_repository/6.1_dockerhub.md)：官方镜像仓库

相关信息如下表：

| 操作 | 命令 |
|------|------|
| 列出所有镜像 | `docker images` |
| 按仓库名过滤 | `docker images nginx` |
| 列出虚悬镜像 | `docker images -f dangling=true` |
| 只输出 ID | `docker images -q` |
| 显示摘要 | `docker images --digests` |
| 自定义格式 | `docker images --format "..."` |
| 查看空间占用 | `docker system df` |

### 4.8.2 延伸阅读

- [获取镜像](4.1_pull.md)：从 Registry 拉取镜像
- [删除镜像](4.3_rm.md)：清理本地镜像
- [镜像](../02_basic_concept/2.1_image.md)：理解镜像概念

相关信息如下表：

| 操作 | 命令 |
|------|------|
| 删除指定镜像 | `docker rmi 镜像名:标签` |
| 强制删除 | `docker rmi -f 镜像名` |
| 删除虚悬镜像 | `docker image prune` |
| 删除未使用镜像 | `docker image prune -a` |
| 批量删除 | `docker rmi $(docker images -q -f ...)` |
| 查看空间占用 | `docker system df` |

### 4.8.3 延伸阅读

- [列出镜像](4.2_list.md)：查看和过滤镜像
- [删除容器](../05_container/5.6_rm.md)：清理容器
- [数据卷](../08_data/volume.md)：清理数据卷
