##获取镜像
可以使用docker pull命令来预先下载所需要的镜像。

下面的例子下载一个centos镜像。
```
$ sudo docker pull centos
Pulling repository centos
b7de3133ff98: Pulling dependent layers
5cc9e91966f7: Pulling fs layer
511136ea3c5a: Download complete
ef52fb1fe610: Download complete
```
下载过程中，会输出获取镜像的每一层信息。

下载完成后，即可随时创建一个容器了。
```
$ sudo docker run -t -i centos /bin/bash
bash-4.1#
```
