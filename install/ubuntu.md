## Ubuntu 系列安裝 Docker

### 透過系統內建套件安裝
Ubuntu 14.04 版本套件庫中已經內建了 Docker 套件，可以直接安裝。
```
$ sudo apt-get update
$ sudo apt-get install -y docker.io
$ sudo ln -sf /usr/bin/docker.io /usr/local/bin/docker
$ sudo sed -i '$acomplete -F _docker docker' /etc/bash_completion.d/docker.io
```

如果使用作業系統內建套件安裝 Docker，目前安裝的版本是比較舊的 0.9.1。 要安裝更新的版本，可以透過更新 Docker 套件庫的方式進行安裝。

### 透過Docker 套件庫安裝最新版本
要安裝最新的 Docker 版本，首先需要安裝 apt-transport-https 支持，之後透過新增套件庫來安裝。
```
$ sudo apt-get install apt-transport-https
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
$ sudo bash -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
$ sudo apt-get update
$ sudo apt-get install -y lxc-docker
```

### 14.04 之前版本
如果是較舊版本的 Ubuntu 系統，需要先更新核心。
```
$ sudo apt-get update
$ sudo apt-get install linux-image-generic-lts-raring linux-headers-generic-lts-raring
$ sudo reboot
```
然後重複上面的步驟即可。

安裝之後啟動 Docker 服務。
```
$ sudo service docker start
```
