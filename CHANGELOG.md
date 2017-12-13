## 主要修订记录

* 0.9: 2017-12-31

* 0.9-rc3: 2017-12-20

  * 增加 `私有仓库高级配置`

  * 精简示例代码

  * 调整目录结构

* 0.9-rc2: 2017-12-10

  * 增加 Docker 中文资源链接
  * 增加介绍基于 Docker 的 CI/CD 工具 `Drone`
  * 增加 `docker secret` 相关内容
  * 增加 `docker config` 相关内容
  * 增加 `LinuxKit` 相关内容

  * 更新 `CoreOS` 章节
  * 更新 `etcd` 章节，基于 3.x 版本

  * 删除 `Docker Compose` 中的 `links`指令

  * 替换 `docker daemon` 命令为 `dockerd`
  * 替换 `docker ps` 命令为 `docker container ls`
  * 替换 `docker images` 命令为 `docker image ls`

  * 修改 `安装 Docker` 一节中部分文字表述

  * 移除历史遗留文件和错误的文件
  * 优化文字排版
  * 调整目录结构
  * 修复内容逻辑错误
  * 修复`404` 链接

* 0.9-rc1: 2017-11-29

  * 根据最新版本（v17.09）修订内容

  * 增加 `Dockerfile` 多阶段构建( `multistage builds` ) `Docker 17.05` 新增特性
  * 增加 `docker exec` 子命令介绍
  * 增加 `docker` 管理子命令 `container` `image` `network` `volume` 介绍
  * 增加 `树莓派单片电脑` 安装 Docker
  * 增加 Docker 存储驱动 `OverlayFS` 相关内容

  * 更新 `Docker CE` `v17.x` 安装说明
  * 更新 `Docker 网络` 一节
  * 更新 `Docker Machine` 基于 0.13.0 版本
  * 更新 `Docker Compose` 基于 3 文件格式

  * 删除 `Docker Swarm` 相关内容，替换为 `Swarm mode` `Docker 1.12.0` 新增特性
  * 删除 `docker run` `--link` 参数

  * 精简 `Docker Registry` 一节

  * 替换 `docker run` `-v` 参数为 `--mount`

  * 修复 `404` 链接
  * 优化文字排版
  * 增加离线阅读功能

* 0.8.0: 2017-01-08

  * 修正文字内容
  * 根据最新版本（1.12）修订安装使用
  * 补充附录章节

* 0.7.0: 2016-06-12

  * 根据最新版本进行命令调整
  * 修正若干文字描述

* 0.6.0: 2015-12-24

  * 补充 Machine 项目
  * 修正若干 bug

* 0.5.0: 2015-06-29

  * 添加 Compose 项目
  * 添加 Machine 项目
  * 添加 Swarm 项目
  * 完善 Kubernetes 项目内容
  * 添加 Mesos 项目内容

* 0.4.0: 2015-05-08

  * 添加 Etcd 项目
  * 添加 Fig 项目
  * 添加 CoreOS 项目
  * 添加 Kubernetes 项目

* 0.3.0: 2014-11-25

  * 完成仓库章节；
  * 重写安全章节；
  * 修正底层实现章节的架构、命名空间、控制组、文件系统、容器格式等内容；
  * 添加对常见仓库和镜像的介绍；
  * 添加 Dockerfile 的介绍；
  * 重新校订中英文混排格式。
  * 修订文字表达。
  * 发布繁体版本分支：zh-Hant。

* 0.2.0: 2014-09-18

  * 对照官方文档重写介绍、基本概念、安装、镜像、容器、仓库、数据管理、网络等章节；
  * 添加底层实现章节；
  * 添加命令查询和资源链接章节；
  * 其它修正。

* 0.1.0: 2014-09-05

  * 添加基本内容;
  * 修正错别字和表达不通顺的地方。
