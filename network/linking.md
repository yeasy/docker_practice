## 容器互聯
容器的連接（linking）系統是除了端口映射外，另一種跟容器中應用交互的方式。

該系統會在源和接收容器之間創建一個隧道，接收容器可以看到源容器指定的信息。

### 自定義容器命名
連接系統依據容器的名稱來執行。因此，首先需要自定義一個好記的容器命名。

雖然當創建容器的時候，系統默認會分配一個名字。自定義命名容器有2個好處：
* 自定義的命名，比較好記，比如一個web應用容器我們可以給它起名叫web
* 當要連接其他容器時候，可以作為一個有用的參考點，比如連接web容器到db容器

使用 `--name` 標記可以為容器自定義命名。
```
$ sudo docker run -d -P --name web training/webapp python app.py
```

使用 `docker ps` 來驗證設定的命名。
```
$ sudo docker ps -l
CONTAINER ID  IMAGE                  COMMAND        CREATED       STATUS       PORTS                    NAMES
aed84ee21bde  training/webapp:latest python app.py  12 hours ago  Up 2 seconds 0.0.0.0:49154->5000/tcp  web
```
也可以使用 `docker inspect` 來查看容器的名字
```
$ sudo docker inspect -f "{{ .Name }}" aed84ee21bde
/web
```
註意：容器的名稱是唯一的。如果已經命名了一個叫 web 的容器，當你要再次使用 web 這個名稱的時候，需要先用`docker rm` 來刪除之前創建的同名容器。

在執行 `docker run` 的時候如果添加 `--rm` 標記，則容器在終止後會立刻刪除。註意，`--rm` 和 `-d` 參數不能同時使用。

###容器互聯
使用 `--link` 參數可以讓容器之間安全的進行交互。

下面先創建一個新的數據庫容器。
```
$ sudo docker run -d --name db training/postgres
```
刪除之前創建的 web 容器
```
$ docker rm -f web
```
然後創建一個新的 web 容器，並將它連接到 db 容器
```
$ sudo docker run -d -P --name web --link db:db training/webapp python app.py
```
此時，db 容器和 web 容器建立互聯關系。

`--link` 參數的格式為 `--link name:alias`，其中 `name` 是要鏈接的容器的名稱，`alias` 是這個連接的別名。

使用 `docker ps` 來查看容器的連接
```
$ docker ps
CONTAINER ID  IMAGE                     COMMAND               CREATED             STATUS             PORTS                    NAMES
349169744e49  training/postgres:latest  su postgres -c '/usr  About a minute ago  Up About a minute  5432/tcp                 db, web/db
aed84ee21bde  training/webapp:latest    python app.py         16 hours ago        Up 2 minutes       0.0.0.0:49154->5000/tcp  web
```
可以看到自定義命名的容器，db 和 web，db 容器的 names 列有 db 也有 web/db。這表示 web 容器鏈接到 db 容器，web 容器將被允許訪問 db 容器的信息。

Docker 在兩個互聯的容器之間創建了一個安全隧道，而且不用映射它們的端口到宿主主機上。在啟動 db 容器的時候並沒有使用 `-p` 和 `-P` 標記，從而避免了暴露數據庫端口到外部網路上。

Docker 通過 2 種方式為容器公開連接信息：
* 環境變量
* 更新 `/etc/hosts` 文件

使用 `env` 命令來查看 web 容器的環境變量
```
$ sudo docker run --rm --name web2 --link db:db training/webapp env
. . .
DB_NAME=/web2/db
DB_PORT=tcp://172.17.0.5:5432
DB_PORT_5000_TCP=tcp://172.17.0.5:5432
DB_PORT_5000_TCP_PROTO=tcp
DB_PORT_5000_TCP_PORT=5432
DB_PORT_5000_TCP_ADDR=172.17.0.5
. . .
```
其中 DB_ 開頭的環境變量是供 web 容器連接 db 容器使用，前綴采用大寫的連接別名。

除了環境變量，Docker 還添加 host 信息到父容器的 `/etc/hosts` 的文件。下面是父容器 web 的 hosts 文件
```
$ sudo docker run -t -i --rm --link db:db training/webapp /bin/bash
root@aed84ee21bde:/opt/webapp# cat /etc/hosts
172.17.0.7  aed84ee21bde
. . .
172.17.0.5  db
```
這裏有 2 個 hosts，第一個是 web 容器，web 容器用 id 作為他的主機名，第二個是 db 容器的 ip 和主機名。
可以在 web 容器中安裝 ping 命令來測試跟db容器的連通。
```
root@aed84ee21bde:/opt/webapp# apt-get install -yqq inetutils-ping
root@aed84ee21bde:/opt/webapp# ping db
PING db (172.17.0.5): 48 data bytes
56 bytes from 172.17.0.5: icmp_seq=0 ttl=64 time=0.267 ms
56 bytes from 172.17.0.5: icmp_seq=1 ttl=64 time=0.250 ms
56 bytes from 172.17.0.5: icmp_seq=2 ttl=64 time=0.256 ms
```
用 ping 來測試db容器，它會解析成 `172.17.0.5`。
*註意：官方的 ubuntu 鏡像默認沒有安裝 ping，需要自行安裝。

用戶可以鏈接多個子容器到父容器，比如可以鏈接多個 web 到 db 容器上。
