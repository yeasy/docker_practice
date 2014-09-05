##数据卷容器
如果你有一些持续更新的数据需要在容器之间共享，最好创建Data Volume Container，然后加载它。现在就来创建一个命名的数据卷容器：
```
$ sudo docker run -d -v /dbdata --name dbdata training/postgres echo Data-only container for postgres
```
然后，你可以在其他容器中使用--volumes-from 来挂载/dbdata卷
```
$ sudo docker run -d --volumes-from dbdata --name db1 training/postgres
$ sudo docker run -d --volumes-from dbdata --name db2 training/postgres
```
还可以使用多个--volumes-from 参数来从多个容器挂载多个数据卷
也可以从其他已经挂载了容器卷的容器来挂载数据卷
```
$ sudo docker run -d --name db3 --volumes-from db1 training/postgres
```
如果你移除了挂载的容器，包括初始容器，或者后来的db1 db2，这些卷在有容器使用它的时候不会被删除。这可以让我们在容器之间升级和移动数据。