## 列出本地镜像
使用`docker images`显示本地已有的镜像。
```
$ sudo docker images
REPOSITORY       TAG      IMAGE ID      CREATED      VIRTUAL SIZE
ubuntu           12.04    74fe38d11401  4 weeks ago  209.6 MB
ubuntu           precise  74fe38d11401  4 weeks ago  209.6 MB
ubuntu           14.04    99ec81b80c55  4 weeks ago  266 MB
ubuntu           latest   99ec81b80c55  4 weeks ago  266 MB
ubuntu           trusty   99ec81b80c55  4 weeks ago  266 MB
...
```

在列出信息中，可以看到几个字段信息

* 来自于哪个仓库，比如ubuntu
* 镜像的标记，比如 14.04
* 它的`ID`号（唯一）
* 创建时间
* 镜像大小

其中镜像的`ID`唯一标识了镜像，注意到`ubuntu:14.04`和`ubuntu:trusty`具有相同的镜像`ID`，说明它们实际上是同一镜像。

`TAG`信息用来标记来自同一个仓库的不同镜像。例如`ubuntu`仓库中有多个镜像，通过`TAG`信息来区分发行版本，例如10.04、12.04、12.10、13.04、14.04等。例如下面的命令指定使用镜像`ubuntu:14.04`来启动一个容器。
```
$ sudo docker run -t -i ubuntu:14.04 /bin/bash
```

如果不指定具体的标记，则默认使用`latest`标记信息。
