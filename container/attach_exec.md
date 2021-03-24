# 进入容器

在使用 `-d` 参数时，容器启动后会进入后台，启动完容器之后会停在host端；

某些时候需要进入容器进行操作，包括使用 `docker attach` 命令或 `docker exec` 命令，推荐大家使用 `docker exec` 命令，原因会在下面说明。

## `attach` 命令

下面示例如何使用 `docker attach` 命令。

```bash
$ docker run -dit ubuntu
243c32535da7d142fb0e6df616a3c3ada0b8ab417937c853a9e1c251f499f550

$ docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
243c32535da7        ubuntu:latest       "/bin/bash"         18 seconds ago      Up 17 seconds                           nostalgic_hypatia

$ docker attach 243c
root@243c32535da7:/#
```

*注意：* 如果从这个 stdin 中exit回到host端，会导致容器的停止。

## `exec` 命令

### `-i` `-t` 参数

`docker exec` 后边可以跟多个参数，这里主要说明 `-i` `-t` 参数。

只用 `-i` 参数时，由于没有分配伪终端，界面没有我们熟悉的 Linux 命令提示符，但命令执行结果仍然可以返回。

当 `-i` `-t` 参数一起使用时，则可以看到我们熟悉的 Linux 命令提示符。

```bash
$ docker run -dit ubuntu
69d137adef7a8a689cbcb059e94da5489d3cddd240ff675c640c8d96e84fe1f6

$ docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
69d137adef7a        ubuntu:latest       "/bin/bash"         18 seconds ago      Up 17 seconds                           zealous_swirles

$ docker exec -i 69d1 bash
ls
bin
boot
dev
...

$ docker exec -it 69d1 bash
root@69d137adef7a:/#
```

如果从这个 stdin 中 exit回到host端，但不会导致容器的停止。这就是为什么推荐大家使用 `docker exec` 的原因。


## attach和exec的区别
 attach和exec的区别：
（1）attach直接进入容器启动命令的终端，不会启动新的进程；
（2）exec则是在容器中打开新的终端，并且可以启动新的进程；
（3）如果想直接在终端中查看命令的输出，用attach，其他情况使用exec；

更多参数说明请使用 `docker exec --help` 查看。
