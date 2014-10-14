## CentOS 系列安装 Docker

Docker 支持 CentOS6 及以后的版本。

### CentOS6
对于 CentOS6，可以使用 [EPEL](https://fedoraproject.org/wiki/EPEL) 库安装 Docker，命令如下
```
$ sudo yum install http://mirrors.yun-idc.com/epel/6/i386/epel-release-6-8.noarch.rpm
$ sudo yum install docker-io
```

### CentOS7
CentOS7 系统 `CentOS-Extras` 库中已带 Docker，可以直接安装：
```
$ sudo yum install docker
```

安装之后启动 Docker 服务，并让它随系统启动自动加载。
```
$ sudo service docker start
$ sudo chkconfig docker on
```
