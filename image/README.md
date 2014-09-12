#Docker image详细介绍

在之前的介绍中，我们知道docker images是docker的三大组件之一。

docker把下载的images存储到docker主机上，如果一个image不在主机上，docker会从一个镜像仓库下载，默认的仓库是 DOCKER HUB 公共仓库。

接下来将介绍更多关于docker images的内容，包括：
* 使用和管理本地主机上的images
* 创建一个基础的images
* 上传images到docker hub（公共images仓库）


使用 docker images 显示本机上的images
```
$ sudo docker images
REPOSITORY       TAG      IMAGE ID      CREATED      VIRTUAL SIZE
training/webapp  latest   fc77f57ad303  3 weeks ago  280.5 MB
ubuntu           13.10    5e019ab7bf6d  4 weeks ago  180 MB
ubuntu           saucy    5e019ab7bf6d  4 weeks ago  180 MB
ubuntu           12.04    74fe38d11401  4 weeks ago  209.6 MB
ubuntu           precise  74fe38d11401  4 weeks ago  209.6 MB
ubuntu           12.10    a7cf8ae4e998  4 weeks ago  171.3 MB
ubuntu           quantal  a7cf8ae4e998  4 weeks ago  171.3 MB
ubuntu           14.04    99ec81b80c55  4 weeks ago  266 MB
ubuntu           latest   99ec81b80c55  4 weeks ago  266 MB
ubuntu           trusty   99ec81b80c55  4 weeks ago  266 MB
ubuntu           13.04    316b678ddf48  4 weeks ago  169.4 MB
ubuntu           raring   316b678ddf48  4 weeks ago  169.4 MB
ubuntu           10.04    3db9c44f4520  4 weeks ago  183 MB
ubuntu           lucid    3db9c44f4520  4 weeks ago  183 MB
```

在列出信息中，可以看到几个字段信息

* 来自于哪个仓库，比如ubuntu
* image的标记，比如 14.04
* 它的ID号（唯一）
* 什么时候被创建的
* 镜像大小

仓库中可能有同一个images的多个发行版，比如ubuntu镜像，就有10.04、12.04、12.10、13.04、14.04等发行版,每个发行版的标记都不同，可以使用tag信息来指定images
使用一个images的标记来启动容器
```
$ sudo docker run -t -i ubuntu:14.04 /bin/bash
$ sudo docker run -t -i ubuntu:12.04 /bin/bash
```
上面的命令会从指定image启动一个容器，并提供用户控制台来交互。用户登录进入后可以看到系统内运行了一个bash进程。

如果你不指定具体的发行版，比如仅使用ubuntu，那么docker会使用最新的发行版ubuntu:latest。
