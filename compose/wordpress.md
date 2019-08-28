## 使用 WordPress

> 本小节内容适合 `PHP` 开发人员阅读。

`Compose` 可以很便捷的让 `Wordpress` 运行在一个独立的环境中。

### 创建空文件夹

假设新建一个名为 `wordpress` 的文件夹，然后进入这个文件夹。

### 创建 `docker-compose.yml` 文件

[`docker-compose.yml`](https://github.com/yeasy/docker_practice/blob/master/compose/demo/wordpress/docker-compose.yml) 文件将开启一个 `wordpress` 服务和一个独立的 `MySQL` 实例：

```yaml
version: "3.1"

services:

  wordpress:
    image: wordpress:latest
    container_name: wpblog
    restart: always
    ports:
      - 8000:80
    environment:
      WORDPRESS_DB_HOST: wpdb
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    depends_on:
      - wpdb
    links:
      - wpdb:mysql
    volumes:
      - ~/docker/web/wp-app:/var/www/html

  wpdb:
    # https://hub.docker.com/_/mysql/ - or mariadb https://hub.docker.com/_/mariadb

    # mysql:5.7
    # image: mysql:5.7

    # or
    image: mysql:8
    command: [
      '--default_authentication_plugin=mysql_native_password',
      '--character-set-server=utf8mb4',
      '--collation-server=utf8mb4_unicode_ci'
    ]

    container_name: wpdb
    restart: always
    # ports:
    #   - 3306:3306
    environment:
      MYSQL_ROOT_PASSWORD: xiaohan
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
    volumes:
      - ~/docker/db/mysql:/var/lib/mysql
```

### 构建并运行项目

运行 `docker-compose up -d` Compose 就会拉取镜像再创建我们所需要的镜像，然后启动 `wordpress` 和数据库容器。 接着浏览器访问 `127.0.0.1:8000` 端口就能看到 `WordPress` 安装界面了。
