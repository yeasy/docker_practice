# 第四章 使用镜像

在之前的介绍中，我们知道镜像是 Docker 的三大组件之一。

Docker 运行容器前需要本地存在对应的镜像，如果本地不存在该镜像，Docker 会从镜像仓库下载该镜像。

## 本章内容

本章将介绍更多关于镜像的内容，包括：

* [从仓库获取镜像](4.1_pull.md)
* [列出镜像](4.2_list.md)
* [删除本地镜像](4.3_rm.md)
* [利用 commit 理解镜像构成](4.4_commit.md)
* [使用 Dockerfile 定制镜像](4.5_build.md)
* [其它制作镜像的方式](4.6_other.md)
* [镜像的实现原理](4.7_internal.md)

> **版本提示：镜像存储后端的变迁**
>
> 在 Docker Engine v29 及后续版本中，Docker 全新安装默认启用了 **containerd image store**（替代了传统的 classic store）。这一底层架构级别的变迁，意味着 Docker 解锁了对 OCI Image Index 和 Attestations （例如原生的 provenance 来源证明与 SBOM 软件物料清单）的全量本地支持。
> 读者在执行类似 `docker buildx build --provenance=mode=min --sbom=true` 甚至使用后续审查工具（如 `docker buildx imagetools inspect`）时，其元数据能够与镜像数据一并完好地管理于本地存储系统中，为供应链安全验证补齐了最后一块拼图。
