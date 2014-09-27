## [Ubuntu](https://registry.hub.docker.com/_/ubuntu/)

### 基本信息
[Ubuntu](https://en.wikipedia.org/wiki/Ubuntu)是流行的Linux发行版，其自带软件版本往往较新一些。
该仓库提供了Ubuntu从12.04到14.10各个版本的镜像。

### 使用方法
默认会启动一个最小化的Ubuntu环境。
```
$ sudo docker run --name some-ubuntu -i -t ubuntu
root@523c70904d54:/#
```

### Dockerfile
* [12.04版本](https://github.com/tianon/docker-brew-ubuntu-core/blob/2b105575647a7e2030ff344d427c3920b89e17a9/precise/Dockerfile)
* [14.04版本](https://github.com/tianon/docker-brew-ubuntu-core/blob/2b105575647a7e2030ff344d427c3920b89e17a9/trusty/Dockerfile)
* [14.10版本](https://github.com/tianon/docker-brew-ubuntu-core/blob/2b105575647a7e2030ff344d427c3920b89e17a9/utopic/Dockerfile)
