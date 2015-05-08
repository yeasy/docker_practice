## Compose 命令说明

大部分命令都可以运行在一个或多个服务上。如果没有特别的说明，命令则应用在项目所有的服务上。

执行 `docker-compose [COMMAND] --help` 查看具体某个命令的使用说明。

基本的使用格式是
```sh
docker-compose [options] [COMMAND] [ARGS...]
```

## 选项

* `--verbose` 输出更多调试信息。
* `--version` 打印版本并退出。
* `-f, --file FILE` 使用特定的 compose 模板文件，默认为 `docker-compose.yml`。
* `-p, --project-name NAME` 指定项目名称，默认使用目录名称。

## 命令

### `build`

构建或重新构建服务。

服务一旦构建后，将会带上一个标记名，例如 web_db。

可以随时在项目目录下运行 `docker-compose build` 来重新构建服务。

### `help`

获得一个命令的帮助。

### `kill`

通过发送 `SIGKILL` 信号来强制停止服务容器。支持通过参数来指定发送的信号，例如
```sh
$ docker-compose kill -s SIGINT
```

### `logs`

查看服务的输出。

### `port`

打印绑定的公共端口。

### `ps`

列出所有容器。

### `pull`

拉取服务镜像。

### `rm`

删除停止的服务容器。

### `run`

在一个服务上执行一个命令。

例如：

```
$ docker-compose run ubuntu ping docker.com
```

将会启动一个 ubuntu 服务，执行 `ping docker.com` 命令。

默认情况下，所有关联的服务将会自动被启动，除非这些服务已经在运行中。

该命令类似启动容器后运行指定的命令，相关卷、链接等等都将会按照期望创建。

两个不同点：
* 给定命令将会覆盖原有的自动运行命令；
* 不会自动创建端口，以避免冲突。

如果不希望自动启动关联的容器，可以使用 `--no-deps` 选项，例如

```
$ docker-compose run --no-deps web python manage.py shell
```

将不会启动 web 容器所关联的其它容器。

### `scale`

设置同一个服务运行的容器个数。

通过 `service=num` 的参数来设置数量。例如：

```
$ docker-compose scale web=2 worker=3
```

### `start`

启动一个已经存在的服务容器。

### `stop`

停止一个已经运行的容器，但不删除它。通过 `docker-compose start` 可以再次启动这些容器。

### `up`

构建，（重新）创建，启动，链接一个服务相关的容器。

链接的服务都将会启动，除非他们已经运行。

默认情况， `docker-compose up` 将会整合所有容器的输出，并且退出时，所有容器将会停止。

如果使用 `docker-compose up -d` ，将会在后台启动并运行所有的容器。

默认情况，如果该服务的容器已经存在， `docker-compose up` 将会停止并尝试重新创建他们（保持使用 `volumes-from` 挂载的卷），以保证 `docker-compose.yml` 的修改生效。如果你不想容器被停止并重新创建，可以使用 `docker-compose up --no-recreate`。如果需要的话，这样将会启动已经停止的容器。

## 环境变量

环境变量可以用来配置 Compose 的行为。

以`DOCKER_`开头的变量和用来配置 Docker 命令行客户端的使用一样。如果使用 boot2docker , `$(boot2docker shellinit)` 将会设置它们为正确的值。

### `COMPOSE_PROJECT_NAME`

设置通过 Compose 启动的每一个容器前添加的项目名称，默认是当前工作目录的名字。

### `COMPOSE_FILE`

设置要使用的 `docker-compose.yml` 的路径。默认路径是当前工作目录。

### `DOCKER_HOST`

设置 Docker daemon 的地址。默认使用 `unix:///var/run/docker.sock`，与 Docker 客户端采用的默认值一致。

### `DOCKER_TLS_VERIFY`

如果设置不为空，则与 Docker daemon 交互通过 TLS 进行。

### `DOCKER_CERT_PATH`

配置 TLS 通信所需要的验证（`ca.pem`、`cert.pem` 和 `key.pem`）文件的路径，默认是 `~/.docker` 。
