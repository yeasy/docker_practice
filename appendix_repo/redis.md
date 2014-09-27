## [Redis](https://registry.hub.docker.com/_/redis/)

### 基本信息
[Redis](https://en.wikipedia.org/wiki/Redis)是开源的内存Key-Value数据库实现。
该仓库提供了Redis从2.6到2.8.9各个版本的镜像。

### 使用方法
默认会在`6379`端口启动数据库。
```
$ sudo docker run --name some-redis -d redis
```
另外还可以启用[持久存储](http://redis.io/topics/persistence)。
```
$ sudo docker run --name some-redis -d redis redis-server --appendonly yes
```
默认数据存储位置在`VOLUME/data`。可以使用`--volumes-from some-volume-container`或`-v /docker/host/dir:/data`将数据存放到本地。

使用其他应用连接到容器，可以用
```
$ sudo docker run --name some-app --link some-redis:redis -d application-that-uses-redis
```
或者通过`redis-cli`
```
$ sudo docker run -it --link some-redis:redis --rm redis sh -c 'exec redis-cli -h "$REDIS_PORT_6379_TCP_ADDR" -p "$REDIS_PORT_6379_TCP_PORT"'
```

### Dockerfile
* [2.6版本](https://github.com/docker-library/redis/blob/02d9cd887a4e0d50db4bb085eab7235115a6fe4a/2.6.17/Dockerfile)
* [最新2.8版本](https://github.com/docker-library/redis/blob/d0665bb1bbddd4cc035dbc1fc774695fa534d648/2.8.13/Dockerfile)
