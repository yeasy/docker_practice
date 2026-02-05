# [WordPress](https://hub.docker.com/_/wordpress/)

## 基本信息

[WordPress](https://en.wikipedia.org/wiki/WordPress) 是开源的 Blog 和内容管理系统框架，它基于 PHP 和 MySQL。

该仓库位于 `https://hub.docker.com/_/wordpress/` ，提供了 WordPress 4.x ~ 5.x 版本的镜像。

## 使用方法

启动容器需要 MySQL 的支持，默认端口为 `80`。

首先创建网络
```bash
$ docker network create my-wordpress-net
```

启动 MySQL 容器
```bash
$ docker run --name some-mysql -d --network my-wordpress-net -e MYSQL_ROOT_PASSWORD=mysecretpassword mysql
```

启动 WordPress 容器
```bash
$ docker run --name some-wordpress -d --network my-wordpress-net -e WORDPRESS_DB_HOST=some-mysql -e WORDPRESS_DB_PASSWORD=mysecretpassword wordpress
```

启动 WordPress 容器时可以指定的一些环境变量包括：

* `WORDPRESS_DB_HOST`: MySQL 服务的主机名
* `WORDPRESS_DB_USER`: MySQL 数据库的用户名
* `WORDPRESS_DB_PASSWORD`: MySQL 数据库的密码
* `WORDPRESS_DB_NAME`: WordPress 要使用的数据库名


## Dockerfile

请到 https://github.com/docker-library/docs/tree/master/wordpress 查看。
