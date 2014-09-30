##容器互联
容器的连接（linking）系统是除了端口映射外，另一种跟容器中应用交互的方式。

该系统会在源和接收容器之间创建一个隧道，接收容器可以看到源容器指定的信息。

###自定义容器命名
连接系统依据容器的名称来执行。因此，首先需要自定义一个好记的容器命名。

虽然当创建容器的时候，系统默认会分配一个名字。自定义命名容器有2个好处：
* 自定义的命名，比较好记，比如一个web应用容器我们可以给它起名叫web
* 当要连接其他容器时候，可以作为一个有用的参考点，比如连接web容器到db容器


使用`--name`标记可以为容器自定义命名。
```
$ sudo docker run -d -P --name web training/webapp python app.py
```

使用`docker ps`来验证设定的命名。
```
$ sudo docker ps -l
CONTAINER ID  IMAGE                  COMMAND        CREATED       STATUS       PORTS                    NAMES
aed84ee21bde  training/webapp:latest python app.py  12 hours ago  Up 2 seconds 0.0.0.0:49154->5000/tcp  web
```
也可以使用`docker inspect`来查看容器的名字
```
$ sudo docker inspect -f "{{ .Name }}" aed84ee21bde
/web
```
注意：容器的名称是唯一的。如果已经命名了一个叫web的容器，当你要再次使用web这个名称的时候，需要先用`docker rm`来删除之前创建的同名容器。

在执行`docker run`的时候如果添加`--rm`标记，则容器在终止后会立刻删除。注意，`--rm`和`-d`参数不能同时使用。

###容器互联
使用`--link`参数可以让容器之间安全的进行交互。

下面先创建一个新的数据库容器。
```
$ sudo docker run -d --name db training/postgres
```
删除之前创建的web容器
```
$ docker rm -f web
```
然后创建一个新的web容器，并将它连接到db容器
```
$ sudo docker run -d -P --name web --link db:db training/webapp python app.py
```
此时，db容器和web容器建立互联关系。

`--link`参数的格式为`--link name:alias`，其中`name`是要链接的容器的名称，`alias`是这个连接的别名。

使用`docker ps`来查看容器的连接
```
$ docker ps
CONTAINER ID  IMAGE                     COMMAND               CREATED             STATUS             PORTS                    NAMES
349169744e49  training/postgres:latest  su postgres -c '/usr  About a minute ago  Up About a minute  5432/tcp                 db, web/db
aed84ee21bde  training/webapp:latest    python app.py         16 hours ago        Up 2 minutes       0.0.0.0:49154->5000/tcp  web
```
可以看到自定义命名的容器，db和web，db容器的names列有db也有web/db。这表示web容器链接到db容器，web容器将被允许访问db容器的信息。

Docker在两个互联的容器之间创建了一个安全隧道，而且不用映射它们的端口到宿主主机上。在启动db容器的时候并没有使用-p和-P标记，从而避免了暴露数据库端口到外部网络上。

Docker 通过2种方式为容器公开连接信息：
* 环境变量
* 更新`/etc/hosts`文件

使用`env`命令来查看web容器的环境变量
```
$ sudo docker run --rm --name web2 --link db:db training/webapp env
. . .
DB_NAME=/web2/db
DB_PORT=tcp://172.17.0.5:5432
DB_PORT_5000_TCP=tcp://172.17.0.5:5432
DB_PORT_5000_TCP_PROTO=tcp
DB_PORT_5000_TCP_PORT=5432
DB_PORT_5000_TCP_ADDR=172.17.0.5
. . .
```
其中DB_开头的环境变量是供web容器连接db容器使用，前缀采用大写的连接别名。

除了环境变量，docker还添加host信息到父容器的`/etc/hosts`的文件。下面是父容器web的hosts文件
```
$ sudo docker run -t -i --rm --link db:db training/webapp /bin/bash
root@aed84ee21bde:/opt/webapp# cat /etc/hosts
172.17.0.7  aed84ee21bde
. . .
172.17.0.5  db
```
这里有2个hosts，第一个是web容器，web容器用id作为他的主机名，第二个是db容器的ip和主机名。
可以在web容器中安装ping命令来测试跟db容器的连通。
```
root@aed84ee21bde:/opt/webapp# apt-get install -yqq inetutils-ping
root@aed84ee21bde:/opt/webapp# ping db
PING db (172.17.0.5): 48 data bytes
56 bytes from 172.17.0.5: icmp_seq=0 ttl=64 time=0.267 ms
56 bytes from 172.17.0.5: icmp_seq=1 ttl=64 time=0.250 ms
56 bytes from 172.17.0.5: icmp_seq=2 ttl=64 time=0.256 ms
```
用ping来ping db容器，它会解析成172.17.0.5。

注意：官方的ubuntu镜像默认没有安装ping
注意：用户可以链接多个子容器到父容器，比如可以链接多个web到db容器上。
