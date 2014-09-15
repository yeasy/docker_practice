##容器之间的通信
判断2个容器之间是否能够通信，在操作系统层面，取决于3个因素：
* 网络拓扑是否连接到容器的网络接口？默认docker会将所有的容器连接到docker0这网桥来提供数据包通信。其他拓扑结构将在稍后的文档中详细介绍。
* 主机是否开启ip转发，ip_forward参数为1的时候可以提供数据包转发。通常你只需要为docker 设定 --ip-forward=true,
docker 就会在服务启动的时候设定ip_forward参数为1。下面是手工检查并手工设定该参数的方法。
```
# Usually not necessary: turning on forwarding,
# on the host where your Docker server is running
$ cat /proc/sys/net/ipv4/ip_forward
0
$ sudo echo 1 > /proc/sys/net/ipv4/ip_forward
$ cat /proc/sys/net/ipv4/ip_forward
1
```
*你的iptables是否允许这条特殊的连接被建立？当docker的设定--iptables=false时，docker不会改变系统的iptables
设定，否则它会在--icc=true的时候添加一条默认的ACCEPT策略到 FORWARD链，当—icc=false时，策略为DROP。几乎所有的人都会开启ip_forward来启用容器间的通信。但是否要改变icc-true配置是一个战略问题。这样iptable就可以防止其他被感染容器对宿主主机的恶意端口扫描和访问。
当你选择更安全的设定--icc=false后，如何保持你希望的容器之间通信呢？
答案就是--link=CONTAINER_NAME:ALIAS选项，在之前的dns服务设定中提及过。如果docker 使用icc=false and --iptables=true 2个参数，当docker run使用--link=选型时，docker会为2个容器在iptable中参数一对ACCEPT规则，开放的端口取决与dockerfile中的EXPOSE行，详见第五章。
注意：--link= 中的CONTAINER_NAME 必须是自动生成的docker名字比如stupefied_pare，或者你用--name参数指定的名字，主机名在--link中不会被识别。
你可以使用iptables命令来检查FORWARD链是ACCEPT 还是DROP
当--icc=false时，默认规则应该是这样
```
$ sudo iptables -L -n
...
Chain FORWARD (policy ACCEPT)
target     prot opt source               destination
DROP       all  --  0.0.0.0/0            0.0.0.0/0
...
```
当添加了--link后，ACCEPT规则被改写了，添加了新的端口和IP规则
```
$ sudo iptables -L -n
...
Chain FORWARD (policy ACCEPT)
target     prot opt source               destination
ACCEPT     tcp  --  172.17.0.2           172.17.0.3           tcp spt:80
ACCEPT     tcp  --  172.17.0.3           172.17.0.2           tcp dpt:80
DROP       all  --  0.0.0.0/0            0.0.0.0/0
```
