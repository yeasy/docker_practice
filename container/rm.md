# 删除容器

可以使用 `docker container rm` 来删除一个处于终止状态的容器。例如

```bash
$ docker container rm trusting_newton
trusting_newton
```

如果要删除一个运行中的容器，可以添加 `-f` 参数。Docker 会发送 `SIGKILL` 信号给容器。

# 清理所有处于终止状态的容器

用 `docker container ls -a` 命令可以查看所有已经创建的包括终止状态的容器，如果数量太多要一个个删除可能会很麻烦，用下面的命令可以清理掉所有处于终止状态的容器。

```bash
$ docker container prune
```

# 批量删除所有已经退出的容器
```bash
$ docker rm -v $(docker ps -aq -f status=exited)
```

# unpause容器
有时我们只是希望让容器暂停工作一段时间，比如要对容器的文件系统打个快照，或者docker host需要使用CPU，可以执行:docker pause CONTAINER [CONTAINER...]，如图所示：
    ```bash
        $ docker pause bdf593fda8be
            bdf593fda8be
        $ docker ps
        CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                  PORTS               NAMES
        bdf593fda8be        ubuntu:15.10        "/bin/bash"         3 minutes ago       Up 3 minutes (Paused)                       cranky_mclaren                  
    ```
    
