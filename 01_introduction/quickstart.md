# 快速上手 (5分钟)

本节将通过一个简单的 Web 应用例子，带你快速体验 Docker 的核心流程：构建镜像、运行容器。

## 1. 准备代码

创建一个名为 `hello-docker` 的文件夹，并在其中创建一个 `index.html` 文件：

```html
<h1>Hello, Docker!</h1>
```

## 2. 编写 Dockerfile

在同级目录下创建一个名为 `Dockerfile` (无后缀) 的文件：

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
```

## 3. 构建镜像

打开终端，进入该目录，执行构建命令：

```bash
$ docker build -t my-hello-world .
```

* `docker build`: 构建命令
* `-t my-hello-world`: 给镜像起个名字（标签）
* `.`: 指定上下文路径为当前目录

## 4. 运行容器

使用刚才构建的镜像启动一个容器：

```bash
$ docker run -d -p 8080:80 my-hello-world
```

* `docker run`: 运行命令
* `-d`: 后台运行
* `-p 8080:80`: 将宿主机的 8080 端口映射到容器的 80 端口

## 5. 访问测试

打开浏览器访问 [http://localhost:8080](http://localhost:8080)，你应该能看到 "Hello, Docker!"。

## 6. 清理

停止并删除容器：

```bash
# 查看正在运行的容器 ID
$ docker ps

# 停止容器
$ docker stop <CONTAINER_ID>

# 删除容器
$ docker rm <CONTAINER_ID>
```

恭喜！你已经完成了第一次 Docker 实战。接下来请阅读 [Docker 核心概念](../02_basic_concept/README.md) 做深入了解。
