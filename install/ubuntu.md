## Ubuntu 系列安装 Docker

### 通过系统自带包安装
Ubuntu 14.04 版本系统中已经自带了 Docker 包，可以直接安装。
```
$ sudo apt-get update
$ sudo apt-get install -y docker.io
$ sudo ln -sf /usr/bin/docker.io /usr/local/bin/docker
$ sudo sed -i '$acomplete -F _docker docker' /etc/bash_completion.d/docker.io
```

如果使用操作系统自带包安装 Docker，目前安装的版本是比较旧的 0.9.1。 要安装更新的版本，可以通过使用 Docker 源的方式。

### 通过Docker源安装最新版本
要安装最新的 Docker 版本，首先需要安装 apt-transport-https 支持，之后通过添加源来安装。
```
$ sudo apt-get install apt-transport-https
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
$ sudo bash -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
$ sudo apt-get update
$ sudo apt-get install lxc-docker
```

### 14.04 之前版本
如果是较低版本的 Ubuntu 系统，需要先更新内核。
```
$ sudo apt-get update
$ sudo apt-get install linux-image-generic-lts-raring linux-headers-generic-lts-raring
$ sudo reboot
```
然后重复上面的步骤即可。

安装之后启动 Docker 服务。
```
$ sudo service docker start
```
