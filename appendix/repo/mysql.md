## [MySQL](https://hub.docker.com/_/mysql/)

### 基本信息
[MySQL](https://en.wikipedia.org/wiki/MySQL) 是开源的关系数据库实现。

该仓库位于 https://hub.docker.com/_/mysql/ ，提供了 MySQL 各个版本的镜像，包括 5.6 系列、5.7 系列等。

### 使用方法
默认会在 `3306` 端口启动数据库。

```
$ docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=mysecretpassword -d mysql
```
之后就可以使用其它应用来连接到该容器。

```
$ docker run --name some-app --link some-mysql:mysql -d application-that-uses-mysql
```
或者通过 `mysql`。

```
$ docker run -it --link some-mysql:mysql --rm mysql sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'
```

### Dockerfile

请到 https://github.com/docker-library/docs/tree/master/mysql 查看
