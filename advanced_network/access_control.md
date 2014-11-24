## 容器訪問控制
容器的訪問控制，主要透過 Linux 上的 `iptables` 防火墻來進行管理和實做。`iptables` 是 Linux 上默認的防火墻軟件，在大部分發行版中都自帶。

### 容器訪問外部網路
容器要想訪問外部網路，需要本地系統的轉發支持。在Linux 系統中，檢查轉發是否打開。

```
$sysctl net.ipv4.ip_forward
net.ipv4.ip_forward = 1
```
如果為 0，說明沒有開啟轉發，則需要手動打開。
```
$sysctl -w net.ipv4.ip_forward=1
```
如果在啟動 Docker 服務的時候設定 `--ip-forward=true`, Docker 就會自動設定系統的 `ip_forward` 參數為 1。

### 容器之間訪問
容器之間相互訪問，需要兩方面的支持。
* 容器的網路拓撲是否已經互聯。默認情況下，所有容器都會被連接到 `docker0` 網橋上。
* 本地系統的防火墻軟件 -- `iptables` 是否允許透過。

#### 訪問所有端口
當啟動 Docker 服務時候，默認會新增一條轉發策略到 iptables 的 FORWARD 鏈上。策略為透過（`ACCEPT`）還是禁止（`DROP`）取決於配置`--icc=true`（缺省值）還是 `--icc=false`。當然，如果手動指定 `--iptables=false` 則不會新增 `iptables` 規則。

可見，默認情況下，不同容器之間是允許網路互通的。如果為了安全考慮，可以在 `/etc/default/docker` 文件中配置 `DOCKER_OPTS=--icc=false` 來禁止它。

#### 訪問指定端口
在透過 `-icc=false` 關閉網路訪問後，還可以透過 `--link=CONTAINER_NAME:ALIAS` 選項來訪問容器的開放端口。

例如，在啟動 Docker 服務時，可以同時使用 `icc=false --iptables=true` 參數來關閉允許相互的網路訪問，並讓 Docker 可以修改系統中的 `iptables` 規則。

此時，系統中的 `iptables` 規則可能是類似
```
$ sudo iptables -nL
...
Chain FORWARD (policy ACCEPT)
target     prot opt source               destination
DROP       all  --  0.0.0.0/0            0.0.0.0/0
...
```

之後，啟動容器（`docker run`）時使用 `--link=CONTAINER_NAME:ALIAS` 選項。Docker 會在 `iptable` 中為 兩個容器分別新增一條 `ACCEPT` 規則，允許相互訪問開放的端口（取決於 Dockerfile 中的 EXPOSE 行）。

當新增了 `--link=CONTAINER_NAME:ALIAS` 選項後，新增了 `iptables` 規則。
```
$ sudo iptables -nL
...
Chain FORWARD (policy ACCEPT)
target     prot opt source               destination
ACCEPT     tcp  --  172.17.0.2           172.17.0.3           tcp spt:80
ACCEPT     tcp  --  172.17.0.3           172.17.0.2           tcp dpt:80
DROP       all  --  0.0.0.0/0            0.0.0.0/0
```

註意：`--link=CONTAINER_NAME:ALIAS` 中的 `CONTAINER_NAME` 目前必須是 Docker 分配的名字，或使用 `--name` 參數指定的名字。主機名則不會被識別。
