# Docker命令查询

##基本语法
    docker [OPTIONS] COMMAND [arg...]
一般来说，docker命令可以用来管理daemon，或者通过CLI命令管理镜像和容器。可以通过`man docker`来查看这些命令。


##选项
    -D=true|false
        使用debug模式。默认为false。

    -H, --host=[unix:///var/run/docker.sock]: tcp://[host:port]来绑定或者unix://[/path/to/socket]来使用。
        在daemon模式下绑定的socket，通过一个或多个tcp://host:port, unix:///path/to/socket, fd://* or fd://socketfd来指定。

    --api-enable-cors=true|false
        在远端API中启用CORS头。缺省为false。

    -b=""
        将容器挂载到一个已存在的网桥上。指定为'none'时则禁用容器的网络。

    --bip=""
        让动态创建的docker0采用给定的CIDR地址; 与-b选项互斥。

    -d=true|false
        使用daemon模式。缺省为false。

    --dns=""
        让Docker使用给定的DNS服务器。

    -g=""
        指定Docker运行时的root路径。缺省为/var/lib/docker。

    --icc=true|false
        启用容器间通信。默认为true。

    --ip=""
        绑定端口时候的默认IP地址。缺省为0.0.0.0。

    --iptables=true|false
        禁止Docker添加iptables规则。缺省为true。

    --mtu=VALUE
        指定容器网络的mtu。缺省为1500。

    -p=""
        指定daemon的PID文件路径。缺省为/var/run/docker.pid。

    -s=""
        强制Docker运行时使用给定的存储驱动。

    -v=true|false
        输出版本信息并退出。缺省值为false。

    --selinux-enabled=true|false
        启用SELinux支持。缺省值为false。SELinux目前不支持BTRFS存储驱动。


##命令
docker的命令可以采用`docker-CMD`或者`docker CMD`的方式执行。两者一致。

    docker-attach(1)
        依附到一个正在运行的容器中。

    docker-build(1)
        从一个Dockerfile创建一个镜像

    docker-commit(1)
        从一个容器的修改中创建一个新的镜像

    docker-cp(1)
        从容器中复制文件到宿主系统中

    docker-diff(1)
        检查一个容器文件系统的修改

    docker-events(1)
        从服务端获取实时的事件

    docker-export(1)
        导出容器内容为一个tar包

    docker-history(1)
        显示一个镜像的历史

    docker-images(1)
        列出存在的镜像

    docker-import(1)
        导入一个文件（典型为tar包）路径或目录来创建一个镜像

    docker-info(1)
        显示一些相关的系统信息

    docker-inspect(1)
        显示一个容器的底层具体信息。

    docker-kill(1)
        关闭一个运行中的容器 (包括进程和所有资源)

    docker-load(1)
        从一个tar包中加载一个镜像

    docker-login(1)
        注册或登录到一个Docker的仓库服务器

    docker-logout(1)
        从Docker的仓库服务器登出

    docker-logs(1)
        获取容器的log信息

    docker-pause(1)
        暂停一个容器中的所有进程

    docker-port(1)
        查找一个nat到一个私有网口的公共口

    docker-ps(1)
        列出容器

    docker-pull(1)
        从一个Docker的仓库服务器下拉一个镜像或仓库

    docker-push(1)
        将一个镜像或者仓库推送到一个Docker的注册服务器

    docker-restart(1)
        重启一个运行中的容器

    docker-rm(1)
        删除给定的若干个容器

    docker-rmi(1)
        删除给定的若干个镜像

    docker-run(1)
        创建一个新容器，并在其中运行给定命令

    docker-save(1)
        保存一个镜像为tar包文件

    docker-search(1)
        在Docker index中搜索一个镜像

    docker-start(1)
        启动一个容器

    docker-stop(1)
        终止一个运行中的容器

    docker-tag(1)
        为一个image打标签

    docker-top(1)
        查看一个容器中的正在运行的进程信息

    docker-unpause(1)
        将一个容器内所有的进程从暂停状态中恢复

    docker-version(1)
        输出Docker的版本信息

    docker-wait(1)
        阻塞直到一个容器终止，然后输出它的退出符

##一张图总结Docker的命令

![命令周期](../_images/cmd_logic.png)
