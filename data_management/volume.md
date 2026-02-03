# 数据卷

## 为什么需要数据卷

容器的存储层有一个关键问题：**容器删除后，数据就没了**。

```
┌─────────────────────────────────────────────────────────────────┐
│                        容器存储层问题                            │
│                                                                 │
│    容器运行 ─────► 写入数据 ─────► 容器删除 ─────► 数据丢失！     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

数据卷（Volume）解决了这个问题，它的生命周期独立于容器。

---

## 数据卷的特性

| 特性 | 说明 |
|------|------|
| **持久化** | 容器删除后数据仍然保留 |
| **共享** | 多个容器可以挂载同一个数据卷 |
| **即时生效** | 对数据卷的修改立即可见 |
| **不影响镜像** | 数据卷中的数据不会打包进镜像 |
| **性能更好** | 绕过 UnionFS，直接读写 |

---

## 数据卷 vs 容器存储层

```
容器存储层（不推荐存储重要数据）：
┌─────────────────────────────────────────┐
│       容器存储层（可读写）               │
├─────────────────────────────────────────┤
│       镜像层（只读）                     │
└─────────────────────────────────────────┘
  生命周期 = 容器生命周期
  容器删除 → 数据丢失
  
数据卷（推荐）：
┌─────────────────────────────────────────┐
│       容器                              │
│  ┌─────────────────────────────────┐    │
│  │     /app/data ──────────────────│────┼──► 数据卷 my-data
│  └─────────────────────────────────┘    │     (独立于容器)
└─────────────────────────────────────────┘
  容器删除 → 数据卷保留
```

---

## 数据卷基本操作

### 创建数据卷

```bash
$ docker volume create my-vol
```

### 列出所有数据卷

```bash
$ docker volume ls
DRIVER    VOLUME NAME
local     my-vol
local     postgres_data
local     redis_data
```

### 查看数据卷详情

```bash
$ docker volume inspect my-vol
[
    {
        "CreatedAt": "2026-01-15T10:00:00Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/my-vol/_data",
        "Name": "my-vol",
        "Options": {},
        "Scope": "local"
    }
]
```

**关键字段**：
- `Mountpoint`：数据卷在宿主机上的实际存储位置
- `Driver`：存储驱动（默认 local，也可以用第三方驱动）

---

## 挂载数据卷

### 方式一：--mount（推荐）

```bash
$ docker run -d \
    --name web \
    --mount source=my-vol,target=/usr/share/nginx/html \
    nginx
```

**参数说明**：

| 参数 | 说明 |
|------|------|
| `source` | 数据卷名称（不存在会自动创建） |
| `target` | 容器内挂载路径 |
| `readonly` | 可选，只读挂载 |

### 方式二：-v（简写）

```bash
$ docker run -d \
    --name web \
    -v my-vol:/usr/share/nginx/html \
    nginx
```

**格式**：`-v 数据卷名:容器路径[:选项]`

### 两种方式对比

| 特性 | --mount | -v |
|------|---------|-----|
| 语法 | 键值对，更清晰 | 冒号分隔，更简洁 |
| 自动创建卷 | source 不存在会报错 | 自动创建 |
| 推荐程度 | ✅ 推荐（更明确） | 常用（更简洁） |

### 只读挂载

```bash
# --mount 方式
$ docker run -d \
    --mount source=my-vol,target=/data,readonly \
    nginx

# -v 方式
$ docker run -d \
    -v my-vol:/data:ro \
    nginx
```

---

## 使用场景示例

### 场景一：数据库持久化

```bash
# 创建数据卷
$ docker volume create postgres_data

# 启动 PostgreSQL，数据存储在数据卷中
$ docker run -d \
    --name postgres \
    -e POSTGRES_PASSWORD=secret \
    -v postgres_data:/var/lib/postgresql/data \
    postgres:16

# 即使删除容器，数据仍然保留
$ docker rm -f postgres

# 重新启动，数据还在
$ docker run -d \
    --name postgres \
    -e POSTGRES_PASSWORD=secret \
    -v postgres_data:/var/lib/postgresql/data \
    postgres:16
```

### 场景二：多容器共享数据

```bash
# 创建共享数据卷
$ docker volume create shared-data

# 容器 A 写入数据
$ docker run -d --name writer \
    -v shared-data:/data \
    alpine sh -c "while true; do date >> /data/log.txt; sleep 5; done"

# 容器 B 读取数据
$ docker run --rm \
    -v shared-data:/data \
    alpine cat /data/log.txt
