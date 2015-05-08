##Fig客户端参考

大部分命令都可以运行在一个或多个服务上。如果没有特别的说明，这个命令则可以应用在所有的服务上。

执行 `fig [COMMAND] --help` 查看所有的使用说明。

###选项

`--verbose`

显示更多信息。

`--version`

打印版本并退出。

`-f, --file FILE`

使用特定的Fig文件，默认使用fig.yml。

`-p, --project-name NAME`

使用特定的项目名称，默认使用文件夹名称。

###命令

`build`

构建或重新构建服务。

服务一旦构建后，将会标记为project_service，例如figtest_db。
如果修改服务的 `Dockerfile` 或构建目录信息，你可以运行 `fig build` 来重新构建。

`help`

获得一个命令的帮助。

`kill`

强制停止服务容器。

`logs`

查看服务的输出。

`port`

打印端口绑定的公共端口。

`ps`

列出所有容器。

`pull`

拉取服务镜像。

`rm`

删除停止的服务容器。

`run`

在一个服务上执行一个命令。

例如：

```
$ fig run web python manage.py shell
```

默认情况下，链接的服务将会启动，除非这些服务已经在运行中。

一次性命令会在使用与服务的普通容器相同的配置的新容器中开始运行，然后卷、链接等等都将会按照期望创建。
与普通容器唯一的不同就是，这个命令将会覆盖原有的命令，如果端口有冲突则不会创建。

链接还可以在一次性命令和那个服务的其他容器间创建，然后你可以像下面一样进行一些操作：

```
$ fig run db psql -h db -U docker
```

如果你不希望在执行一次性命令时启动链接的容器，可以指定--no-deps选项：

```
$ fig run --no-deps web python manage.py shell
```

`scale`

设置一个服务需要运行的容器个数。

通过service=num的参数来设置数量。例如：

```
$ fig scale web=2 worker=3
```

`start`

启动一个服务已经存在的容器.

`stop`

停止一个已经运行的容器，但不删除它。通过 `fig start` 可以再次启动这些容器。

`up`

构建，（重新）创建，启动，链接一个服务的容器。

链接的服务都将会启动，除非他们已经运行。

默认情况， `fig up` 将会聚合每个容器的输出，而且如果容器已经存在，所有容器将会停止。如果你运行 `fig up -d` ，将会在后台启动并运行所有的容器。

默认情况，如果这个服务的容器已经存在， `fig up` 将会停止并重新创建他们（保持使用volumes-from挂载的卷），以保证 `fig.yml` 的修改生效。如果你不想容器被停止并重新创建，可以使用 `fig up --no-recreate` 。如果需要的话，这样将会启动已经停止的容器。

###环境变量

环境变量可以用来配置Fig的行为。

变量以DOCKER_开头，它们和用来配置Docker命令行客户端的使用一样。如果你在使用 boot2docker , `$(boot2docker shellinit)` 将会设置它们为正确的值。

`FIG_PROJECT_NAME`

设置通过Fig启动的每一个容器前添加的项目名称.默认是当前工作目录的名字。

`FIG_FILE`

设置要使用的 `fig.yml` 的路径。默认路径是当前工作目录。

`DOCKER_HOST`

设置docker进程的URL。默认docker client使用 `unix:///var/run/docker.sock` 。

`DOCKER_TLS_VERIFY`

如果设置不为空的字符，允许和进程进行 TLS 通信。

`DOCKER_CERT_PATH`

配置 `ca.pem` 的路径， `cert.pem` 和 `key.pem` 文件用来进行TLS验证.默认路径是 `~/.docker` 。
