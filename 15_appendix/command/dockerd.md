# 服务端命令(dockerd)

## dockerd 命令选项

* `--api-cors-header=""`：CORS 头部域，默认不允许 CORS，要允许任意的跨域访问，可以指定为 "*"；
* `--authorization-plugin=""`：载入认证的插件；
* `-b=""`：将容器挂载到一个已存在的网桥上。指定为 `none` 时则禁用容器的网络，与 `--bip` 选项互斥；
* `--bip=""`：让动态创建的 `docker0` 网桥采用给定的 CIDR 地址; 与 `-b` 选项互斥；
* `--cgroup-parent=""`：指定 cgroup 的父组，默认 fs cgroup 驱动为 `/docker`，systemd cgroup 驱动为 `system.slice`；
* `--cluster-store=""`：构成集群（如 `Swarm`）时，集群键值数据库服务地址；
* `--cluster-advertise=""`：构成集群时，自身的被访问地址，可以为 `host:port` 或 `interface:port`；
* `--cluster-store-opt=""`：构成集群时，键值数据库的配置选项；
* `--config-file="/etc/docker/daemon.json"`：daemon 配置文件路径；
* `--containerd=""`：containerd 文件的路径；
* `-D, --debug=true|false`：是否使用 Debug 模式。缺省为 false；
* `--default-gateway=""`：容器的 IPv4 网关地址，必须在网桥的子网段内；
* `--default-gateway-v6=""`：容器的 IPv6 网关地址；
* `--default-ulimit=[]`：默认的 ulimit 值；
* `--disable-legacy-registry=true|false`：是否允许访问旧版本的镜像仓库服务器；
* `--dns=""`：指定容器使用的 DNS 服务器地址；
* `--dns-opt=""`：DNS 选项；
* `--dns-search=[]`：DNS 搜索域；
* `--exec-opt=[]`：运行时的执行选项；
* `--exec-root=""`：容器执行状态文件的根路径，默认为 `/var/run/docker`；
* `--fixed-cidr=""`：限定分配 IPv4 地址范围；
* `--fixed-cidr-v6=""`：限定分配 IPv6 地址范围；
* `-G, --group=""`：分配给 unix 套接字的组，默认为 `docker`；
* `-g, --graph=""`：Docker 运行时的根路径，默认为 `/var/lib/docker`；
* `-H, --host=[]`：指定命令对应 Docker daemon 的监听接口，可以为 unix 套接字 `unix:///path/to/socket`，文件句柄 `fd://socketfd` 或 tcp 套接字 `tcp://[host[:port]]`，默认为 `unix:///var/run/docker.sock`；
* `--icc=true|false`：是否启用容器间以及跟 daemon 所在主机的通信。默认为 true。
* `--insecure-registry=[]`：允许访问给定的非安全仓库服务；
* `--ip=""`：绑定容器端口时候的默认 IP 地址。缺省为 `0.0.0.0`；
* `--ip-forward=true|false`：是否检查启动在 Docker 主机上的启用 IP 转发服务，默认开启。注意关闭该选项将不对系统转发能力进行任何检查修改；
* `--ip-masq=true|false`：是否进行地址伪装，用于容器访问外部网络，默认开启；
* `--iptables=true|false`：是否允许 Docker 添加 iptables 规则。缺省为 true；
* `--ipv6=true|false`：是否启用 IPv6 支持，默认关闭；
* `-l, --log-level="debug|info|warn|error|fatal"`：指定日志输出级别；
* `--label="[]"`：添加指定的键值对标注；
* `--log-driver="json-file|syslog|journald|gelf|fluentd|awslogs|splunk|etwlogs|gcplogs|none"`：指定日志后端驱动，默认为 `json-file`；
* `--log-opt=[]`：日志后端的选项；
* `--mtu=VALUE`：指定容器网络的 `mtu`；
* `-p=""`：指定 daemon 的 PID 文件路径。缺省为 `/var/run/docker.pid`；
* `--raw-logs`：输出原始，未加色彩的日志信息；
* `--registry-mirror=<scheme>://<host>`：指定 `docker pull` 时使用的注册服务器镜像地址；
* `-s, --storage-driver=""`：指定使用给定的存储后端；
* `--selinux-enabled=true|false`：是否启用 SELinux 支持。缺省值为 false。SELinux 目前尚不支持 overlay 存储驱动；
* `--storage-opt=[]`：驱动后端选项；
* `--tls=true|false`：是否对 Docker daemon 启用 TLS 安全机制，默认为否；
* `--tlscacert=/.docker/ca.pem`：TLS CA 签名的可信证书文件路径；
* `--tlscert=/.docker/cert.pem`：TLS 可信证书文件路径；
* `--tlscert=/.docker/key.pem`：TLS 密钥文件路径；
* `--tlsverify=true|false`：启用 TLS 校验，默认为否；
* `--userland-proxy=true|false`：是否使用用户态代理来实现容器间和出容器的回环通信，默认为 true；
* `--userns-remap=default|uid:gid|user:group|user|uid`：指定容器的用户命名空间，默认是创建新的 UID 和 GID 映射到容器内进程。

## 参考

* [官方文档](https://docs.docker.com/engine/reference/commandline/dockerd/)
