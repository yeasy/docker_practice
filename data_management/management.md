##利用Data Volume Container 来备份、恢复、移动数据卷
数据卷另外一个功能是使用他们来备份、恢复、移动数据。使用--volume标记来创建一个加载了卷的新的容器，命令如下：
```
$ sudo docker run --volumes-from dbdata -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata
```
这里我们创建了一个容器，先从dbdata容器来挂载数据卷。然后从本地主机挂载当前到容器的/backup目录。最后，使用tar命令来将dbdata
卷备份为back.tar。当命令执行完、容器停止之后，我们就备份了dbdata数据卷。


你可以使用这个备份来恢复这个容器。
```
$ sudo docker run -v /dbdata --name dbdata2 ubuntu /bin/bash
```
然后使用untar解压这个备份文件到新容器卷中。
```
$ sudo docker run --volumes-from dbdata2 -v $(pwd):/backup busybox tar xvf 
/backup/backup.tar
```
你可以用上述技术实现数据卷的备份、移动、恢复。