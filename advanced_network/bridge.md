##创建自己的桥接
如果希望完全使用自己的桥接设置，可以在启动docker服务的时候，使用 -b BRIDGE or --bridge=BRIDGE 来告诉docker使用你的网桥。如果服务已经启动，旧的网桥还在使用中，那需要先停止服务，再删除旧的网桥
```
#停止旧网桥并删除
$ sudo service docker stop
$ sudo ip link set dev docker0 down
$ sudo brctl delbr docker0
```
然后在开启服务前，创建你自己希望的网桥接口，这里建立一个网桥的配置：
```
# 创建自己的网桥
$ sudo brctl addbr bridge0
$ sudo ip addr add 192.168.5.1/24 dev bridge0
$ sudo ip link set dev bridge0 up
```
```
# 确认网桥启动
$ ip addr show bridge0
4: bridge0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state UP group default
    link/ether 66:38:d0:0d:76:18 brd ff:ff:ff:ff:ff:ff
    inet 192.168.5.1/24 scope global bridge0
       valid_lft forever preferred_lft forever
```

```
# 告诉docker桥接设置，并启动docker服务（在ubuntu上）
$ echo 'DOCKER_OPTS="-b=bridge0"' >> /etc/default/docker
$ sudo service docker start
```
docker服务启动成功并绑定容器到新的网桥，新建一个容器，你会看到它的ip是我们的设置的新ip段，docker会自动检测到它。用brctl 
show可以看到容器启动或则停止后网桥的配置变化，在容器中使用```ip addr```和```ip route```来查看ip地址配置和路由信息。