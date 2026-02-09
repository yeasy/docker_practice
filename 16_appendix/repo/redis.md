## [Redis](https://hub.docker.com/_/redis/)

### 基本信息

[Redis](https://en.wikipedia.org/wiki/Redis) 是开源的内存 Key-Value 数据库实现。

该仓库位于 `https://hub.docker.com/_/redis/` ，提供了 Redis 3.x ~ 6.x 各个版本的镜像。

### 使用方法

默认会在 `6379` 端口启动数据库。

```bash
$ docker run --name some-redis -d -p 6379:6379 redis
```

另外还可以启用 [持久存储](https://redis.io/topics/persistence)。

```bash
$ docker run --name some-redis -d -p 6379:6379 redis redis-server --appendonly yes
```

默认数据存储位置在 `VOLUME/data`。可以使用 `--volumes-from some-volume-container` 或 `-v /docker/host/dir:/data` 将数据存放到本地。

使用其他应用连接到容器，首先创建网络
```bash
$ docker network create my-redis-net
```

然后启动 redis 容器
```bash
$ docker run --name some-redis -d --network my-redis-net redis
```

最后启动应用容器
```bash
$ docker run --name some-app -d --network my-redis-net application-that-uses-redis
```

或者通过 `redis-cli`

```bash
$ docker run -it --rm \
    --network my-redis-net \
    redis \
    sh -c 'exec redis-cli -h some-redis'
```

### Dockerfile

请到 https://github.com/docker-library/docs/tree/master/redis 查看。
