## 使用
在使用swarm管理集群前，需要把集群中所有的节点的docker daemon的监听方式更改为0.0.0.0:2375,可以有两种方式达到这个目的，第一种是在启动docker daemon的时候指定
> sudo docker -H 0.0.0.0:2375&

第二种方式是直接修改docker的配置文件(以下方式是在ubuntu上面，其他版本的linux上略有不同)
> sudo vim /etc/default/docker

在文件的最后添加下面这句代码：
> DOCKER_OPTS="-H 0.0.0.0:2375 -H unix:///var/run/docker.sock"

需要注意的是，一定要在**所有的**节点上进行的。
修改之后要重启docker
> sudo service docker restart

Docker的集群管理需要使用服务发现(Discovery service backend)功能，Swarm支持以下的几种方式：DockerHub上内置的服务发现功能，本地的文件，etcd，counsel，zookeeper和IP列表，本文会详细讲解前两种方式，其他的用法都是大同小异的。

先说一下本次试验的环境，本次试验包括三台机器，IP地址分别为192.168.1.84,192.168.1.83和192.168.1.124.利用这三台机器组成一个docker集群，其中83这台机器同时充当swarm manager节点。

第一种方式，使用DockerHub上面内置的服务发现功能

第一步：在上面三台机器中的任何一台机器上面执行swarm create命令来获取一个集群标志。这条命令执行完毕后，swarm会前往DockerHub上内置的发现服务中获取一个全球唯一的token，用来标识要管理的集群。
> sudo docker run --rm swarm create

我们在84这台机器上执行这条命令，输出如下：
<pre><code>
rio@084:~$ sudo docker run --rm swarm create
b7625e5a7a2dc7f8c4faacf2b510078e
</code></pre>

可以看到我们返回的token是b7625e5a7a2dc7f8c4faacf2b510078e，每次返回的结果都是不一样的。这个token一定要记住，后面的操作都会用到这个token。

第二步：在**所有**要加入这个集群的节点上面执行swarm join命令，表示要把这台机器加入这个集群当中。在本次试验中，就是要在83,84和124这三台机器上执行下面的这条命令：
<pre><code>
sudo docker run --rm swarm join addr=ip_address:2375 token://token_id
</code></pre>
其中的ip_address换成执行这条命令的机器的IP，token_id换成上一步执行swarm create返回的token。
在83这台机器上面的执行结果如下：
<pre><code>
rio@083:~$ sudo docker run --rm swarm join --addr=192.168.1.83:2375 token://b7625e5a7a2dc7f8c4faacf2b510078e
time="2015-05-19T11:48:03Z" level=info msg="Registering on the discovery service  every 25 seconds..." addr="192.168.1.83:2375" discovery="token://b7625e5a7a2dc7 f8c4faacf2b510078e"
</code></pre>
这条命令不会自动返回，要我们自己执行Ctrl+C返回。

第三步：启动swarm manager
因为我们要使用83这台机器充当swarm manager节点，所以需要在83这台机器上面执行swarm manage命令：
<pre><code>
sudo docker run -d -p 2376:2375 swarm manage token://b7625e5a7a2dc7f8c4faacf2b510078e
</code></pre>
执行结果如下：
<pre><code>
rio@083:~$ sudo docker run -d -p 2376:2375 swarm manage token://b7625e5a7a2dc7f8c4faacf2b510078e
83de3e9149b7a0ef49916d1dbe073e44e8c31c2fcbe98d962a4f85380ef25f76
</code></pre>
这条命令如果执行成功会返回已经启动的swarm的container的ID，此时整个集群已经启动起来了。
现在通过docker ps命令来看下有没有启动成功
<pre><code>
rio@083:~$ sudo docker ps
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS                    NAMES
83de3e9149b7        swarm:latest        "/swarm manage token   4 minutes ago       Up 4 minutes        0.0.0.0:2376->2375/tcp   stupefied_stallman
</code></pre>
可以看到，swarm已经成功启动。
在执行swarm manage这条命令的时候，有几点需要注意的：

1. 这条命令需要在充当swarm manager的机器上执行
2. swarm要以daemon的形式执行
3. 映射的端口可以使任意的除了2375以外的并且是未被占用的端口，但一定不能是2375这个端口，因为2375已经被docker本身给占用了。

