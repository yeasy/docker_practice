## Debian/Ubuntu
`Debian` 和 `Ubuntu` 都是目前较为流行的 Debian 系的服务器操作系统，十分适合研发场景。Docker Hub 上提供了官方镜像，国内各大容器云服务也基本都提供了相应的支持。

### Debian 系统简介

![Debian 操作系统](_images/debian-logo.png)

`Debian` 是由 `GPL` 和其他自由软件许可协议授权的自由软件组成的操作系统，由 Debian 计划（Debian Project）组织维护。Debian 计划是一个独立的、分散的组织，由 3000 人志愿者组成，接受世界多个非盈利组织的资金支持，Software in the Public Interest 提供支持并持有商标作为保护机构。Debian 以其坚守 Unix 和自由软件的精神，以及其给予用户的众多选择而闻名。现时 Debian 包括了超过 25,000 个软件包并支持 12 个计算机系统结构。

Debian 作为一个大的系统组织框架，其下有多种不同操作系统核心的分支计划，主要为采用 Linux 核心的 Debian GNU/Linux 系统，其他还有采用 GNU Hurd 核心的 Debian GNU/Hurd 系统、采用 FreeBSD 核心的 Debian GNU/kFreeBSD 系统，以及采用 NetBSD 核心的 Debian GNU/NetBSD 系统。甚至还有利用 Debian 的系统架构和工具，采用 OpenSolaris 核心构建而成的 Nexenta OS 系统。在这些 Debian 系统中，以采用 Linux 核心的 Debian GNU/Linux 最为著名。

众多的 Linux 发行版，例如 Ubuntu、Knoppix 和 Linspire 及 Xandros 等，都基于 Debian GNU/Linux。

#### 使用 Debian 官方镜像

读者可以使用 docker search 搜索 Docker Hub，查找 Debian 镜像：

```bash
$ docker search debian
NAME         DESCRIPTION    STARS     OFFICIAL   AUTOMATED
debian       Debian is...   1565      [OK]
neurodebian  NeuroDebian...   26      [OK]
armbuild/debian port of debian 8                 [OK]
...
```

官方提供了大家熟知的 debian 镜像以及面向科研领域的 neurodebian 镜像。

可以使用 docker run 直接运行 Debian 镜像。

```bash
$ docker run -it debian bash
root@668e178d8d69:/# cat /etc/issue
Debian GNU/Linux 8
```

Debian 镜像很适合作为基础镜像，构建自定义镜像。

### Ubuntu 系统简介

![Ubuntu 操作系统](_images/ubuntu-logo.jpg)

Ubuntu 是一个以桌面应用为主的GNU/Linux操作系统，其名称来自非洲南部祖鲁语或豪萨语的“ubuntu”一词（官方译名“友帮拓”，另有“吾帮托”、“乌班图”、“有奔头”或“乌斑兔”等译名）。Ubuntu 意思是“人性”以及“我的存在是因为大家的存在”，是非洲传统的一种价值观，类似华人社会的“仁爱”思想。 Ubuntu 基于 Debian 发行版和 GNOME/Unity 桌面环境，与 Debian 的不同在于它每 6 个月会发布一个新版本，每 2 年推出一个长期支持（Long Term Support，LTS）版本，一般支持 3 年时间。

#### 使用 Ubuntu 官方镜像

Ubuntu 相关的镜像有很多，这里使用 `--filter=stars=10` 参数，只搜索那些被收藏 10 次以上的镜像。

```bash
$ docker search --filter=stars=10 ubuntu

NAME                                 DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
ubuntu                               Official Ubuntu base image                      840       [OK]
dockerfile/ubuntu                    Trusted automated Ubuntu (http://www.ubunt...   30                   [OK]
crashsystems/gitlab-docker           A trusted, regularly updated build of GitL...   20                   [OK]
sylvainlasnier/memcached             This is a Memcached 1.4.14 docker images b...   16                   [OK]
ubuntu-upstart                       Upstart is an event-based replacement for ...   16        [OK]
mbentley/ubuntu-django-uwsgi-nginx                                                   16                   [OK]
clue/ttrss                           The Tiny Tiny RSS feed reader allows you t...   14                   [OK]
dockerfile/ubuntu-desktop            Trusted automated Ubuntu Desktop (LXDE) (h...   14                   [OK]
tutum/ubuntu                         Ubuntu image with SSH access. For the root...   12                   [OK]
```

