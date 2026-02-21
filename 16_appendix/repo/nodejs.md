## [Node.js]

本节涵盖了相关内容与详细描述，主要探讨以下几个方面：

### 基本信息

[Node.js](https://en.wikipedia.org/wiki/Node.js) 是基于 JavaScript 的可扩展服务端和网络软件开发平台。

该仓库位于 `https://hub.docker.com/_/node/`。具体可用版本以 Docker Hub 上的 tags 列表为准。

### 使用方法

在项目中创建一个 Dockerfile。

```docker
FROM node:12
## replace this with your application's default port

EXPOSE 8888
```

然后创建镜像，并启动容器。

```bash
$ docker build -t my-nodejs-app
$ docker run -it --rm --name my-running-app my-nodejs-app
```

也可以直接运行一个简单容器。

```bash
$ docker run -it --rm \
    --name my-running-script \
    # -v "$ ":/usr/src/myapp \

    --mount type=bind,src="$(pwd)",target=/usr/src/myapp \
    -w /usr/src/myapp \
    node:12-alpine \
    node your-daemon-or-script.js
```

### Dockerfile

请到 https://github.com/docker-library/docs/tree/master/node 查看。
