# Docker Desktop 启用 Kubernetes

使用 Docker Desktop 可以很方便的启用 Kubernetes，由于国内获取不到 `k8s.gcr.io` 镜像，我们必须首先解决这一问题。

## 获取 `k8s.gcr.io` 镜像

由于国内拉取不到 `k8s.gcr.io` 镜像，我们可以使用开源项目 [AliyunContainerService/k8s-for-docker-desktop](https://github.com/AliyunContainerService/k8s-for-docker-desktop) 来获取所需的镜像。

## 启用 Kubernetes

在 Docker Desktop 设置页面，点击 `Kubernetes`，选择 `Enable Kubernetes`，稍等片刻，看到左下方 `Kubernetes` 变为 `running`，Kubernetes 启动成功。

![](https://github.com/AliyunContainerService/k8s-for-docker-desktop/raw/master/images/k8s.png)

## 测试

```bash
$ kubectl version
```

如果正常输出信息，则证明 Kubernetes 成功启动。
