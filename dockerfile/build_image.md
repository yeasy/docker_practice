## 创建镜像
编写完成Dockerfile之后，可以通过`docker build`命令来创建镜像。

基本的格式为`docker build [选项] 路径`，该命令将读取指定路径下（包括子目录）的Dockerfile，并将该路径下所有内容发送给Docker服务端，由服务端来创建镜像。因此一般建议放置Dockerfile的目录为空目录。也可以通过`.dockerignore`文件（每一行添加一条匹配模式）来让Docker忽略路径下的目录和文件。

要指定镜像的标签信息，可以通过`-t`选项，例如
```
$ sudo docker build -t myrepo/myapp /tmp/test1/
```


