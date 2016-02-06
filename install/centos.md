## CentOS 系列安装 Docker

系统的要求跟 Ubuntu 情况类似，64 位操作系统，内核版本至少为 3.10。

Docker 目前支持 CentOS 6.5 及以后的版本，推荐使用 CentOS 7 系统。

首先，也是要添加 yum 软件源。

```sh
$ sudo tee /etc/yum.repos.d/docker.repo <<-'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/$releasever/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF
```

之后更新 yum 软件源缓存，并安装 docker-engine。
```sh
$ sudo yum update
$ sudo yum install -y docker-engine
```

对于 CentOS 7 系统，`CentOS-Extras` 源中已内置 Docker，如果已经配置了`CentOS-Extras` 源，可以直接通过上面的 yum 命令进行安装。


另外，也可以使用官方提供的脚本来安装 Docker。
```sh
$ sudo curl -sSL https://get.docker.com/ | sh
```

可以配置让 Docker 服务在系统启动后自动启动。
```sh
$ sudo chkconfig docker on
```
