##fig.yml 参考

每个在 `fig.yml` 定义的服务都需要指定一个镜像或镜像的构建内容。像 `docker run` 的命令行一样，其它内容是可选的。

`docker run` 在 `Dockerfile` 中设置的选项(例如：`CMD`, `EXPOSE`, `VOLUME`, `ENV`) 作为已经提供的默认设置 - 你不需要在 `fig.yml` 中重新设置。

`image`

这里可以设置为标签或镜像ID的一部分。它可以是本地的，也可以是远程的 - 如果镜像在本地不存在，`Fig` 将会尝试拉去这个镜像。

```
image: ubuntu
image: orchardup/postgresql
image: a4bc65fd
```

`build`

指定 `Dockerfile` 所在文件夹的路径。 `Fig` 将会构建这个镜像并给它生成一个名字，然后使用这个镜像。

```
build: /path/to/build/dir
```

`command`

覆盖默认的命令。

```
command: bundle exec thin -p 3000
```

`links`

在其它的服务中连接容器。使用服务名称（经常也作为别名）或服务名称加服务别名 `（SERVICE:ALIAS）` 都可以。

```
links:
 - db
 - db:database
 - redis
```

可以在服务的容器中的 `/etc/hosts` 里创建别名。例如：

```
172.17.2.186  db
172.17.2.186  database
172.17.2.187  redis
```

环境变量也将被创建 - 细节查看环境变量参考章节。

`ports`

暴漏端口。使用宿主和容器 `（HOST:CONTAINER）` 或者仅仅容器的端口（宿主将会随机选择端口）都可以。

注：当使用 `HOST:CONTAINER` 格式来映射端口时，如果你使用的容器端口小于60你可能会得到错误得结果，因为 `YAML` 将会解析 `xx:yy` 这种数字格式为60进制。所以我们建议用字符指定你得端口映射。

```
ports:
 - "3000"
 - "8000:8000"
 - "49100:22"
 - "127.0.0.1:8001:8001"
```

`expose`

暴露不发布到宿主机的端口 - 它们只被连接的服务访问。仅仅内部的端口可以被指定。

```
expose:
 - "3000"
 - "8000"
```

`volumes`

卷挂载路径设置。可以设置宿主机路径 `（HOST:CONTAINER）` 或访问模式 `（HOST:CONTAINER:ro）` 。

```
volumes:
 - /var/lib/mysql
 - cache/:/tmp/cache
 - ~/configs:/etc/configs/:ro
```

`volumes_from`

从另一个服务或容器挂载所有卷。

```
volumes_from:
 - service_name
 - container_name
```

`environment`

设置环境变量。你可以使用数组或字典两种格式。

环境变量在运行 `Fig` 的机器上被解析成一个key。它有助于安全和指定的宿主值。

```
environment:
  RACK_ENV: development
  SESSION_SECRET:

environment:
  - RACK_ENV=development
  - SESSION_SECRET
```

`net`

设置网络模式。使用和 `docker client` 的 `--net` 参数一样的值。

```
net: "bridge"
net: "none"
net: "container:[name or id]"
net: "host"
```

`dns`

配置DNS服务器。它可以是一个值，也可以是一个列表。

```
dns: 8.8.8.8
dns:
  - 8.8.8.8
  - 9.9.9.9
```

`working_dir, entrypoint, user, hostname, domainname, mem_limit, privileged`

这些都是和 `docker run` 对应的一个值。

```
working_dir: /code
entrypoint: /code/entrypoint.sh
user: postgresql

hostname: foo
domainname: foo.com

mem_limit: 1000000000
privileged: true
```
