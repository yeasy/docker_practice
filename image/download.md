##下载images
现在我们指定了一个image，training/sinatra，我们可以使用docker pull命令来下载它
```
$ sudo docker pull training/sinatra
然后我们就可以使用这个image来启动容器了
$ sudo docker run -t -i training/sinatra /bin/bash
root@a8cb6ce02d85:/#
```