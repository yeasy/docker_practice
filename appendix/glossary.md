# 附录七：术语表

本附录整理了本书中常见的一些专业术语及其解释。

## A

* **Alpine**：一个轻量级的 Linux 发行版，常作为基础镜像用于构建体积较小的 Docker 镜像。
* **API (Application Programming Interface)**：应用程序编程接口，Docker Daemon 提供 RESTful API 供客户端或外部程序与之交互。

## B

* **Base Image (基础镜像)**：没有父镜像的镜像，通常是操作系统的最小安装集合（如 `ubuntu` 或 `alpine`）。
* **BuildKit**：Docker 下一代的构建引擎，提供了更高的构建性能、更好的缓存处理和并发构建支持。
* **Buildx**：Docker CLI 的一个插件，扩展了构建功能，支持 BuildKit 的所有高级特性，例如多系统架构镜像构建。

## C

* **Cgroups (Control Groups)**：控制组，Linux 内核特性，用于限制、记录、隔离进程组使用的物理资源（如 CPU、内存、磁盘 I/O 等）。
* **Cluster (集群)**：一组协同工作的节点（如主机、虚拟机等），在容器领域常指 Kubernetes 集群。
* **Compose (Docker Compose)**：用于定义和运行多容器 Docker 应用程序的工具，通过 YAML 文件配置应用服务。
* **Container (容器)**：镜像的运行实例，带有额外的可写文件层，具有独立性。
* **Containerd**：行业标准的容器运行时，核心功能是管理宿主机上容器的生命周期（创建、启动、停止、销毁）。

## D

* **Daemon (守护进程)**：Docker 的后台守护进程，负责接收和处理 Docker API 请求，并管理镜像、容器、网络和数据卷等对象。
* **Docker**：开源的应用容器引擎，让开发者可以打包应用程序及其依赖包到一个可移植的容器中，然后发布到任何流行的 Linux 或 Windows 机器上。
* **Docker Desktop**：包含 Docker Engine、Docker CLI 客户端、Docker Compose 和 Kubernetes 等的桌面应用程序，适用于 macOS 和 Windows。
* **Docker Hub**：Docker 官方的公共镜像仓库服务，提供容器镜像的存储和分发。
* **Dockerfile**：包含用于组合镜像的命令的文本文件，Docker 通过读取 `Dockerfile` 中的指令即可自动完成镜像构建。

## E

* **Etcd**：一个高可用、强一致性的分布式键值存储系统，常用于容器集群（如 Kubernetes）的服务发现和状态配置管理。

## I

* **Image (镜像)**：Docker 镜像是一个只读模板，带有创建 Docker 容器的说明。

## K

* **Kubernetes (K8s)**：开源的容器编排引擎，用于自动化容器化应用程序的部署、扩展和管理。

## L

* **Layer (镜像层)**：Docker 镜像由多个只读层叠合而成，每一层通常代表 Dockerfile 中的一条指令的操作结果，通过联合文件系统（UFS）叠加在一起形成完整的文件系统。

## M

* **Multistage Build (多阶段构建)**：Dockerfile 中的特性，允许在同一个 Dockerfile 中使用多个 `FROM` 语句，从一个阶段复制所需的构建产物到另一个阶段，从而大幅减小最终镜像的体积。

## N

* **Namespace (命名空间)**：Linux 内核特性，用于隔离各种系统资源，如进程、网络、挂载点等，使容器看起来就像是一个独立的操作系统。
* **Node (节点)**：容器集群（如 Kubernetes）中的一台工作机器，可以是物理机或虚拟机。

## O

* **OCI (Open Container Initiative)**：开放容器规范，由多家行业领头企业共同制定的容器运行时和镜像格式的行业标准。
* **Orchestration (编排)**：自动化部署、管理、扩展和网络配置容器的系统和技术（如 Kubernetes）。

## P

* **Pod**：Kubernetes 中最小的、可部署的计算单元，包含一个或多个紧密相关的容器，共享相同的网络命名空间和存储。
* **Prometheus**：开源的系统监控和告警工具包，广泛应用于云原生的监控体系中。

## R

* **Registry (注册服务器)**：提供 Docker 镜像下载和上传等存储分发服务的服务器。
* **Repository (仓库)**：集中存放某个应用的所有镜像的地方，通常由镜像名定义。一个 Registry 中可以包含多个 Repository。

## S

* **Swarm (Docker Swarm)**：Docker 原生的集群和编排管理工具，可将多个 Docker 主机组合成一个统一的虚拟 Docker 主机池。

## U

* **UFS (Union File System)**：联合文件系统，一种分层、轻量级并且高性能的文件系统，它支持对文件系统的修改一层层叠加。

## V

* **Volume (数据卷)**：专为绕过联合文件系统而设计的特殊目录，用于实现容器数据的持久化，或在多个容器之间提供文件共享。
