## 配置加速器

由于伟大的墙，在国内访问 Docker Hub 时可能会遇到困难，因此在国内使用 Docker 的时候一般需要配置加速器。国内一些云服务商提供了加速器服务：

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

### 检查加速器是否生效

配置完加速器需要检查是否生效，在命令行执行 `ps -ef | grep dockerd`，如果从结果中看到了配置的 `--registry-mirror` 参数说明配置成功。

```bash
$ sudo ps -ef | grep dockerd
root      5346     1  0 19:03 ?        00:00:00 /usr/bin/dockerd --registry-mirror=https://jxus37ad.mirror.aliyuncs.com
$
```
