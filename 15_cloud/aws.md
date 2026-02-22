## 亚马逊云

如图 13-1 所示，AWS 是全球主流云服务平台之一。

![AWS](./_images/aws-logo.jpg)

图 13-1 AWS 标识

[AWS](https://www.amazonaws.cn)，即 Amazon Web Services，是亚马逊 (Amazon) 公司的 IaaS 和 PaaS 平台服务。AWS 提供了一整套基础设施和应用程序服务，使用户几乎能够在云中运行一切应用程序：从企业应用程序和大数据项目，到社交游戏和移动应用程序。AWS 面向用户提供包括弹性计算、存储、数据库、应用程序在内的一整套云计算服务，能够帮助企业降低 IT 投入成本和维护成本。

在容器领域，AWS 目前主流能力可以按场景分为四类：

1. `Amazon EKS`：托管 Kubernetes 控制平面，适合标准云原生工作负载。
2. `Amazon ECS`：AWS 原生容器编排服务，适合深度集成 AWS 生态 (IAM、ALB、CloudWatch) 场景。
3. `AWS Fargate`：无服务器容器运行时，可与 EKS/ECS 结合使用，减少节点运维。
4. `Amazon ECR`：镜像仓库服务，提供私有镜像管理、扫描与访问控制。

实践建议：

* 团队已具备 Kubernetes 经验，优先选择 EKS；
* 追求更低运维复杂度且业务主要运行在 AWS，可优先 ECS + Fargate；
* 无论编排方案如何，都建议使用 ECR 统一管理镜像生命周期。

![AWS 容器服务](./_images/ECS.jpg)

图 13-2 AWS 容器服务示意图
