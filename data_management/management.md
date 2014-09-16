##利用数据卷容器来备份、恢复、迁移数据卷
可以利用数据卷对其中的数据进行进行备份、恢复和迁移。

###备份
首先使用`--volume--from`标记来创建一个加载dbdata容器卷的容器，并从本地主机挂载当前到容器的/backup目录。命令如下：
```
$ sudo docker run --volumes-from dbdata -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata
```
容器启动后，使用了`tar`命令来将dbdata卷备份为本地的`/backup/backup.tar`。


###恢复
如果要恢复数据到一个容器，首先创建一个带有数据卷的容器dbdata2。
```
$ sudo docker run -v /dbdata --name dbdata2 ubuntu /bin/bash
```
然后创建另一个容器，挂载dbdata2的容器，并使用`untar`解压备份文件到挂载的容器卷中。
```
$ sudo docker run --volumes-from dbdata2 -v $(pwd):/backup busybox tar xvf
/backup/backup.tar
```
