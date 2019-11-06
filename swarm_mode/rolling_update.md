# SWarm mode 与滚动升级

在 [部署服务](deploy.md) 一节中我们使用 `nginx:1.13.7-alpine` 镜像部署了一个名为 `nginx` 的服务。

现在我们想要将 `NGINX` 版本升级到 `1.13.12`，那么在 Swarm mode 中如何升级服务呢？

你可能会想到，先停止原来的服务，再使用新镜像部署一个服务，不就完成服务的 “升级” 了吗。

这样做的弊端很明显，如果新部署的服务出现问题，原来的服务删除之后，很难恢复，那么在 Swarm mode 中到底该如何对服务进行滚动升级呢？

答案就是使用 `docker service update` 命令。

```bash
$ docker service update \
    --image nginx:1.13.12-alpine \
    nginx
```

以上命令使用 `--image` 选项更新了服务的镜像。当然我们也可以使用 `docker service update` 更新任意的配置。

`--secret-add` 选项可以增加一个密钥

`--secret-rm` 选项可以删除一个密钥

更多选项可以通过 `docker service update -h` 命令查看。

## 服务回退

现在假设我们发现 `nginx` 服务的镜像升级到 `nginx:1.13.12-alpine` 出现了一些问题，我们可以使用命令一键回退。

```bash
$ docker service rollback nginx
```

现在使用 `docker service ps` 命令查看 `nginx` 服务详情。

```bash
$ docker service ps nginx

ID                  NAME                IMAGE                  NODE                DESIRED STATE       CURRENT STATE                ERROR               PORTS
rt677gop9d4x        nginx.1             nginx:1.13.7-alpine   VM-20-83-debian     Running             Running about a minute ago
d9pw13v59d00         \_ nginx.1         nginx:1.13.12-alpine  VM-20-83-debian     Shutdown            Shutdown 2 minutes ago
i7ynkbg6ybq5         \_ nginx.1         nginx:1.13.7-alpine   VM-20-83-debian     Shutdown            Shutdown 2 minutes ago
```

结果的输出详细记录了服务的部署、滚动升级、回退的过程。
