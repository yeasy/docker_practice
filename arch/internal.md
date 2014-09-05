docker有三个内部组件
* docker images
* docker registries
* docker containers

### Docker images
docker images 就是一个只读的模板。比如：一个image可以包含一个ubuntu的操作系统，里面安装了apache或者你需要的应用程序。images可以用来创建docker containers，docker提供了一个很简单的机制来创建images或者更新现有的images，你甚至可以直接从其他人那里下载一个已经做好的images

###Docker registries
Docker registries 也叫docker 仓库，它有公有仓库和私有仓库2种形式，他们都可以用来让你上传和下载images。公有的仓库也叫 Docker Hub。它提供了一个巨大的image库可以让你下载，你也可以在自己的局域网内建一个自己的私有仓库。

###Docker containers
Docker containers也叫docker容器，容器是从image镜像创建的。它可以被启动、开始、停止、删除。每个容器都是相互隔离的、安全的平台。