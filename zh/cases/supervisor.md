## 使用 Supervisor 来管理进程
Docker 容器在启动的时候开启单个进程，比如，一个 ssh 或者 apache 的 daemon 服务。但我们经常需要在一个机器上开启多个服务，这可以有很多方法，最简单的就是把多个启动命令方到一个启动脚本里面，启动的时候直接启动这个脚本，另外就是安装进程管理工具。

本小节将使用进程管理工具 supervisor 来管理容器中的多个进程。使用 Supervisor 可以更好的控制、管理、重启我们希望运行的进程。在这里我们演示一下如何同时使用 ssh 和 apache 服务。

### 配置
首先创建一个 Dockerfile，内容和各部分的解释如下。
```
FROM ubuntu:13.04
MAINTAINER examples@docker.com
RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade -y
```

### 安装 supervisor
安装 ssh、apache 和 supervisor。
```
RUN apt-get install -y openssh-server apache2 supervisor
RUN mkdir -p /var/run/sshd
RUN mkdir -p /var/log/supervisor
```

这里安装 3 个软件，还创建了 2 个 ssh 和 supervisor 服务正常运行所需要的目录。
```
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
```
添加 supervisord 的配置文件，并复制配置文件到对应目录下面。

```
EXPOSE 22 80
CMD ["/usr/bin/supervisord"]
```
这里我们映射了 22 和 80 端口，使用 supervisord 的可执行路径启动服务。


### supervisor配置文件内容
```
[supervisord]
nodaemon=true
[program:sshd]
command=/usr/sbin/sshd -D

[program:apache2]
command=/bin/bash -c "source /etc/apache2/envvars && exec /usr/sbin/apache2 -DFOREGROUND"
```
配置文件包含目录和进程，第一段 supervsord 配置软件本身，使用 nodaemon 参数来运行。第二段包含要控制的 2 个服务。每一段包含一个服务的目录和启动这个服务的命令。

### 使用方法
创建镜像。
```
$ sudo docker build -t test/supervisord .
```
启动 supervisor 容器。
```
$ sudo docker run -p 22 -p 80 -t -i test/supervisords
2013-11-25 18:53:22,312 CRIT Supervisor running as root (no user in config file)
2013-11-25 18:53:22,312 WARN Included extra file "/etc/supervisor/conf.d/supervisord.conf" during parsing
2013-11-25 18:53:22,342 INFO supervisord started with pid 1
2013-11-25 18:53:23,346 INFO spawned: 'sshd' with pid 6
2013-11-25 18:53:23,349 INFO spawned: 'apache2' with pid 7
```
使用 `docker run` 来启动我们创建的容器。使用多个 `-p` 来映射多个端口，这样我们就能同时访问 ssh 和 apache 服务了。

可以使用这个方法创建一个只有 ssh 服务的基础镜像，之后创建镜像可以使用这个镜像为基础来创建