集群启动成功以后，现在我们可以在任何一台节点上使用swarm list命令查看集群中的节点了，本实验在124这台机器上执行swarm list命令：
<pre><code>
rio@124:~$ sudo docker run --rm swarm list token://b7625e5a7a2dc7f8c4faacf2b510078e
192.168.1.84:2375
192.168.1.124:2375
192.168.1.83:2375
</code></pre>
输出结果列出的IP地址正是我们使用swarm join命令加入集群的机器的IP地址。
现在我们可以在任何一台安装了docker的机器上面通过命令(命令中要指明swarm manager机器的IP地址)来在集群中运行container了。
本次试验，我们在192.168.1.85这台机器上使用docker info命令来查看集群中的节点的信息。其中info可以换成其他的docker支持的命令。
<pre><code>
rio@085:~$ sudo docker -H 192.168.1.83:2376 info
Containers: 8
Strategy: spread
Filters: affinity, health, constraint, port, dependency
Nodes: 2
 sclu083: 192.168.1.83:2375
  └ Containers: 1
  └ Reserved CPUs: 0 / 2
  └ Reserved Memory: 0 B / 4.054 GiB
 sclu084: 192.168.1.84:2375
  └ Containers: 7
  └ Reserved CPUs: 0 / 2
  └ Reserved Memory: 0 B / 4.053 GiB
</code></pre>
结果输出显示这个集群中只有两个节点，IP地址分别是192.168.1.83和192.168.1.84，结果不对呀，我们明明把三台机器加入了这个集群，还有124这一台机器呢？
经过排查，发现是忘了修改124这台机器上面改docker daemon的监听方式，只要按照上面的步骤修改写docker daemon的监听方式就可以了。

在使用这个方法的时候，使用swarm create可能会因为网络的原因会出现类似于下面的这个问题：
<pre><code>
rio@227:~$ sudo docker run --rm swarm create
[sudo] password for rio:
time="2015-05-19T12:59:26Z" level=fatal msg="Post https://discovery-stage.hub.docker.com/v1/clusters: dial tcp: i/o timeout"
</code></pre>

第二种方法：使用文件

第二种方法相对于第一种方法要简单得多，也不会出现类似于上面的问题。

第一步：在swarm manager节点上新建一个文件，把要加入集群的机器啊IP地址和端口号写入文件中，本次试验就是要在83这台机器上面操作：
<pre><code>
rio@083:~$ echo 192.168.1.83:2375 >> cluster
rio@083:~$ echo 192.168.1.84:2375 >> cluster
rio@083:~$ echo 192.168.1.124:2375 >> cluster
rio@083:~$ cat cluster
192.168.1.83:2375
192.168.1.84:2375
192.168.1.124:2375
</code></pre>

第二步：在083这台机器上面执行swarm manage这条命令：
<pre><code>
rio@083:~$ sudo docker run -d -p 2376:2375 -v $(pwd)/cluster:/tmp/cluster swarm manage file:///tmp/cluster
364af1f25b776f99927b8ae26ca8db5a6fe8ab8cc1e4629a5a68b48951f598ad
</code></pre>
使用docker ps来查看有没有启动成功：
<pre><code>
rio@083:~$ sudo docker ps
CONTAINER ID        IMAGE               COMMAND                CREATED              STATUS              PORTS                    NAMES
364af1f25b77        swarm:latest        "/swarm manage file:   About a minute ago   Up About a minute   0.0.0.0:2376->2375/tcp   happy_euclid
</code></pre>
可以看到，此时整个集群已经启动成功。

在使用这条命令的时候需要注意的是注意：这里一定要使用-v命令，因为cluster文件是在本机上面，启动的容器默认是访问不到的，所以要通过-v命令共享。

接下来的就可以在任何一台安装了docker的机器上面通过命令使用集群，同样的，在85这台机器上执行docker info命令查看集群的节点信息：
<pre><code>
rio@s085:~$ sudo docker -H 192.168.1.83:2376 info
Containers: 9
Strategy: spread
Filters: affinity, health, constraint, port, dependency
Nodes: 3
 atsgxxx: 192.168.1.227:2375
  └ Containers: 0
  └ Reserved CPUs: 0 / 4
  └ Reserved Memory: 0 B / 2.052 GiB
 sclu083: 192.168.1.83:2375
  └ Containers: 2
  └ Reserved CPUs: 0 / 2
  └ Reserved Memory: 0 B / 4.054 GiB
 sclu084: 192.168.1.84:2375
  └ Containers: 7
  └ Reserved CPUs: 0 / 2
  └ Reserved Memory: 0 B / 4.053 GiB
</code></pre>
