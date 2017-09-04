## 镜像加速器

国内访问 Docker Hub 有时会遇到困难，此时可以配置镜像加速器。Docker官方和国内很多云服务商都提供了加速器服务，例如：

* [Docker 官方提供的中国registry mirror](https://docs.docker.com/registry/recipes/mirror/#use-case-the-china-registry-mirror)
* [阿里云加速器](https://cr.console.aliyun.com/#/accelerator)
* [DaoCloud 加速器](https://www.daocloud.io/mirror#accelerator-doc)
* [灵雀云加速器](http://docs.alauda.cn/feature/accelerator.html)

注册用户并且申请加速器，会获得如 `https://jxus37ad.mirror.aliyuncs.com` 这样的地址。我们需要将其配置给 Docker 引擎。

### Ubuntu 14.04、Debian 7 Wheezy

对于使用 [upstart](http://upstart.ubuntu.com/) 的系统而言，编辑 `/etc/default/docker` 文件，在其中的 `DOCKER_OPTS` 中添加获得的加速器配置 `--registry-mirror=<加速器地址>`，如：

```bash
DOCKER_OPTS="--registry-mirror=https://jxus37ad.mirror.aliyuncs.com"
```

重新启动服务。

```bash
$ sudo service docker restart
```

### Ubuntu 16.04、Debian 8 Jessie、CentOS 7

对于使用 [systemd](https://www.freedesktop.org/wiki/Software/systemd/) 的系统，用 `systemctl enable docker` 启用服务后，编辑 `/etc/systemd/system/multi-user.target.wants/docker.service` 文件，找到 `ExecStart=` 这一行，在这行最后添加加速器地址 `--registry-mirror=<加速器地址>`，如：

```bash
ExecStart=/usr/bin/dockerd --registry-mirror=https://jxus37ad.mirror.aliyuncs.com
```

*注：对于 1.12 以前的版本，`dockerd` 换成 `docker daemon`。*

重新加载配置并且重新启动。

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```

### Windows 10
对于使用 WINDOWS 10 的系统，在系统右下角托盘图标内右键菜单选择 `Settings`，打开配置窗口后左侧导航菜单选择 `Docker Daemon`。编辑窗口内的JSON串，填写如阿里云、DaoCloud之类的加速器地址，如：

```bash
{
  "registry-mirrors": [
    "https://sr5arhkn.mirror.aliyuncs.com",
    "http://14d216f4.m.daocloud.io"
  ],
  "insecure-registries": []
}
```
编辑完成，点击Apply保存后Docker服务会重新启动。

### macOS

对于macOS的用户，如果你使用的是**Docker for Mac**，那配置起来很简单。在任务栏点击应用图标 -> Perferences... -> Daemon -> Registry mirrors。在列表中添加云服务商提供的加速器地址即可。修改完成之后，点击`Apply & Restart`按钮，Docker就会重启并应用配置的镜像地址了。

如果你使用的是**Docker Toolbox**。先看看你的系统版本，如果是macOS 10.1以上的，那么请改用Docker for Mac，这个在性能上超过Docker Toolbox一大截，具体可以看看官网的这篇文章：[Docker for Mac vs. Docker Toolbox](https://docs.docker.com/docker-for-mac/docker-toolbox/)。如果系统版本没达到，或者因为历史原因必须使用Docker Toolbox的话。

```bash
docker-machine ssh default
sudo sed -i "s|EXTRA_ARGS='|EXTRA_ARGS='--registry-mirror=加速地址 |g" /var/lib/boot2docker/profile
exit
docker-machine restart default
```

关于Docker Toolbox配置的内容参考自DaoCloud的文档:[Docker 加速器](http://guide.daocloud.io/dcs/daocloud-9153151.html#docker-toolbox)

### 检查加速器是否生效

Linux系统下配置完加速器需要检查是否生效，在命令行执行 `ps -ef | grep dockerd`，如果从结果中看到了配置的 `--registry-mirror` 参数说明配置成功。

```bash
$ sudo ps -ef | grep dockerd
root      5346     1  0 19:03 ?        00:00:00 /usr/bin/dockerd --registry-mirror=https://jxus37ad.mirror.aliyuncs.com
$
```
如果`Docker`版本大于1.13或17.05.0-ce，也可以
```bash
$ sudo docker info|grep "Registry Mirrors" -A 1
Registry Mirrors:
 https://registry.docker-cn.com/
```
