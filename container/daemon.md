##守護態執行

更多的時候，需要讓 Docker 容器在後臺以守護態（Daemonized）形式執行。此時，可以透過新增 `-d` 參數來實作。

例以下面的命令會在後臺執行容器。
```
$ sudo docker run -d ubuntu:14.04 /bin/sh -c "while true; do echo hello world; sleep 1; done"
1e5535038e285177d5214659a068137486f96ee5c2e85a4ac52dc83f2ebe4147
```

容器啟動後會返回一個唯一的 id，也可以透過 `docker ps` 命令來查看容器訊息。
```
$ sudo docker ps
CONTAINER ID  IMAGE         COMMAND               CREATED        STATUS       PORTS NAMES
1e5535038e28  ubuntu:14.04  /bin/sh -c 'while tr  2 minutes ago  Up 1 minute        insane_babbage
```
要取得容器的輸出訊息，可以透過 `docker logs` 命令。
```
$ sudo docker logs insane_babbage
hello world
hello world
hello world
. . .
```
