## 使用

Docker Machine 支持多种后端驱动，包括虚拟机、本地主机和云平台等。

### 本地主机实例

使用 `virtualbox` 类型的驱动，创建一台 Docker 主机，命名为 test。

```bash
$ docker-machine create -d virtualbox test
```

查看主机

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

### 支持驱动

通过 `-d` 选项可以选择支持的驱动类型。

* amazonec2
* azure
* digitalocean
* exoscale
* generic
* google
* none
* openstack
* rackspace
* softlayer
* virtualbox
* vmwarevcloudair
* vmwarevsphere


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
