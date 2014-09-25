##进入容器
进入容器有很多方法，其中docker自带的有个命令为`docker attach`。
当你多个窗口同时attach到一个容器的时候，你在一个窗口执行命令其他窗口都能同步显示，当某个命令阻塞之后,那么你就无法进入容器，执行命令操作了。

很多同学都会想到ssh，ssh这里不做介绍了。

推建大家使用下面的方法：
###nsenter
从util-linux版本2.23开始，nsenter工具就包含在其中。它用来访问另一个进程的名字空间。nsenter要正常工作需要有root权限。
很不幸，Ubuntu 14.4仍然使用的是util-linux版本2.20。安装最新版本的util-linux（2.24)版，请按照以下步骤：
```
#curl https://www.kernel.org/pub/linux/utils/util-linux/v2.24/util-linux-2.24.tar.gz | tar -zxf-
#cd util-linux-2.24
#./configure --without-ncurses
#make nsenter
#sudo cp nsenter /usr/local/bin
```
为了连接到容器，你还需要找到容器的第一个进程的PID。
```
docker inspect --format "{{ .State.Pid }}" <container-id>
```
通过这个PID，你就可以连接到这个容器：
```
nsenter --target $PID --mount --uts --ipc --net --pid
```
