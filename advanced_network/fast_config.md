##快速配置指南

下面是一个跟docker网络相关的命令列表，希望可以让你快速找到需要的信息。有些命令选项只有在docker服务启动的时候才可以执行，而且不能马上生效。
* -b BRIDGE or --bridge=BRIDGE — 桥接配置
* --bip=CIDR —  定制docker0的掩码
* -H SOCKET... or --host=SOCKET... — 它告诉docker从哪个通道来接收run container  stop 
container这样的命令，也是docker api的地址

* --icc=true|false — 请看下文容器之间的通信
* --ip-forward=true|false — 请看下文容器之间的通信
* --iptables=true|false — 请看下文容器之间的通信
* --mtu=BYTES —请看下文定制docker0

下面2个可以在docker服务启动和docker run执行的时候指定，服务启动的时候指定则会为docker run设定默认值，docker run 后面指定可以覆盖默认值。
* --dns=IP_ADDRESS... — 请看下文dns配置
* --dns-search=DOMAIN... — 请看下文dns配置

最后这些选项只有在docker run后执行，因为它是针对容器的特性内容。
*-h HOSTNAME or --hostname=HOSTNAME — 主机名配置
*--link=CONTAINER_NAME:ALIAS — link系统
*--net=bridge|none|container:NAME_or_ID|host —桥接配置
*-p SPEC or --publish=SPEC — 映射容器端口到宿主主机
* -P or --publish-all=true|false — 映射容器端口到宿主主机