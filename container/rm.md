## 删除容器
可以使用 `docker rm` 来删除一个处于终止状态的容器。例如
```bash
$ docker rm  trusting_newton
trusting_newton
```
如果要删除一个运行中的容器，可以添加 `-f` 参数。Docker 会发送 `SIGKILL` 信号给容器。

## 清理所有处于终止状态的容器

用 `docker ps -a` 命令可以查看所有已经创建的包括终止状态的容器，如果数量太多要一个个删除可能会很麻烦，用 `docker container prune` 可以清理掉所有处于终止状态的容器。

## Docker 1.13+

在 Docker 1.13+ 版本中推荐使用 `docker container` 来管理容器。

```bash
$ docker container rm trusting_newton

$ docker container prune
```
