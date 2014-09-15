##守护态运行

更多的时候，需要让Docker容器在后台以守护态（Daemonized）形式运行。此时，可以通过添加`-d`参数来实现。

例如下面的命令会在后台运行容器。
```
$ sudo docker run -d ubuntu:14.04 /bin/sh -c "while true; do echo hello world; sleep 1; done"
1e5535038e285177d5214659a068137486f96ee5c2e85a4ac52dc83f2ebe4147
```

容器启动后会返回一个唯一的id，也可以通过`docker ps`命令来查看容器信息。
```
$ sudo docker ps
CONTAINER ID  IMAGE         COMMAND               CREATED        STATUS       PORTS NAMES
1e5535038e28  ubuntu:14.04  /bin/sh -c 'while tr  2 minutes ago  Up 1 minute        insane_babbage
```
要获取容器的输出信息，可以通过`docker logs`命令。
```
$ sudo docker logs insane_babbage
hello world
hello world
hello world
. . .
```
