# GitHub Actions

GitHub [Actions](https://github.com/features/actions) 是 GitHub 推出的一款 CI/CD 工具。

我们可以在每个 `job` 的 `step` 中使用 Docker 执行构建步骤。

```yaml
on: push

name: CI

jobs:
  my-job:
    name: Build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@master
        with:
          fetch-depth: 2
      - name: run docker container
        uses: docker://golang:alpine
        with:
          args: go version
```

## 参考资料

* [Actions Docs](https://help.github.com/en/actions)
