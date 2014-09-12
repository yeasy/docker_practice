##centos6/7系列安装docker

使用EPEL软件仓库可以安装docker，版本必须在centos6 以后
如果是centos6，用下面的命令安装
```
#wget http://mirrors.hustunique.com/epel/6/i386/epel-release-6-8.noarch.rpm
#rpm -ivhepel-release-6-8.noarch.rpm
#yum install docker-io
```

centos7 直接通过系统命令安装：
```
yum install docker-io
```
如果之前的系统中存在docker这个软件，最好先删除掉这个包。
```
yum remove docker-io
```

安装之后启动docker服务并添加自动启动到系统服务。
```
$ service docker start
$ chkconfig docker on
```
