## [Ubuntu](https://hub.docker.com/_/ubuntu/)

### 基本信息

[Ubuntu](https://en.wikipedia.org/wiki/Ubuntu) 是流行的 Linux 发行版，其自带软件版本往往较新一些。

该仓库位于 `https://hub.docker.com/_/ubuntu/`。具体可用版本以 Docker Hub 上的 tags 列表为准。

### 使用方法

默认会启动一个最小化的 Ubuntu 环境。

```bash
$ docker run --name some-ubuntu -it ubuntu:20.04
root@523c70904d54:/#
```

### Dockerfile

请到 https://github.com/docker-library/docs/tree/master/ubuntu 查看。
