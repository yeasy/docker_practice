## 安装

安装 Compose 之前，要先安装 Docker，在此不再赘述。

### PIP 安装
这种方式最为推荐。

执行命令。
```sh
$ sudo pip install -U docker-compose
```

安装成功后，可以查看 `docker-compose` 命令的用法。
```sh
$ docker-compose -h
Fast, isolated development environments using Docker.

Usage:
  docker-compose [options] [COMMAND] [ARGS...]
  docker-compose -h|--help

Options:
  --verbose                 Show more output
  --version                 Print version and exit
  -f, --file FILE           Specify an alternate compose file (default: docker-compose.yml)
  -p, --project-name NAME   Specify an alternate project name (default: directory name)

Commands:
  build     Build or rebuild services
  help      Get help on a command
  kill      Kill containers
  logs      View output from containers
  port      Print the public port for a port binding
  ps        List containers
  pull      Pulls service images
  rm        Remove stopped containers
  run       Run a one-off command
  scale     Set number of containers for a service
  start     Start services
  stop      Stop services
  restart   Restart services
  up        Create and start containers
```

之后，可以添加 bash 补全命令。
```sh
$ curl -L https://raw.githubusercontent.com/docker/compose/1.2.0/contrib/completion/bash/docker-compose > /etc/bash_completion.d/docker-compose

```

### 二进制包
发布的二进制包可以在 [https://github.com/docker/compose/releases](https://github.com/docker/compose/releases) 找到。

下载后直接放到执行路径即可。

例如，在常见的 Linux 平台上。

```
$ sudo curl -L https://github.com/docker/compose/releases/download/1.2.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
$ sudo chmod a+x /usr/local/bin/docker-compose
```


