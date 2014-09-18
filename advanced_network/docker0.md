##配置docker0
Docker服务默认会创建一个`docker0`接口，它在内核层连通了其他的物理或虚拟网卡，这就将所有容器和本地主机都放到同一个物理网络。

Docker默认指定了`docker0`的IP地址和子网掩码，让主机和容器之间可以通过网桥相互通信，它还给出了MTU（接口允许接收的最大传输单元），通常是1500bytes，或宿主主机网络路由上支持的默认值，这2个都可以在服务启动的时候进行配置。
* --bip=CIDR -- IP地址加掩码格式，例如192.168.1.5/24
* --mtu=BYTES -- 覆盖默认的Docker mtu配置

也可以在配置文件中配置DOCKER_OPTS，然后重启服务。
由于目前Docker网桥是Linux网桥，用户可以使用`brctl show`来查看网桥和端口连接信息。
```
$ sudo brctl show
bridge name     bridge id               STP enabled     interfaces
docker0         8000.3a1d7362b4ee       no              veth65f9
                                             vethdda6
```
注：`brctl`命令在Debian、Ubuntu中可以使用`sudo apt-get install bridge-utils`来安装。


每次创建一个新容器的时候，Docker从可用的地址段中选择一个空闲的ip地址分配给容器的eth0端口。Docker主机上接口`docker0`的IP作为所有容器的默认网关。
```
$ sudo docker run -i -t --rm base /bin/bash
$ ip addr show eth0
24: eth0: <BROADCAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 32:6f:e0:35:57:91 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.3/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::306f:e0ff:fe35:5791/64 scope link
       valid_lft forever preferred_lft forever
$ ip route
default via 172.17.42.1 dev eth0
172.17.0.0/16 dev eth0  proto kernel  scope link  src 172.17.0.3
$ exit
```
