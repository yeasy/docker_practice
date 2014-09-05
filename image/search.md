##查找images

docker的一个特点是很多人因为各种不同的用途创建了各种不同的images。它们都被上传到了docker hub共有仓库上，我们可以在docker hub的网站上来查找它们。使用docker search命令。比如，当我们的团队需要ruby和sinatra作为web应用程序的开发时，我们使用docker search 来搜索合适的image，使用关键字sinatra

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

我们看到返回了很多包含sinatra的images。其中包括image名字、描述、星级（表示该image的受欢迎程度）、是否官方创建、是否自动创建。官方的images是stackbrew项目组创建和维护的，autimated 资源允许你验证image的来源和内容。

现在我们已经回顾了可用的images，并决定使用training/sinatra镜像。到目前为止，我们看到了2种images 资源。比如ubuntu，被称为基础或则根镜像。这些基础镜像是docker公司创建、验证、支持、提供。他们往往使用一个单词作为他们的名字。

还有一种类型，比如我们选择的training/sinatra镜像。它是由docker的用户创建并维护的，你可以通过指定image名字的前缀来指定他们，比如training。