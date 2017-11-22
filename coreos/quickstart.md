# 快速搭建CoreOS集群

在这里我们要搭建一个集群环境，毕竟单机环境没有什么挑战不是？

然后为了在你的电脑运行一个集群环境，我们使用Vagrant。

*Vagrant的使用这里不再阐述，请自行学习*

如果你第一次接触CoreOS这样的分布式平台，运行一个集群看起来好像一个很复杂的任务，这里我们给你展示在本地快速搭建一个CoreOS集群环境是多么的容易。

## 准备工作

首先要确认在你本地的机器上已经安装了最新版本的Virtualbox, Vagrant 和 git。

这是我们可以在本地模拟集群环境的前提条件，如果你已经拥有，请继续，否则自行搜索学习。

## 配置工作

从CoreOS官方代码库获取基本配置，并进行修改

首先，获取模板配置文件

```bash
$ git clone https://github.com/coreos/coreos-vagrant
$ cd coreos-vagrant
$ cp user-data.sample user-data
```

获取新的token

```bash
$ curl https://discovery.etcd.io/new
```

把获取的token放到user-data文件中，示例如下：

```yml
#cloud-config

coreos:
  etcd:
    discovery: https://discovery.etcd.io/<token>
```

## 启动集群

默认情况下，CoreOS Vagrantfile 将会启动单机。

我们需要复制并修改config.rb.sample文件.

复制文件

```bash
cp config.rb.sample config.rb
```

修改集群配置参数num_instances为3。

启动集群

```bash
vagrant up
=>
Bringing machine 'core-01' up with 'virtualbox' provider...
Bringing machine 'core-02' up with 'virtualbox' provider...
Bringing machine 'core-03' up with 'virtualbox' provider...
==> core-01: Box 'coreos-alpha' could not be found. Attempting to find and install...
    core-01: Box Provider: virtualbox
    core-01: Box Version: >= 0
==> core-01: Adding box 'coreos-alpha' (v0) for provider: virtualbox
    core-01: Downloading: http://storage.core-os.net/coreos/amd64-usr/alpha/coreos_production_vagrant.box
    core-01: Progress: 46% (Rate: 6105k/s, Estimated time remaining: 0:00:16)
```

添加ssh的公匙

```bash
ssh-add ~/.vagrant.d/insecure_private_key
```

连接集群中的第一台机器

```bash
vagrant ssh core-01 -- -A
```

## 测试集群

使用fleet来查看机器运行状况

```bash
fleetctl list-machines
=>
MACHINE   IP            METADATA
517d1c7d... 172.17.8.101  -
cb35b356... 172.17.8.103  -
17040743... 172.17.8.102  -
```

如果你也看到了如上类似的信息，恭喜，本地基于三台机器的集群已经成功启动，是不是很简单。

那么之后你就可以基于CoreOS的三大工具做任务分发，分布式存储等很多功能了。
