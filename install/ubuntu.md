## Ubuntu 系列安裝 Docker

### 通過系統自帶包安裝
Ubuntu 14.04 版本系統中已經自帶了 Docker 包，可以直接安裝。
```
$ sudo apt-get update
$ sudo apt-get install -y docker.io
$ sudo ln -sf /usr/bin/docker.io /usr/local/bin/docker
$ sudo sed -i '$acomplete -F _docker docker' /etc/bash_completion.d/docker.io
```

如果使用作業系統自帶包安裝 Docker，目前安裝的版本是比較舊的 0.9.1。 要安裝更新的版本，可以通過使用 Docker 源的方式。

### 通過Docker源安裝最新版本
要安裝最新的 Docker 版本，首先需要安裝 apt-transport-https 支持，之後通過添加源來安裝。
```
$ sudo apt-get install apt-transport-https
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
$ sudo bash -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
$ sudo apt-get update
$ sudo apt-get install lxc-docker
```

### 14.04 之前版本
如果是較低版本的 Ubuntu 系統，需要先更新內核。
```
$ sudo apt-get update
$ sudo apt-get install linux-image-generic-lts-raring linux-headers-generic-lts-raring
$ sudo reboot
```
然後重復上面的步驟即可。

安裝之後啟動 Docker 服務。
```
$ sudo service docker start
```
