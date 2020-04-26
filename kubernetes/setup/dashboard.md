# Kubernetes Dashboard

[Kubernetes Dashboard](https://github.com/kubernetes/dashboard) 是基于网页的 Kubernetes 用户界面。

![](https://d33wubrfki0l68.cloudfront.net/349824f68836152722dab89465835e604719caea/6e0b7/images/docs/ui-dashboard.png)

## 部署

执行以下命令即可部署 Dashboard：

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0/aio/deploy/recommended.yaml
```

## 访问

通过命令行代理访问，执行以下命令：

```bash
$ kubectl proxy
```

到 http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/ 即可访问。

## 登录

目前，Dashboard 仅支持使用 Bearer 令牌登录。下面教大家如何创建该令牌：

```bash
$ kubectl create sa dashboard-admin -n kube-system

$ kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=kube-system:dashboard-admin

$ ADMIN_SECRET=$(kubectl get secrets -n kube-system | grep dashboard-admin | awk '{print $1}')

$ DASHBOARD_LOGIN_TOKEN=$(kubectl describe secret -n kube-system ${ADMIN_SECRET} | grep -E '^token' | awk '{print $2}')

echo ${DASHBOARD_LOGIN_TOKEN}
```

将结果粘贴到登录页面，即可登录。

## 参考文档

* [官方文档](https://kubernetes.io/zh/docs/tasks/access-application-cluster/web-ui-dashboard/)
