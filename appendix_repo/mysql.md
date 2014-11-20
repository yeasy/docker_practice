## [MySQL](https://registry.hub.docker.com/_/mysql/)

### 基本信息
[MySQL](https://en.wikipedia.org/wiki/MySQL) 是開源的關系數據庫實現。
該倉庫提供了 MySQL 各個版本的鏡像，包括 5.6 系列、5.7 系列等。

### 使用方法
默認會在 `3306` 端口啟動數據庫。
```
$ sudo docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=mysecretpassword -d mysql
```
之後就可以使用其它應用來連接到該容器。
```
$ sudo docker run --name some-app --link some-mysql:mysql -d application-that-uses-mysql
```
或者通過 `mysql`。
```
$ sudo docker run -it --link some-mysql:mysql --rm mysql sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'
```

### Dockerfile
* [5.6 版本](https://github.com/docker-library/mysql/blob/7461a52b43f06839a4d8723ae8841f4cb616b3d0/5.6/Dockerfile)
* [5.7 版本](https://github.com/docker-library/mysql/blob/7461a52b43f06839a4d8723ae8841f4cb616b3d0/5.7/Dockerfile)
