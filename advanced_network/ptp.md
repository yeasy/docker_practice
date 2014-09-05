##创建一个点到点连接
默认docker会将所有容器连接到由docker0提供的虚拟子网，你也可以使用自己创建的网桥。但如果你想要2个特殊的容器之间可以直连通信，而不用去配置复杂的主机网卡桥接。
解决办法很简单：创建一对接口，把2个容器放到这对接口中，配置成点到点链路类型。这2个容器就可以直接通信了。配置如下：
```
# 在2个终端中启动2个容器
$ sudo docker run -i -t --rm --net=none base /bin/bash
root@1f1f4c1f931a:/#
$ sudo docker run -i -t --rm --net=none base /bin/bash
root@12e343489d2f:/#
```

找到他们的process IDs ，然后创建他们的 namespace entries
```
$ sudo docker inspect -f '{{.State.Pid}}' 1f1f4c1f931a
2989
$ sudo docker inspect -f '{{.State.Pid}}' 12e343489d2f
3004
$ sudo mkdir -p /var/run/netns
$ sudo ln -s /proc/2989/ns/net /var/run/netns/2989
$ sudo ln -s /proc/3004/ns/net /var/run/netns/3004
```

创建"peer"接口，然后配置路由
```
$ sudo ip link add A type veth peer name B

$ sudo ip link set A netns 2989
$ sudo ip netns exec 2989 ip addr add 10.1.1.1/32 dev A
$ sudo ip netns exec 2989 ip link set A up
$ sudo ip netns exec 2989 ip route add 10.1.1.2/32 dev A

$ sudo ip link set B netns 3004
$ sudo ip netns exec 3004 ip addr add 10.1.1.2/32 dev B
$ sudo ip netns exec 3004 ip link set B up
$ sudo ip netns exec 3004 ip route add 10.1.1.1/32 dev B
```
现在这2个容器就可以相互ping通，并成功建立连接。点到点链路不需要子网和子网掩码，使用ip route 来连接单个ip地址到指定的网络接口。
如果没有特殊需要你不需要指定--net=none来创建点到点链路。

还有一个办法就是创建一个只跟主机通信的容器，除非有特殊需求，你可以仅用--icc=false来限制主机间的通信。