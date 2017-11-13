## 数据卷容器
如果你有一些持续更新的数据需要在容器之间共享，最好创建数据卷容器。

数据卷容器，其实就是一个正常的容器，专门用来提供数据卷供其它容器挂载的。

首先，创建一个名为 dbdata 的数据卷容器：
```bash
$ docker run -d -v /dbdata --name dbdata training/postgres echo Data-only container for postgres
```
然后，在其他容器中使用 `--volumes-from` 来挂载 dbdata 容器中的数据卷。
```bash
$ docker run -d --volumes-from dbdata --name db1 training/postgres
$ docker run -d --volumes-from dbdata --name db2 training/postgres
```
可以使用超过一个的 `--volumes-from` 参数来指定从多个容器挂载不同的数据卷。
也可以从其他已经挂载了数据卷的容器来级联挂载数据卷。
```bash
$ docker run -d --name db3 --volumes-from db1 training/postgres
```
*注意：使用 `--volumes-from` 参数所挂载数据卷的容器自己并不需要保持在运行状态。

如果删除了挂载的容器（包括 dbdata、db1 和 db2），数据卷并不会被自动删除。如果要删除一个数据卷，必须在删除最后一个还挂载着它的容器时使用 `docker rm -v` 命令来指定同时删除关联的容器。
这可以让用户在容器之间升级和移动数据卷。具体的操作将在下一节中进行讲解。
