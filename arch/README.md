#架构
docker使用C/S架构，docker daemon作为server端接受client的请求，并处理（创建、运行、分发容器），他们可以运行在一个机器上，也通过sockerts或者RESTful API通信。

![Docker基本架构](../images/docker_arch.png)


Docker daemon一般在宿主主机后台运行，用户使用client而直接跟daemon交互。Docker client 以系统做bin命令的形式存在，用户用docker命令来跟docker daemon交互。