## BuildKit

BuildKit 是下一代的镜像构建组件，在 https://github.com/moby/buildkit 开源。

下面介绍如何在 Docker CE 18.09+ 版本中使用 BuildKit 构建 Docker 镜像。

```bash
$ export DOCKER_BUILDKIT=1

# Windows

$ set $env:DOCKER_BUILDKIT=1
```
