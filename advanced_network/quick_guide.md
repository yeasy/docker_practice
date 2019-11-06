# 快速配置指南

下面是一个跟 Docker 网络相关的命令列表。

其中有些命令选项只有在 Docker 服务启动的时候才能配置，而且不能马上生效。

* `-b BRIDGE` 或 `--bridge=BRIDGE` 指定容器挂载的网桥
* `--bip=CIDR` 定制 docker0 的掩码
* `-H SOCKET...` 或 `--host=SOCKET...` Docker 服务端接收命令的通道
* `--icc=true|false` 是否支持容器之间进行通信
* `--ip-forward=true|false` 请看下文容器之间的通信
* `--iptables=true|false` 是否允许 Docker 添加 iptables 规则
* `--mtu=BYTES` 容器网络中的 MTU

下面2个命令选项既可以在启动服务时指定，也可以在启动容器时指定。在 Docker 服务启动的时候指定则会成为默认值，后面执行 `docker run` 时可以覆盖设置的默认值。

* `--dns=IP_ADDRESS...` 使用指定的DNS服务器
* `--dns-search=DOMAIN...` 指定DNS搜索域

最后这些选项只有在 `docker run` 执行时使用，因为它是针对容器的特性内容。

* `-h HOSTNAME` 或 `--hostname=HOSTNAME` 配置容器主机名
* `--link=CONTAINER_NAME:ALIAS` 添加到另一个容器的连接
* `--net=bridge|none|container:NAME_or_ID|host` 配置容器的桥接模式
* `-p SPEC` 或 `--publish=SPEC` 映射容器端口到宿主主机
* `-P or --publish-all=true|false` 映射容器所有端口到宿主主机
