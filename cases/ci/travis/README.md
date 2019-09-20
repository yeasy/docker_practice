## 在 Travis CI 中使用 Docker

当代码提交到 GitHub 时，[Travis CI](https://travis-ci.com/) 会根据项目根目录 `.travis.yml` 文件设置的指令，执行一系列操作。

本小节介绍如何在 Travis CI 中使用 Docker 进行持续集成/持续部署（CI/CD）。这里以当代码提交到 GitHub 时自动构建 Docker 镜像并推送到 Docker Hub 为例进行介绍。

### 准备

首先登录 https://travis-ci.com/account/repositories 选择 GitHub 仓库，按照指引安装 GitHub App 来启用 GitHub 仓库构建。

在项目根目录新建一个 `Dockerfile` 文件。

```dockerfile
FROM alpine

RUN echo "Hello World"
```

新建 Travis CI 配置文件 `.travis.yml` 文件。

```yml
language: bash

dist: xenial

services:
  - docker

before_script:
  # 登录到 docker hub
  - echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

script:
  # 这里编写测试代码的命令
  - echo "test code"

after_success:
  # 当代码测试通过后执行的命令
  - docker build -t username/alpine .
  - docker push username/alpine
```

> 请提前在 Travis CI 仓库设置页面配置 `DOCKER_PASSWORD` `DOCKER_USERNAME` 变量

### 查看结果

将项目推送到 GitHub，登录 [Travis CI](https://travis-ci.com/) 查看构建详情。
