## Compose 模板文件

模板文件是使用 Compose 的核心，涉及到的指令关键字也比较多。但大家不用担心，这里面大部分指令跟 `docker run` 相关参数的含义都是类似的。

默认的模板文件名称为 `docker-compose.yml`，格式为 YAML 格式。

在旧版本（版本 1）中，其中每个顶级元素为服务名称，次级元素为服务容器的配置信息，例如

```yaml
webapp:
  image: examples/web
  ports:
    - "80:80"
  volumes:
    - "/data"
```

版本 2 扩展了 Compose 的语法，同时尽量保持跟版本 1 的兼容，除了可以声明网络和存储信息外，最大的不同一是添加了版本信息，另一个是需要将所有的服务放到 `services` 根下面。

例如，上面例子改写为版本 2，内容为

```yaml
version: "2"
services:
  webapp:
    image: examples/web
    ports:
      - "80:80"
    volumes:
      - "/data"
```


注意每个服务都必须通过 `image` 指令指定镜像或 `build` 指令（需要 Dockerfile）等来自动构建生成镜像。

如果使用 `build` 指令，在 `Dockerfile` 中设置的选项(例如：`CMD`, `EXPOSE`, `VOLUME`, `ENV` 等) 将会自动被获取，无需在 `docker-compose.yml` 中再次设置。

下面分别介绍各个指令的用法。

### `build`

指定 `Dockerfile` 所在文件夹的路径（可以是绝对路径，或者相对 docker-compose.yml 文件的路径）。 `Compose` 将会利用它自动构建这个镜像，然后使用这个镜像。

```
build: /path/to/build/dir
```

### `cap_add, cap_drop`
指定容器的内核能力（capacity）分配。

例如，让容器拥有所有能力可以指定为：

```yml
cap_add:
  - ALL
```

去掉 NET_ADMIN 能力可以指定为：

```yml
cap_drop:
  - NET_ADMIN
```

### `command`

覆盖容器启动后默认执行的命令。

```bash
command: echo "hello world"
```

### `cgroup_parent`
指定父 cgroup 组，意味着将继承该组的资源限制。

例如，创建了一个 cgroup 组名称为 `cgroups_1`。

```yml
cgroup_parent: cgroups_1
```

### `container_name`
指定容器名称。默认将会使用 `项目名称_服务名称_序号` 这样的格式。

例如：
```yml
container_name: docker-web-container
```

需要注意，指定容器名称后，该服务将无法进行扩展（scale），因为 Docker 不允许多个容器具有相同的名称。

### `devices`
指定设备映射关系。

例如：
```yml
devices:
  - "/dev/ttyUSB1:/dev/ttyUSB0"
```

### `dns`

自定义 DNS 服务器。可以是一个值，也可以是一个列表。

```bash
dns: 8.8.8.8
dns:
  - 8.8.8.8
  - 9.9.9.9
```

### `dns_search`

配置 DNS 搜索域。可以是一个值，也可以是一个列表。

```bash
dns_search: example.com
dns_search:
  - domain1.example.com
  - domain2.example.com
```

### `dockerfile`
如果需要指定额外的编译镜像的 Dockefile 文件，可以通过该指令来指定。

例如
```yml
dockerfile: Dockerfile-alternate
```

注意，该指令不能跟 `image` 同时使用，否则 Compose 将不知道根据哪个指令来生成最终的服务镜像。

### `env_file`
从文件中获取环境变量，可以为单独的文件路径或列表。

如果通过 `docker-compose -f FILE` 方式来指定 Compose 模板文件，则 `env_file` 中变量的路径会基于模板文件路径。

如果有变量名称与 `environment` 指令冲突，则按照惯例，以后者为准。

```bash
env_file: .env

env_file:
  - ./common.env
  - ./apps/web.env
  - /opt/secrets.env
```

环境变量文件中每一行必须符合格式，支持 `#` 开头的注释行。

```bash
# common.env: Set development environment
PROG_ENV=development
```

### `environment`

设置环境变量。你可以使用数组或字典两种格式。

只给定名称的变量会自动获取运行 Compose 主机上对应变量的值，可以用来防止泄露不必要的数据。

例如
```yml
environment:
  RACK_ENV: development
  SESSION_SECRET:
```

