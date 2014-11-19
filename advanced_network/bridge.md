## 自定義網橋
除了默認的 `docker0` 網橋，用戶也可以指定網橋來連接各個容器。

在啟動 Docker 服務的時候，使用 `-b BRIDGE`或`--bridge=BRIDGE` 來指定使用的網橋。

如果服務已經執行，那需要先停止服務，並刪除舊的網橋。
```
$ sudo service docker stop
$ sudo ip link set dev docker0 down
$ sudo brctl delbr docker0
```
然後創建一個網橋 `bridge0`。
```
$ sudo brctl addbr bridge0
$ sudo ip addr add 192.168.5.1/24 dev bridge0
$ sudo ip link set dev bridge0 up
```
查看確認網橋創建並啟動。
```
$ ip addr show bridge0
4: bridge0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state UP group default
    link/ether 66:38:d0:0d:76:18 brd ff:ff:ff:ff:ff:ff
    inet 192.168.5.1/24 scope global bridge0
       valid_lft forever preferred_lft forever
```
配置 Docker 服務，默認橋接到創建的網橋上。
```
$ echo 'DOCKER_OPTS="-b=bridge0"' >> /etc/default/docker
$ sudo service docker start
```
啟動 Docker 服務。
新建一個容器，可以看到它已經橋接到了 `bridge0` 上。

可以繼續用 `brctl show` 命令查看橋接的信息。另外，在容器中可以使用 `ip addr` 和 `ip route` 命令來查看 IP 地址配置和路由信息。
