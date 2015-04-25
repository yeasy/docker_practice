## 移除本地镜像
如果要移除本地的镜像，可以使用 `docker rmi` 命令。注意 `docker rm` 命令是移除容器。
```
$ sudo docker rmi training/sinatra
Untagged: training/sinatra:latest
Deleted: 5bc342fa0b91cabf65246837015197eecfa24b2213ed6a51a8974ae250fedd8d
Deleted: ed0fffdcdae5eb2c3a55549857a8be7fc8bc4241fb19ad714364cbfd7a56b22f
Deleted: 5c58979d73ae448df5af1d8142436d81116187a7633082650549c52c3a2418f0
```

*注意：在删除镜像之前要先用 `docker rm` 删掉依赖于这个镜像的所有容器。而在出现有容器使用正在删除的镜像时，需要先移除该容器，而使用这个 bash 小程序，可以移除所有已经退出或正在运行的容器：`sudo docker ps -a | grep Exit | awk '{print $1}' | sudo xargs docker rm`（[通过这篇文章](https://github.com/gnu4cn/docker_practice/blob/master/image/rmi.md)）, 之后就可以使用命令 `sudo docker rmi IMAGE ID [IMAGE ID, IMAGE ID, IMAGE ID, ...]` 方式删除这些镜像了。
