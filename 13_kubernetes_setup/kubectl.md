# kubectl 使用

[kubectl](https://github.com/kubernetes/kubernetes) 是 Kubernetes 自带的客户端，可以用它来直接操作 Kubernetes。

使用格式有两种：
```bash
kubectl [flags]
kubectl [command]
```

## get

显示一个或多个资源

## describe

显示资源详情

## create

从文件或标准输入创建资源

## update

从文件或标准输入更新资源

## delete

通过文件名、标准输入、资源名或者 label selector 删除资源

## logs

输出 pod 中一个容器的日志

## rollout

对 Deployment 等资源执行滚动更新/回滚

## exec

在容器内部执行命令

## port-forward

将本地端口转发到 Pod

## proxy

为 Kubernetes API server 启动代理服务器

## run

在集群中使用指定镜像启动容器

## expose

将 replication controller service 或 pod 暴露为新的 Kubernetes service

## label

更新资源的 label

## config

修改 Kubernetes 配置文件

## cluster-info

显示集群信息

## api-versions

以 “组/版本” 的格式输出服务端支持的 API 版本

## version

输出服务端和客户端的版本信息

## help

显示各个命令的帮助信息
