# CoreOS工具介绍

CoreOS 提供了三大工具，它们分别是：服务发现，容器管理和进程管理。

## 使用etcd服务发现

CoreOS 的第一个重要组件就是使用 etcd 来实现的服务发现。

如果你使用默认的样例 cloud-config 文件，那么 etcd 会在启动时自动运行。

例如：

```yml
#cloud-config

hostname: coreos0
ssh_authorized_keys:
  - ssh-rsa AAAA...
coreos:
  units:
    - name: etcd.service
      command: start
    - name: fleet.service
      command: start
  etcd:
    name: coreos0
    discovery: https://discovery.etcd.io/<token>
```

配置文件里有一个token，获取它可以通过如下方式：

访问地址

https://discovery.etcd.io/new

你将会获取一个包含你得 teoken 的 URL。

## 通过Docker进行容器管理

第二个组件就是 docker，它用来运行你的代码和应用。

每一个 CoreOS 的机器上都安装了它，具体使用请参考本书其他章节。

## 使用fleet进行进程管理

第三个 CoreOS 组件是 fleet。

它是集群的分布式初始化系统。你应该使用 fleet 来管理你的 docker 容器的生命周期。

Fleet通过接受systemd单元文件来工作，同时在你集群的机器上通过单元文件中编写的偏好来对它们进行调度。

首先，让我们构建一个简单的可以运行 docker 容器的 systemd 单元。把这个文件保存在 home 目录并命名为 hello.service：

```yml
hello.service

[Unit]
Description=My Service
After=docker.service

[Service]
TimeoutStartSec=0
ExecStartPre=-/usr/bin/docker kill hello
ExecStartPre=-/usr/bin/docker rm hello
ExecStartPre=/usr/bin/docker pull busybox
ExecStart=/usr/bin/docker run --name hello busybox /bin/sh -c "while true; do echo Hello World; sleep 1; done"
ExecStop=/usr/bin/docker stop hello
```

然后，读取并启动这个单元：

```yml
$ fleetctl load hello.service
=> Unit hello.service loaded on 8145ebb7.../172.17.8.105
$ fleetctl start hello.service
=> Unit hello.service launched on 8145ebb7.../172.17.8.105
```

这样，你的容器将在集群里被启动。

下面我们查看下它的状态：

```yml
$ fleetctl status hello.service
● hello.service - My Service
   Loaded: loaded (/run/fleet/units/hello.service; linked-runtime)
   Active: active (running) since Wed 2014-06-04 19:04:13 UTC; 44s ago
 Main PID: 27503 (bash)
   CGroup: /system.slice/hello.service
           ├─27503 /bin/bash -c /usr/bin/docker start -a hello || /usr/bin/docker run --name hello busybox /bin/sh -c "while true; do echo Hello World; sleep 1; done"
           └─27509 /usr/bin/docker run --name hello busybox /bin/sh -c while true; do echo Hello World; sleep 1; done

Jun 04 19:04:57 core-01 bash[27503]: Hello World
..snip...
Jun 04 19:05:06 core-01 bash[27503]: Hello World
```

我们可以停止容器：

```yml
fleetctl destroy hello.service
```

至此，就是CoreOS提供的三大工具。
