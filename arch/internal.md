docker有三个内部组件
* docker images
* docker registries
* docker containers

### Docker images
docker images 就是一个只读的模板。比如：一个image可以包含一个完整的ubuntu的操作系统，里面仅安装了apache或者你需要的其它应用程序。
images可以用来创建docker containers，docker提供了一个很简单的机制来创建images或者更新现有的images，你甚至可以直接从其他人那里下载一个已经做好的images来直接使用。

###Docker registries
Docker registries 也叫docker仓库，它有公有仓库和私有仓库2种形式，他们都可以用来让你上传和下载images。公有的仓库，即[Docker Hub](https://hub.docker.com)，提供了一个数量庞大的image库供用户下载。当然，你也可以在自己的局域网内建一个自己的私有仓库。

*从这个意义上看，Docker Hub的功能跟GitHub类似。

###Docker containers
即docker容器，容器是从image镜像创建的运行实例。它可以被启动、开始、停止、删除。每个容器都是相互隔离的、保证安全的平台。
*image是只读的，container在启动的时候创建可写的一层作为最上层。
