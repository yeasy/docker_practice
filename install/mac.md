## macOS 安装 Docker

### 系统要求

[Docker for Mac](https://docs.docker.com/docker-for-mac/) 要求系统最低为 macOS 10.10.3 Yosemite，或者 2010 年以后的 Mac 机型，准确说是带 [Intel MMU 虚拟化](https://en.wikipedia.org/wiki/X86_virtualization#Intel-VT-d)的，最低 4GB 内存。

如果系统不满足需求，可以安装 [Docker Toolbox](https://docs.docker.com/toolbox/overview/)。

### 安装

#### 使用 Homebrew 安装

[Homebrew](http://brew.sh/) 的 [Cask](https://caskroom.github.io/) 已经支持 Docker for Mac，因此可以很方便的使用 Homebrew Cask 来进行安装：

```bash
$ brew cask install docker
```

#### 手动下载安装

如果需要手动下载，可以通过这个链接下载：<https://download.docker.com/mac/stable/Docker.dmg>

如同 macOS 其它软件一样，安装也非常简单，双击下载的 `.dmg` 文件，然后将那只叫 [Moby](https://blog.docker.com/2013/10/call-me-moby-dock/) 的鲸鱼图标拖拽到 `Application` 文件夹即可（其间需要输入用户密码）。

<img src="_images/install-mac-dmg.png" width="80%" >

### 运行

从应用中找到 Docker 图标并点击运行。

<img src="_images/install-mac-apps.png" width="80%" >

运行之后，会在右上角菜单栏看到多了一个鲸鱼图标，这个图标表明了 Docker 的运行状态。

<img src="_images/install-mac-menubar.png" width="60%">

第一次点击图标，可能会看到这个安装成功的界面，点击 "Got it!" 可以关闭这个窗口。

<img src="_images/install-mac-success.png" width="40%">

以后每次点击鲸鱼图标会弹出操作菜单。

<img src="_images/install-mac-menu.png" width="40%">

*在国内使用 Docker 的话，需要配置加速器，在菜单中点击 `Preferences...`，然后查看 `Advanced` 标签，在其中的 `Registry mirrors` 部分里可以点击加号来添加加速器地址。*

<img src="_images/install-mac-preference-advanced.png" width="60%">

启动终端后，通过命令可以检查安装后的 Docker 版本。

```bash
$ docker --version
Docker version 17.10.0-ce, build f4ffd25
$ docker-compose --version
docker-compose version 1.17.0-rc1, build a0f95af
$ docker-machine --version
docker-machine version 0.13.0, build 9ba6da9
```

如果 `docker version`、`docker info` 都正常的话，可以运行一个 [Nginx 服务器](https://hub.docker.com/_/nginx/)：

```bash
$ docker run -d -p 80:80 --name webserver nginx
```

服务运行后，可以访问 <http://localhost>，如果看到了 "Welcome to nginx!"，就说明 Docker for Mac 安装成功了。

<img src="_images/install-mac-example-nginx.png" width="80%">

要停止 Nginx 服务器并删除执行下面的命令：

```bash
$ docker stop webserver
$ docker rm webserver
```

### 参考文档

* [Docker 官方 macOS 安装文档](https://docs.docker.com/docker-for-mac/install/)
