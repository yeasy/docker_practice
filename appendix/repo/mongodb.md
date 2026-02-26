## MongoDB

### 基本信息

[MongoDB](https://en.wikipedia.org/wiki/MongoDB) 是开源的 NoSQL 数据库实现。

该仓库位于 `https://hub.docker.com/_/mongo/`。具体可用版本以 Docker Hub 上的 tags 列表为准。

### 使用方法

默认会在 `27017` 端口启动数据库。

```bash
$ docker run --name mongo -d mongo
```

使用其他应用连接到容器，首先创建网络
```bash
$ docker network create my-mongo-net
```

然后启动 MongoDB 容器
```bash
$ docker run --name some-mongo -d --network my-mongo-net mongo
```

最后启动应用容器
```bash
$ docker run --name some-app -d --network my-mongo-net application-that-uses-mongo
```

或者通过 `mongo`

```bash
$ docker run -it --rm \
    --network my-mongo-net \
    mongo \
    sh -c 'exec mongo "some-mongo:27017/test"'
```

### Dockerfile

请到 https://github.com/docker-library/docs/tree/master/mongo 查看。
