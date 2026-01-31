# 删除容器

## 基本用法

使用 `docker rm` 删除已停止的容器：

```bash
$ docker rm 容器名或ID
```

> 💡 `docker rm` 是 `docker container rm` 的简写，两者等效。

---

## 删除选项

| 选项 | 说明 | 示例 |
|------|------|------|
| 无参数 | 删除已停止的容器 | `docker rm mycontainer` |
| `-f` | 强制删除运行中的容器 | `docker rm -f mycontainer` |
| `-v` | 同时删除关联的匿名卷 | `docker rm -v mycontainer` |

### 删除已停止的容器

```bash
$ docker rm mycontainer
mycontainer
```

### 强制删除运行中的容器

```bash
# 不加 -f 会报错
$ docker rm running_container
Error: cannot remove running container

# 加 -f 强制删除
$ docker rm -f running_container
running_container
```

> ⚠️ 强制删除会向容器发送 SIGKILL 信号，可能导致数据丢失。建议先 `docker stop` 优雅停止。

### 删除容器及其数据卷

```bash
# 删除容器时同时删除其匿名卷
$ docker rm -v mycontainer
```

> 注意：只删除匿名卷，命名卷不会被删除。

---

## 批量删除

### 删除所有已停止的容器

```bash
# 方式一：使用 prune 命令（推荐）
$ docker container prune

WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
abc123...
def456...
Total reclaimed space: 150MB

# 方式二：不提示确认
$ docker container prune -f
```

### 删除所有容器（包括运行中的）

```bash
# 先停止所有容器，再删除
$ docker stop $(docker ps -q)
$ docker rm $(docker ps -aq)

# 或者直接强制删除
$ docker rm -f $(docker ps -aq)
```

### 按条件删除

```bash
# 删除所有已退出的容器
$ docker rm $(docker ps -aq -f status=exited)

# 删除名称包含 "test" 的容器
$ docker rm $(docker ps -aq -f name=test)

# 删除 24 小时前创建的容器
$ docker container prune --filter "until=24h"
```

---

## 常用过滤条件

`docker ps` 的过滤条件可以配合 `rm` 使用：

| 过滤条件 | 说明 | 示例 |
|---------|------|------|
| `status=exited` | 已退出的容器 | `-f status=exited` |
| `status=created` | 已创建未启动 | `-f status=created` |
| `name=xxx` | 名称匹配 | `-f name=myapp` |
| `ancestor=xxx` | 基于某镜像创建 | `-f ancestor=nginx` |
| `before=xxx` | 在某容器之前创建 | `-f before=mycontainer` |
| `since=xxx` | 在某容器之后创建 | `-f since=mycontainer` |

### 示例

```bash
# 删除所有基于 nginx 镜像的容器
$ docker rm $(docker ps -aq -f ancestor=nginx)

# 删除所有创建后未启动的容器
$ docker rm $(docker ps -aq -f status=created)
```

---

## 容器与镜像的依赖关系

> 有容器依赖的镜像无法删除。

```bash
# 尝试删除有容器依赖的镜像
$ docker image rm nginx
Error: image is being used by stopped container abc123

# 需要先删除依赖该镜像的容器
$ docker rm abc123
$ docker image rm nginx
```

---

## 清理策略建议

### 开发环境

```bash
# 定期清理已停止的容器
$ docker container prune -f

# 一键清理所有未使用资源
$ docker system prune -f
```

### 生产环境

```bash
# 使用 --rm 参数运行临时容器
$ docker run --rm ubuntu echo "Hello"
# 容器退出后自动删除

# 定期清理（设置保留时间）
$ docker container prune --filter "until=168h"  # 保留 7 天内的
```

### 完整清理脚本

```bash
#!/bin/bash
# cleanup.sh - Docker 资源清理脚本

echo "清理已停止的容器..."
docker container prune -f

echo "清理未使用的镜像..."
docker image prune -f

echo "清理未使用的数据卷..."
docker volume prune -f

echo "清理未使用的网络..."
docker network prune -f

echo "清理完成！"
docker system df
```

---

## 常见问题

### Q: 容器无法删除

```bash
Error: container is running
```

解决：先停止容器，或使用 `-f` 强制删除

```bash
$ docker stop mycontainer
$ docker rm mycontainer
# 或
$ docker rm -f mycontainer
```

### Q: 删除后磁盘空间没释放

可能原因：
1. 容器的数据卷未删除（使用 `-v` 参数）
2. 镜像未删除
3. 构建缓存未清理

解决：

```bash
# 查看空间占用
$ docker system df

# 完整清理
$ docker system prune -a --volumes
```

---

## 本章小结

| 操作 | 命令 |
|------|------|
| 删除已停止容器 | `docker rm 容器名` |
| 强制删除运行中容器 | `docker rm -f 容器名` |
| 删除容器及匿名卷 | `docker rm -v 容器名` |
| 清理所有已停止容器 | `docker container prune` |
| 删除所有容器 | `docker rm -f $(docker ps -aq)` |

## 延伸阅读

- [终止容器](stop.md)：优雅停止容器
- [删除镜像](../image/rm.md)：清理镜像
- [数据卷](../data_management/volume.md)：数据卷管理
