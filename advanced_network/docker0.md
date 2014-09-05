##定制docker0
docker服务默认会创建一个docker0接口，它在linux内核层桥接所有物理或虚拟网卡，这就将所有容器和主机接口都放到同一个物理网络。
Docker指定了docker0的ip地址和子网掩码，让主机和容器之间可以通过网桥相互通信，它还给出了MTU-接口允许接收的最大传输单元，通常是1500bytes或宿主主机网络路由上支持的默认值，这2个都需要在服务启动的时候配置。
* --bip=CIDR — 192.168.1.5/24.ip地址加掩码 使用这种格式
* --mtu=BYTES —  覆盖默认的docker mtu配置

你可以在配置文件中配置DOCKER_OPTS，然后重启来改变这些参数。
```
# 当容器启动后，你可以使用brctl来确认他们是否已经连接到docker0网桥
$ sudo brctl show
bridge name     bridge id               STP enabled     interfaces
docker0         8000.3a1d7362b4ee       no              veth65f9
                                             vethdda6
```                                             
如果brctl命令没安装的话，在ubuntu中你可以使用apt-get install bridge-utils这个命令来安装
docker0 网桥设置会在每次创建新容器的时候被使用。docker从可用的地址段中选择一个空闲的ip地址给容器的eth0端口，子网掩码使用网桥docker0的配置，docker主机本身的ip作为容器的网关使用。
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
转发数据包需要在主机上设定ip_forward参数为1,上文介绍过。