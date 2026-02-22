# 21.2 GitHub Actions

GitHub [Actions](https://github.com/features/actions) 是 GitHub 推出的一款 CI/CD 工具。

我们可以在每个 `job` 的 `step` 中使用 Docker 执行构建步骤。

## 21.2.1 最小可用示例

在仓库根目录创建 `/.github/workflows/ci.yml`：

```yaml
name: CI

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          tags: local/test:ci
```

该示例会在 GitHub Actions 中构建当前仓库的 Docker 镜像（不推送到 registry）。

## 21.2.2 最佳实践

* 固定 action 的主版本（例如 `@v4` / `@v6`），避免使用 `@master` 这类浮动引用。
* 设置最小权限（例如 `contents: read`），需要写入权限时再打开。
* 需要依赖缓存时，优先使用官方支持的缓存方案（例如针对语言包管理器的 cache 或 BuildKit cache）。

如果你需要在某个步骤里直接运行容器镜像（而不是构建镜像），可以使用 `docker://` 语法：

```yaml
- name: Run container step
  uses: docker://golang:alpine
  with:
    args: go version
```

## 21.2.3 参考资料

* [Actions Docs](https://docs.github.com/en/actions)
