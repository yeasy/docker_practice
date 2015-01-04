##安装 Fig

首先，安装 1.3 或者更新的 Docker 版本。

如果你的工作环境是 OS X ，可以通过查看 [Mac 安装指南(英文)](https://docs.docker.com/installation/mac/) ，完成安装 Docker 和 boot2docker 。一旦 boot2docker 运行后，执行以下指令设置一个环境变量，接着 Fig 就可以和它交互了。

```
$(boot2docker shellinit)
```
**如果想避免重启后重新设置，可以把上面的命令加到你的 ` ~/.bashrc` 文件里。*

关于 `Ubuntu` 还有 `其它的平台` 的安装，可以参照 [Ubuntu 安装指南(中文)](../install/ubuntu.md) 以及 [官方安装手册(英文)](https://docs.docker.com/installation/)。


下一步，安装 Fig ： 

```
curl -L https://github.com/docker/fig/releases/download/1.0.1/fig-`uname -s`-`uname -m` > /usr/local/bin/fig; chmod +x /usr/local/bin/fig
```
**如果你的 Docker 是管理员身份安装，以上命令可能也需要相同的身份。*  

目前 Fig 的发行版本只支持 OSX 和 64 位的 Linux 系统。但因为它是用 Python 语言写的，所以对于其它平台上的用户，可以通过 Python 安装包来完成安装（支持的系统同样适用）。

```
$ sudo pip install -U fig
```
到这里就已经完成了。 执行 `fig --version` ，确认能够正常运行。

