# [WordPress](https://hub.docker.com/_/wordpress/)

## 基本信息

[WordPress](https://en.wikipedia.org/wiki/WordPress) 是开源的 Blog 和内容管理系统框架，它基于 PHP 和 MySQL。

该仓库位于 `https://hub.docker.com/_/wordpress/` ，提供了 WordPress 4.x ~ 5.x 版本的镜像。

## 使用方法

启动容器需要 MySQL 的支持，默认端口为 `80`。

```bash
$ docker run --name some-wordpress --link some-mysql:mysql -d wordpress
```

启动 WordPress 容器时可以指定的一些环境变量包括：

* `WORDPRESS_DB_USER` 缺省为 `root`
* `WORDPRESS_DB_PASSWORD` 缺省为连接 mysql 容器的环境变量 `MYSQL_ROOT_PASSWORD` 的值
* `WORDPRESS_DB_NAME` 缺省为 `wordpress`

## Dockerfile

请到 https://github.com/docker-library/docs/tree/master/wordpress 查看。
