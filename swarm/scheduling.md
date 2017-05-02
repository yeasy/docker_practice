## Swarm 中的调度器
调度是集群十分重要的功能，Swarm 目前支持三种调度策略：`spread`、`binpack` 和 `random`。

在执行`swarm manage`命令启动管理服务的时候，可以通过 `--strategy` 参数指定调度策略，默认的是 `spread`。

简单来说，这三种调度策略的优化目标如下：

* `spread`：如果节点配置相同，选择一个正在运行的容器数量最少的那个节点，即尽量平摊容器到各个节点；
* `binpack`：跟 `spread` 相反，尽可能的把所有的容器放在一台节点上面运行，即尽量少用节点，避免容器碎片化。
* `random`：直接随机分配，不考虑集群中节点的状态，方便进行测试使用。

### spread 调度策略
仍然以之前创建好的集群为例，来演示下 spread 策略的行为。

在 `192.168.0.2` 节点启动管理服务，管理 token://946d65606f7c2f49766e4dddac5b4365 的集群。

```sh
$ docker run -d -p 12375:2375 swarm manage  --strategy "spread" token://946d65606f7c2f49766e4dddac5b4365
c6f25e6e6abbe45c8bcf75ac674f2b64d5f31a5c6070d64ba954a0309b197930
```

列出集群中节点。

```sh
$ docker run --rm swarm list token://946d65606f7c2f49766e4dddac5b4365
192.168.0.3:2375
192.168.0.2:2375
```

此时，两个节点上除了 swarm 外都没有运行其它容器。

启动一个 ubuntu 容器。

```sh
$ docker -H 192.168.0.2:12375 run -d ubuntu:14.04 ping 127.0.0.1
bac3dfda5306181140fc959969d738549d607bc598390f57bdd432d86f16f069
```

查看发现它实际上被调度到了 `192.168.0.3` 节点（当节点配置相同时候，初始节点随机选择）。

再次启动一个 ubuntu 容器。

```sh
$ docker -H 192.168.0.2:12375 run -d ubuntu:14.04 ping 127.0.0.1
8247067ba3a31e0cb692a8373405f95920a10389ce3c2a07091408281695281c
```

查看它的位置，发现被调度到了另外一个节点：`192.168.0.2` 节点。

```sh
$ docker -H 192.168.0.2:12375 ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                         NAMES
8247067ba3a3        ubuntu:14.04        "ping 127.0.0.1"         1 minutes ago       Up 1 minutes                            Host-2/sick_galileo
bac3dfda5306        ubuntu:14.04        "ping 127.0.0.1"         2 minutes ago       Up 2 minutes                            Host-3/compassionate_ritchie
```

当节点配置不同的时候，`spread`会更愿意分配到配置较高的节点上。

### binpack 调度策略
现在来看看 `binpack` 策略下的情况。

直接启动若干 ubuntu 容器，并查看它们的位置。

```sh
$ docker -H 192.168.0.2:12375 run -d ubuntu:14.04 ping 127.0.0.1
$ docker -H 192.168.0.2:12375 ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                         NAMES
4c4f45eba866        ubuntu:14.04        "ping 127.0.0.1"         3 minutes ago       Up 3 minutes                            Host-3/hopeful_brown
5e650541233c        ubuntu:14.04        "ping 127.0.0.1"         3 minutes ago       Up 3 minutes                            Host-3/pensive_wright
99c5a092530a        ubuntu:14.04        "ping 127.0.0.1"         3 minutes ago       Up 3 minutes                            Host-3/naughty_engelbart
4ab392c26eb2        ubuntu:14.04        "ping 127.0.0.1"         3 minutes ago       Up 3 minutes                            Host-3/thirsty_mclean
```
可以看到，所有的容器都是分布在同一个节点（`192.168.0.3`）上运行的。