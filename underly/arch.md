##基本架构
Docker采用了C/S架构，包括客户端和服务端。
docker daemon作为服务端接受来自客户的请求，并处理这些请求（创建、运行、分发容器）。
客户端和服务端既可以运行在一个机器上，也可通过socket或者RESTful API来进行通信。

![Docker基本架构](../_images/docker_arch.png)


Docker daemon一般在宿主主机后台运行，等待接收来自客户端的消息。
Docker客户端则为用户提供一系列可执行命令，用户用这些命令实现跟docker daemon交互。
