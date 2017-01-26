## 数据卷
数据卷是一个可供一个或多个容器使用的特殊目录，它绕过 UFS，可以提供很多有用的特性：
* 数据卷可以在容器之间共享和重用
* 对数据卷的修改会立马生效
* 对数据卷的更新，不会影响镜像
* 数据卷默认会一直存在，即使容器被删除


*注意：数据卷的使用，类似于 Linux 下对目录或文件进行 mount，镜像中的被指定为挂载点的目录中的文件会隐藏掉，能显示看的是挂载的数据卷。


### 创建一个数据卷
在用 `docker run` 命令的时候，使用 `-v` 标记来创建一个数据卷并挂载到容器里。在一次 run 中多次使用可以挂载多个数据卷。

下面创建一个名为 web 的容器，并加载一个数据卷到容器的 `/webapp` 目录。
```
$ sudo docker run -d -P --name web -v /webapp training/webapp python app.py
```
*注意：也可以在 Dockerfile 中使用 `VOLUME` 来添加一个或者多个新的卷到由该镜像创建的任意容器。

### 删除数据卷
数据卷是被设计用来持久化数据的，它的生命周期独立于容器，Docker不会在容器被删除后自动删除数据卷，并且也不存在垃圾回收这样的机制来处理没有任何容器引用的数据卷。如果需要在删除容器的同时移除数据卷。可以在删除容器的时候使用 `docker rm -v` 这个命令。无主的数据卷可能会占据很多空间，要清理会很麻烦。Docker官方正在试图解决这个问题，相关工作的进度可以查看这个[PR](https://github.com/docker/docker/pull/8484)。

### 挂载一个主机目录作为数据卷
使用 `-v` 标记也可以指定挂载一个本地主机的目录到容器中去。
```
$ sudo docker run -d -P --name web -v /src/webapp:/opt/webapp training/webapp python app.py
```
上面的命令加载主机的 `/src/webapp` 目录到容器的 `/opt/webapp`
目录。这个功能在进行测试的时候十分方便，比如用户可以放置一些程序到本地目录中，来查看容器是否正常工作。本地目录的路径必须是绝对路径，如果目录不存在 Docker 会自动为你创建它。

*注意：Dockerfile 中不支持这种用法，这是因为 Dockerfile 是为了移植和分享用的。然而，不同操作系统的路径格式不一样，所以目前还不能支持。

Docker 挂载数据卷的默认权限是读写，用户也可以通过 `:ro` 指定为只读。
```
$ sudo docker run -d -P --name web -v /src/webapp:/opt/webapp:ro
training/webapp python app.py
```
加了 `:ro` 之后，就挂载为只读了。

### 查看数据卷的具体信息

在主机里使用以下命令可以查看指定容器的信息
```
$ docker inspect web
...
```

在输出的内容中找到其中和数据卷相关的部分，可以看到所有的数据卷都是创建在主机的`/var/lib/docker/volumes/`下面的
```
"Volumes": {
    "/webapp": "/var/lib/docker/volumes/fac362...80535"
},
"VolumesRW": {
    "/webapp": true
}
...
```
注：从Docker 1.8.0起，数据卷配置在"Mounts"Key下面，可以看到所有的数据卷都是创建在主机的`/mnt/sda1/var/lib/docker/volumes/....`下面了。
```
"Mounts": [
            {
                "Name": "b53ebd40054dae599faf7c9666acfe205c3e922fc3e8bc3f2fd178ed788f1c29",
                "Source": "/mnt/sda1/var/lib/docker/volumes/b53ebd40054dae599faf7c9666acfe205c3e922fc3e8bc3f2fd178ed788f1c29/_data",
                "Destination": "/webapp",
                "Driver": "local",
                "Mode": "",
                "RW": true,
                "Propagation": ""
            }
        ]
...
```

### 挂载一个本地主机文件作为数据卷
`-v` 标记也可以从主机挂载单个文件到容器中
```
$ sudo docker run --rm -it -v ~/.bash_history:/.bash_history ubuntu /bin/bash
```
这样就可以记录在容器输入过的命令了。

*注意：如果直接挂载一个文件，很多文件编辑工具，包括 `vi` 或者 `sed --in-place`，可能会造成文件 inode 的改变，从 Docker 1.1
.0起，这会导致报错误信息。所以最简单的办法就直接挂载文件的父目录。
