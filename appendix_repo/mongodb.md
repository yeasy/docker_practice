## [MongoDB](https://registry.hub.docker.com/_/mongo/)

### 基本信息
[MongoDB](https://en.wikipedia.org/wiki/MongoDB)是开源的NoSQL数据库实现。
该仓库提供了MongoDB从2.2到2.7各个版本的镜像。

### 使用方法
默认会在`27017`端口启动数据库。
```
$ sudo docker run --name some-mongo -d mongo
```

使用其他应用连接到容器，可以用
```
$ sudo docker run --name some-app --link some-mongo:mongo -d application-that-uses-mongo
```
或者通过`mongo`
```
$ sudo docker run -it --link some-mongo:mongo --rm mongo sh -c 'exec mongo "$MONGO_PORT_27017_TCP_ADDR:$MONGO_PORT_27017_TCP_PORT/test"'
```

### Dockerfile
* [2.2版本](https://github.com/docker-library/mongo/blob/77c841472ccb6cc87fea1218269d097405edc6cb/2.2/Dockerfile)
* [2.4版本](https://github.com/docker-library/mongo/blob/807078cb7b5f0289f6dabf9f6875d5318122bc30/2.4/Dockerfile)
* [2.6版本](https://github.com/docker-library/mongo/blob/77c841472ccb6cc87fea1218269d097405edc6cb/2.6/Dockerfile)
* [2.7版本](https://github.com/docker-library/mongo/blob/807078cb7b5f0289f6dabf9f6875d5318122bc30/2.7/Dockerfile)
