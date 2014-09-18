## 编辑网络配置文件

Docker 1.2.0开始支持在运行中的容器里编辑`/etc/hosts`, `/etc/hostname`和`/etc/resolve.conf`文件。

但是这些修改是临时的，只在运行的容器中保留，容器终止或重启后并不会被保存下来。也不会被`docker commit`提交。
