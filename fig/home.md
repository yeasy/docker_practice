##快速搭建基于 Docker 的隔离开发环境

使用 `Dockerfile` 文件指定你的应用环境，让它能在任意地方复制使用：

```
FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
```

在 `fig.yml` 文件中指定应用使用的不同服务，让它们能够在一个独立的环境中一起运行：

```  
web:
  build: .
  command: python app.py
  links:
   - db
  ports:
   - "8000:8000"
db:
  image: postgres
```
（注意不需要再额外安装 Postgres 了！）  

接着执行命令 `fig up` ，然后 Fig 就会启动并运行你的应用了。

![Docker](../_images/fig-example-large.gif)

Fig 可用的命令有:   

* 启动、停止，和重建服务
* 查看服务的运行状态
* 查看运行中的服务的输入日志
* 对服务发送命令

##快速上手
我们试着让一个基本的 Python web 应用运行在 Fig 上。这个实验假设你已经知道一些 Python 知识，如果你不熟悉，但清楚概念上的东西也是没有问题的。

首先，[安装 Docker 和 Fig](install.md)  

为你的项目创建一个目录

```
$ mkdir figtest
$ cd figtest
```
进入目录，创建 `app.py`，这是一个能够让 Redis 上的一个值自增的简单 web 应用，基于 Flask 框架。  

```
from flask import Flask
from redis import Redis
import os
app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    redis.incr('hits')
    return 'Hello World! I have been seen %s times.' % redis.get('hits')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```
在 `requirements.txt` 文件中指定应用的 Python 依赖包。   

```  
flask
redis
```
下一步我们要创建一个包含应用所有依赖的 Docker 镜像，这里将阐述怎么通过 `Dockerfile` 文件来创建。

```
FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
```
以上的内容首先告诉 Docker 在容器里面安装 Python ，代码的路径还有Python 依赖包。关于 Dockerfile 的更多信息可以查看 [镜像创建](../image/create.md#利用 Dockerfile 来创建镜像) 和 [Dockerfile 使用](../dockerfile/README.md)

接着我们通过 `fig.yml` 文件指定一系列的服务：

```
web:
  build: .
  command: python app.py
  ports:
   - "5000:5000"
  volumes:
   - .:/code
  links:
   - redis
redis:
  image: redis
  ```
这里指定了两个服务：  

* web 服务，通过当前目录的 `Dockerfile` 创建。并且说明了在容器里面执行`python app.py ` 命令 ，转发在容器里开放的 5000 端口到本地主机的 5000 端口，连接 Redis 服务，并且挂载当前目录到容器里面，这样我们就可以不用重建镜像也能直接使用代码。
* redis 服务，我们使用公用镜像 [redis](https://registry.hub.docker.com/_/redis/)。  
* 
现在如果执行 `fig up` 命令 ，它就会拉取 redis 镜像，启动所有的服务。

```
$ fig up
Pulling image redis...
Building web...
Starting figtest_redis_1...
Starting figtest_web_1...
redis_1 | [8] 02 Jan 18:43:35.576 # Server started, Redis version 2.8.3
web_1   |  * Running on http://0.0.0.0:5000/
```
这个 web 应用已经开始在你的 docker 守护进程里面监听着 5000 端口了（如果你有使用 boot2docker ，执行 `boot2docker ip` ，就会看到它的地址）。

如果你想要在后台运行你的服务，可以在执行 `fig up` 命令的时候添加 `-d` 参数，然后使用 `fig ps` 查看有什么进程在运行。

```
$ fig up -d
Starting figtest_redis_1...
Starting figtest_web_1...
$ fig ps
        Name                 Command            State       Ports
-------------------------------------------------------------------
figtest_redis_1   /usr/local/bin/run         Up
figtest_web_1     /bin/sh -c python app.py   Up      5000->5000/tcp
```

`fig run` 指令可以帮为你的服务发送命令。例如：查看 web 服务可以获取到的环境变量:

```
$ fig run web env
```
执行帮助命令 `fig --help` 查看其它可用的参数。

假设你使用了 `fig up -d` 启动 Fig，可以通过以下命令停止你的服务：

```
$ fig stop
```
以上内容或多或少得讲述了如何 Fig 。通过查看下面的引用章节可以了解到关于命令、配置和环境变量的更多细节。如果你任何想法或建议，[可以在 GitHub 上提出](https://github.com/docker/fig)。

