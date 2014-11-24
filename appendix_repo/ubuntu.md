## [Ubuntu](https://registry.hub.docker.com/_/ubuntu/)

### 基本訊息
[Ubuntu](https://en.wikipedia.org/wiki/Ubuntu) 是流行的 Linux 發行版，其自帶軟件版本往往較新一些。
該倉庫提供了 Ubuntu從12.04 ~ 14.10 各個版本的鏡像。

### 使用方法
默認會啟動一個最小化的 Ubuntu 環境。
```
$ sudo docker run --name some-ubuntu -i -t ubuntu
root@523c70904d54:/#
```

### Dockerfile
* [12.04 版本](https://github.com/tianon/docker-brew-ubuntu-core/blob/2b105575647a7e2030ff344d427c3920b89e17a9/precise/Dockerfile)
* [14.04 版本](https://github.com/tianon/docker-brew-ubuntu-core/blob/2b105575647a7e2030ff344d427c3920b89e17a9/trusty/Dockerfile)
* [14.10 版本](https://github.com/tianon/docker-brew-ubuntu-core/blob/2b105575647a7e2030ff344d427c3920b89e17a9/utopic/Dockerfile)
