# Debian/Ubuntu
`Debian` 和 `Ubuntu` 都是目前较为流行的 **Debian 系** 的服务器操作系统，十分适合研发场景。`Docker Hub` 上提供了官方镜像，国内各大容器云服务也基本都提供了相应的支持。

## Debian 系统简介

![Debian 操作系统](_images/debian-logo.png)

`Debian` 是由 `GPL` 和其他自由软件许可协议授权的自由软件组成的操作系统，由 **Debian 计划（Debian Project）** 组织维护。**Debian 计划** 是一个独立的、分散的组织，由 `3000` 人志愿者组成，接受世界多个非盈利组织的资金支持，`Software in the Public Interest` 提供支持并持有商标作为保护机构。`Debian` 以其坚守 `Unix` 和自由软件的精神，以及其给予用户的众多选择而闻名。现时 `Debian` 包括了超过 `25,000` 个软件包并支持 `12` 个计算机系统结构。

`Debian` 作为一个大的系统组织框架，其下有多种不同操作系统核心的分支计划，主要为采用 `Linux` 核心的 `Debian GNU/Linux` 系统，其他还有采用 `GNU Hurd` 核心的 `Debian GNU/Hurd` 系统、采用 `FreeBSD` 核心的 `Debian GNU/kFreeBSD` 系统，以及采用 `NetBSD` 核心的 `Debian GNU/NetBSD` 系统。甚至还有利用 `Debian` 的系统架构和工具，采用 `OpenSolaris` 核心构建而成的 `Nexenta OS` 系统。在这些 `Debian` 系统中，以采用 `Linux` 核心的 `Debian GNU/Linux` 最为著名。

众多的 `Linux` 发行版，例如 `Ubuntu`、`Knoppix` 和 `Linspire` 及 `Xandros` 等，都基于 `Debian GNU/Linux`。

### 使用 Debian 官方镜像

读者可以使用 `docker search` 查找 `Debian` 镜像：

```bash
$ docker search debian
NAME         DESCRIPTION    STARS     OFFICIAL   AUTOMATED
debian       Debian is...   1565      [OK]
neurodebian  NeuroDebian...   26      [OK]
armbuild/debian port of debian 8                 [OK]
...
```

官方提供了大家熟知的 `debian` 镜像以及面向科研领域的 `neurodebian` 镜像。

可以使用 `docker run` 直接运行 `Debian` 镜像。

```bash
$ docker run -it debian bash
root@668e178d8d69:/# cat /etc/issue
Debian GNU/Linux 8
```

`Debian` 镜像很适合作为基础镜像，构建自定义镜像。

## Ubuntu 系统简介

![Ubuntu 操作系统](_images/ubuntu-logo.jpg)

`Ubuntu` 是一个以桌面应用为主的 `GNU/Linux` 操作系统，其名称来自非洲南部祖鲁语或豪萨语的“ubuntu”一词（官方译名“友帮拓”，另有“吾帮托”、“乌班图”、“有奔头”或“乌斑兔”等译名）。`Ubuntu` 意思是“人性”以及“我的存在是因为大家的存在”，是非洲传统的一种价值观，类似华人社会的“仁爱”思想。 `Ubuntu` 基于 `Debian` 发行版和 `GNOME/Unity` 桌面环境，与 `Debian` 的不同在于它每 6 个月会发布一个新版本，每 2 年推出一个长期支持 **（Long Term Support，LTS）** 版本，一般支持 3 年时间。

### 使用 Ubuntu 官方镜像

`Ubuntu` 相关的镜像有很多，这里使用 `--filter=stars=10` 参数，只搜索那些被收藏 `10` 次以上的镜像。

