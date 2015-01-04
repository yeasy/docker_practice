# 项目简介

![](../_images/kubernetes_logo.svg)

Kubernetes 是 Google 团队发起的开源项目，它的目标是管理跨多个主机的容器，提供基本的部署，维护以及运用伸缩，主要实现语言为Go语言。Kubernetes是：
* 易学：轻量级，简单，容易理解
* 便携：支持公有云，私有云，混合云，以及多种云平台
* 可拓展：模块化，可插拔，支持钩子，可任意组合
* 自修复：自动重调度，自动重启，自动复制

Kubernetes构建于Google数十年经验，一大半来源于Google生产环境规模的经验。结合了社区最佳的想法和实践。

在分布式系统中，部署，调度，伸缩一直是最为重要的也最为基础的功能。Kubernets就是希望解决这一序列问题的。

Kubernets 目前在[github.com/GoogleCloudPlatform/kubernetes](https://github.com/GoogleCloudPlatform/kubernetes)进行维护，截至定稿最新版本为 0.7.2 版本。

### Kubernetes 能够运行在任何地方！

虽然Kubernets最初是为GCE定制的，但是在后续版本中陆续增加了其他云平台的支持，以及本地数据中心的支持。