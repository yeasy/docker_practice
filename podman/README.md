# podman

[`podman`](https://github.com/containers/podman) 是一个无守护程序与 docker 命令兼容的下一代 Linux 容器工具。

## 安装

```bash
$ sudo yum -y install podman
```

## 使用

`podman` 与 docker 命令完全兼容，只需将 `docker` 替换为 `podman` 即可，例如运行一个容器：

```bash
# $ docker run -d -p 80:80 nginx:alpine

$ podman run -d -p 80:80 nginx:alpine
```

## 参考

* https://developers.redhat.com/blog/2019/02/21/podman-and-buildah-for-docker-users/
