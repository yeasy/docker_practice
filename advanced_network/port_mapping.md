##映射容器端口到宿主主机的实现

默认情况下，容器可以主动访问到外部网络的连接，但是外部网络无法访问到容器。
### 容器访问外部实现
容器所有到外部网络的连接，源地址都会被NAT成本地系统的IP地址。这是使用`iptables`的源地址伪装操作实现的。

查看主机的NAT规则。
```
$ sudo iptables -t nat -nL
...
Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
MASQUERADE  all  --  172.17.0.0/16       !172.17.0.0/16
...
```
其中，上述规则将所有源地址在`172.17.0.0/16`网段，目标地址为其他网段（外部网络）的流量动态伪装为从系统网卡发出。MASQUERADE跟传统SNAT的好处是它能动态从网卡获取地址。

### 外部访问容器实现

容器允许外部访问，可以在`docker run`时候通过`-p`或`-P`参数来启用。

不管用那种办法，其实也是在本地的`iptable`的nat表中添加相应的规则。

使用`-P`时：
```
$ iptables -t nat -nL
...
Chain DOCKER (2 references)
target     prot opt source               destination
DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:49153 to:172.17.0.2:80
```

使用`-p 80:80`时：
```
$ iptables -t nat -nL
Chain DOCKER (2 references)
target     prot opt source               destination
DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:80 to:172.17.0.2:80
```
注意：
* 这里的规则映射了0.0.0.0，意味着将接受主机来自所有接口的流量。用户可以通过`-p IP:host_port:container_port`或`-p
IP::port`来指定允许访问容器的主机上的IP、接口等，以制定更严格的规则。
* 如果希望永久绑定到某个固定的IP地址，可以在Docker 配置文件`/etc/default/docker`中指定`DOCKER_OPTS="--ip=IP_ADDRESS"`，之后重启Docker服务即可生效。
