## Docker 網絡實現

Docker 的網絡實現其實就是利用了 Linux 上的網絡名字空間和虛擬網絡設備（特別是 veth pair）。建議先熟悉了解這兩部分的基本概念再閱讀本章。

### 基本原理
首先，要實現網絡通信，機器需要至少一個網絡接口（物理接口或虛擬接口）來收發數據包；此外，如果不同子網之間要進行通信，需要路由機制。

Docker 中的網絡接口默認都是虛擬的接口。虛擬接口的優勢之一是轉發效率較高。
Linux 通過在內核中進行數據復制來實現虛擬接口之間的數據轉發，發送接口的發送緩存中的數據包被直接復制到接收接口的接收緩存中。對於本地系統和容器內系統看來就像是一個正常的以太網卡，只是它不需要真正同外部網絡設備通信，速度要快很多。

Docker 容器網絡就利用了這項技術。它在本地主機和容器內分別創建一個虛擬接口，並讓它們彼此連通（這樣的一對接口叫做 `veth pair`）。

### 創建網絡參數
Docker 創建一個容器的時候，會執行如下操作：
* 創建一對虛擬接口，分別放到本地主機和新容器中；
* 本地主機一端橋接到默認的 docker0 或指定網橋上，並具有一個唯一的名字，如 veth65f9；
* 容器一端放到新容器中，並修改名字作為 eth0，這個接口只在容器的名字空間可見；
* 從網橋可用地址段中獲取一個空閑地址分配給容器的 eth0，並配置默認路由到橋接網卡 veth65f9。

完成這些之後，容器就可以使用 eth0 虛擬網卡來連接其他容器和其他網絡。

可以在 `docker run` 的時候通過 `--net` 參數來指定容器的網絡配置，有4個可選值：
* `--net=bridge` 這個是默認值，連接到默認的網橋。
* `--net=host` 告訴 Docker 不要將容器網絡放到隔離的名字空間中，即不要容器化容器內的網絡。此時容器使用本地主機的網絡，它擁有完全的本地主機接口訪問權限。容器程序可以跟主機其它 root 程序一樣可以打開低範圍的端口，可以訪問本地網絡服務比如 D-bus，還可以讓容器做一些影響整個主機系統的事情，比如重啟主機。因此使用這個選項的時候要非常小心。如果進一步的使用 `--privileged=true`，容器會被允許直接配置主機的網絡堆棧。
* `--net=container:NAME_or_ID` 讓 Docker 將新建容器的程序放到一個已存在容器的網絡棧中，新容器程序有自己的文件系統、程序列表和資源限制，但會和已存在的容器共享 IP 地址和端口等網絡資源，兩者程序可以直接通過 `lo` 環回接口通信。
* `--net=none` 讓 Docker 將新容器放到隔離的網絡棧中，但是不進行網絡配置。之後，用戶可以自己進行配置。

### 網絡配置細節
用戶使用 `--net=none` 後，可以自行配置網絡，讓容器達到跟平常一樣具有訪問網絡的權限。通過這個過程，可以了解 Docker 配置網絡的細節。

首先，啟動一個 `/bin/bash` 容器，指定 `--net=none` 參數。
```
$ sudo docker run -i -t --rm --net=none base /bin/bash
root@63f36fc01b5f:/#
```
在本地主機查找容器的程序 id，並為它創建網絡命名空間。
```
$ sudo docker inspect -f '{{.State.Pid}}' 63f36fc01b5f
2778
$ pid=2778
$ sudo mkdir -p /var/run/netns
$ sudo ln -s /proc/$pid/ns/net /var/run/netns/$pid
```
檢查橋接網卡的 IP 和子網掩碼信息。
```
$ ip addr show docker0
21: docker0: ...
inet 172.17.42.1/16 scope global docker0
...
```
創建一對 “veth pair” 接口 A 和 B，綁定 A 到網橋 `docker0`，並啟用它
```
$ sudo ip link add A type veth peer name B
$ sudo brctl addif docker0 A
$ sudo ip link set A up
```
將B放到容器的網絡命名空間，命名為 eth0，啟動它並配置一個可用 IP（橋接網段）和默認網關。
```
$ sudo ip link set B netns $pid
$ sudo ip netns exec $pid ip link set dev B name eth0
$ sudo ip netns exec $pid ip link set eth0 up
$ sudo ip netns exec $pid ip addr add 172.17.42.99/16 dev eth0
$ sudo ip netns exec $pid ip route add default via 172.17.42.1
```
以上，就是 Docker 配置網絡的具體過程。

當容器結束後，Docker 會清空容器，容器內的 eth0 會隨網絡命名空間一起被清除，A 接口也被自動從 `docker0` 卸載。

此外，用戶可以使用 `ip netns exec` 命令來在指定網絡名字空間中進行配置，從而配置容器內的網絡。
