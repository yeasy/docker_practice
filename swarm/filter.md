## Swarm 过滤器
swarm 的调度器(scheduler)在选择节点运行容器的时候支持几种过滤器 (filter)：Constraint,Affinity,Port,Dependency,Health

可以在执行 `swarm manage` 命令的时候通过 `--filter` 选项来设置。

###Constraint Filter
constraint 是一个跟具体节点相关联的键值对，可以看做是每个节点的标签，这个标签可以在启动docker daemon的时候指定，比如
```bash
sudo docker -d --label label_name=label01
```

也可以写在docker的配置文件里面（在ubuntu上面是 `/etc/default/docker`）。

在本次试验中，给083添加标签--label label_name=083,084添加标签--label label_name=084,124添加标签--label label_name=124,

以083为例，打开/etc/default/docker文件，修改DOCKER_OPTS：
```bash
DOCKER_OPTS="-H 0.0.0.0:2375 -H unix:///var/run/docker.sock  --label label_name=083"
```

在使用docker run命令启动容器的时候使用 `-e constarint:key=value` 的形式，可以指定container运行的节点。

比如我们想在84上面启动一个 redis 容器。
```bash
rio@085:~$ sudo docker -H 192.168.1.83:2376 run --name redis_1 -d -e constraint:label_name==084 redis
fee1b7b9dde13d64690344c1f1a4c3f5556835be46b41b969e4090a083a6382d
```
注意，是**两个**等号，不是一个等号，这一点会经常被忽略。

接下来再在084这台机器上启动一个redis 容器。
```bash
rio@085:~$ sudo docker -H 192.168.1.83:2376 run --name redis_2 -d -e constraint:label_name==084 redis         4968d617d9cd122fc2e17b3bad2f2c3b5812c0f6f51898024a96c4839fa000e1
```
然后再在083这台机器上启动另外一个 redis 容器。
```bash
rio@085:~$ sudo docker -H 192.168.1.83:2376 run --name redis_3 -d -e constraint:label_name==083 redis         7786300b8d2232c2335ac6161c715de23f9179d30eb5c7e9c4f920a4f1d39570
```

现在来看下执行情况：
```bash
rio@085:~$ sudo docker -H 192.168.1.83:2376 ps
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS               NAMES
7786300b8d22        redis:latest        "/entrypoint.sh redi   15 minutes ago      Up 53 seconds       6379/tcp            083/redis_3
4968d617d9cd        redis:latest        "/entrypoint.sh redi   16 minutes ago      Up 2 minutes        6379/tcp            084/redis_2
fee1b7b9dde1        redis:latest        "/entrypoint.sh redi   19 minutes ago      Up 5 minutes        6379/tcp            084/redis_1
```

可以看到，执行结果跟预期的一样。

但是如果指定一个不存在的标签的话来运行容器会报错。
```bash
rio@085:~$ sudo docker -H 192.168.1.83:2376 run --name redis_0 -d -e constraint:label_name==0 redis
FATA[0000] Error response from daemon: unable to find a node that satisfies label_name==0
```

###Affinity Filter
通过使用 Affinity Filter，可以让一个容器紧挨着另一个容器启动，也就是说让两个容器在同一个节点上面启动。

现在其中一台机器上面启动一个 redis 容器。
```bash
rio@085:~$ sudo docker -H 192.168.1.83:2376 run -d --name redis redis
ea13eddf667992c5d8296557d3c282dd8484bd262c81e2b5af061cdd6c82158d
rio@085:~$ sudo docker -H 192.168.1.83:2376  ps
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                  PORTS               NAMES
ea13eddf6679        redis:latest        /entrypoint.sh redis   24 minutes ago      Up Less than a second   6379/tcp            083/redis
```

然后再次启动两个 redis 容器。
```bash
rio@085:~$ sudo docker -H 192.168.1.83:2376  run -d --name redis_1 -e affinity:container==redis redis
bac50c2e955211047a745008fd1086eaa16d7ae4f33c192f50412e8dcd0a14cd
rio@085:~$ sudo docker -H 192.168.1.83:2376  run -d --name redis_1 -e affinity:container==redis redis
bac50c2e955211047a745008fd1086eaa16d7ae4f33c192f50412e8dcd0a14cd
```
现在来查看下运行结果,可以看到三个容器都是在一台机器上运行
```bash
rio@085:~$ sudo docker -H 192.168.1.83:2376  ps
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                  PORTS               NAMES
449ed25ad239        redis:latest        /entrypoint.sh redis   24 minutes ago      Up Less than a second   6379/tcp            083/redis_2
bac50c2e9552        redis:latest        /entrypoint.sh redis   25 minutes ago      Up 10 seconds           6379/tcp            083/redis_1
ea13eddf6679        redis:latest        /entrypoint.sh redis   28 minutes ago      Up 3 minutes            6379/tcp            083/redis
```
通过 `-e affinity:image=image_name` 命令可以指定只有已经下载了`image_name`镜像的机器才运行容器
```bash
sudo docker –H 192.168.1.83:2376 run –name redis1 –d –e affinity:image==redis redis 
```
redis1 这个容器只会在已经下载了 redis 镜像的节点上运行。

```bash
sudo docker -H 192.168.1.83:2376 run -d --name redis -e affinity:image==~redis redis
```
这条命令达到的效果是：在有 redis 镜像的节点上面启动一个名字叫做 redis 的容器，如果每个节点上面都没有 redis 容器，就按照默认的策略启动 redis 容器。

###Port Filter
Port 也会被认为是一个唯一的资源
```bash
sudo docker -H 192.168.1.83:2376 run -d -p 80:80 nginx
```

执行完这条命令，之后任何使用 80 端口的容器都是启动失败。
