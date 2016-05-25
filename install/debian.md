# Debian操作系统安装Docker

## 支持的版本

- Debian testing stretch (64-bit)
- Debian 8.0 Jessie (64-bit)
- Debian 7.7 Wheezy (64-bit)

## 预安装

Docker 支持 64 位、内核高于 3.10 的 Debian 操作系统，内核低于 3.10 将导致数据丢失和系统不稳定等问题。  
查看内核版本使用以下命令：

```
$ uname -r
```

### 更新APT仓库

Docker 的 APT 仓库包含了 1.7.1 及以上版本的 Docker，安装前需要更新 APT 设置，来使用新的仓库：

#### 1. 清理旧的仓库信息

```sh
 $ apt-get purge lxc-docker*
 $ apt-get purge docker.io*
```

#### 2. 更新和安装软件包

```sh
 $ apt-get update
 $ apt-get install apt-transport-https ca-certificates
```

#### 3. 添加 GPG 键

```
 $ apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
```

#### 4. 添加 APT 源

编辑文件 `/etc/apt/sources.list.d/docker.list`，清理已存在的信息，写入APT源地址内容。以下以 Debian Jessie 为例，非 Jessie 版本的系统注意修改为自己对应的代号。

```sh
$ sudo cat <<EOF > /etc/apt/sources.list.d/docker.list
deb https://apt.dockerproject.org/repo debian-jessie main
EOF
```

其他两个版本内容：

```
deb https://apt.dockerproject.org/repo debian-wheezy main
```

```
deb https://apt.dockerproject.org/repo debian-stretch main
```

#### 5. 校验安装结果

```
 $ apt-cache policy docker-engine
docker-engine:
  Installed: 1.11.0-0~jessie
  Candidate: 1.11.0-0~jessie
  Version table:
 *** 1.11.0-0~jessie 0
        500 https://apt.dockerproject.org/repo/ debian-jessie/main amd64 Packages
        100 /var/lib/dpkg/status
  .....
```

以后，当执行 `apt-get upgrade` 等命令时，将使用新设置的的 APT 源。

## 安装 Docker

```
$ sudo apt-get install docker-engine
```

## 为非 root 用户授权

```
# 如果没有就建立一个 Docker 组
$ sudo groupadd docker

# 增加一个用户（用真实的名字替换下面的 ${USER}）到 Docker 组，需重登陆来生效
$ sudo gpasswd -a ${USER} docker

# 重启 Docker 服务
$ sudo service docker restart
```

## 更新 Docker

```
$ apt-get upgrade docker-engine
```

## 卸载 Docker

```sh
# 卸载软件包
$ sudo apt-get purge docker-engine

#卸载依赖包
$ sudo apt-get autoremove --purge docker-engine

#如有必要，执行以下命令，删除全部镜像、容器、数据卷和其他docker相关用户信息:
$ rm -rf /var/lib/docker
```
