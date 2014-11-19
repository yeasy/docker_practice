##刪除容器
可以使用 `docker rm` 來刪除一個處於終止狀態的容器。
例如
```
$sudo docker rm  trusting_newton
trusting_newton
```
如果要刪除一個運行中的容器，可以添加 `-f` 參數。Docker 會發送 `SIGKILL` 信號給容器。

