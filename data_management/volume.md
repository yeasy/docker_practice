##数据卷
数据卷是一个可供一个或多个容器使用的特殊目录，它绕过UFS，可以提供很多有用的特性：
* 数据卷可以在容器之间共享和重用
* 对数据卷的修改会立马生效
* 对数据卷的更新，不会影响镜像
* 卷会一直存在，直到没有容器使用

###添加一个数据卷
在用`docker run`命令的时候，使用-v标记来添加一个数据卷。在一次run中多次使用可以挂载多个数据卷，下面加载一个卷到web容器上。
```
$ sudo docker run -d -P --name web -v /webapp training/webapp python app.py
```
创建一个新的卷到容器的/webapp
*注意：也可以在dockerfile中使用volume来添加一个或者多个新的卷到由该image创建的任意容器

###挂载一个主机目录作为数据卷
使用-v标记也可以挂载一个主机的目录到容器中去
```
$ sudo docker run -d -P --name web -v /src/webapp:/opt/webapp
training/webapp python app.py
```
上面的命令加载主机的/src/webapp到容器的/opt/webapp
目录。这个在测试的时候特别好用，比如我们可以加载我们的源码到容器中，来查看他们是否正常工作。目录的路径必须是主机上的绝对路径，如果目录不存在docker会自动为你创建它。
*注意:dockerfile 中不能用，各种操作系统的文件路径格式不一样，所以不一定适合所有的主机。

docker 加载的数据卷默认是读写权限，但我们可以把它加载为只读。
```
$ sudo docker run -d -P --name web -v /src/webapp:/opt/webapp:ro
training/webapp python app.py
```
加了ro之后，就挂载为只读了。

###挂载一个宿主主机文件作为数据卷
-v标记也可以从主机挂载单个文件到容器中
```
$ sudo docker run --rm -it -v ~/.bash_history:/.bash_history ubuntu /bin/bash
```
这样就可以记录在容器输入过的命令了。
*注意：很多工具子在使用vi或者sed --in-place的时候会导致inode的改变，从docker 1.1
.0起，它会报错，所以最简单的办法就直接mount父目录。