```bash
$ docker search --filter=stars=10 ubuntu

NAME                                                      DESCRIPTION                                     STARS               OFFICIAL            AUTOMATED
ubuntu                                                    Ubuntu is a Debian-based Linux operating sys…   10539               [OK]
dorowu/ubuntu-desktop-lxde-vnc                            Docker image to provide HTML5 VNC interface …   395                                     [OK]
rastasheep/ubuntu-sshd                                    Dockerized SSH service, built on top of offi…   243                                     [OK]
consol/ubuntu-xfce-vnc                                    Ubuntu container with "headless" VNC session…   210                                     [OK]
ubuntu-upstart                                            Upstart is an event-based replacement for th…   105                 [OK]
ansible/ubuntu14.04-ansible                               Ubuntu 14.04 LTS with ansible                   98                                      [OK]
neurodebian                                               NeuroDebian provides neuroscience research s…   64                  [OK]
1and1internet/ubuntu-16-nginx-php-phpmyadmin-mysql-5      ubuntu-16-nginx-php-phpmyadmin-mysql-5          50                                      [OK]
ubuntu-debootstrap                                        debootstrap --variant=minbase --components=m…   42                  [OK]
nuagebec/ubuntu                                           Simple always updated Ubuntu docker images w…   24                                      [OK]
i386/ubuntu                                               Ubuntu is a Debian-based Linux operating sys…   19
1and1internet/ubuntu-16-apache-php-5.6                    ubuntu-16-apache-php-5.6                        14                                      [OK]
1and1internet/ubuntu-16-apache-php-7.0                    ubuntu-16-apache-php-7.0                        13                                      [OK]
eclipse/ubuntu_jdk8                                       Ubuntu, JDK8, Maven 3, git, curl, nmap, mc, …   12                                      [OK]
1and1internet/ubuntu-16-nginx-php-phpmyadmin-mariadb-10   ubuntu-16-nginx-php-phpmyadmin-mariadb-10       11                                      [OK]
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
Get:1 http://archive.ubuntu.com/ubuntu bionic InRelease [242 kB]
Get:2 http://security.ubuntu.com/ubuntu bionic-security InRelease [88.7 kB]
Get:3 http://security.ubuntu.com/ubuntu bionic-security/multiverse amd64 Packages [7348 B]
Get:4 http://security.ubuntu.com/ubuntu bionic-security/universe amd64 Packages [823 kB]
Get:5 http://archive.ubuntu.com/ubuntu bionic-updates InRelease [88.7 kB]
Get:6 http://archive.ubuntu.com/ubuntu bionic-backports InRelease [74.6 kB]
Get:7 http://archive.ubuntu.com/ubuntu bionic/universe amd64 Packages [11.3 MB]
Get:8 http://security.ubuntu.com/ubuntu bionic-security/restricted amd64 Packages [31.0 kB]
Get:9 http://security.ubuntu.com/ubuntu bionic-security/main amd64 Packages [835 kB]
Get:10 http://archive.ubuntu.com/ubuntu bionic/restricted amd64 Packages [13.5 kB]
Get:11 http://archive.ubuntu.com/ubuntu bionic/main amd64 Packages [1344 kB]
Get:12 http://archive.ubuntu.com/ubuntu bionic/multiverse amd64 Packages [186 kB]
Get:13 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 Packages [1127 kB]
Get:14 http://archive.ubuntu.com/ubuntu bionic-updates/universe amd64 Packages [1350 kB]
Get:15 http://archive.ubuntu.com/ubuntu bionic-updates/multiverse amd64 Packages [11.4 kB]
Get:16 http://archive.ubuntu.com/ubuntu bionic-updates/restricted amd64 Packages [44.7 kB]
Get:17 http://archive.ubuntu.com/ubuntu bionic-backports/main amd64 Packages [2496 B]
Get:18 http://archive.ubuntu.com/ubuntu bionic-backports/universe amd64 Packages [4252 B]
Fetched 17.6 MB in 1min 25s (207 kB/s)
Reading package lists... Done
```

首先，安装 `curl` 工具。

```bash
root@7d93de07bf76:/# apt-get install curl
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  ca-certificates krb5-locales libasn1-8-heimdal libcurl4 libgssapi-krb5-2 libgssapi3-heimdal libhcrypto4-heimdal libheimbase1-heimdal libheimntlm0-heimdal libhx509-5-heimdal
  libk5crypto3 libkeyutils1 libkrb5-26-heimdal libkrb5-3 libkrb5support0 libldap-2.4-2 libldap-common libnghttp2-14 libpsl5 libroken18-heimdal librtmp1 libsasl2-2 libsasl2-modules libsasl2-modules-db libsqlite3-0 libssl1.1 libwind0-heimdal openssl publicsuffix
...
root@7d93de07bf76:/# curl
curl: try 'curl --help' or 'curl --manual' for more information
```

接下来，再安装 `apache` 服务。

```bash
root@7d93de07bf76:/# apt-get install -y apache2
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  apache2-bin apache2-data apache2-utils file libapr1 libaprutil1 libaprutil1-dbd-sqlite3 libaprutil1-ldap libexpat1 libgdbm-compat4 libgdbm5 libicu60 liblua5.2-0 libmagic-mgc libmagic1 libperl5.26 libxml2 mime-support netbase perl perl-modules-5.26 ssl-cert xz-utils
...
```

启动这个 `apache` 服务，然后使用 `curl` 来测试本地访问。

```bash
root@7d93de07bf76:/# service apache2 start
 * Starting web server apache2                                                                                                                               AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.17.0.2. Set the 'ServerName' directive globally to suppress this message
 *
root@7d93de07bf76:/# curl 127.0.0.1

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <!--
    Modified from the Debian original for Ubuntu
    Last updated: 2016-11-16
    See: https://launchpad.net/bugs/1288690
  -->
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Apache2 Ubuntu Default Page: It works</title>
    <style type="text/css" media="screen">
...
```

配合使用 `-p` 参数对外映射服务端口，可以允许容器外来访问该服务。

## 相关资源

* `Debian` 官网：https://www.debian.org/
* `Neuro Debian` 官网：http://neuro.debian.net/
* `Debian` 官方仓库：https://github.com/Debian
* `Debian` 官方镜像：https://hub.docker.com/_/debian/
* `Debian` 官方镜像仓库：https://github.com/tianon/docker-brew-debian/
* `Ubuntu` 官网：https://ubuntu.com
* `Ubuntu` 官方仓库：https://github.com/ubuntu
* `Ubuntu` 官方镜像：https://hub.docker.com/_/ubuntu/
* `Ubuntu` 官方镜像仓库：https://github.com/tianon/docker-brew-ubuntu-core
