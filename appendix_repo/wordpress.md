## [WordPress](https://registry.hub.docker.com/_/wordpress/)

### 基本信息
[WordPress](https://en.wikipedia.org/wiki/WordPress) 是開源的 Blog 和內容管理系統框架，它基於 PhP 和 MySQL。
該倉庫提供了 WordPress 4.0 版本的鏡像。

### 使用方法
啟動容器需要 MySQL 的支持，默認端口為 `80`。
```
$ sudo docker run --name some-wordpress --link some-mysql:mysql -d wordpress
```
啟動 WordPress 容器時可以指定的一些環境參數包括
* `-e WORDPRESS_DB_USER=...` 缺省為 “root”
* `-e WORDPRESS_DB_PASSWORD=...` 缺省為連接 mysql 容器的環境變量 `MYSQL_ROOT_PASSWORD` 的值
* `-e WORDPRESS_DB_NAME=...` 缺省為 “wordpress”
* `-e WORDPRESS_AUTH_KEY=...`, `-e WORDPRESS_SECURE_AUTH_KEY=...`, `-e WORDPRESS_LOGGED_IN_KEY=...`, `-e WORDPRESS_NONCE_KEY=...`, `-e WORDPRESS_AUTH_SALT=...`, `-e WORDPRESS_SECURE_AUTH_SALT=...`, `-e WORDPRESS_LOGGED_IN_SALT=...`, `-e WORDPRESS_NONCE_SALT=...` 缺省為隨機 sha1 串

### Dockerfile
* [4.0 版本](https://github.com/docker-library/wordpress/blob/aee00669e7c43f435f021cb02871bffd63d5677a/Dockerfile)