```

### 场景三：配置文件持久化

```bash
# 将 nginx 配置存储在数据卷中
$ docker run -d \
    -v nginx-config:/etc/nginx/conf.d \
    -v nginx-logs:/var/log/nginx \
    -p 80:80 \
    nginx
```

---

## 数据卷管理

### 删除数据卷

```bash
# 删除指定数据卷
$ docker volume rm my-vol

# 删除容器时同时删除数据卷
$ docker rm -v container_name
```

### 清理未使用的数据卷

```bash
# 查看未被任何容器使用的数据卷
$ docker volume ls -f dangling=true

# 删除所有未使用的数据卷
$ docker volume prune

# 强制删除（不提示确认）
$ docker volume prune -f
```

> ⚠️ **注意**：数据卷不会自动垃圾回收。长期运行的系统应定期清理无用数据卷。

---

## 数据卷备份与恢复

### 备份数据卷

```bash
# 使用临时容器挂载数据卷，打包备份
$ docker run --rm \
    -v my-vol:/source:ro \
    -v $(pwd):/backup \
    alpine tar czf /backup/my-vol-backup.tar.gz -C /source .
```

**原理**：
1. 创建临时容器
2. 挂载要备份的数据卷到 `/source`
3. 挂载当前目录到 `/backup`
4. 使用 tar 打包

### 恢复数据卷

```bash
# 创建新数据卷
$ docker volume create my-vol-restored

# 解压备份到新数据卷
$ docker run --rm \
    -v my-vol-restored:/target \
    -v $(pwd):/backup:ro \
    alpine tar xzf /backup/my-vol-backup.tar.gz -C /target
```

### 备份脚本示例

```bash
#!/bin/bash
# backup-volume.sh

VOLUME_NAME=$1
BACKUP_DIR=${2:-/backups}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

docker run --rm \
    -v ${VOLUME_NAME}:/source:ro \
    -v ${BACKUP_DIR}:/backup \
    alpine tar czf /backup/${VOLUME_NAME}_${TIMESTAMP}.tar.gz -C /source .

echo "Backed up ${VOLUME_NAME} to ${BACKUP_DIR}/${VOLUME_NAME}_${TIMESTAMP}.tar.gz"
```

---

## 数据卷 vs 绑定挂载

Docker 有两种主要的数据持久化方式：

| 特性 | 数据卷 (Volume) | 绑定挂载 (Bind Mount) |
|------|----------------|---------------------|
| **管理方式** | Docker 管理 | 用户管理 |
| **存储位置** | `/var/lib/docker/volumes/` | 任意宿主机路径 |
| **可移植性** | 更好 | 依赖宿主机路径 |
| **适用场景** | 生产数据持久化 | 开发时同步代码 |
| **备份** | 需要工具 | 直接访问文件 |

```bash
# 数据卷
$ docker run -v mydata:/app/data nginx

# 绑定挂载
$ docker run -v /host/path:/app/data nginx
```

详见 [绑定挂载](bind-mounts.md) 章节。

---

## 常见问题

### Q: 如何知道容器使用了哪些数据卷？

```bash
$ docker inspect container_name --format '{{json .Mounts}}' | jq
```

### Q: 数据卷的数据在哪里？

```bash
# 查看数据卷详情
$ docker volume inspect my-vol

# Mountpoint 字段显示实际路径
"Mountpoint": "/var/lib/docker/volumes/my-vol/_data"
```

> ⚠️ **注意**：不建议直接修改 Mountpoint 中的文件，应通过容器操作。

### Q: 如何在不同机器间迁移数据卷？

1. 在源机器备份：`docker run --rm -v mydata:/data -v $(pwd):/backup alpine tar czf /backup/data.tar.gz -C /data .`
2. 传输 tar.gz 文件
3. 在目标机器恢复

---

## 本章小结

| 操作 | 命令 |
|------|------|
| 创建数据卷 | `docker volume create name` |
| 列出数据卷 | `docker volume ls` |
| 查看详情 | `docker volume inspect name` |
| 删除数据卷 | `docker volume rm name` |
| 清理未用 | `docker volume prune` |
| 挂载数据卷 | `-v name:/path` 或 `--mount source=name,target=/path` |

## 延伸阅读

- [绑定挂载](bind-mounts.md)：挂载宿主机目录
- [tmpfs 挂载](tmpfs.md)：内存中的临时存储
- [存储驱动](../underly/ufs.md)：Docker 存储的底层原理
