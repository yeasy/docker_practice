##查找images

docker hub是一个公共仓库，供用户上传和下载制作好的不同用途的镜像，我们可以在docker hub的网站上来查找满足自己需求的镜像。

使用docker search命令。比如，当开发团队需要ruby和sinatra作为web应用程序的开发时，可以使用docker search 来搜索合适的镜像，使用关键字sinatra

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


可以看到返回了很多包含sinatra的镜像。其中包括镜像名字、描述、星级（表示该image的受欢迎程度）、是否官方创建、是否自动创建。
官方的镜像是由stackbrew项目组创建和维护的，autimated 资源允许用户验证image的来源和内容。

现在可以下载使用training/sinatra镜像。

到目前为止，我们看到了2种镜像资源。
一种是类似ubuntu这样的基础镜像，被称为基础或根镜像。这些基础镜像是由docker公司创建、验证、支持、提供。这样的镜像往往使用单个单词作为名字。
还有一种类型，比如training/sinatra镜像。它是由docker的用户创建并维护的，你可以通过指定image名字的前缀来指定使用某个用户的镜像，比如training。
