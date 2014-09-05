##映射一个容器端口到宿主主机

默认情况下，容器可以建立到外部网络的连接，但是外部网络无法连接到容器。所有到外部的连接，源地址都会被伪装成宿主主机的ip地址，iptables的 masquerading来做到这一点。

```
# 查看主机的masquerading规则
$ sudo iptables -t nat -L -n
...
Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
MASQUERADE  all  --  172.17.0.0/16       !172.17.0.0/16
...
```

当你希望容器接收外部连接时，你需要在docker run执行的时候就指定对应选项，第五章详细介绍了2种方法：
* 指定-P --publish-all=true|false 选项会映射dockerfile 
中expose的所有端口，主机端口在49000-49900中随机挑选。当你的另外一个容器需要学习这个端口时候，很不方便。
* 指定-p SPEC或则 --publish=SPEC,可以指定任意端口从主机映射容器内部

不管用那种办法，你可以通过查看iptable的 nat表来观察docker 在网络层做了什么操作。
```
#使用-P时：
$ iptables -t nat -L -n
...
Chain DOCKER (2 references)
target     prot opt source               destination
DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:49153 to:172.17.0.2:80
#使用-p 80:80时：
$ iptables -t nat -L -n
Chain DOCKER (2 references)
target     prot opt source               destination
DNAT       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:80 to:172.17.0.2:80
```
注意：
* 这里看到docker映射了0.0.0.0.它接受主机上的所有接口地址。可以通过-p IP:host_port:container_port 或则 -p 
IP::port 来指定主机上的ip、接口，制定更严格的规则。
* 如果你希望永久改变绑定的主机ip地址，可以 在dcoker 配置中指定--ip=IP_ADDRESS. 记得重启服务。