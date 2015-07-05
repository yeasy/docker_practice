## 利用数据卷容器来备份、恢复、迁移数据卷
可以利用数据卷对其中的数据进行进行备份、恢复和迁移。

### 备份
首先使用 `--volumes-from` 标记来创建一个加载 dbdata 容器卷的容器，并从主机挂载当前目录到容器的 /backup 目录。命令如下：
```
$ sudo docker run --volumes-from dbdata -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata
```
容器启动后，使用了 `tar` 命令来将 dbdata 卷备份为容器中 /backup/backup.tar 文件，也就是主机当前目录下的名为 `backup.tar` 的文件。


### 恢复
如果要恢复数据到一个容器，首先创建一个带有空数据卷的容器 dbdata2。
```
$ sudo docker run -v /dbdata --name dbdata2 ubuntu /bin/bash
```
然后创建另一个容器，挂载 dbdata2 容器卷中的数据卷，并使用 `untar` 解压备份文件到挂载的容器卷中。
```
$ sudo docker run --volumes-from dbdata2 -v $(pwd):/backup busybox tar xvf
/backup/backup.tar
```
为了查看/验证恢复的数据，可以再启动一个容器挂载同样的容器卷来查看
```
$ sudo docker run --volumes-from dbdata2 busybox /bin/ls /dbdata
```