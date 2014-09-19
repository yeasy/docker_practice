##导出和导入容器

###导出容器
如果要导出本地某个容器，可以使用`docker export`命令。
```
$ sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                    PORTS               NAMES
7691a814370e        ubuntu:14.04        "/bin/bash"         36 hours ago        Exited (0) 21 hours ago                       test
$ sudo docker export 7691a814370e > ubuntu.tar
```
这样将导出容器快照到本地文件。

###导入容器快照
可以使用`docker import`从容器快照文件中再导入为镜像，例如
```
$ cat ubuntu.tar | sudo docker import - test/buntu:v1.0
$ sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED              VIRTUAL SIZE
test/ubuntu         v1.0                9d37a6082e97        About a minute ago   171.3 MB
```
此外，也可以通过指定URL或者某个目录来导入，例如
```
$sudo docker import http://example.com/exampleimage.tgz example/imagerepo
```

*注：用户既可以使用`docker load`来导入镜像存储文件到本地镜像库，也可以使用`docker import`来导入一个容器快照到本地镜像库。这两者的区别在于容器快照文件将丢弃所有的历史记录和元数据信息（即仅保存容器当时的快照状态），而镜像存储文件将保存完整记录，体积也要大。此外，从容器快照文件导入时可以重新指定标签等元数据信息。


