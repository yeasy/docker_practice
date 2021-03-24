# 启动容器

启动容器有两种方式，一种是基于镜像新建一个容器并启动，另外一个是将在终止状态（`exited`）的容器重新启动。

因为 Docker 的容器实在太轻量级了，很多时候用户都是随时删除和新创建容器。

## 新建并启动

所需要的命令主要为 `docker run`。

例如，下面的命令输出一个 “Hello World”，之后终止容器。

```bash
$ docker run ubuntu:18.04 /bin/echo 'Hello world'
Hello world
```

这跟在本地直接执行 `/bin/echo 'hello world'` 几乎感觉不出任何区别。

下面的命令则启动一个 bash 终端，允许用户进行交互。

```bash
$ docker run -t -i ubuntu:18.04 /bin/bash
root@af8bae53bdd3:/#
```

其中，`-t` 选项让Docker分配一个伪终端（pseudo-tty）并绑定到容器的标准输入上， `-i` 则让容器的标准输入保持打开。

在交互模式下，用户可以通过所创建的终端来输入命令，例如

```bash
root@af8bae53bdd3:/# pwd
/
root@af8bae53bdd3:/# ls
bin boot dev etc home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var
```

当利用 `docker run` 来创建容器时，Docker 在后台运行的标准操作包括：

* 检查本地是否存在指定的镜像，不存在就从 [registry](../repository/README.md) 下载
* 利用镜像创建并启动一个容器
* 分配一个文件系统，并在只读的镜像层外面挂载一层可读写层
* 从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去
* 从地址池配置一个 ip 地址给容器
* 执行用户指定的应用程序
* 执行完毕后容器被终止

## 启动已终止容器

可以利用 `docker container start` 命令，直接将一个已经终止（`exited`）的容器启动运行。

容器的核心为所执行的应用程序，所需要的资源都是应用程序运行所必需的。除此之外，并没有其它的资源。可以在伪终端中利用 `ps` 或 `top` 来查看进程信息。

```bash
root@ba267838cc1b:/# ps
  PID TTY          TIME CMD
    1 ?        00:00:00 bash
   11 ?        00:00:00 ps
```

可见，容器中仅运行了指定的 bash 应用。这种特点使得 Docker 对资源的利用率极高，是货真价实的轻量级虚拟化。


#停止容器
docker stop可以停止运行的容器。
理解：容器在docker host中实际上是一个进程，docker stop命令本质上是向该进程发送一个SIGTERM信号。如果
想要快速停止容器，可使用docker kill命令，其作用是向容器进程发送SIGKILL信号。
```bash
        $ docker ps
        CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                  PORTS               NAMES
        bdf593fda8be        ubuntu:15.10        "/bin/bash"         3 minutes ago       Up 3 minutes (Paused)                       cranky_mclaren                  
    
        $ docker stop bdf593fda8be
            bdf593fda8be
        $ docker ps
        CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
        LM-
  
```
备注：docker ps 列出容器，默认列出只在运行的容器；加-a可以显示所有的容器，包括未运行的（例如异常退出（Exited）状态的容器）。

```bash
    $ docker ps -a
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    bdf593fda8be        ubuntu:15.10        "/bin/bash"         18 minutes ago      Up 6 minutes                            cranky_mclaren
    $ docker ps -a
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                    PORTS               NAMES
    2a545c90e593        ubuntu:15.10        "/bin/echo -d 'Hello…"   1 second ago        Exited (0) 1 second ago                       blissful_leakey
    bdf593fda8be        ubuntu:15.10        "/bin/bash"              18 minutes ago      Up 6 minutes                                  cranky_mclaren
```


#重启容器
对于已经处于停止状态的容器，可以通过docker start重新启动。
```bash
       $ docker start bdf593fda8be
            bdf593fda8be
       $ docker ps
            CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
            bdf593fda8be        ubuntu:15.10        "/bin/bash"         11 minutes ago      Up 2 seconds                            cranky_mclaren
            L
```
docker start会保留容器的第一次启动时的所有参数。
docker restart可以重启容器，其作用就是依次执行docker stop和docker start。
容器可能因某种错误而停止运行。对于服务类容器，通常希望它能够自动重启。启动容器时设置--restart就可以达到效果。

--restart=always意味着无论容器因何种原因退出（包括正常退出），都立即重启；

```bash
$ docker run -it ubuntu:15.10 /bin/echo --restart=always -d "Hello world"
--restart=always -d Hello world

$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                     PORTS               NAMES
ad0723ad8383        ubuntu:15.10        "/bin/echo --restart…"   9 seconds ago       Exited (0) 8 seconds ago                       gracious_chatelet
2a545c90e593        ubuntu:15.10        "/bin/echo -d 'Hello…"   6 minutes ago       Exited (0) 6 minutes ago                       blissful_leakey
bdf593fda8be        ubuntu:15.10        "/bin/bash"              25 minutes ago      Up 13 minutes                                  cranky_mclaren
```
