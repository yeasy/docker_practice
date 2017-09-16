## Windows 10 PC 安装 Docker CE

### 系统要求

Docker CE 支持 64 位版本的 Windows 10 Pro，且必须开启 Hyper-V。

### 安装

点击以下链接下载 [stable](https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe) 或 [edge](https://download.docker.com/win/edge/Docker%20for%20Windows%20Installer.exe) 版本的 Docker CE。

下载好之后双击 Docker for Windows Installer.exe 开始安装。

### 运行

在 Windows 搜索栏 输入 Docker 点击 Docker for Windows 开始运行。

![](_images/install-win-docker-app-search.png)

Docker CE 启动之后会在 Windows 任务栏出现鲸鱼图标。

![](_images/install-win-taskbar-circle.png)

等待片刻，点击 Got it 开始使用 Docker CE。

![](_images/install-win-success-popup-cloud.png)

### 镜像加速

鉴于国内网络问题，后续拉取 Docker 镜像十分缓慢，强烈建议安装 Docker 之后配置 [国内镜像加速](mirror.md)。

### 参考文档

* [Docker 官方 Windows PC 安装文档](https://docs.docker.com/docker-for-windows/install/)