根据搜索出来的结果，读者可以自行选择下载镜像并使用。

下面以 `ubuntu:18.04` 为例，演示如何使用该镜像安装一些常用软件。

首先使用 `-ti` 参数启动容器，登录 `bash`，查看 `ubuntu` 的发行版本号。

```bash
$ docker run -ti ubuntu:18.04 /bin/bash
root@7d93de07bf76:/# cat /etc/os-release
NAME="Ubuntu"
VERSION="18.04.1 LTS (Bionic Beaver)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 18.04.1 LTS"
VERSION_ID="18.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=bionic
UBUNTU_CODENAME=bionic
```

当试图直接使用 `apt-get` 安装一个软件的时候，会提示 `E: Unable to locate package`。

```bash
root@7d93de07bf76:/# apt-get install curl
Reading package lists... Done
Building dependency tree
Reading state information... Done
E: Unable to locate package curl
```

这并非系统不支持 `apt-get` 命令。Docker 镜像在制作时为了精简清除了 `apt` 仓库信息，因此需要先执行 `apt-get update` 命令来更新仓库信息。更新信息后即可成功通过 `apt-get` 命令来安装软件。

```bash
root@7d93de07bf76:/# apt-get update
Ign http://archive.ubuntu.com trusty InRelease
Ign http://archive.ubuntu.com trusty-updates InRelease
Ign http://archive.ubuntu.com trusty-security InRelease
Ign http://archive.ubuntu.com trusty-proposed InRelease
Get:1 http://archive.ubuntu.com trusty Release.gpg [933 B]
...
```

首先，安装 curl 工具。

```bash
root@7d93de07bf76:/# apt-get install curl
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following extra packages will be installed:
  ca-certificates krb5-locales libasn1-8-heimdal libcurl3 libgssapi-krb5-2
  libgssapi3-heimdal libhcrypto4-heimdal libheimbase1-heimdal
  libheimntlm0-heimdal libhx509-5-heimdal libidn11 libk5crypto3 libkeyutils1
  libkrb5-26-heimdal libkrb5-3 libkrb5support0 libldap-2.4-2
  libroken18-heimdal librtmp0 libsasl2-2 libsasl2-modules libsasl2-modules-db
  libwind0-heimdal openssl
...
root@7d93de07bf76:/# curl
curl: try 'curl --help' or 'curl --manual' for more information
```

接下来，再安装 apache 服务。

```bash
root@7d93de07bf76:/# apt-get install -y apache2
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following extra packages will be installed:
  apache2-bin apache2-data libapr1 libaprutil1 libaprutil1-dbd-sqlite3
  libaprutil1-ldap libxml2 sgml-base ssl-cert xml-core
...
```

启动这个 apache 服务，然后使用 curl 来测试本地访问。

```bash
root@7d93de07bf76:/# service apache2 start
 * Starting web server apache2                                                                                                                               AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.17.0.2. Set the 'ServerName' directive globally to suppress this message
 *
root@7d93de07bf76:/# curl 127.0.0.1

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <!--
    Modified from the Debian original for Ubuntu
    Last updated: 2014-03-19
    See: https://launchpad.net/bugs/1288690
  -->
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Apache2 Ubuntu Default Page: It works</title>
    <style type="text/css" media="screen">
...
```

配合使用 `-p` 参数对外映射服务端口，可以允许容器外来访问该服务。

### 相关资源

* `Debian` 官网：https://www.debian.org/
* `Neuro Debian` 官网：http://neuro.debian.net/
* `Debian` 官方仓库：https://github.com/Debian
* `Debian` 官方镜像：https://hub.docker.com/_/debian/
* `Debian` 官方镜像仓库：https://github.com/tianon/docker-brew-debian/
* `Ubuntu` 官网：http://www.ubuntu.org.cn/global
* `Ubuntu` 官方仓库：https://github.com/ubuntu
* `Ubuntu` 官方镜像：https://hub.docker.com/_/ubuntu/
* `Ubuntu` 官方镜像仓库：https://github.com/tianon/docker-brew-ubuntu-core
