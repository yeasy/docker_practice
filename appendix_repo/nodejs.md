## [Node.js](https://registry.hub.docker.com/_/node/)

### 基本信息
[Node.js](https://en.wikipedia.org/wiki/Node.js)是基于 JavaScript 的可扩展服务端和网络软件开发平台。
该仓库提供了 Node.js 0.8 ~ 0.11 各个版本的镜像。

### 使用方法
在项目中创建一个 Dockerfile。
```
FROM node:0.10-onbuild
# replace this with your application's default port
EXPOSE 8888
```
然后创建镜像，并启动容器
```
$ sudo docker build -t my-nodejs-app
$ sudo docker run -it --rm --name my-running-app my-nodejs-app
```

也可以直接运行一个简单容器。
```
$ sudo docker run -it --rm --name my-running-script -v "$(pwd)":/usr/src/myapp -w /usr/src/myapp node:0.10 node your-daemon-or-script.js
```

### Dockerfile
* [0.8 版本](https://github.com/docker-library/node/blob/d017d679e92e84a810c580cdb29fcdbba23c2bb9/0.8/Dockerfile)
* [0.10 版本](https://github.com/docker-library/node/blob/913a225f2fda34d6a811fac1466e4f09f075fcf6/0.10/Dockerfile)
* [0.11 版本](https://github.com/docker-library/node/blob/d017d679e92e84a810c580cdb29fcdbba23c2bb9/0.11/Dockerfile)
