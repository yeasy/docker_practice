# 第十章 Docker Buildx

Docker Buildx 是一个 docker CLI 插件，其扩展了 docker 命令，支持 [Moby BuildKit](10.1_buildkit.md) 提供的功能。提供了与 docker build 相同的用户体验，并增加了许多新功能。

> Buildx 需要 Docker v19.03+ （Docker 19.03 及以上版本）。在较新版本中已更常用且功能更完整。

## 本章内容

本章将详细介绍 Docker Buildx 的使用，包括：

* [使用 BuildKit 构建镜像](10.1_buildkit.md)
* [使用 Buildx 构建镜像](10.2_buildx.md)
* [构建多种系统架构支持的 Docker 镜像](10.3_multi-arch-images.md)

> **供应链安全与存储后端前瞻**：现代软件供应链中，镜像来源证明（Provenance，在 BuildKit 中默认以 `mode=min` 添加）和软件物料清单（SBOM，可通过 `--sbom=true` 显式开启）已经成为极其重要的构建产出。这些 Attestations 数据会作为 manifest 附着在 **镜像索引 (Image Index)** 上。
> 正是基于此诉求，自 Docker Engine 29 起在**新安装场景**默认启用的 `containerd image store` 提供对 Image Index 的完美本地支持能力，解决了传统经典存储后端（Classic Store）无法有效处理带 Attestations 镜像索引的瓶颈。这使得你可以利用 `docker buildx imagetools inspect` 等手段，甚至做到无需拉取完整镜像内容即可在 Registry 或本地高效校验镜像的安全元数据。
