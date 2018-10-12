## 使用

Docker Machine 支持多种后端驱动，包括虚拟机、本地主机和云平台等。

### 创建本地主机实例

#### Virtualbox 驱动

使用 `virtualbox` 类型的驱动，创建一台 Docker 主机，命名为 test。

```bash
$ docker-machine create -d virtualbox test
```

你也可以在创建时加上如下参数，来配置主机或者主机上的 Docker。

`--engine-opt dns=114.114.114.114` 配置 Docker 的默认 DNS

`--engine-registry-mirror https://registry.docker-cn.com` 配置 Docker 的仓库镜像

`--virtualbox-memory 2048` 配置主机内存

`--virtualbox-cpu-count 2` 配置主机 CPU

更多参数请使用 `docker-machine create --driver virtualbox --help` 命令查看。

#### macOS xhyve 驱动

`xhyve` 驱动 GitHub: https://github.com/zchee/docker-machine-driver-xhyve

[`xhyve`](https://github.com/mist64/xhyve) 是 macOS 上轻量化的虚拟引擎，使用其创建的 Docker Machine 较 `VirtualBox` 驱动创建的运行效率要高。

```bash
$ brew install docker-machine-driver-xhyve

$ docker-machine create \
      -d xhyve \
      # --xhyve-boot2docker-url ~/.docker/machine/cache/boot2docker.iso \
      --engine-opt dns=114.114.114.114 \
      --engine-registry-mirror https://registry.docker-cn.com \
      --xhyve-memory-size 2048 \
      --xhyve-rawdisk \
      --xhyve-cpu-count 2 \
      xhyve
```

>注意：非首次创建时建议加上 `--xhyve-boot2docker-url ~/.docker/machine/cache/boot2docker.iso` 参数，避免每次创建时都从 GitHub 下载 ISO 镜像。

更多参数请使用 `docker-machine create --driver xhyve --help` 命令查看。

#### Windows 10

Windows 10 安装 Docker for Windows 之后不能再安装 VirtualBox，也就不能使用 `virtualbox` 驱动来创建 Docker Machine，我们可以选择使用 `hyperv` 驱动。

> 注意，必须事先在 `Hyper-V` 管理器中新建一个 **外部虚拟交换机** 执行下面的命令时，使用 `--hyperv-virtual-switch=MY_SWITCH` 指定虚拟交换机名称

```bash
$ docker-machine create --driver hyperv --hyperv-virtual-switch=MY_SWITCH vm
```

更多参数请使用 `docker-machine create --driver hyperv --help` 命令查看。

### 使用介绍

创建好主机之后，查看主机

```bash
$ docker-machine ls

NAME      ACTIVE   DRIVER       STATE     URL                         SWARM   DOCKER       ERRORS
test      -        virtualbox   Running   tcp://192.168.99.187:2376           v17.10.0-ce
```

创建主机成功后，可以通过 `env` 命令来让后续操作对象都是目标主机。

```bash
$ docker-machine env test
```

后续根据提示在命令行输入命令之后就可以操作 test 主机。

也可以通过 `SSH` 登录到主机。

```bash
$ docker-machine ssh test

docker@test:~$ docker --version
Docker version 17.10.0-ce, build f4ffd25
```

连接到主机之后你就可以在其上使用 Docker 了。

### 官方支持驱动

通过 `-d` 选项可以选择支持的驱动类型。

* amazonec2
* azure
* digitalocean
* exoscale
* generic
* google
* hyperv
* none
* openstack
* rackspace
* softlayer
* virtualbox
* vmwarevcloudair
* vmwarefusion
* vmwarevsphere

### 第三方驱动

请到 [第三方驱动列表](https://github.com/docker/docker.github.io/blob/master/machine/AVAILABLE_DRIVER_PLUGINS.md) 查看


### 操作命令

* `active`                查看活跃的 Docker 主机
* `config`                输出连接的配置信息
* `create`                创建一个 Docker 主机
* `env`                   显示连接到某个主机需要的环境变量
* `inspect`               输出主机更多信息
* `ip`                    获取主机地址
* `kill`                  停止某个主机
* `ls`                    列出所有管理的主机
* `provision`             重新设置一个已存在的主机
* `regenerate-certs`      为某个主机重新生成 TLS 认证信息
* `restart`               重启主机
* `rm`                    删除某台主机
* `ssh`                   SSH 到主机上执行命令
* `scp`                   在主机之间复制文件
* `mount`                 挂载主机目录到本地
* `start`                 启动一个主机
* `status`                查看主机状态
* `stop`                  停止一个主机
* `upgrade`               更新主机 Docker 版本为最新
* `url`                   获取主机的 URL
* `version`               输出 docker-machine 版本信息
* `help`                  输出帮助信息

每个命令，又带有不同的参数，可以通过

```bash
$ docker-machine COMMAND --help
```

来查看具体的用法。
