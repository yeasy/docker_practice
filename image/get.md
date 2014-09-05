##获取images

我们如何获取新的images呢？当我们启动容器使用的image不再本地主机上时，docker会自动下载他们。这很耗时，我们可以使用docker pull命令来预先下载我们需要的image。下面的例子下载一个centos镜像。
```
$ sudo docker pull centos
Pulling repository centos
b7de3133ff98: Pulling dependent layers
5cc9e91966f7: Pulling fs layer
511136ea3c5a: Download complete
ef52fb1fe610: Download complete
```
我们可以看到下载的image的每一个层次，这样当我们使用这个image来启动容器的时候，它就可以马上启动了。
```
$ sudo docker run -t -i centos /bin/bash
bash-4.1#
```