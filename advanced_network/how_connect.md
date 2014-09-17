##Docker 如何连接到容器？

让我们回顾一些基础知识：
机器需要一个网络接口来发送和接受数据包，路由表来定义如何到达哪些地址段。这里的网络接口可以不是物理接口。事实上，每个linxu机器上的lo环回接口（docker 容器中也有）就是一个完全的linux内核虚拟接口，它直接复制发送缓存中的数据包到接收缓存中。docker让宿主主机和容器使用特殊的虚拟接口来通信--通信的2端叫“peers“，他们在主机内核中连接在一起，所以能够相互通信。创建他们很简单，前面介绍过了。

docker创建容器的步骤如下：
* 创建一对虚拟接口
* 其中宿主主机一端使用一个名字比如veth65f9，他是唯一的,另外一端桥接到默认的docker0,或其它你指定的桥接网卡。
* 主机上的veth65f9这种接口映射到新的新容器中的名称通常是eth0,在容器这个隔离的network namespace 
中，它是唯一的，不会有其他接口名字和它冲突。
* 从主机桥接网卡的地址段中获取一个空闲地址给eth0使用，并设定默认路由到桥接网卡。
* 完成这些之后，容器就可以使用这eth0虚拟网卡来连接其他容器和其他网络。
	
你也可以为特殊的容器设定特定的参数，在docker run的时候使用--net，它有4个可选参数：
* --net=bridge — .默认连接到docker0网桥。
* --net=host —  告诉docker不要将容器放到隔离的网络堆栈中。从本质上讲，这个选项告诉docker
不要容器化容器的网络！尽管容器还是有自己的文件系统、进程列表和资源限制。但使用ip addr命令这样命令就可以知道实际上此时的的容器处于和docker 宿主主机的一样的网络级别，它拥有完全的宿主主机接口访问权限。虽然它不允许容器重新配置主机的网络堆栈，除非--privileged=true — 但是容器进程可以跟其他root进程一样可以打开低数字的端口，可以访问本地网络服务比如D-bus，还可以让容器做一些意想不到的事情，比如重启主机，使用这个选项的时候要非常小心！
* --net=container:NAME_or_ID — 
告诉docker将新容器的进程放到一个已经存在的容器的网络堆栈中，新容器进程有它自己的文件系统、进程列表和资源限制，但它会和那个已经存在的容器共享ip地址和端口，他们之间来可以通过环回接口通信。
* --net=none — 告诉docker将新容器放到自己的网络堆栈中，但是不要配置它的网络,
类似于vmware的host-only。这可以让你创建任何自定义的配置，本文最后一段将介绍 他们。

下面通过配置一个以--net=none启动的容器，使他达到跟平常一样具有访问网络的权限。来介绍docker是如何连接到容器中的。

启动一个/bin/bash 指定--net=none
```
$ sudo docker run -i -t --rm --net=none base /bin/bash
root@63f36fc01b5f:/#
```
再开启一个新的终端，查找这个容器的进程id，然后创建它的命名空间，后面的ip netns会用到
```
$ sudo docker inspect -f '{{.State.Pid}}' 63f36fc01b5f
2778
$ pid=2778
$ sudo mkdir -p /var/run/netns
$ sudo ln -s /proc/$pid/ns/net /var/run/netns/$pid     
```
检查桥接网卡的ip和子网掩码
```
$ ip addr show docker0
21: docker0: ...
inet 172.17.42.1/16 scope global docker0
...
```
创建一对”peer“接口A和B，绑定A到网桥，并启用它
```
$ sudo ip link add A type veth peer name B
$ sudo brctl addif docker0 A
$ sudo ip link set A up
```
将B放到容器的网络命名空间，命名为eth0,配置一个空闲的ip
```
$ sudo ip link set B netns $pid
$ sudo ip netns exec $pid ip link set dev B name eth0
$ sudo ip netns exec $pid ip link set eth0 up
$ sudo ip netns exec $pid ip addr add 172.17.42.99/16 dev eth0
$ sudo ip netns exec $pid ip route add default via 172.17.42.1
```
自此，你又可以像平常一样使用网络了
当你退出shell后，docker清空容器，容器的eth0随网络命名空间一起被摧毁，A 接口也被自动从docker0取消注册。不用其他命令，所有东西都被清理掉了！
注意ip netns exec命令，它可以让我们像root一样配置网络命名空间。但在容器内部无法使用，因为统一的安全策略，docker限制容器进程配置自己的网络。使用ip netns exec 可以让我们不用设置--privileged=true就可以完成一些可能带来危险的操作。
