# 第十六章 容器与云计算

> **版本说明**：云平台的 Kubernetes 版本和容器服务功能更新迅速。本章示例使用通用的 API 版本（如 `apps/v1`），建议查阅各云厂商官方文档获取最新的服务版本和配置指南。

Docker 目前已经得到了众多公有云平台的支持，并成为除虚拟机之外的核心云业务。

除了 AWS、Google、Azure 等，国内的各大公有云厂商，基本上都同时支持了虚拟机服务和基于 Kubernetes 的容器云业务。有的还推出了其他服务，例如[容器镜像服务](https://cloud.tencent.com/act/cps/redirect?redirect=11588&cps_key=3a5255852d5db99dcd5da4c72f05df61)让用户在云上享有安全高效的镜像托管、分发等服务。

## 本章内容

* [简介](16.1_intro.md)
* [腾讯云](16.2_tencentCloud.md)
* [阿里云](16.3_alicloud.md)
* [亚马逊云](16.4_aws.md)
* [多云部署策略](16.5_multicloud.md)
