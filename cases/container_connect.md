## 多臺物理主機之間的容器互聯（暴露容器到真實網路中）
Docker 默認的橋接網卡是 docker0。它只會在本機橋接所有的容器網卡，舉例來說容器的虛擬網卡在主機上看一般叫做 veth***  而 Docker 只是把所有這些網卡橋接在一起，如下：
```
[root@opnvz ~]# brctl show
bridge name     bridge id               STP enabled     interfaces
docker0         8000.56847afe9799       no              veth0889
                                             veth3c7b
                                             veth4061
```
在容器中看到的地址一般是像下面這樣的地址：
```
root@ac6474aeb31d:~# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
11: eth0: <BROADCAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 4a:7d:68:da:09:cf brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.3/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::487d:68ff:feda:9cf/64 scope link
       valid_lft forever preferred_lft forever
```
這樣就可以把這個網路看成是一個私有的網路，通過 nat 連接外網，如果要讓外網連接到容器中，就需要做端口映射，即 -p 參數。

如果在企業內部應用，或者做多個物理主機的集群，可能需要將多個物理主機的容器組到一個物理網路中來，那麽就需要將這個網橋橋接到我們指定的網卡上。

### 拓撲圖
主機 A 和主機 B 的網卡一都連著物理交換機的同一個 vlan 101,這樣網橋一和網橋三就相當於在同一個物理網路中了，而容器一、容器三、容器四也在同一物理網路中了，他們之間可以相互通信，而且可以跟同一 vlan 中的其他物理機器互聯。
![物理拓撲圖](../_images/container_connect_topology.png)

### ubuntu 示例
下面以 ubuntu 為例創建多個主機的容器聯網:
創建自己的網橋,編輯 /etc/network/interface 文件
```
auto br0
iface br0 inet static
address 192.168.7.31
netmask 255.255.240.0
gateway 192.168.7.254
bridge_ports em1
bridge_stp off
dns-nameservers 8.8.8.8 192.168.6.1
```
將 Docker 的默認網橋綁定到這個新建的 br0 上面，這樣就將這臺機器上容器綁定到 em1 這個網卡所對應的物理網路上了。

ubuntu 修改 /etc/default/docker 文件，添加最後一行內容

```
# Docker Upstart and SysVinit configuration file
# Customize location of Docker binary (especially for development testing).
#DOCKER="/usr/local/bin/docker"
# Use DOCKER_OPTS to modify the daemon startup options.
#DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4"

# If you need Docker to use an HTTP proxy, it can also be specified here.
#export http_proxy="http://127.0.0.1:3128/"

# This is also a handy place to tweak where Docker's temporary files go.
#export TMPDIR="/mnt/bigdrive/docker-tmp"

DOCKER_OPTS="-b=br0"
```

在啟動 Docker 的時候 使用 -b 參數 將容器綁定到物理網路上。重啟 Docker 服務後，再進入容器可以看到它已經綁定到你的物理網路上了。

```
root@ubuntudocker:~# docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                        NAMES
58b043aa05eb        desk_hz:v1          "/startup.sh"       5 days ago          Up 2 seconds        5900/tcp, 6080/tcp, 22/tcp   yanlx
root@ubuntudocker:~# brctl show
bridge name     bridge id               STP enabled     interfaces
br0             8000.7e6e617c8d53       no              em1
                                            vethe6e5
```
這樣就直接把容器暴露到物理網路上了，多臺物理主機的容器也可以相互聯網了。需要註意的是，這樣就需要自己來保證容器的網路安全了。
