##存出和载入镜像

###存出镜像
如果要导出镜像到本地文件，可以使用`docker save`命令。
```
$sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu              latest              826544226fdc        2 weeks ago         194.2 MB
ouruser/sinatra     v2                  51619aaca804        2 weeks ago         373.3 MB
ubuntu              14.04               c4ff7513909d        5 weeks ago         225.4 MB
$sudo docker export ubuntu:14.04 > ubuntu_14.04.tar
```


###载入镜像
可以使用`docker load`从导出的本地文件中再导入到本地镜像库，例如
```
$sudo docker load --input ubuntu_14.04.tar
```
或
```
$sudo docker load < ubuntu_14.04.tar
```
这将导入镜像以及其相关的元数据信息（包括标签等）。
