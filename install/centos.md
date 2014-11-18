## CentOS 系列安裝 Docker

Docker 支持 CentOS6 及以後的版本。

### CentOS6
對於 CentOS6，可以使用 [EPEL](https://fedoraproject.org/wiki/EPEL) 庫安裝 Docker，命令如下
```
$ sudo yum install http://mirrors.yun-idc.com/epel/6/i386/epel-release-6-8.noarch.rpm
$ sudo yum install docker-io
```

### CentOS7
CentOS7 系統 `CentOS-Extras` 庫中已帶 Docker，可以直接安裝：
```
$ sudo yum install docker
```

安裝之後啟動 Docker 服務，並讓它隨系統啟動自動加載。
```
$ sudo service docker start
$ sudo chkconfig docker on
```
