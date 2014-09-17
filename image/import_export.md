##导出和导入镜像

###导出镜像
如果要导出本地的镜像到文件，可以使用`docker export`命令。
```
$sudo docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                    PORTS               NAMES
7691a814370e        ubuntu:14.04        "/bin/bash"         36 hours ago        Exited (0) 21 hours ago                       test
$sudo docker export 7691a814370e > ubuntu.tar

```

*注意：也可以使用`docker save`命令导出一个镜像，它会记录从基础镜像到目前状态的所有历史记录，文件体积较大。

###导入镜像
可以使用`docker import`从导出的本地文件中再导入镜像，例如
```
$cat ubuntu.tar | sudo docker import - test_repo/localubuntu:v1.0
```

此外，也可以通过指定URL或者某个目录来导入，例如
```
$sudo docker import http://example.com/exampleimage.tgz example/imagerepo
```

