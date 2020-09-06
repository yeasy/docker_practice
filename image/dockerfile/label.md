# LABEL 指令

`LABEL` 指令用来给镜像以键值对的形式添加一些元数据（metadata）。

```docker
LABEL <key>=<value> <key>=<value> <key>=<value> ...
```

我们还可以用一些标签来申明镜像的作者、文档地址等：

```docker
LABEL org.opencontainers.image.authors="yeasy"

LABEL org.opencontainers.image.documentation="https://yeasy.gitbooks.io"
```

具体可以参考 https://github.com/opencontainers/image-spec/blob/master/annotations.md
