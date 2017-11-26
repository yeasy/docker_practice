## 容器格式

最初，Docker 采用了 `LXC` 中的容器格式。从 0.7 版本以后开始去除 LXC，转而使用自行开发的 [libcontainer](https://github.com/docker/libcontainer)，从 1.11 开始，则进一步演进为使用 [runC](https://github.com/opencontainers/runc) 和 [containerd](https://containerd.tools/)。

对更多容器格式的支持，还在进一步的发展中。
