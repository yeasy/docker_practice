# 实战 WordPress

## 简介

WordPress 是全球最流行的内容管理系统（CMS）。使用 Docker Compose 可以在几分钟内搭建一个包含数据库、Web 服务和持久化存储的生产级 WordPress 环境。

---

## 项目结构

```
wordpress/
├── docker-compose.yml
├── .env                # 环境变量（敏感信息）
└── nginx/              # 可选：反向代理配置
    └── nginx.conf
```

---

## 编写 `docker-compose.yml`

这是一个生产可用的最小化配置：

```yaml
services:
  # 数据库服务
  db:
    image: mysql:8.0
    container_name: wordpress_db
    restart: always
    command: 
      # 使用原生密码认证（旧版 WP 兼容性）
      - --default-authentication-plugin=mysql_native_password
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/mysql
    networks:
      - wp_net

  # WordPress 服务
  wordpress:
    image: wordpress:latest
    container_name: wordpress_app
    restart: always
    ports:
      - "8000:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: ${DB_PASSWORD}
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wp_data:/var/www/html
      # 增加上传文件大小限制
      - ./uploads.ini:/usr/local/etc/php/conf.d/uploads.ini
    depends_on:
      - db
    networks:
      - wp_net

volumes:
  db_data:  # 数据库持久化
  wp_data:  # WordPress 文件(插件/主题/上传)持久化

networks:
  wp_net:
```

---

## 配置文件详解

### 1. 环境变量 (.env)

为了安全，不要在 `docker-compose.yml` 中直接写密码。创建 `.env` 文件：

```ini
DB_ROOT_PASSWORD=somestrongrootpassword
DB_PASSWORD=somestronguserpassword
```

Compose 会自动读取此同级目录下的文件。

### 2. 数据持久化

我们定义了两个命名卷：
- `db_data`: 确保 MySQL 容器重建后数据不丢失
- `wp_data`: 保存 WordPress 的核心文件、插件、主题和上传的媒体文件

### 3. PHP 配置优化

默认的 WordPress 镜像上传文件限制较小（通常 2MB）。创建 `uploads.ini`：

```ini
file_uploads = On
memory_limit = 256M
upload_max_filesize = 64M
post_max_size = 64M
max_execution_time = 600
```

---

## 启动与运行

1. 启动服务：

```bash
$ docker compose up -d
```

2. 访问安装界面：
   打开浏览器访问 `http://localhost:8000`

3. 查看日志：

```bash
$ docker compose logs -f
```

---

## 生产环境最佳实践

### 1. 数据库备份

不要只依赖 Volume。建议定期备份数据库：

```bash
# 导出 SQL
$ docker exec wordpress_db mysqldump -u wordpress -pwordpress wordpress > backup.sql
```

或者添加一个自动备份容器：

```yaml
  backup:
    image: tiredofit/db-backup
    volumes:
      - ./backups:/backup
    environment:
      - DB_TYPE=mysql
      - DB_HOST=db
      - DB_NAME=wordpress
      - DB_USER=wordpress
      - DB_PASS=${DB_PASSWORD}
      - DB_DUMP_FREQ=1440 # 每天备份一次
    depends_on:
      - db
    networks:
      - wp_net
```

### 2. 使用 Nginx 反向代理

在生产环境中，不要直接暴露 WordPress 端口，而是通过 Nginx 进行反向代理并配置 SSL。

### 3. 使用 Redis 缓存

WordPress 支持 Redis 缓存以提高性能。

```yaml
  redis:
    image: redis:alpine
    restart: always
    networks:
      - wp_net
```

在 WordPress 容器环境变量中添加：
```yaml
      WORDPRESS_REDIS_HOST: redis
```
并安装 Redis Object Cache 插件。

---

## 常见问题

### Q: 数据库连接错误

**现象**：访问页面显示 "Error establishing a database connection"。

**排查**：
1. 检查 `docker compose logs wordpress`
2. 确认 `.env` 中的密码与 YAML 文件引用一致
3. 确认 `WORDPRESS_DB_HOST` 也是 `db`（服务名）
4. MySQL 8.0 可能需要几秒钟启动，WordPress 会自动重试，稍等片刻即可。

### Q: 无法上传大文件

**解决**：确保挂载了 `uploads.ini` 配置，并且重启了容器：
```bash
$ docker compose restart wordpress
```

---

## 延伸阅读

- [Compose 模板文件](compose_file.md)：深入了解配置项
- [数据卷](../07_data_network/data/volume.md)：理解数据持久化
- [Docker Hub WordPress](https://hub.docker.com/_/wordpress)：官方镜像文档
