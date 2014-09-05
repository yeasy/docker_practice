##端口映射
当我们使用-P 标记时，docker 会随机映射一个49000 到49900的端口到内部容器的端口。
使用docker ps 可以看到 这次是49155映射到了5000
```
$ sudo docker run -d -P training/webapp python app.py
$ sudo docker ps nostalgic_morse
CONTAINER ID  IMAGE                   COMMAND       CREATED        STATUS        PORTS                    NAMES
bc533791f3f5  training/webapp:latest  python app.py 5 seconds ago  Up 2 seconds  0.0.0.0:49155->5000/tcp  nostalgic_morse
```
-p（小写的P）可以指定我们要映射的端口，但是，在一个指定端口上只可以绑定一个容器。
```
$ sudo docker run -d -p 5000:5000 training/webapp python app.py
```
-p默认会绑定本地所有接口地址，所以我们一般指定一个地址，比如localhost
```
$ sudo docker run -d -p 127.0.0.1:5000:5000 training/webapp python app.py
```
或者绑定localhost的任意端口到容器的5000端口
```
$ sudo docker run -d -p 127.0.0.1::5000 training/webapp python app.py
```
还可以使用upd标记来指定udp端口
```
$ sudo docker run -d -p 127.0.0.1:5000:5000/udp training/webapp python app.py
```
使用dicker port 来查看当前绑定的端口配置，也可以查看到绑定的地址
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