或者

```yml
environment:
  - RACK_ENV=development
  - SESSION_SECRET
```

注意，如果变量名称或者值中用到 `true|false，yes|no` 等表达布尔含义的词汇，最好放到引号里，避免 YAML 自动解析某些内容为对应的布尔语义。

`http://yaml.org/type/bool.html` 中给出了这些特定词汇，包括

```bash
 y|Y|yes|Yes|YES|n|N|no|No|NO
|true|True|TRUE|false|False|FALSE
|on|On|ON|off|Off|OFF
```

### `expose`

暴露端口，但不映射到宿主机，只被连接的服务访问。

仅可以指定内部端口为参数

```bash
expose:
 - "3000"
 - "8000"
```

### `extends`
基于其它模板文件进行扩展。

例如我们已经有了一个 webapp 服务，定义一个基础模板文件为 `common.yml`。
```bash
# common.yml
webapp:
  build: ./webapp
  environment:
    - DEBUG=false
    - SEND_EMAILS=false
```

再编写一个新的 `development.yml` 文件，使用 `common.yml` 中的 webapp 服务进行扩展。
```bash
# development.yml
web:
  extends:
    file: common.yml
    service: webapp
  ports:
    - "8000:8000"
  links:
    - db
  environment:
    - DEBUG=true
db:
  image: postgres
```
后者会自动继承 common.yml 中的 webapp 服务及环境变量定义。

使用 extends 需要注意：

* 要避免出现循环依赖，例如 `A 依赖 B，B 依赖 C，C 反过来依赖 A` 的情况。
* extends 不会继承 links 和 volumes_from 中定义的容器和数据卷资源。

一般的，推荐在基础模板中只定义一些可以共享的镜像和环境变量，在扩展模板中具体指定应用变量、链接、数据卷等信息。

### `external_links`
链接到 docker-compose.yml 外部的容器，甚至 并非 `Compose` 管理的外部容器。参数格式跟 `links` 类似。

```
external_links:
 - redis_1
 - project_db_1:mysql
 - project_db_1:postgresql
```

### `extra_hosts`
类似 Docker 中的 `--add-host` 参数，指定额外的 host 名称映射信息。

例如：
```yml
extra_hosts:
 - "googledns:8.8.8.8"
 - "dockerhub:52.1.157.61"
```

会在启动后的服务容器中 `/etc/hosts` 文件中添加如下两条条目。
```bash
8.8.8.8 googledns
52.1.157.61 dockerhub
```

### `image`

指定为镜像名称或镜像 ID。如果镜像在本地不存在，`Compose` 将会尝试拉去这个镜像。

例如：
```bash
image: ubuntu
image: orchardup/postgresql
image: a4bc65fd
```

### `labels`
为容器添加 Docker 元数据（metadata）信息。例如可以为容器添加辅助说明信息。
```yml
labels:
  com.startupteam.description: "webapp for a startup team"
  com.startupteam.department: "devops department"
  com.startupteam.release: "rc3 for v1.0"
```

### `links`

链接到其它服务中的容器。使用服务名称（同时作为别名）或服务名称：服务别名 `（SERVICE:ALIAS）` 格式都可以。

```bash
links:
 - db
 - db:database
 - redis
```

使用的别名将会自动在服务容器中的 `/etc/hosts` 里创建。例如：

```bash
172.17.2.186  db
172.17.2.186  database
172.17.2.187  redis
```

被链接容器中相应的环境变量也将被创建。

### `log_driver`
类似 Docker 中的 `--log-driver` 参数，指定日志驱动类型。

目前支持三种日志驱动类型。

```yml
log_driver: "json-file"
log_driver: "syslog"
log_driver: "none"
```

### `log_opt`
日志驱动的相关参数。

例如
```yml
log_driver: "syslog"
log_opt:
  syslog-address: "tcp://192.168.0.42:123"
```

### `net`

设置网络模式。使用和 `docker client` 的 `--net` 参数一样的值。

```bash
net: "bridge"
net: "none"
net: "container:[name or id]"
net: "host"
```

### `pid`
跟主机系统共享进程命名空间。打开该选项的容器之间，以及容器和宿主机系统之间可以通过进程 ID 来相互访问和操作。

