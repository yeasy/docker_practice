# CoreOS 工具介绍

`CoreOS` 内置了 `服务发现`，`容器管理` 工具。

## 服务发现

`CoreOS` 的第一个重要组件就是使用 `etcd` 来实现的服务发现。

如果你使用默认的样例 `cloud-config` 文件，那么 `etcd` 会在启动时自动运行。

```yml
#cloud-config

hostname: coreos0
ssh_authorized_keys:
  - ssh-rsa AAAA...
coreos:
  units:
    - name: etcd.service
      command: start
    - name: fleet.service
      command: start
  etcd:
    name: coreos0
    discovery: https://discovery.etcd.io/<token>
```

配置文件里有一个 `token`，你可以通过访问 https://discovery.etcd.io/new 来获取一个包含你 `teoken` 的 URL。

## 容器管理

第二个组件就是 `Docker`，它用来运行你的代码和应用。`CoreOS` 内置 `Docker`，具体使用请参考本书其他章节。

`CoreOS` 也内置了由自己开发的容器 `Rkt`，`Rkt` 不属于本书的讨论范围，这里不再赘述。
