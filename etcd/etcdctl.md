## 使用 etcdctl

etcdctl 是一个命令行客户端，它能提供一些简洁的命令，供用户直接跟 etcd 服务打交道，而无需基于 HTTP API 方式。这在某些情况下将很方便，例如用户对服务进行测试或者手动修改数据库内容。我们也推荐在刚接触 etcd 时通过 etcdctl 命令来熟悉相关的操作，这些操作跟 HTTP API 实际上是对应的。

etcd 项目二进制发行包中已经包含了 etcdctl 工具，没有的话，可以从 [github.com/coreos/etcd/releases](https://github.com/coreos/etcd/releases) 下载。

etcdctl 支持如下的命令，大体上分为数据库操作和非数据库操作两类，后面将分别进行解释。

```bash
$ etcdctl -h
NAME:
   etcdctl - A simple command line client for etcd.

USAGE:
   etcdctl [global options] command [command options] [arguments...]

VERSION:
   2.0.0-rc.1

COMMANDS:
   backup	backup an etcd directory
   mk		make a new key with a given value
   mkdir	make a new directory
   rm		remove a key
   rmdir	removes the key if it is an empty directory or a key-value pair
   get		retrieve the value of a key
   ls		retrieve a directory
   set		set the value of a key
   setdir	create a new or existing directory
   update	update an existing key with a given value
   updatedir	update an existing directory
   watch	watch a key for changes
   exec-watch	watch a key for changes and exec an executable
   member	member add, remove and list subcommands
   help, h	Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --debug			output cURL commands which can be used to reproduce the request
   --no-sync			don't synchronize cluster information before sending request
   --output, -o 'simple'	output response in the given format (`simple` or `json`)
   --peers, -C 			a comma-delimited list of machine addresses in the cluster (default: "127.0.0.1:4001")
   --cert-file 			identify HTTPS client using this SSL certificate file
   --key-file 			identify HTTPS client using this SSL key file
   --ca-file 			verify certificates of HTTPS-enabled servers using this CA bundle
   --help, -h			show help
   --version, -v		print the version
```

### 数据库操作
数据库操作围绕对键值和目录的 CRUD （符合 REST 风格的一套操作：Create）完整生命周期的管理。

etcd 在键的组织上采用了层次化的空间结构（类似于文件系统中目录的概念），用户指定的键可以为单独的名字，如 `testkey`，此时实际上放在根目录 `/` 下面，也可以为指定目录结构，如 `cluster1/node2/testkey`，则将创建相应的目录结构。

*注：CRUD 即 Create, Read, Update, Delete，是符合 REST 风格的一套 API 操作。*

#### set
指定某个键的值。例如
```bash
$ etcdctl set /testdir/testkey "Hello world"
Hello world
```
支持的选项包括：
```bash
--ttl '0'			该键值的超时时间（单位为秒），不配置（默认为 0）则永不超时
--swap-with-value value 若该键现在的值是 value，则进行设置操作
--swap-with-index '0'	若该键现在的索引值是指定索引，则进行设置操作
```

#### get
获取指定键的值。例如
```bash
$ etcdctl set testkey hello
hello
$ etcdctl update testkey world
world
```

当键不存在时，则会报错。例如
```bash
$ etcdctl get testkey2
Error:  100: Key not found (/testkey2) [1]
```

支持的选项为
```bash
--sort	对结果进行排序
--consistent 将请求发给主节点，保证获取内容的一致性
```

#### update
当键存在时，更新值内容。例如
```bash
$ etcdctl set testkey hello
hello
$ etcdctl update testkey world
world
```

当键不存在时，则会报错。例如
```bash
$ etcdctl update testkey2 world
Error:  100: Key not found (/testkey2) [1]
```

支持的选项为
```bash
--ttl '0'	超时时间（单位为秒），不配置（默认为 0）则永不超时
```

#### rm
删除某个键值。例如
```bash
$ etcdctl rm testkey
```

当键不存在时，则会报错。例如
```bash
$ etcdctl rm testkey2
Error:  100: Key not found (/testkey2) [8]
```

支持的选项为
```bash
--dir		如果键是个空目录或者键值对则删除
--recursive		删除目录和所有子键
--with-value 	检查现有的值是否匹配
--with-index '0'	检查现有的 index 是否匹配
```

#### mk
如果给定的键不存在，则创建一个新的键值。例如
```bash
$ etcdctl mk /testdir/testkey "Hello world"
Hello world
```
当键存在的时候，执行该命令会报错，例如
```bash
$ etcdctl set testkey "Hello world"
Hello world
$ ./etcdctl mk testkey "Hello world"
Error:  105: Key already exists (/testkey) [2]
```

支持的选项为
```bash
--ttl '0'	超时时间（单位为秒），不配置（默认为 0）则永不超时
```

#### mkdir
如果给定的键目录不存在，则创建一个新的键目录。例如
```bash
$ etcdctl mkdir testdir
```
当键目录存在的时候，执行该命令会报错，例如
```bash
$ etcdctl mkdir testdir
$ etcdctl mkdir testdir
Error:  105: Key already exists (/testdir) [7]
```
支持的选项为
```bash
--ttl '0'	超时时间（单位为秒），不配置（默认为 0）则永不超时
```

#### setdir

创建一个键目录，无论存在与否。

支持的选项为
```bash
--ttl '0'	超时时间（单位为秒），不配置（默认为 0）则永不超时
```

#### updatedir
更新一个已经存在的目录。
支持的选项为
```bash
--ttl '0'	超时时间（单位为秒），不配置（默认为 0）则永不超时
```

#### rmdir
删除一个空目录，或者键值对。

若目录不空，会报错
```bash
$ etcdctl set /dir/testkey hi
hi
$ etcdctl rmdir /dir
Error:  108: Directory not empty (/dir) [13]
```

#### ls
列出目录（默认为根目录）下的键或者子目录，默认不显示子目录中内容。

例如
```bash
$ ./etcdctl set testkey 'hi'
hi
$ ./etcdctl set dir/test 'hello'
hello
$ ./etcdctl ls
/testkey
/dir
$ ./etcdctl ls dir
/dir/test
```

支持的选项包括
```bash
--sort	将输出结果排序
--recursive	如果目录下有子目录，则递归输出其中的内容
-p		对于输出为目录，在最后添加 `/` 进行区分
```

### 非数据库操作

#### backup
备份 etcd 的数据。

支持的选项包括
```bash
--data-dir 		etcd 的数据目录
--backup-dir 	备份到指定路径
```
#### watch
监测一个键值的变化，一旦键值发生更新，就会输出最新的值并退出。

例如，用户更新 testkey 键值为 Hello world。
```bash
$ etcdctl watch testkey
Hello world
```

支持的选项包括
```bash
--forever		一直监测，直到用户按 `CTRL+C` 退出
--after-index '0'	在指定 index 之前一直监测
--recursive		返回所有的键值和子键值
```
#### exec-watch
监测一个键值的变化，一旦键值发生更新，就执行给定命令。

例如，用户更新 testkey 键值。
```bash
$etcdctl exec-watch testkey -- sh -c 'ls'
default.etcd
Documentation
etcd
etcdctl
etcd-migrate
README-etcdctl.md
README.md
```

支持的选项包括
```bash
--after-index '0'	在指定 index 之前一直监测
--recursive		返回所有的键值和子键值
```

#### member
通过 list、add、remove 命令列出、添加、删除 etcd 实例到 etcd 集群中。

例如本地启动一个 etcd 服务实例后，可以用如下命令进行查看。
```bash
$ etcdctl member list
ce2a822cea30bfca: name=default peerURLs=http://localhost:2380,http://localhost:7001 clientURLs=http://localhost:2379,http://localhost:4001

```
### 命令选项
* `--debug`			输出 cURL 命令，显示执行命令的时候发起的请求
* `--no-sync`			发出请求之前不同步集群信息
* `--output, -o 'simple'`	输出内容的格式 (`simple` 为原始信息，`json` 为进行json格式解码，易读性好一些)
* `--peers, -C`			指定集群中的同伴信息，用逗号隔开 (默认为: "127.0.0.1:4001")
* `--cert-file` 			HTTPS 下客户端使用的 SSL 证书文件
* `--key-file`			HTTPS 下客户端使用的 SSL 密钥文件
* `--ca-file` 			服务端使用 HTTPS 时，使用 CA 文件进行验证
* `--help, -h`			显示帮助命令信息
* `--version, -v`		打印版本信息
