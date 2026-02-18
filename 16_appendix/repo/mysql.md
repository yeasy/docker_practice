## [MySQL]

### 基本信息

[MySQL](https://en.wikipedia.org/wiki/MySQL) 是开源的关系数据库实现。

该仓库位于 `https://hub.docker.com/_/mysql/`。具体可用版本以 Docker Hub 上的 tags 列表为准。

### 使用方法

默认会在 `3306` 端口启动数据库。

```bash
$ docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=mysecretpassword -d mysql
```

之后就可以使用其它应用来连接到该容器。

首先创建网络
```bash
$ docker network create my-mysql-net
```

然后启动 MySQL 容器
```bash
$ docker run --name some-mysql -d --network my-mysql-net -e MYSQL_ROOT_PASSWORD=mysecretpassword mysql
```

最后启动应用容器
```bash
$ docker run --name some-app -d --network my-mysql-net application-that-uses-mysql
```

或者通过 `mysql` 命令行连接。

```bash
$ docker run -it --rm \
    --network my-mysql-net \
    mysql \
    sh -c 'exec mysql -hsome-mysql -P3306 -uroot -pmysecretpassword'
```


### Dockerfile

请到 https://github.com/docker-library/docs/tree/master/mysql 查看
