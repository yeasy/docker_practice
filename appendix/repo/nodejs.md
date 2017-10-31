## [Node.js](https://hub.docker.com/_/node/)

### 基本信息
[Node.js](https://en.wikipedia.org/wiki/Node.js)是基于 JavaScript 的可扩展服务端和网络软件开发平台。

该仓库位于 https://hub.docker.com/_/node/ ，提供了 Node.js 0.10 ~ 6.3.x 各个版本的镜像。

### 使用方法
在项目中创建一个 Dockerfile。

```
FROM node:0.10-onbuild
# replace this with your application's default port
EXPOSE 8888
```
然后创建镜像，并启动容器。

```
$ docker build -t my-nodejs-app
$ docker run -it --rm --name my-running-app my-nodejs-app
```

也可以直接运行一个简单容器。

```
$ docker run -it --rm --name my-running-script -v "$(pwd)":/usr/src/myapp -w /usr/src/myapp node:0.10 node your-daemon-or-script.js
```

### Dockerfile

请到 https://github.com/docker-library/docs/tree/master/node 查看。
