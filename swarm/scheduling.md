## swarm 调度策略
swarm支持多种调度策略来选择节点。每次在swarm启动container的时候，swarm会根据选择的调度策略来选择节点运行container。目前支持的有:spread,binpack和random。

在执行`swarm manage`命令启动 swarm 集群的时候可以通过 `--strategy` 参数来指定，默认的是spread。

spread和binpack策略会根据每台节点的可用CPU，内存以及正在运行的containers的数量来给各个节点分级，而random策略，顾名思义，他不会做任何的计算，只是单纯的随机选择一个节点来启动container。这种策略一般只做调试用。

使用spread策略，swarm会选择一个正在运行的container的数量最少的那个节点来运行container。这种情况会导致启动的container会尽可能的分布在不同的机器上运行，这样的好处就是如果有节点坏掉的时候不会损失太多的container。

binpack 则相反，这种情况下，swarm会尽可能的把所有的容器放在一台节点上面运行。这种策略会避免容器碎片化，因为他会把未使用的机器分配给更大的容器，带来的好处就是swarm会使用最少的节点运行最多的容器。

### spread 策略
先来演示下 spread 策略的情况。
```sh
rio@083:~$ sudo docker run -d -p 2376:2375 -v $(pwd)/cluster:/tmp/cluster swarm manage --strategy=spread file:///tmp/cluster
7609ac2e463f435c271d17887b7d1db223a5d696bf3f47f86925c781c000cb60
ats@sclu083:~$ sudo docker ps
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS                    NAMES
7609ac2e463f        swarm:latest        "/swarm manage --str   6 seconds ago       Up 5 seconds        0.0.0.0:2376->2375/tcp   focused_babbage
```
三台机器除了83运行了 Swarm之外，其他的都没有运行任何一个容器，现在在85这台节点上面在swarm集群上启动一个容器
```sh
rio@085:~$ sudo docker -H 192.168.1.83:2376 run --name node-1 -d -P redis
2553799f1372b432e9b3311b73e327915d996b6b095a30de3c91a47ff06ce981
rio@085:~$ sudo docker -H 192.168.1.83:2376 ps
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                  PORTS                          NAMES
2553799f1372        redis:latest        /entrypoint.sh redis   24 minutes ago      Up Less than a second   192.168.1.84:32770->6379/tcp   084/node-1
```
启动一个 redis 容器，查看结果
```sh

rio@085:~$ sudo docker -H 192.168.1.83:2376 run --name node-2 -d -P redis
7965a17fb943dc6404e2c14fb8585967e114addca068f233fcaf60c13bcf2190
rio@085:~$ sudo docker -H 192.168.1.83:2376 ps
CONTAINER ID        IMAGE                            COMMAND                CREATED                  STATUS              PORTS                           NAMES
7965a17fb943        redis:latest   /entrypoint.sh redis   Less than a second ago   Up 1 seconds        192.168.1.124:49154->6379/tcp   124/node-2                  
2553799f1372        redis:latest                     /entrypoint.sh redis   29 minutes ago           Up 4 minutes        192.168.1.84:32770->6379/tcp    084/node-1
```
再次启动一个 redis 容器，查看结果
```sh
rio@085:~$ sudo docker -H 192.168.1.83:2376 run --name node-3 -d -P redis
65e1ed758b53fbf441433a6cb47d288c51235257cf1bf92e04a63a8079e76bee
rio@085:~$ sudo docker -H 192.168.1.83:2376 ps
CONTAINER ID        IMAGE                            COMMAND                CREATED                  STATUS              PORTS                           NAMES
7965a17fb943        redis:latest                     /entrypoint.sh redis   Less than a second ago   Up 4 minutes        192.168.1.227:49154->6379/tcp   124/node-2
65e1ed758b53        redis:latest                     /entrypoint.sh redis   25 minutes ago           Up 17 seconds       192.168.1.83:32770->6379/tcp    083/node-3
2553799f1372        redis:latest                     /entrypoint.sh redis   33 minutes ago           Up 8 minutes        192.168.1.84:32770->6379/tcp    084/node-1
```
可以看到三个容器都是分布在不同的节点上面的。

### binpack 策略
现在来看看binpack策略下的情况。在083上面执行命令：
```sh
rio@083:~$ sudo docker run -d -p 2376:2375 -v $(pwd)/cluster:/tmp/cluster swarm manage --strategy=binpack  file:///tmp/cluster
f1c9affd5a0567870a45a8eae57fec7c78f3825f3a53fd324157011aa0111ac5
```

现在在集群中启动三个 redis 容器，查看分布情况：
```sh
rio@085:~$ sudo docker -H 192.168.1.83:2376 run --name node-1 -d -P redis
18ceefa5e86f06025cf7c15919fa64a417a9d865c27d97a0ab4c7315118e348c
rio@085:~$ sudo docker -H 192.168.1.83:2376 run --name node-2 -d -P redis
7e778bde1a99c5cbe4701e06935157a6572fb8093fe21517845f5296c1a91bb2
rio@085:~$ sudo docker -H 192.168.1.83:2376 run --name node-3 -d -P redis
2195086965a783f0c2b2f8af65083c770f8bd454d98b7a94d0f670e73eea05f8
rio@085:~$ sudo docker -H 192.168.1.83:2376 ps
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                  PORTS                          NAMES
2195086965a7        redis:latest        /entrypoint.sh redis   24 minutes ago      Up Less than a second   192.168.1.83:32773->6379/tcp   083/node-3
7e778bde1a99        redis:latest        /entrypoint.sh redis   24 minutes ago      Up Less than a second   192.168.1.83:32772->6379/tcp   083/node-2
18ceefa5e86f        redis:latest        /entrypoint.sh redis   25 minutes ago      Up 22 seconds           192.168.1.83:32771->6379/tcp   083/node-1
```

可以看到，所有的容器都是分布在同一个节点上运行的。