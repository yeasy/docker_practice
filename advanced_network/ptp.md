## 示例：創建一個點到點連接
默認情況下，Docker 會將所有容器連接到由 `docker0` 提供的虛擬子網中。

用戶有時候需要兩個容器之間可以直連通信，而不用通過主機網橋進行橋接。

解決辦法很簡單：創建一對 `peer` 接口，分別放到兩個容器中，配置成點到點鏈路類型即可。

首先啟動 2 個容器：
```
$ sudo docker run -i -t --rm --net=none base /bin/bash
root@1f1f4c1f931a:/#
$ sudo docker run -i -t --rm --net=none base /bin/bash
root@12e343489d2f:/#
```

找到進程號，然後創建網絡名字空間的跟蹤文件。
```
$ sudo docker inspect -f '{{.State.Pid}}' 1f1f4c1f931a
2989
$ sudo docker inspect -f '{{.State.Pid}}' 12e343489d2f
3004
$ sudo mkdir -p /var/run/netns
$ sudo ln -s /proc/2989/ns/net /var/run/netns/2989
$ sudo ln -s /proc/3004/ns/net /var/run/netns/3004
```

創建一對 `peer` 接口，然後配置路由
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
現在這 2 個容器就可以相互 ping 通，並成功建立連接。點到點鏈路不需要子網和子網掩碼。

此外，也可以不指定 `--net=none` 來創建點到點鏈路。這樣容器還可以通過原先的網絡來通信。

利用類似的辦法，可以創建一個只跟主機通信的容器。但是一般情況下，更推薦使用 `--icc=false` 來關閉容器之間的通信。
