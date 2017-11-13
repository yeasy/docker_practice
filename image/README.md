# 使用 Docker 镜像

在之前的介绍中，我们知道镜像是 Docker 的三大组件之一。

Docker 运行容器前需要本地存在对应的镜像，如果镜像不存在本地，Docker 会从镜像仓库下载（默认是 Docker Hub ）。

本章将介绍更多关于镜像的内容，包括：
* 从仓库获取镜像；
* 管理本地主机上的镜像；
* 介绍镜像实现的基本原理。

Docker 在 1.13 版本引进了新的管理命令（management commands），在 Docker 1.13+ 推荐使用 `docker image` 子命令来管理 Docker 镜像。
