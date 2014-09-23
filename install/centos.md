## CentOS系列安装docker

Docker支持CentOS6及以后的版本。

对于CentOS6，可以使用[EPEL](https://fedoraproject.org/wiki/EPEL)库安装Docker，命令如下
```
$ sudo yum install http://mirrors.yun-idc.com/epel/6/i386/epel-release-6-8.noarch.rpm
$ sudo yum install docker-io
```

CentOS7系统CentOS-Extras库中已带Docker，可以直接安装：
```
$ sudo yum install docker
```

安装之后启动Docker服务，并让它随系统启动自动加载。
```
$ sudo service docker start
$ sudo chkconfig docker on
```
