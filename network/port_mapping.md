## 外部訪問容器
容器中可以執行一些網路應用，要讓外部也可以訪問這些應用，可以通過 `-P` 或 `-p` 參數來指定端口映射。

當使用 -P 標記時，Docker 會隨機映射一個 `49000~49900` 的端口到內部容器開放的網路端口。

使用 `docker ps` 可以看到，本地主機的 49155 被映射到了容器的 5000 端口。此時訪問本機的 49115 端口即可訪問容器內 web 應用提供的界面。
```
$ sudo docker run -d -P training/webapp python app.py
$ sudo docker ps -l
CONTAINER ID  IMAGE                   COMMAND       CREATED        STATUS        PORTS                    NAMES
bc533791f3f5  training/webapp:latest  python app.py 5 seconds ago  Up 2 seconds  0.0.0.0:49155->5000/tcp  nostalgic_morse
```
同樣的，可以通過 `docker logs` 命令來查看應用的信息。
```
$ sudo docker logs -f nostalgic_morse
* Running on http://0.0.0.0:5000/
10.0.2.2 - - [23/May/2014 20:16:31] "GET / HTTP/1.1" 200 -
10.0.2.2 - - [23/May/2014 20:16:31] "GET /favicon.ico HTTP/1.1" 404 -
```

-p（小寫的）則可以指定要映射的端口，並且，在一個指定端口上只可以綁定一個容器。支持的格式有 `ip:hostPort:containerPort | ip::containerPort | hostPort:containerPort`。

### 映射所有接口地址
使用 `hostPort:containerPort` 格式本地的 5000 端口映射到容器的 5000 端口，可以執行
```
$ sudo docker run -d -p 5000:5000 training/webapp python app.py
```
此時默認會綁定本地所有接口上的所有地址。

### 映射到指定地址的指定端口
可以使用 `ip:hostPort:containerPort` 格式指定映射使用一個特定地址，比如 localhost 地址 127.0.0.1
```
$ sudo docker run -d -p 127.0.0.1:5000:5000 training/webapp python app.py
```
### 映射到指定地址的任意端口
使用 `ip::containerPort` 綁定 localhost 的任意端口到容器的 5000 端口，本地主機會自動分配一個端口。
```
$ sudo docker run -d -p 127.0.0.1::5000 training/webapp python app.py
```
還可以使用 udp 標記來指定 udp 端口
```
$ sudo docker run -d -p 127.0.0.1:5000:5000/udp training/webapp python app.py
```
### 查看映射端口配置
使用 `docker port` 來查看當前映射的端口配置，也可以查看到綁定的地址
```
$ docker port nostalgic_morse 5000
127.0.0.1:49155.
```
註意：
* 容器有自己的內部網路和 ip 地址（使用 `docker inspect` 可以獲取所有的變量，Docker 還可以有一個可變的網路配置。）
* -p 標記可以多次使用來綁定多個端口

例如
```
$ sudo docker run -d -p 5000:5000  -p 3000:80 training/webapp python app.py
```
