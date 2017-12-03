## 安装

`etcd` 基于 Go 语言实现，因此，用户可以从 [项目主页](https://github.com/coreos/etcd) 下载源代码自行编译，也可以下载编译好的二进制文件，甚至直接使用制作好的 Docker 镜像文件来体验。

>注意：本章节内容基于 etcd `3.x` 版本

### 二进制文件方式下载

编译好的二进制文件都在 [github.com/coreos/etcd/releases](https://github.com/coreos/etcd/releases/) 页面，用户可以选择需要的版本，或通过下载工具下载。

例如，使用 `curl` 工具下载压缩包，并解压。

```bash
$ curl -L  https://github.com/coreos/etcd/releases/download/v3.2.10/etcd-v3.2.10-linux-amd64.tar.gz -o etcd-v3.2.10-linux-amd64.tar.gz
$ tar xzvf etcd-v3.2.10-linux-amd64.tar.gz
$ cd etcd-v3.2.10-linux-amd64
```

解压后，可以看到文件包括

```bash
$ ls
Documentation README-etcdctl.md README.md READMEv2-etcdctl.md etcd etcdctl
```

其中 `etcd` 是服务主文件，`etcdctl` 是提供给用户的命令客户端，其他文件是支持文档。

下面将 `etcd` `etcdctl` 文件放到系统可执行目录（例如 `/usr/local/bin/`）。

```bash
$ sudo cp etcd* /usr/local/bin/
```

默认 `2379` 端口处理客户端的请求，`2380` 端口用于集群各成员间的通信。启动 etcd 显示类似如下的信息：

```bash
$ etcd
2017-12-03 11:18:34.406082 I | etcdmain: etcd Version: 3.2.10
2017-12-03 11:18:34.406226 I | etcdmain: Git SHA: GitNotFound
2017-12-03 11:18:34.406235 I | etcdmain: Go Version: go1.9.2
2017-12-03 11:18:34.406242 I | etcdmain: Go OS/Arch: darwin/amd64
2017-12-03 11:18:34.406250 I | etcdmain: setting maximum number of CPUs to 4, total number of available CPUs is 4
2017-12-03 11:18:34.406265 N | etcdmain: failed to detect default host (default host not supported on darwin_amd64)
2017-12-03 11:18:34.406279 W | etcdmain: no data-dir provided, using default data-dir ./default.etcd
2017-12-03 11:18:34.406457 N | etcdmain: the server is already initialized as member before, starting as etcd member...
2017-12-03 11:18:34.411579 I | embed: listening for peers on http://localhost:2380
2017-12-03 11:18:34.411938 I | embed: listening for client requests on localhost:2379
```

此时，可以使用 `etcdctl` 命令进行测试，设置和获取键值 `testkey: "hello world"`，检查 etcd 服务是否启动成功：

```bash
$ etcdctl member list
8e9e05c52164694d, started, default, http://localhost:2380, http://localhost:2379

$ etcdctl put testkey "hello world"
OK

$ etcdctl get testkey
testkey
hello world
```

说明 etcd 服务已经成功启动了。

### Docker 镜像方式运行

镜像名称为 `quay.io/coreos/etcd`，可以通过下面的命令启动 `etcd` 服务监听到 `2379` 和 `2380` 端口。

```bash
$ export NODE1=192.168.1.21

$ docker run --name etcd \
    -p 2379:2379 \
    -p 2380:2380 \
    --volume=etcd-data:/etcd-data \
    quay.io/coreos/etcd:latest \
    /usr/local/bin/etcd \
    --data-dir=/etcd-data --name node1 \
    --initial-advertise-peer-urls http://${NODE1}:2380 --listen-peer-urls http://0.0.0.0:2380 \
    --advertise-client-urls http://${NODE1}:2379 --listen-client-urls http://0.0.0.0:2379 \
    --initial-cluster node1=http://${NODE1}:2380
```

>注意：etcd 官方标注 `quay.io/coreos/etcd` 即将废弃，启用新的 `gcr.io/etcd-development/etcd` 镜像，但后者由于网络原因，国内不能下载到该镜像，这里仍然使用前者作为演示。

打开新的终端按照上一步的方法测试 etcd 是否成功启动。

### macOS 中运行

```bash
$ brew install etcd

$ etcd

$ etcdctl member list
```
