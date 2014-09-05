##centos6\7系列安装docker

使用EPEL软件仓库可以安装docker，版本必须在centos6 以后
如果是centos6
```
#wget http://mirrors.hustunique.com/epel/6/i386/epel-release-6-8.noarch.rpm
#rpm -ivhepel-release-6-8.noarch.rpm
#yum install docker-io
```
用上面这个命令安装就可以了
centos7 直接安装就可以了
如果之前的系统中存在docker这个软件，最好先删除掉这个包，一个老旧的包
```
$ service docker start
$ chkconfig docker on
```