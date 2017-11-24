## [MongoDB](https://store.docker.com/images/mongo/)

### 基本信息

[MongoDB](https://en.wikipedia.org/wiki/MongoDB) 是开源的 NoSQL 数据库实现。

该仓库位于 https://store.docker.com/images/mongo/ ，提供了 MongoDB 2.x ~ 3.x 各个版本的镜像。

### 使用方法

默认会在 `27017` 端口启动数据库。

```bash
$ docker run --name mongo -d mongo
```

使用其他应用连接到容器，可以用

```bash
$ docker run --name some-app --link some-mongo:mongo -d application-that-uses-mongo
```

或者通过 `mongo`

```bash
$ docker run -it --link some-mongo:mongo --rm mongo sh -c 'exec mongo "$MONGO_PORT_27017_TCP_ADDR:$MONGO_PORT_27017_TCP_PORT/test"'
```

### Dockerfile

请到 https://github.com/docker-library/docs/tree/master/mongo 查看。
