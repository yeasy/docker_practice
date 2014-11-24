## [Redis](https://registry.hub.docker.com/_/redis/)

### 基本信息
[Redis](https://en.wikipedia.org/wiki/Redis) 是開源的內存 Key-Value 數據庫實做。
該倉庫提供了 Redis 2.6 ~ 2.8.9 各個版本的鏡像。

### 使用方法
默認會在 `6379` 端口啟動數據庫。
```
$ sudo docker run --name some-redis -d redis
```
另外還可以啟用 [持久存儲](http://redis.io/topics/persistence)。
```
$ sudo docker run --name some-redis -d redis redis-server --appendonly yes
```
默認數據存儲位置在 `VOLUME/data`。可以使用 `--volumes-from some-volume-container` 或 `-v /docker/host/dir:/data` 將數據存放到本地。

使用其他應用連接到容器，可以用
```
$ sudo docker run --name some-app --link some-redis:redis -d application-that-uses-redis
```
或者透過 `redis-cli`
```
$ sudo docker run -it --link some-redis:redis --rm redis sh -c 'exec redis-cli -h "$REDIS_PORT_6379_TCP_ADDR" -p "$REDIS_PORT_6379_TCP_PORT"'
```

### Dockerfile
* [2.6 版本](https://github.com/docker-library/redis/blob/02d9cd887a4e0d50db4bb085eab7235115a6fe4a/2.6.17/Dockerfile)
* [最新 2.8 版本](https://github.com/docker-library/redis/blob/d0665bb1bbddd4cc035dbc1fc774695fa534d648/2.8.13/Dockerfile)
