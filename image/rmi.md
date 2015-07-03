## 移除本地镜像
如果要移除本地的镜像，可以使用 `docker rmi` 命令。注意 `docker rm` 命令是移除容器。
```
$ sudo docker rmi training/sinatra
Untagged: training/sinatra:latest
Deleted: 5bc342fa0b91cabf65246837015197eecfa24b2213ed6a51a8974ae250fedd8d
Deleted: ed0fffdcdae5eb2c3a55549857a8be7fc8bc4241fb19ad714364cbfd7a56b22f
Deleted: 5c58979d73ae448df5af1d8142436d81116187a7633082650549c52c3a2418f0
```

*注意：在删除镜像之前要先用 `docker rm` 删掉依赖于这个镜像的所有容器。

##清理所有未打过标签的本地镜像

`docker images` 可以列出本地所有的镜像，其中很可能会包含有很多中间状态的未打过标签的镜像，大量占据着磁盘空间。

使用下面的命令可以清理所有未打过标签的本地镜像

```
$ sudo docker rmi $(docker images -q -f "dangling=true")
```

其中 `-q` 和 `-f` 是缩写, 完整的命令其实可以写着下面这样，是不是更容易理解一点？

```
$ sudo docker rmi $(docker images --quiet --filter "dangling=true")
```