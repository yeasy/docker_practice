##Fig 和 Django 入门

我们现在将使用 Fig 配置并运行一个 Django/PostgreSQL 应用。在开始之前，先确保 Fig 已经 [安装](install.md)。

设置好三个必要的文件。首先，应用将要运行在一个安装好所有依赖环境的 Docker 容器里面，那么我们可以通过指定 `Dockerfile` 文件来指定 Docker 容器安装什么内容。内容如下： 

```
FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
```
以上内容指定了的应用使用一个 Python 镜像，并安装必要的 Python 依赖包。关于 Dockerfile 的更多信息可以查看 [镜像创建](../image/create.md#利用 Dockerfile 来创建镜像) 和 [Dockerfile 使用](../dockerfile/README.md)

第二，在 `requirements.txt` 文件里面写明需要安装的具体依赖包名 。

```
Django
psycopg2
```

最后，通过 `fig.yml` 文件把所有的东西联系起来。它描述了应用的构成（一个 web 服务和一个 数据库）、使用的具体 Docker 镜像、它们之间的连接、挂载的卷，以及和开放的端口。 

```
db:
  image: postgres
web:
  build: .
  command: python manage.py runserver 0.0.0.0:8000
  volumes:
    - .:/code
  ports:
    - "8000:8000"
  links:
    - db
```
查看 [`fig.yml` 章节]() 了解更多详细的工作机制。

使用 `fig run` 命令开始着手一个 Django 应用。

```
$ fig run web django-admin.py startproject figexample .
```
首先 Fig 会使用 `Dockerfile` 为 web 服务创建一个容器。然后它就会在容器里运行 `django-admin.py startproject figexample .` 。

这将在当前目录生成一个 Django 应用。

```
$ ls
Dockerfile       fig.yml          figexample       manage.py       requirements.txt
```
首先我们要为应用是设置好数据库的连接信息。用以下内容替换 `figexample/settings.py` 文件中 `DATABASES = ...` 定义的节点内容。

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
```
这些信息是在 [postgres](https://registry.hub.docker.com/_/postgres/) Docker 镜像预先定义好的。
然后，运行 `fig up` ：
	
```
Recreating myapp_db_1...
Recreating myapp_web_1...
Attaching to myapp_db_1, myapp_web_1
myapp_db_1 |
myapp_db_1 | PostgreSQL stand-alone backend 9.1.11
myapp_db_1 | 2014-01-27 12:17:03 UTC LOG:  database system is ready to accept connections
myapp_db_1 | 2014-01-27 12:17:03 UTC LOG:  autovacuum launcher started
myapp_web_1 | Validating models...
myapp_web_1 |
myapp_web_1 | 0 errors found
myapp_web_1 | January 27, 2014 - 12:12:40
myapp_web_1 | Django version 1.6.1, using settings 'figexample.settings'
myapp_web_1 | Starting development server at http://0.0.0.0:8000/
myapp_web_1 | Quit the server with CONTROL-C.

```
这个 web 应用已经开始在你的 docker 守护进程里面监听着 5000 端口了（如果你有使用 boot2docker ，执行 `boot2docker ip` ，就会看到它的地址）。