##docker中的容器互联-linking系统
docker有一个linking 系统可以连接多个容器。它会创建一对父子关系，父容器可以看到所选择的子容器的信息。
###容器的命名系统
linking系统依据容器的名称来执行。当我们创建容器的时候，系统会随机分配一个名字。当然我们也可以自己来命名容器，这样做有2个好处：
* 当我们自己指定名称的时候，比较好记，比如一个web应用我们可以给它起名叫web
* 当我们要连接其他容器时候，可以作为一个有用的参考点，比如连接web容器到db容器
使用--name标记可以为容器命名
```
$ sudo docker run -d -P --name web training/webapp python app.py
```
使用docker -ps 来验证我们设定的命名
```
$ sudo docker ps -l
CONTAINER ID  IMAGE                  COMMAND        CREATED       STATUS       PORTS                    NAMES
aed84ee21bde  training/webapp:latest python app.py  12 hours ago  Up 2 seconds 0.0.0.0:49154->5000/tcp  web
```
也可以使用docker inspect来查看容器的名字
```
$ sudo docker inspect -f "{{ .Name }}" aed84ee21bde
/web
```
注意：容器的名称是唯一的。如果你命名了一个叫web的容器，当你要再次使用web这个名称的时候，你需要用docker 
rm来删除之前创建的容器，也可以再执行docker run的时候 加—rm标记来停止旧的容器，并删除，rm 和-d 参数是不兼容的。

###容器互联
links可以让容器之间安全的交互，使用--link标记。下面先创建一个新的数据库容器，
```
$ sudo docker run -d --name db training/postgres
```
删除之前创建的web容器
```
$ docker rm -f web
```
创建一个新的web容器，并将它link到db容器
```
$ sudo docker run -d -P --name web --link db:db training/webapp python app.py
```
--link标记的格式：--link name:alias，name是我们要链接的容器的名称，alias是这个链接的别名。

使用docker ps来查看容器的链接
```
$ docker ps
CONTAINER ID  IMAGE                     COMMAND               CREATED             STATUS             PORTS                    NAMES
349169744e49  training/postgres:latest  su postgres -c '/usr  About a minute ago  Up About a minute  5432/tcp                 db, web/db
aed84ee21bde  training/webapp:latest    python app.py         16 hours ago        Up 2 minutes       0.0.0.0:49154->5000/tcp  web
我们可以看到我们命名的容器，db和web，db容器的names列有db也有web/db。这表示web容器链接到db容器，他们是一个父子关系。在这个link中，2个容器中有一对父子关系。docker在2个容器之间创建了一个安全的连接，而且不用映射他们的端口到宿主主机上。在启动db容器的时候也不用-p和-P标记。使用link之后我们就可以不用暴露数据库端口到网络上。
docker 通过2种方式为父子关系的容器公开连接信息：
* 环境变量
* 更新/etc/hosts文件

使用env命令来查看容器的环境变量
```$ sudo docker run --rm --name web2 --link db:db training/webapp env
    . . .
    DB_NAME=/web2/db
    DB_PORT=tcp://172.17.0.5:5432
    DB_PORT_5000_TCP=tcp://172.17.0.5:5432
    DB_PORT_5000_TCP_PROTO=tcp
    DB_PORT_5000_TCP_PORT=5432
    DB_PORT_5000_TCP_ADDR=172.17.0.5
    . . .
```
除了环境变量，docker还添加host信息到父容器的/etc/hosts的文件。下面是父容器web的hosts文件
```
$ sudo docker run -t -i --rm --link db:db training/webapp /bin/bash
root@aed84ee21bde:/opt/webapp# cat /etc/hosts
172.17.0.7  aed84ee21bde
. . .
172.17.0.5  db
```
这里有2个hosts，第一个是web容器，web容器用id作为他的主机名，第二个是db容器的ip和主机名
```
root@aed84ee21bde:/opt/webapp# apt-get install -yqq inetutils-ping
root@aed84ee21bde:/opt/webapp# ping db
PING db (172.17.0.5): 48 data bytes
56 bytes from 172.17.0.5: icmp_seq=0 ttl=64 time=0.267 ms
56 bytes from 172.17.0.5: icmp_seq=1 ttl=64 time=0.250 ms
56 bytes from 172.17.0.5: icmp_seq=2 ttl=64 time=0.256 ms
用ping来ping db容器，它会解析成172.17.0.5 
```
注意：官方的ubuntu镜像默认没有安装ping
注意：你可以链接多个子容器到父容器，比如我们可以链接多个web到db容器上。