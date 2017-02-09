## [CentOS](https://hub.docker.com/_/centos/)

### 基本信息
[CentOS](https://en.wikipedia.org/wiki/CentOS) 是流行的 Linux 发行版，其软件包大多跟 RedHat 系列保持一致。

该仓库位于 https://hub.docker.com/_/centos/ ，提供了 CentOS 从 5 ~ 7 各个版本的镜像。

### 使用方法
默认会启动一个最小化的 CentOS 环境。

```sh
$ docker run --name some-centos -i -t centos bash
bash-4.2#
```

### Dockerfile

#### CentOS 5 版本
```
FROM scratch
MAINTAINER The CentOS Project <cloud-ops@centos.org>
ADD c5-docker.tar.xz /
LABEL name="CentOS Base Image" \
    vendor="CentOS" \
    license="GPLv2" \
    build-date="2016-03-31"

# Default command
CMD ["/bin/bash"]
```

#### CentOS 6 版本
```
FROM scratch
MAINTAINER https://github.com/CentOS/sig-cloud-instance-images
ADD centos-6-docker.tar.xz /

LABEL name="CentOS Base Image" \
    vendor="CentOS" \
    license="GPLv2" \
    build-date="20160729"

CMD ["/bin/bash"]
```

#### CentOS 7 版本
```
FROM scratch
MAINTAINER https://github.com/CentOS/sig-cloud-instance-images
ADD centos-7-docker.tar.xz /

LABEL name="CentOS Base Image" \
    vendor="CentOS" \
    license="GPLv2" \
    build-date="20160729"

CMD ["/bin/bash"]
```


