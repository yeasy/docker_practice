## [Ubuntu](https://registry.hub.docker.com/_/ubuntu/)

### 基本信息
[Ubuntu](https://en.wikipedia.org/wiki/Ubuntu) 是流行的 Linux 发行版，其自带软件版本往往较新一些。
该仓库提供了 Ubuntu从12.04 ~ 14.10 各个版本的镜像。

### 使用方法
默认会启动一个最小化的 Ubuntu 环境。
```
$ sudo docker run --name some-ubuntu -i -t ubuntu
root@523c70904d54:/#
```

### Dockerfile
* [12.04 版本](https://github.com/tianon/docker-brew-ubuntu-core/blob/2b105575647a7e2030ff344d427c3920b89e17a9/precise/Dockerfile)
* [14.04 版本](https://github.com/tianon/docker-brew-ubuntu-core/blob/2b105575647a7e2030ff344d427c3920b89e17a9/trusty/Dockerfile)
* [14.10 版本](https://github.com/tianon/docker-brew-ubuntu-core/blob/2b105575647a7e2030ff344d427c3920b89e17a9/utopic/Dockerfile)
