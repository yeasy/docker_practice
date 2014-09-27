## [MySQL](https://registry.hub.docker.com/_/mysql/)

### 基本信息
[MySQL](https://en.wikipedia.org/wiki/MySQL)是开源的关系数据库实现。
该仓库提供了MySQL各个版本的镜像，包括5.6系列、5.7系列等。

### 使用方法
默认会在`3306`端口启动数据库。
```
$ sudo docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=mysecretpassword -d mysql
```
之后就可以使用其它应用来连接到该容器。
```
$ sudo docker run --name some-app --link some-mysql:mysql -d application-that-uses-mysql
```
或者通过`mysql`。
```
$ sudo docker run -it --link some-mysql:mysql --rm mysql sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'
```

### Dockerfile
* [5.6版本](https://github.com/docker-library/mysql/blob/7461a52b43f06839a4d8723ae8841f4cb616b3d0/5.6/Dockerfile)
* [5.7版本](https://github.com/docker-library/mysql/blob/7461a52b43f06839a4d8723ae8841f4cb616b3d0/5.7/Dockerfile)
