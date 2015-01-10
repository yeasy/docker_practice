## [CentOS](https://registry.hub.docker.com/_/centos/)

### 基本信息
[CentOS](https://en.wikipedia.org/wiki/CentOS) 是流行的 Linux 发行版，其软件包大多跟 RedHat 系列保持一致。
该仓库提供了 CentOS 从 5 ~ 7 各个版本的镜像。

### 使用方法
默认会启动一个最小化的 CentOS 环境。
```
$ sudo docker run --name some-centos -i -t centos bash
bash-4.2#
```

### Dockerfile
* [CentOS 5 版本](https://github.com/CentOS/sig-cloud-instance-images/blob/2e5a9c4e8b7191b393822e4b9e98820db5638a77/docker/Dockerfile)
* [CentOS 6 版本](https://github.com/CentOS/sig-cloud-instance-images/blob/8717e33ea5432ecb33d7ecefe8452a973715d037/docker/Dockerfile)
* [CentOS 7 版本](https://github.com/CentOS/sig-cloud-instance-images/blob/af7a1b9f8f30744360a10fe44c53a1591bef26f9/docker/Dockerfile)
