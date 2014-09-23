## 使用Docker Hub管理镜像
[Docker Hub](https://hub.docker.com/)是一个公共仓库，供用户上传和下载制作好的不同用途的镜像，用户可以在Docker Hub的网站上来查找满足自己需求的镜像。

###查找镜像

使用`docker search`命令。比如，当开发团队需要ruby和sinatra作为web应用程序的开发时，可以使用关键字sinatra进行搜索。

```
$ sudo docker search sinatra
NAME                                   DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
training/sinatra                       Sinatra training image                          0                    [OK]
marceldegraaf/sinatra                  Sinatra test app                                0
mattwarren/docker-sinatra-demo                                                         0                    [OK]
luisbebop/docker-sinatra-hello-world                                                   0                    [OK]
bmorearty/handson-sinatra              handson-ruby + Sinatra for Hands on with D...   0
subwiz/sinatra                                                                         0
bmorearty/sinatra                                                                      0
```

可以看到返回了很多包含sinatra的镜像。其中包括镜像名字、描述、星级（表示该镜像的受欢迎程度）、是否官方创建、是否自动创建。
官方的镜像是由stackbrew项目组创建和维护的，automated 资源允许用户验证镜像的来源和内容。

现在可以下载使用training/sinatra镜像。

到目前为止，我们看到了2种镜像资源。
一种是类似ubuntu这样的基础镜像，被称为基础或根镜像。这些基础镜像是由Docker公司创建、验证、支持、提供。这样的镜像往往使用单个单词作为名字。
还有一种类型，比如training/sinatra镜像。它是由Docker的用户创建并维护的，你可以通过指定镜像名字的前缀来指定使用某个用户的镜像，比如training。

###获取镜像
可以使用`docker pull`命令来预先下载所需要的镜像。

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
*注：有时候官方镜像下载较慢，可以试试`203.195.193.251:5000`镜像，如
```
$ sudo docker pull 203.195.193.251:5000/centos
```

完成后，即可随时创建一个容器了。
```
$ sudo docker run -t -i centos /bin/bash
bash-4.1#
```

###上传镜像
用户也可以通过`docker push`命令，把自己创建的镜像上传到Docker Hub中来共享。
```
$ sudo docker push ouruser/sinatra
The push refers to a repository [ouruser/sinatra] (len: 1)
Sending image list
Pushing repository ouruser/sinatra (3 tags)
```

