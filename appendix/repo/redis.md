## [Redis](https://hub.docker.com/_/redis/)

### 基本信息

[Redis](https://en.wikipedia.org/wiki/Redis) 是开源的内存 Key-Value 数据库实现。

该仓库位于 `https://hub.docker.com/_/redis/` ，提供了 Redis 3.x ~ 4.x 各个版本的镜像。

### 使用方法

默认会在 `6379` 端口启动数据库。

```bash
$ docker run --name some-redis -d redis
```

另外还可以启用 [持久存储](http://redis.io/topics/persistence)。

```bash
$ docker run --name some-redis -d redis redis-server --appendonly yes
```

默认数据存储位置在 `VOLUME/data`。可以使用 `--volumes-from some-volume-container` 或 `-v /docker/host/dir:/data` 将数据存放到本地。

使用其他应用连接到容器，可以用

```bash
$ docker run --name some-app --link some-redis:redis -d application-that-uses-redis
```

或者通过 `redis-cli`

```bash
$ docker run -it --rm \
    --link some-redis:redis \
    redis \
    sh -c 'exec redis-cli -h "$REDIS_PORT_6379_TCP_ADDR" -p "$REDIS_PORT_6379_TCP_PORT"'
```

### Dockerfile

请到 https://github.com/docker-library/docs/tree/master/redis 查看。
