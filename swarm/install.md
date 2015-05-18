## 安装
安装swarm的最简单的方式是使用Docker官方的swarm镜像
> $ sudo docker pull swarm 

可以使用下面的命令来查看swarm是否成功安装。
 > $ sudo docker run --rm swarm -v
 
 输出下面的形式则表示成功安装(具体输出根据swarm的版本变化)
> $ swarm version 0.2.0 (48fd993)
