##Ubuntu 安装Docker

###通过系统自带包安装
```
$ sudo apt-get update
$ sudo apt-get install docker.io
$ sudo ln -sf /usr/bin/docker.io /usr/local/bin/docker
$ sudo sed -i '$acomplete -F _docker docker' /etc/bash_completion.d/docker.io
```

如果使用操作系统自带包安装docker  ，使用上面的办法，安装的版本是0.9.1 (不建议，因为1.0 生产版本已经发布，下面介绍安装方法）

###通过docker源安装最新版本
如果要安装最新的docker版本，那么需要安装apt-get的https支持
```
$ sudo apt-get install apt-transport-https
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
$ sudo echo "deb https://get.docker.io/ubuntu docker main" > /etc/apt/sources.list.d/docker.list"
$ sudo apt-get update
$ sudo apt-get install lxc-docker
```

###其它版本
如果是低版本的ubuntu需要先更新内核。
```
$ sudo apt-get update
$ sudo apt-get install linux-image-generic-lts-raring linux-headers-generic-lts-raring
$ sudo reboot
```
然后重复上面的步骤即可。
