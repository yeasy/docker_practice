##基本架构
docker采用了C/S架构，包括client端和daemon端。
docker daemon作为server端接受来自client的请求，并处理这些请求（创建、运行、分发容器）。
client端和server端既可以运行在一个机器上，也可通过socket或者RESTful API来进行通信。

![Docker基本架构](../images/docker_arch.png)


Docker daemon一般在宿主主机后台运行，等待接收来自client端的消息。
Docker client 则为用户提供一系列可执行命令，用户用这些docker命令实现跟docker daemon交互。

##核心技术
docker底层的2个核心技术分别是Namespaces和Control groups。

以下内容摘自InfoQ Docker，自1.20版本开始docker已经抛开lxc，不过下面的内容对于理解docker还是有很大帮助。

###pid namespace
不同用户的进程就是通过pid namespace隔离开的，且不同 namespace 中可以有相同pid。所有的LXC进程在docker中的父进程为docker进程，每个lxc进程具有不同的namespace。同时由于允许嵌套，因此可以很方便的实现 Docker in Docker。

###net namespace
有了 pid namespace, 每个namespace中的pid能够相互隔离，但是网络端口还是共享host的端口。网络隔离是通过net namespace实现的， 每个net namespace有独立的 network devices, IP addresses, IP routing tables, /proc/net 目录。这样每个container的网络就能隔离开来。docker默认采用veth的方式将container中的虚拟网卡同host上的一个docker bridge: docker0连接在一起。

###ipc namespace
container中进程交互还是采用linux常见的进程间交互方法(interprocess communication - IPC), 包括常见的信号量、消息队列和共享内存。然而同 VM 不同的是，container 的进程间交互实际上还是host上具有相同pid namespace中的进程间交互，因此需要在IPC资源申请时加入namespace信息 - 每个IPC资源有一个唯一的 32 位 ID。

###mnt namespace
类似chroot，将一个进程放到一个特定的目录执行。mnt namespace允许不同namespace的进程看到的文件结构不同，这样每个 namespace 中的进程所看到的文件目录就被隔离开了。同chroot不同，每个namespace中的container在/proc/mounts的信息只包含所在namespace的mount point。

###uts namespace
UTS("UNIX Time-sharing System") namespace允许每个container拥有独立的hostname和domain name, 使其在网络上可以被视作一个独立的节点而非Host上的一个进程。

###user namespace
每个container可以有不同的 user 和 group id, 也就是说可以在container内部用container内部的用户执行程序而非Host上的用户。

Control groups主要用来隔离各个容器和宿主主机的资源利用。
