## Kubernetes 实战练习

本章将通过一个具体的案例：部署一个 Nginx 网站，并为其配置 Service 和 Ingress，来串联前面学到的知识。

### 目标

1.  部署一个 Nginx Deployment。
2.  创建一个 Service 暴露 Nginx。
3.  （可选）通过 Ingress 访问服务。

### 步骤 1：创建 Deployment

创建一个名为 `nginx-deployment.yaml` 的文件：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.24
        ports:
        - containerPort: 80
```

应用配置：

```bash
kubectl apply -f nginx-deployment.yaml
```

### 步骤 2：创建 Service

创建一个名为 `nginx-service.yaml` 的文件：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort # 使用 NodePort 方便本地测试
```

应用配置：

```bash
kubectl apply -f nginx-service.yaml
```

查看分配的端口：

```bash
kubectl get svc nginx-service
```

如果输出端口是 `80:30080/TCP`，你可以通过 `http://<NodeIP>:30080` 访问 Nginx。

### 步骤 3：模拟滚动更新 (Rolling Update)

修改 `nginx-deployment.yaml`，将镜像版本改为 `nginx:latest`。

```bash
kubectl apply -f nginx-deployment.yaml
```

观察更新过程：

```bash
kubectl rollout status deployment/nginx-deployment
```

### 步骤 4：清理资源

练习结束后，记得清理资源：

```bash
kubectl delete -f nginx-service.yaml
kubectl delete -f nginx-deployment.yaml
```
