## [WordPress](https://registry.hub.docker.com/_/wordpress/)

### 基本信息
[WordPress](https://en.wikipedia.org/wiki/WordPress) 是开源的 Blog 和内容管理系统框架，它基于 PhP 和 MySQL。
该仓库提供了 WordPress 4.0 版本的镜像。

### 使用方法
启动容器需要 MySQL 的支持，默认端口为 `80`。
```
$ sudo docker run --name some-wordpress --link some-mysql:mysql -d wordpress
```
启动 WordPress 容器时可以指定的一些环境参数包括
* `-e WORDPRESS_DB_USER=...` 缺省为 “root”
* `-e WORDPRESS_DB_PASSWORD=...` 缺省为连接 mysql 容器的环境变量 `MYSQL_ROOT_PASSWORD` 的值
* `-e WORDPRESS_DB_NAME=...` 缺省为 “wordpress”
* `-e WORDPRESS_AUTH_KEY=...`, `-e WORDPRESS_SECURE_AUTH_KEY=...`, `-e WORDPRESS_LOGGED_IN_KEY=...`, `-e WORDPRESS_NONCE_KEY=...`, `-e WORDPRESS_AUTH_SALT=...`, `-e WORDPRESS_SECURE_AUTH_SALT=...`, `-e WORDPRESS_LOGGED_IN_SALT=...`, `-e WORDPRESS_NONCE_SALT=...` 缺省为随机 sha1 串

### Dockerfile
* [4.0 版本](https://github.com/docker-library/wordpress/blob/aee00669e7c43f435f021cb02871bffd63d5677a/Dockerfile)
