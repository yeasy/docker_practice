## 安装
Docker Machine 可以在多种操作系统平台上安装，包括 Linux、Mac OS，以及 Windows。


### Linux/Mac OS
在 Linux/Mac OS 上的安装十分简单，推荐从 [官方 Release 库](https://github.com/docker/machine/releases) 直接下载编译好的二进制文件即可。

例如，在 Linux 64 位系统上直接下载对应的二进制包。
```bash
$ sudo curl -L https://github.com/docker/machine/releases/download/v0.3.1-rc1/docker-machine_linux-amd64 > /usr/local/bin/docker-machine
$ chmod +x /usr/local/bin/docker-machine
```

完成后，查看版本信息，验证运行正常。
```bash
$ docker-machine -v
docker-machine version 0.3.1-rc1 (993f2db)
```

### Windows
Windows 下面要复杂一些，首先需要安装 [msysgit](https://msysgit.github.io/)。

msysgit 是 Windows 下的 git 客户端软件包，会提供类似 Linux 下的一些基本的工具，例如 ssh 等。

安装之后，启动 msysgit 的命令行界面，仍然通过下载二进制包进行安装，需要下载 docker 客户端和 docker-machine。

```bash
$ curl -L https://get.docker.com/builds/Windows/x86_64/docker-latest.exe > /bin/docker

$ curl -L https://github.com/docker/machine/releases/download/v0.3.1-rc1/docker-machine_windows-amd64.exe > /bin/docker-machine
```
