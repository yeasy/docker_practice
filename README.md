# Docker — 从入门到实践

[![](https://img.shields.io/github/stars/yeasy/docker_practice.svg?style=social&label=Stars)](https://github.com/yeasy/docker_practice) [![](https://img.shields.io/github/release/yeasy/docker_practice/all.svg)](https://github.com/yeasy/docker_practice/releases) [![](https://img.shields.io/badge/Based-Docker%20CE%20v30.x-blue.svg)](https://github.com/docker/docker-ce) [![](https://img.shields.io/badge/Docker%20%E6%8A%80%E6%9C%AF%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E6%88%98-jd.com-red.svg)][1]

**v1.5.3**

[Docker](https://www.docker.com) 是个划时代的开源项目，它彻底释放了计算虚拟化的威力，极大提高了应用的维护效率，降低了云计算应用开发的成本！使用 Docker，可以让应用的部署、测试和分发都变得前所未有的高效和轻松！

无论是应用开发者、运维人员、还是其他信息技术从业人员，都有必要认识和掌握 Docker，节约有限的生命。

本书既适用于具备基础 Linux 知识的 Docker 初学者，也希望可供理解原理和实现的高级用户参考。同时，书中给出的实践案例，可供在进行实际部署时借鉴。

## 内容特色

*   **入门基础**：前六章为基础内容，帮助深入理解 Docker 的基本概念（镜像、容器、仓库）和核心操作。
*   **进阶应用**：7 ~ 10 章涵盖数据管理、网络配置、Buildx、Compose、运维管理等高级操作。
*   **深入原理**：11 ~ 13 章介绍容器编排(Kubernetes、Etcd)、容器生态、底层实现技术。
*   **实战扩展**：14 ~ 15 章展示操作系统、CI/CD等典型应用场景和实践案例，以及工具参考。
*   **广泛扩展**：涵盖 Fedora CoreOS、容器云等热门开源项目，并展示典型的应用场景和实践案例。

## 阅读方式

### 在线阅读

> 推荐访问官方 GitBook，体验最佳。

*   **GitBook**: [yeasy.gitbook.io/docker_practice](https://yeasy.gitbook.io/docker_practice/)
*   **GitHub**: [github.com/yeasy/docker_practice](https://github.com/yeasy/docker_practice/blob/master/SUMMARY.md)
*   **Mirror**: [docker-practice.com](https://vuepress.mirror.docker-practice.com/)

### 本地阅读

#### 方式 1：Docker 镜像（推荐）

无需安装任何依赖，一条命令即可启动。

```bash
docker run -it --rm -p 4000:80 ccr.ccs.tencentyun.com/dockerpracticesig/docker_practice:vuepress
```
启动后访问 [http://localhost:4000](http://localhost:4000)。
[详情参考](https://github.com/yeasy/docker_practice/wiki/%E7%A6%BB%E7%BA%BF%E9%98%85%E8%AF%BB%E5%8A%9F%E8%83%BD%E8%AF%A6%E8%A7%A3)

#### 方式 2：本地构建（HonKit）

适合想要修改内容或深度定制的读者。需要安装 Node.js 环境。

```bash
npm install
npx honkit serve
```
启动后访问 [http://localhost:4000](http://localhost:4000)。

## 社区交流

欢迎加入 Docker 技术交流群，分享 Docker 资源，交流 Docker 技术。

*   **GitHub Discussions**：[点击前往](https://github.com/yeasy/docker_practice/discussions)（技术问答、交流）
*   **GitHub Issues**：[提交 Bug](https://github.com/yeasy/docker_practice/issues/new/choose)（内容错误、建议）

> **交流 QQ 群**（部分已满，建议优先使用 GitHub Discussions）：
> *   341410255 (I), 419042067 (II), 210028779 (III), 483702734 (IV), 460598761 (V)
> *   581983671 (VI), 252403484 (VII), 544818750 (VIII), 571502246 (IX), 145983035 (X)

## 参与贡献

欢迎 [参与项目维护](CONTRIBUTING.md)。

*   [修订记录](CHANGELOG.md)
*   [贡献者名单](https://github.com/yeasy/docker_practice/graphs/contributors)

## 进阶学习

[![](https://github.com/yeasy/docker_practice/raw/master/_images/docker_primer4.jpg)][1]

《[Docker 技术入门与实战][1]》已更新到第 4 版，讲解最新容器技术栈知识，欢迎大家阅读并反馈建议。

*   [京东图书][1]
*   [天猫图书](https://detail.tmall.com/item.htm?id=997383773726&skuId=6143496614475)

## 鼓励项目

<p align="center">
<img width="200" src="https://github.com/yeasy/docker_practice/raw/master/_images/donate.jpeg">
</p>

<p align="center"><strong>欢迎鼓励项目一杯 coffee~</strong></p>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yeasy/docker_practice&type=Date)](https://star-history.com/#yeasy/docker_practice&Date)

[1]: https://item.jd.com/10200902362001.html
