## 服务端命令

### 使用说明

`dockerd` 参数会随版本变化。建议优先在目标机器上执行 `dockerd --help`，并以 `daemon.json` 为主进行持久化配置。

### 常用选项 (Docker Engine 29.x)

* `--config-file="/etc/docker/daemon.json"`：指定 daemon 配置文件路径；
* `--data-root=""`：Docker 数据目录 (默认 `/var/lib/docker`)；
* `-H, --host=[]`：指定 daemon 监听地址 (Unix socket / TCP)；
* `-D, --debug`：开启调试日志；
* `-l, --log-level="debug|info|warn|error|fatal"`：日志级别；
* `--group=""`：Unix socket 所属用户组 (默认 `docker`)；
* `--containerd=""`：指定 containerd socket；
* `--exec-opt=[]`：运行时执行选项 (如 cgroup 驱动)；
* `--default-ulimit=[]`：设置容器默认 ulimit；
* `--dns=[]` / `--dns-search=[]` / `--dns-opt=[]`：DNS 配置；
* `--registry-mirror=[]`：镜像加速地址；
* `--insecure-registry=[]`：允许访问不安全仓库；
* `--iptables=true|false` / `--ip-forward=true|false` / `--ip-masq=true|false`：网络转发与 NAT 规则控制；
* `--ipv6=true|false`：启用 IPv6；
* `--storage-driver=""` / `--storage-opt=[]`：存储驱动及参数；
* `--log-driver=""` / `--log-opt=[]`：容器日志驱动与参数；
* `--authorization-plugin=[]`：鉴权插件；
* `--selinux-enabled=true|false`：启用 SELinux 集成 (依赖发行版策略)；
* `--userns-remap=...`：用户命名空间映射；
* `--tls` / `--tlscacert` / `--tlscert` / `--tlskey` / `--tlsverify`：TLS 安全配置。

### 历史参数提示

以下参数已移除或不建议继续使用：

* `--graph`：请改用 `--data-root`；
* `--cluster-store` / `--cluster-advertise` / `--cluster-store-opt`：已移除；
* `--disable-legacy-registry`：已移除。

### 参考

* [官方文档](https://docs.docker.com/reference/cli/dockerd/)
