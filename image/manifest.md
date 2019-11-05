## 构建多种系统架构支持的 Docker 镜像 -- docker manifest 命令详解

我们知道使用镜像创建一个容器，该镜像必须与 Docker 宿主机系统架构一致，例如 `Linux x86_64` 架构的系统中只能使用 `Linux x86_64` 的镜像创建容器。

> Windows、macOS 除外，其使用了 [binfmt_misc](https://docs.docker.com/docker-for-mac/multi-arch/) 提供了多种架构支持，在 Windows、macOS 系统上 (x86_64) 可以运行 arm 等其他架构的镜像。

例如我们在 `Linux x86_64` 中构建一个 `username/test` 镜像。

```docker
FROM alpine

CMD echo 1
```

构建镜像后推送到 Docker Hub，之后我们尝试在树莓派 `Linux arm64v8` 中使用这个镜像。

```bash
$ docker run -it --rm username/test
```

可以发现这个镜像根本获取不到。

要解决这个问题，通常采用的做法是通过镜像名区分不同系统架构的镜像，例如在 `Linux x86_64` 和 `Linux arm64v8` 分别构建 `username/test` 和 `username/arm64v8-test` 镜像。运行时使用对应架构的镜像即可。

这样做显得很繁琐，那么有没有一种方法让 Docker 引擎根据系统架构自动拉取对应的镜像呢？

我们发现在 `Linux x86_64` 和 `Linux arm64v8` 架构的计算机中执行 `$ docker run golang:alpine go version` 时我们发现可以正确的运行。

这是什么原因呢？

原因就是 `golang:alpine` 官方镜像有一个 [`manifest` 列表](https://docs.docker.com/registry/spec/manifest-v2-2/)。

当用户获取一个镜像时，Docker 引擎会首先查找该镜像是否有 `manifest` 列表，如果有的话 Docker 引擎会按照 Docker 运行环境（系统及架构）查找出对应镜像（例如 `golang:alpine`）。如果没有的话会直接获取镜像（例如上例中我们构建的 `username/test`）。

我们可以使用 `$ docker manifest inspect golang:alpine` 查看这个 `manifest` 列表的结构。

> 该命令属于实验特性，请参考 [开启实验特性](../install/experimental) 一节。

```bash
$ docker manifest inspect golang:alpine
```

```json
{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.list.v2+json",
   "manifests": [
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 1365,
         "digest": "sha256:5e28ac423243b187f464d635bcfe1e909f4a31c6c8bce51d0db0a1062bec9e16",
         "platform": {
            "architecture": "amd64",
            "os": "linux"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 1365,
         "digest": "sha256:2945c46e26c9787da884b4065d1de64cf93a3b81ead1b949843dda1fcd458bae",
         "platform": {
            "architecture": "arm",
            "os": "linux",
            "variant": "v7"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 1365,
         "digest": "sha256:87fff60114fd3402d0c1a7ddf1eea1ded658f171749b57dc782fd33ee2d47b2d",
         "platform": {
            "architecture": "arm64",
            "os": "linux",
            "variant": "v8"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 1365,
         "digest": "sha256:607b43f1d91144f82a9433764e85eb3ccf83f73569552a49bc9788c31b4338de",
         "platform": {
            "architecture": "386",
            "os": "linux"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 1365,
         "digest": "sha256:25ead0e21ed5e246ce31e274b98c09aaf548606788ef28eaf375dc8525064314",
         "platform": {
            "architecture": "ppc64le",
            "os": "linux"
         }
      },
      {
         "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
         "size": 1365,
         "digest": "sha256:69f5907fa93ea591175b2c688673775378ed861eeb687776669a48692bb9754d",
         "platform": {
            "architecture": "s390x",
            "os": "linux"
         }
      }
   ]
}
```

可以看出 `manifest` 列表中包含了不同系统架构所对应的镜像 `digest` 值，这样 Docker 就可以在不同的架构中使用相同的 `manifest` (例如 `golang:alpine`) 获取对应的镜像。

下面介绍如何使用 `$ docker manifest` 命令创建并推送 `manifest` 列表到 Docker Hub。

### 构建镜像

首先在 `Linux x86_64` 构建 `username/x8664-test` 镜像。并在 `Linux arm64v8` 中构建 `username/arm64v8-test` 镜像，构建好之后推送到 Docker Hub。

### 创建 `manifest` 列表

```bash
# $ docker manifest create MANIFEST_LIST MANIFEST [MANIFEST...]
$ docker manifest create username/test \
      username/x8664-test \
      username/arm64v8-test
```

当要修改一个 `manifest` 列表时，可以加入 `-a,--amend` 参数。

### 设置 `manifest` 列表

```bash
# $ docker manifest annotate [OPTIONS] MANIFEST_LIST MANIFEST
$ docker manifest annotate username/test \
      username/x8664-test \
      --os linux --arch x86_64

$ docker manifest annotate username/test \
      username/arm64v8-test \
      --os linux --arch arm64 --variant v8
```

这样就配置好了 `manifest` 列表。

### 查看 `manifest` 列表

```bash
$ docker manifest inspect username/test
```

### 推送 `manifest` 列表

最后我们可以将其推送到 Docker Hub。

```bash
$ docker manifest push username/test
```

### 测试

我们在 `Linux x86_64` `Linux arm64v8` 中分别执行 `$ docker run -it --rm username/test` 命令，发现可以正确的执行。

### 官方博客

详细了解 `manifest` 可以阅读官方博客。

* https://blog.docker.com/2017/11/multi-arch-all-the-things/