```bash
pid: "host"
```


### `ports`

暴露端口信息。

使用宿主：容器 `（HOST:CONTAINER）`格式，或者仅仅指定容器的端口（宿主将会随机选择端口）都可以。

```
ports:
 - "3000"
 - "8000:8000"
 - "49100:22"
 - "127.0.0.1:8001:8001"
```

*注意：当使用 `HOST:CONTAINER` 格式来映射端口时，如果你使用的容器端口小于 60 并且没放到引号里，可能会得到错误结果，因为 `YAML` 会自动解析 `xx:yy` 这种数字格式为 60 进制。为避免出现这种问题，建议数字串都采用引号包括起来的字符串格式。*

### `security_opt`

指定容器模板标签（label）机制的默认属性（用户、角色、类型、级别等）。

例如配置标签的用户名和角色名。
```yml
security_opt:
    - label:user:USER
    - label:role:ROLE
```

### `ulimits`
指定容器的 ulimits 限制值。

例如，指定最大进程数为 65535，指定文件句柄数为 20000（软限制，应用可以随时修改，不能超过硬限制） 和 40000（系统硬限制，只能 root 用户提高）。

```yml
  ulimits:
    nproc: 65535
    nofile:
      soft: 20000
      hard: 40000
```

### `volumes`

数据卷所挂载路径设置。可以设置宿主机路径 （`HOST:CONTAINER`） 或加上访问模式 （`HOST:CONTAINER:ro`）。

该指令中路径支持相对路径。例如

```yml
volumes:
 - /var/lib/mysql
 - cache/:/tmp/cache
 - ~/configs:/etc/configs/:ro
```

### `volumes_driver`
较新版本的 Docker 支持数据卷的插件驱动。

用户可以先使用第三方驱动创建一个数据卷，然后使用名称来访问它。

此时，可以通过 `volumes_driver` 来指定驱动。

```yml
volume_driver: mydriver
```

### `volumes_from`

从另一个服务或容器挂载它的数据卷。

```bash
volumes_from:
 - service_name
 - container_name
```

### 其它指令

此外，还有包括 `cpu_shares, cpuset, domainname, entrypoint, hostname, ipc, mac_address, mem_limit, memswap_limit, privileged, read_only, restart, stdin_open, tty, user, working_dir` 等指令，基本跟 docker-run 中对应参数的功能一致。

例如，指定使用 cpu 核 0 和 核 1，只用 50% 的 CPU 资源：
```yml
cpu_shares: 73
cpuset: 0,1
```

指定服务容器启动后执行的命令。
```yml
entrypoint: /code/entrypoint.sh
```

指定容器中运行应用的用户名。
```yml
user: nginx
```

指定容器中工作目录。
```yml
working_dir: /code
```

指定容器中搜索域名、主机名、mac 地址等。
```yml
domainname: your_website.com
hostname: test
mac_address: 08-00-27-00-0C-0A
```

指定容器中
```yml
ipc: host
```

指定容器中内存和内存交换区限制都为 1G。
```yml
mem_limit: 1g
memswap_limit: 1g
```

允许容器中运行一些特权命令。
```yml
privileged: true
```

指定容器退出后的重启策略为始终重启。该命令对保持服务始终运行十分有效，在生产环境中推荐配置为 `always` 或者 `unless-stopped`。
```yml
restart: always
```

以只读模式挂载容器的 root 文件系统，意味着不能对容器内容进行修改。
```yml
read_only: true
```

打开标准输入，可以接受外部输入。
```yml
stdin_open: true
```

模拟一个假的远程控制台。
```yml
tty: true
```

### 读取环境变量
从 1.5.0 版本开始，Compose 模板文件支持动态读取主机的系统环境变量。

例如，下面的 Compose 文件将从运行它的环境中读取变量 ${MONGO_VERSION} 的值，并写入执行的指令中。

```yml
db:
  image: "mongo:${MONGO_VERSION}"
```

如果执行 `MONGO_VERSION=3.0 docker-compose up` 则会启动一个 `mongo:3.2` 镜像的容器；如果执行 `MONGO_VERSION=2.8 docker-compose up` 则会启动一个 `mongo:2.8` 镜像的容器。
