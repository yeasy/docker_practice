##下载images
现在将尝试下载training/sinatra镜像，可以使用docker pull命令。
```
$ sudo docker pull training/sinatra
```

然后就可以使用这个image来启动容器了
```
$ sudo docker run -t -i training/sinatra /bin/bash
root@a8cb6ce02d85:/#
```
