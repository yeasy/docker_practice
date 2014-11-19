## 配置 docker0 網橋
Docker 服務默認會創建一個 `docker0` 網橋（其上有一個 `docker0` 內部接口），它在內核層連通了其他的物理或虛擬網卡，這就將所有容器和本地主機都放到同一個物理網絡。

Docker 默認指定了 `docker0` 接口 的 IP 地址和子網掩碼，讓主機和容器之間可以通過網橋相互通信，它還給出了 MTU（接口允許接收的最大傳輸單元），通常是 1500 Bytes，或宿主主機網絡路由上支持的默認值。這些值都可以在服務啟動的時候進行配置。
* `--bip=CIDR` -- IP 地址加掩碼格式，例如 192.168.1.5/24
* `--mtu=BYTES` -- 覆蓋默認的 Docker mtu 配置

也可以在配置文件中配置 DOCKER_OPTS，然後重啟服務。
由於目前 Docker 網橋是 Linux 網橋，用戶可以使用 `brctl show` 來查看網橋和端口連接信息。
```
$ sudo brctl show
bridge name     bridge id               STP enabled     interfaces
docker0         8000.3a1d7362b4ee       no              veth65f9
                                             vethdda6
```
*註：`brctl` 命令在 Debian、Ubuntu 中可以使用 `sudo apt-get install bridge-utils` 來安裝。


每次創建一個新容器的時候，Docker 從可用的地址段中選擇一個空閑的 IP 地址分配給容器的 eth0 端口。使用本地主機上 `docker0` 接口的 IP 作為所有容器的默認網關。
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
