## CentOS 操作系统安装 Docker

### 系统要求

Docker 最低支持 CentOS 7。

Docker 需要安装在 64 位的平台，并且内核版本不低于 3.10。 CentOS 7 满足最低内核的要求，但由于内核版本比较低，部分功能（如 `overlay2` 存储层驱动）无法使用，并且部分功能可能不太稳定。

### 使用脚本自动安装

Docker 官方为了简化安装流程，提供了一套安装脚本，CentOS 系统上可以使用这套脚本安装：

```bash
curl -sSL https://get.docker.com/ | sh
```

执行这个命令后，脚本就会自动的将一切准备工作做好，并且把 Docker 安装在系统中。

不过，由于伟大的墙的原因，在国内使用这个脚本可能会出现某些下载出现错误的情况。国内的一些云服务商提供了这个脚本的修改版本，使其使用国内的 Docker 软件源镜像安装，这样就避免了墙的干扰。

#### 阿里云的安装脚本

```bash
curl -sSL http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh -
```

#### DaoCloud 的安装脚本

```bash
curl -sSL https://get.daocloud.io/docker | sh
```

### 手动安装

#### 添加内核参数

默认配置下，在 CentOS 使用 Docker 可能会碰到下面的这些警告信息：

```bash
WARNING: bridge-nf-call-iptables is disabled
WARNING: bridge-nf-call-ip6tables is disabled
```

添加内核配置参数以启用这些功能。

```bash
$ sudo tee -a /etc/sysctl.conf <<-EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
```

然后重新加载 `sysctl.conf` 即可

```bash
$ sudo sysctl -p
```

#### 添加 yum 源

虽然 CentOS 软件源 `Extras` 中有 Docker，名为 `docker`，但是不建议使用系统源中的这个版本，它的版本相对比较陈旧，而且并非 Docker 官方维护的版本。因此，我们需要使用 Docker 官方提供的 CentOS 软件源。

执行下面的命令添加 `yum` 软件源。

```bash
$ sudo tee /etc/yum.repos.d/docker.repo <<-'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF
```

#### 安装 Docker

更新 `yum` 软件源缓存，并安装 `docker-engine`。

```bash
$ sudo yum update
$ sudo yum install docker-engine
```

#### 启动 Docker 引擎

```bash
$ sudo systemctl enable docker
$ sudo systemctl start docker
```

#### 建立 docker 用户组

默认情况下，`docker` 命令会使用 [Unix socket](https://en.wikipedia.org/wiki/Unix_domain_socket) 与 Docker 引擎通讯。而只有 `root` 用户和 `docker` 组的用户才可以访问 Docker 引擎的 Unix socket。出于安全考虑，一般 Linux 系统上不会直接使用 `root` 用户。因此，更好地做法是将需要使用 `docker` 的用户加入 `docker` 用户组。

建立 `docker` 组：

```bash
$ sudo groupadd docker
```

将当前用户加入 `docker` 组：

```bash
$ sudo usermod -aG docker $USER
```

### 参考文档

参见 [Docker 官方 CentOS 安装文档](https://docs.docker.com/engine/installation/linux/centos/)。
