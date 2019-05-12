## 镜像加速器

国内从 Docker Hub 拉取镜像有时会遇到困难，此时可以配置镜像加速器。国内很多云服务商都提供了国内加速器服务，例如：

* [Azure 中国镜像 `https://dockerhub.azk8s.cn`](https://github.com/Azure/container-service-for-azure-china/blob/master/aks/README.md#22-container-registry-proxy)
* [阿里云加速器(需登录账号获取)](https://cr.console.aliyun.com/cn-hangzhou/mirrors)
* [七牛云加速器 `https://reg-mirror.qiniu.com`](https://kirk-enterprise.github.io/hub-docs/#/user-guide/mirror)

> 由于镜像服务可能出现宕机，建议同时配置多个镜像。

> 国内各大云服务商均提供了 Docker 镜像加速服务，建议根据运行 Docker 的云平台选择对应的镜像加速服务，具体请参考官方文档。

我们以 Azure 中国镜像 `https://dockerhub.azk8s.cn` 为例进行介绍。

### Ubuntu 16.04+、Debian 8+、CentOS 7

对于使用 [systemd](https://www.freedesktop.org/wiki/Software/systemd/) 的系统，请在 `/etc/docker/daemon.json` 中写入如下内容（如果文件不存在请新建该文件）

```json
{
  "registry-mirrors": [
    "https://dockerhub.azk8s.cn",
    "https://reg-mirror.qiniu.com"
  ]
}
```

> 注意，一定要保证该文件符合 json 规范，否则 Docker 将不能启动。

之后重新启动服务。

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```

>注意：如果您之前查看旧教程，修改了 `docker.service` 文件内容，请去掉您添加的内容（`--registry-mirror=https://dockerhub.azk8s.cn`）。

### Windows 10

对于使用 Windows 10 的系统，在系统右下角托盘 Docker 图标内右键菜单选择 `Settings`，打开配置窗口后左侧导航菜单选择 `Daemon`。在 `Registry mirrors` 一栏中填写加速器地址 `https://dockerhub.azk8s.cn`，之后点击 `Apply` 保存后 Docker 就会重启并应用配置的镜像地址了。

### macOS

对于使用 macOS 的用户，在任务栏点击 Docker Desktop 应用图标 -> Perferences... -> Daemon -> Registry mirrors。在列表中填写加速器地址 `https://dockerhub.azk8s.cn`。修改完成之后，点击 `Apply & Restart` 按钮，Docker 就会重启并应用配置的镜像地址了。

### 检查加速器是否生效

执行 `$ docker info`，如果从结果中看到了如下内容，说明配置成功。

```bash
Registry Mirrors:
 https://dockerhub.azk8s.cn/
```

### gcr.io 镜像

国内无法直接获取 `gcr.io/*` 镜像，我们可以将 `gcr.io/<repo-name>/<image-name>:<version>` 替换为 `gcr.azk8s.cn/<repo-name>/<image-name>:<version>` ,例如

```bash
# docker pull gcr.io/google_containers/hyperkube-amd64:v1.9.2

docker pull gcr.azk8s.cn/google_containers/hyperkube-amd64:v1.9.2
```
