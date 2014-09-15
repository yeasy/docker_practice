##端口映射
当我们使用-P 标记时，docker 会随机映射一个49000 到49900的端口到内部容器开放的端口。
使用`docker ps`可以看到，本地主机的49155映射到了容器的5000端口。
```
$ sudo docker run -d -P training/webapp python app.py
$ sudo docker ps -l
CONTAINER ID  IMAGE                   COMMAND       CREATED        STATUS        PORTS                    NAMES
bc533791f3f5  training/webapp:latest  python app.py 5 seconds ago  Up 2 seconds  0.0.0.0:49155->5000/tcp  nostalgic_morse
```
其中，-d是告诉docker在后台启动容器。-P会让docker将容器内必需的网络端口映射到本地主机。


-p（小写的P）则可以指定要映射的端口，并且，在一个指定端口上只可以绑定一个容器。支持的格式有`ip:hostPort:containerPort | ip::containerPort | hostPort:containerPort`。

###映射所有接口地址
使用`hostPort:containerPort`格式本地的5000端口映射到容器的5000端口，可以执行
```
$ sudo docker run -d -p 5000:5000 training/webapp python app.py
```
此时默认会绑定本地所有接口上的所有地址。

###映射到指定地址的指定端口
可以使用`ip:hostPort:containerPort`格式指定映射使用一个特定地址，比如localhost地址127.0.0.1
```
$ sudo docker run -d -p 127.0.0.1:5000:5000 training/webapp python app.py
```
###映射到指定地址的任意端口
使用`ip::containerPort`绑定localhost的任意端口到容器的5000端口，本地主机会自动分配一个端口。
```
$ sudo docker run -d -p 127.0.0.1::5000 training/webapp python app.py
```
还可以使用udp标记来指定udp端口
```
$ sudo docker run -d -p 127.0.0.1:5000:5000/udp training/webapp python app.py
```
###查看映射端口配置
使用`docker port` 来查看当前映射的端口配置，也可以查看到绑定的地址
```
$ docker port nostalgic_morse 5000
127.0.0.1:49155.
```
注意：
* 容器有自己的内部网络和ip地址（使用 docker inspect 可以获取所有的变量，docker还可以有一个可变的网络配置。）
* -p标记可以多次使用来绑定多个端口
比如：
```
$ sudo docker run -d -p 5000:5000  -p 3000:80 training/webapp python app.py
```
