## 移除本地鏡像
如果要移除本地的鏡像，可以使用 `docker rmi` 命令。註意 `docker rm` 命令是移除容器。
```
$ sudo docker rmi training/sinatra
Untagged: training/sinatra:latest
Deleted: 5bc342fa0b91cabf65246837015197eecfa24b2213ed6a51a8974ae250fedd8d
Deleted: ed0fffdcdae5eb2c3a55549857a8be7fc8bc4241fb19ad714364cbfd7a56b22f
Deleted: 5c58979d73ae448df5af1d8142436d81116187a7633082650549c52c3a2418f0
```

*註意：在刪除鏡像之前要先用 `docker rm` 刪掉依賴於這個鏡像的所有容器。
