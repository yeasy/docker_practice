## Ubuntu 系列安装 Docker

### 系统要求

Docker 支持以下版本的Ubuntu操作系统：

* Ubuntu Xenial 16.04 (LTS)
* Ubuntu Wily 15.10
* Ubuntu Trusty 14.04 (LTS)
* Ubuntu Precise 12.04 (LTS)

### 预安装
Docker 目前只能安装在 64 位平台上，并且要求内核版本不低于 3.10，实际上内核越新越好，过低的内核版本容易造成功能的不稳定。

用户可以通过如下命令检查自己的内核版本详细信。

```sh
$ uname -a
Linux Host 3.16.0-43-generic #58~14.04.1-Ubuntu SMP Mon Jun 22 10:21:20 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux
```
或者
```sh
$ cat /proc/version
Linux version 3.16.0-43-generic (buildd@brownie) (gcc version 4.8.2 (Ubuntu 4.8.2-19ubuntu1) ) #58~14.04.1-Ubuntu SMP Mon Jun 22 10:21:20 UTC 2015
```

Docker 目前支持的最低 Ubuntu 版本为 12.04 LTS，但实际上从稳定性上考虑，推荐至少使用 14.04 LTS 版本。

#### 更新APT镜像源

首先需要安装 apt-transport-https 包支持 https 协议的源。
```
$ sudo apt-get install apt-transport-https ca-certificates
```

添加源的 gpg 密钥。
```sh
$ sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
```

获取当前操作系统的代号。
```sh
$ lsb_release -c
Codename:       trusty
```

一般的，12.04 (LTS) 代号为 precise，14.04 (LTS) 代号为 trusty，15.04 代号为 vivid，15.10 代号为 wily，16.04 代号为Xenial 。这里获取到代号为 trusty。

接下来就可以添加 Docker 的官方 apt 软件源了。通过下面命令创建 `/etc/apt/sources.list.d/docker.list` 文件，并写入源的地址内容。非 trusty 版本的系统注意修改为自己对应的代号。

```sh
$ sudo cat <<EOF > /etc/apt/sources.list.d/docker.list
deb https://apt.dockerproject.org/repo ubuntu-trusty main
EOF
```

添加成功后，更新 apt 软件包缓存。
```sh
$ sudo apt-get update
```


#### 分版本的预安装任务

##### 高于 12.04 LTS的版本

-    -    Ubuntu Xenial 16.04 (LTS)
-    Ubuntu Wily 15.10
-    Ubuntu Trusty 14.04 (LTS)


1. 为了让 Docker 使用 aufs 存储，推荐安装 `linux-image-extra` 软件包。
```
$ sudo apt-get install -y linux-image-extra-$(uname -r)
```
2. 在 Ubuntu 14.04 或者 12.04上安装Docker，需要安装`apparmor`（apparmor是Linux内核的一个安全模块，新版本的Ubuntu已经被整合到内核）:
```
$ sudo apt-get install apparmor
```

##### 12.04 LTS版本
如果使用 12.04 LTS 版本，首先要更新系统内核和安装可能需要的软件包，包括 

* linux-image-generic-lts-trusty （必备）
* linux-headers-generic-lts-trusty （必备）
* xserver-xorg-lts-trusty  （带图形界面时必备）
* libgl1-mesa-glx-lts-trusty（带图形界面时必备）

安装命令(根据环境和要求不同，选择安装上述软件包)，如：
```
$ sudo apt-get install linux-image-generic-lts-trusty
```

当然，12.04 LTS 还要根据需要安装`linux-image-extra` 和 `apparmor` 软件包。

*注：Ubuntu 发行版中，LTS （Long-Term-Support）意味着更稳定的功能和更长期（目前为 5 年）的升级支持，生产环境中尽量使用 LTS 版本。*


### 安装 Docker
在成功添加源之后，就可以安装最新版本的 Docker 了，软件包名称为 docker-engine。

```sh
$ sudo apt-get install -y docker-engine
```

如果系统中存在旧版本的 Docker （lxc-docker），会提示是否先删除，选择是即可。

### 其他可选配置
参见 [docker官方配置文档。](https://docs.docker.com/engine/installation/linux/ubuntulinux/)