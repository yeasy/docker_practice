# 客户端命令(docker)

## 客户端命令选项

* `--config=""`：指定客户端配置文件，默认为 `~/.docker`；
* `-D=true|false`：是否使用 debug 模式。默认不开启；
* `-H, --host=[]`：指定命令对应 Docker 守护进程的监听接口，可以为 unix 套接字 `unix:///path/to/socket`，文件句柄 `fd://socketfd` 或 tcp 套接字 `tcp://[host[:port]]`，默认为 `unix:///var/run/docker.sock`；
* `-l, --log-level="debug|info|warn|error|fatal"`：指定日志输出级别；
* `--tls=true|false`：是否对 Docker 守护进程启用 TLS 安全机制，默认为否；
* `--tlscacert=/.docker/ca.pem`：TLS CA 签名的可信证书文件路径；
* `--tlscert=/.docker/cert.pem`：TLS 可信证书文件路径；
* `--tlscert=/.docker/key.pem`：TLS 密钥文件路径；
* `--tlsverify=true|false`：启用 TLS 校验，默认为否。

## 客户端命令

可以通过 `docker COMMAND --help` 来查看这些命令的具体用法。

* `attach`：依附到一个正在运行的容器中；
* `build`：从一个 Dockerfile 创建一个镜像；
* `commit`：从一个容器的修改中创建一个新的镜像；
* `cp`：在容器和本地宿主系统之间复制文件中；
* `create`：创建一个新容器，但并不运行它；
* `diff`：检查一个容器内文件系统的修改，包括修改和增加；
* `events`：从服务端获取实时的事件；
* `exec`：在运行的容器内执行命令；
* `export`：导出容器内容为一个 `tar` 包；
* `history`：显示一个镜像的历史信息；
* `images`：列出存在的镜像；
* `import`：导入一个文件（典型为 `tar` 包）路径或目录来创建一个本地镜像；
* `info`：显示一些相关的系统信息；
* `inspect`：显示一个容器的具体配置信息；
* `kill`：关闭一个运行中的容器 (包括进程和所有相关资源)；
* `load`：从一个 tar 包中加载一个镜像；
* `login`：注册或登录到一个 Docker 的仓库服务器；
* `logout`：从 Docker 的仓库服务器登出；
* `logs`：获取容器的 log 信息；
* `network`：管理 Docker 的网络，包括查看、创建、删除、挂载、卸载等；
* `node`：管理 swarm 集群中的节点，包括查看、更新、删除、提升/取消管理节点等；
* `pause`：暂停一个容器中的所有进程；
* `port`：查找一个 nat 到一个私有网口的公共口；
* `ps`：列出主机上的容器；
* `pull`：从一个Docker的仓库服务器下拉一个镜像或仓库；
* `push`：将一个镜像或者仓库推送到一个 Docker 的注册服务器；
* `rename`：重命名一个容器；
* `restart`：重启一个运行中的容器；
* `rm`：删除给定的若干个容器；
* `rmi`：删除给定的若干个镜像；
* `run`：创建一个新容器，并在其中运行给定命令；
* `save`：保存一个镜像为 tar 包文件；
* `search`：在 Docker index 中搜索一个镜像；
* `service`：管理 Docker 所启动的应用服务，包括创建、更新、删除等；
* `start`：启动一个容器；
* `stats`：输出（一个或多个）容器的资源使用统计信息；
* `stop`：终止一个运行中的容器；
* `swarm`：管理 Docker swarm 集群，包括创建、加入、退出、更新等；
* `tag`：为一个镜像打标签；
* `top`：查看一个容器中的正在运行的进程信息；
* `unpause`：将一个容器内所有的进程从暂停状态中恢复；
* `update`：更新指定的若干容器的配置信息；
* `version`：输出 Docker 的版本信息；
* `volume`：管理 Docker volume，包括查看、创建、删除等；
* `wait`：阻塞直到一个容器终止，然后输出它的退出符。

## 一张图总结 Docker 的命令
![Docker 命令总结](../_images/cmd_logic.png)

## 参考

* [官方文档](https://docs.docker.com/engine/reference/commandline/cli/)
