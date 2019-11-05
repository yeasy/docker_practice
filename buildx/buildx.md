# 使用 Buildx 构建镜像

## 启用 Buildx

`buildx` 命令属于实验特性，参考 [开启实验特性](../install/experimental.md) 一节。

## 使用

你可以直接使用 `docker buildx build` 命令构建镜像。

```bash
$ docker buildx build .
[+] Building 8.4s (23/32)
 => ...
```

Buildx 使用 [BuildKit 引擎](buildkit.md) 进行构建，支持许多新的功能，具体参考 [Buildkit](buildkit.md) 一节。

## 官方文档

* https://docs.docker.com/engine/reference/commandline/buildx/
