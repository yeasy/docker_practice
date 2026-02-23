## 14.3 Docker Desktop 启用 Kubernetes

使用 Docker Desktop 可以很方便的启用 Kubernetes。

### 14.3.1 启用 Kubernetes

在 Docker Desktop 设置页面，点击 `Kubernetes`，选择 `Enable Kubernetes`，稍等片刻，看到左下方 `Kubernetes` 变为 `running`，Kubernetes 启动成功。

![图](https://github.com/docker/docs/raw/main/assets/images/desktop/settings-kubernetes.png)

> 注意：Kubernetes 的镜像存储在 `registry.k8s.io`，如果国内网络无法直接访问，可以在 Docker Desktop 配置中的 `Docker Engine` 处配置镜像加速器，或者利用国内云服务商的镜像仓库手动拉取镜像并 retag。

### 14.3.2 测试

运行以下命令：

```bash
$ kubectl version
```

如果正常输出信息，则证明 Kubernetes 成功启动。
