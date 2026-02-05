# 挂载主机目录（Bind Mounts）

## 什么是 Bind Mount

Bind Mount（绑定挂载）将**宿主机的目录或文件**直接挂载到容器中。容器可以读写宿主机的文件系统。

```
宿主机                           容器
┌─────────────────────┐         ┌─────────────────────┐
│  /home/user/code/   │         │                     │
│  ├── index.html     │◄───────►│  /usr/share/nginx/  │
│  ├── style.css      │ Bind    │  html/              │
│  └── app.js         │ Mount   │  (同一份文件)        │
└─────────────────────┘         └─────────────────────┘
```

---

## Bind Mount vs Volume

| 特性 | Bind Mount | Volume |
|------|------------|--------|
| **数据位置** | 宿主机任意路径 | Docker 管理的目录 |
| **路径指定** | 必须是绝对路径 | 卷名 |
| **可移植性** | 依赖宿主机路径 | 更好（Docker 管理） |
| **性能** | 依赖宿主机文件系统 | 优化的存储驱动 |
| **适用场景** | 开发环境、配置文件 | 生产数据持久化 |
| **备份** | 直接访问文件 | 需要通过 Docker |

### 选择建议

```
需求                          推荐方案
─────────────────────────────────────────
开发时同步代码              → Bind Mount
持久化数据库数据            → Volume
共享配置文件                → Bind Mount
容器间共享数据              → Volume
备份方便                    → Bind Mount（直接访问）
生产环境                    → Volume
```

---

## 基本语法

### 使用 --mount（推荐）

```bash
$ docker run -d \
    --mount type=bind,source=/宿主机路径,target=/容器路径 \
    nginx
```

### 使用 -v（简写）

```bash
$ docker run -d \
    -v /宿主机路径:/容器路径 \
    nginx
```

### 两种语法对比

| 特性 | --mount | -v |
|------|---------|-----|
| 语法 | 键值对，更清晰 | 冒号分隔，更简洁 |
| 路径不存在时 | 报错 | 自动创建目录 |
| 推荐程度 | ✅ 推荐 | 常用 |

---

## 使用场景

### 场景一：开发环境代码同步

```bash
# 将本地代码目录挂载到容器
$ docker run -d \
    -p 8080:80 \
    --mount type=bind,source=$(pwd)/src,target=/usr/share/nginx/html \
    nginx

# 修改本地文件，容器内立即生效（热更新）
$ echo "Hello" > src/index.html
# 浏览器刷新即可看到变化
```

### 场景二：配置文件挂载

```bash
# 挂载自定义 nginx 配置
$ docker run -d \
    --mount type=bind,source=/path/to/nginx.conf,target=/etc/nginx/nginx.conf,readonly \
    nginx
```

### 场景三：日志收集

```bash
# 将容器日志输出到宿主机目录
$ docker run -d \
    --mount type=bind,source=/var/log/myapp,target=/app/logs \
    myapp
```

### 场景四：共享 SSH 密钥

```bash
# 挂载 SSH 密钥（只读）
$ docker run --rm -it \
    --mount type=bind,source=$HOME/.ssh,target=/root/.ssh,readonly \
    alpine ssh user@remote
```

---

## 只读挂载

防止容器修改宿主机文件：

```bash
# --mount 语法
$ docker run -d \
    --mount type=bind,source=/config,target=/app/config,readonly \
    myapp

# -v 语法
$ docker run -d \
    -v /config:/app/config:ro \
    myapp
```

容器内尝试写入会报错：

```bash
$ touch /app/config/new.txt
touch: /app/config/new.txt: Read-only file system
```

---

## 挂载单个文件

```bash
# 挂载 bash 历史记录
$ docker run --rm -it \
    --mount type=bind,source=$HOME/.bash_history,target=/root/.bash_history \
    ubuntu bash

# 挂载自定义配置文件
$ docker run -d \
    --mount type=bind,source=/path/to/my.cnf,target=/etc/mysql/my.cnf \
    mysql
```

> ⚠️ **注意**：挂载单个文件时，如果宿主机上的文件被编辑器替换（而非原地修改），容器内仍是旧文件的 inode。建议重启容器或挂载目录。

---

## 查看挂载信息

```bash
$ docker inspect mycontainer --format '{{json .Mounts}}' | jq
```

输出：

```json
[
  {
    "Type": "bind",
    "Source": "/home/user/code",
    "Destination": "/app",
    "Mode": "",
    "RW": true,
    "Propagation": "rprivate"
  }
]
```

| 字段 | 说明 |
|------|------|
| `Type` | 挂载类型（bind） |
| `Source` | 宿主机路径 |
| `Destination` | 容器内路径 |
| `RW` | 是否可读写 |
| `Propagation` | 挂载传播模式 |

---

## 常见问题

### Q: 路径不存在报错

```bash
$ docker run --mount type=bind,source=/not/exist,target=/app nginx
docker: Error response from daemon: invalid mount config for type "bind": 
bind source path does not exist: /not/exist
```

**解决**：确保源路径存在，或改用 `-v`（会自动创建）

### Q: 权限问题

容器内用户可能无权访问挂载的文件：

```bash
# 方法1：确保宿主机文件权限允许容器用户访问
$ chmod -R 755 /path/to/data

# 方法2：以 root 运行容器
$ docker run -u root ...

# 方法3：使用相同的 UID
$ docker run -u $(id -u):$(id -g) ...
```

### Q: macOS/Windows 性能问题

在 Docker Desktop 上，Bind Mount 性能较差（需要跨文件系统同步）：

```bash
# 使用 :cached 或 :delegated 提高性能（macOS）
$ docker run -v /host/path:/container/path:cached myapp
```

| 选项 | 说明 |
|------|------|
| `:cached` | 宿主机权威，容器读取可能延迟 |
| `:delegated` | 容器权威，宿主机读取可能延迟 |
| `:consistent` | 默认，完全一致（最慢） |

---

## 最佳实践

### 1. 开发环境使用 Bind Mount

```bash
# 代码热更新
$ docker run -v $(pwd):/app -p 3000:3000 node npm run dev
```

### 2. 生产环境使用 Volume

```bash
# 数据持久化
$ docker run -v mysql_data:/var/lib/mysql mysql
```

### 3. 配置文件使用只读挂载

```bash
$ docker run -v /config/nginx.conf:/etc/nginx/nginx.conf:ro nginx
```

### 4. 注意路径安全

```bash
# ❌ 危险：挂载根目录或敏感目录
$ docker run -v /:/host ...

# ✅ 只挂载必要的目录
$ docker run -v /app/data:/data ...
```

---

## 本章小结

| 要点 | 说明 |
|------|------|
| **作用** | 将宿主机目录挂载到容器 |
| **语法** | `-v /宿主机:/容器` 或 `--mount type=bind,...` |
| **只读** | 添加 `readonly` 或 `:ro` |
| **适用场景** | 开发环境、配置文件、日志 |
| **vs Volume** | Bind 更灵活，Volume 更适合生产 |

## 延伸阅读

- [数据卷](volume.md)：Docker 管理的持久化存储
- [tmpfs 挂载](tmpfs.md)：内存临时存储
- [Compose 数据管理](../compose/compose_file.md)：Compose 中的挂载配置
