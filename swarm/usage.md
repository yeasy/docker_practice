## 使用
在使用swarm管理集群前，需要把集群中所有的节点的docker daemon的监听方式更改为0.0.0.0:2375,可以有两种方式，第一种是在启动docker daemon的时候指定
> sudo docker -H 0.0.0.0:2375&

第二种方式是直接修改docker的配置文件(以下方式是在ubuntu上面，其他版本的linux上略有不同)
> sudo vim /etc/docker/docker

在文件的最后添加下面这句代码：
> DOCKER_OPTS="-H 0.0.0.0:2375 -H unix:///var/run/docker.sock"

需要注意的是，一定要在**所有的**节点上进行的。
修改之后呀重启docker
> sudo service docker restart

