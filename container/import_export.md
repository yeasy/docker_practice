##導出和導入容器

###導出容器
如果要導出本地某個容器，可以使用 `docker export` 命令。
```
$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                    PORTS               NAMES
7691a814370e        ubuntu:14.04        "/bin/bash"         36 hours ago        Exited (0) 21 hours ago                       test
$ sudo docker export 7691a814370e > ubuntu.tar
```
這樣將導出容器快照到本地文件。

###導入容器快照
可以使用 `docker import` 從容器快照文件中再導入為映像檔，例如
```
$ cat ubuntu.tar | sudo docker import - test/buntu:v1.0
$ sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED              VIRTUAL SIZE
test/ubuntu         v1.0                9d37a6082e97        About a minute ago   171.3 MB
```
此外，也可以通過指定 URL 或者某個目錄來導入，例如
```
$sudo docker import http://example.com/exampleimage.tgz example/imagerepo
```

*註：用戶既可以使用 `docker load` 來導入映像檔儲存文件到本地映像檔庫，也可以使用 `docker import` 來導入一個容器快照到本地映像檔庫。這兩者的區別在於容器快照文件將丟棄所有的歷史記錄和原始數據信息（即僅保存容器當時的快照狀態），而映像檔儲存文件將保存完整記錄，檔案體積也跟著變大。此外，從容器快照文件導入時可以重新指定標簽等原始數據信息。


