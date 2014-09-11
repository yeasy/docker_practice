#架构
docker采用了C/S架构，包括client端和daemon端。
docker daemon作为server端接受来自client的请求，并处理这些请求（创建、运行、分发容器）。
client端和server端既可以运行在一个机器上，也可通过socket或者RESTful API来进行通信。

![Docker基本架构](../images/docker_arch.png)


Docker daemon一般在宿主主机后台运行，等待接收来自client端的消息。
Docker client 则为用户提供一系列可执行命令，用户用这些docker命令实现跟docker daemon交互。