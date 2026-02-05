# 安装 Fedora CoreOS

## 下载 ISO

在 [下载页面](https://getfedora.org/coreos/download/) `Bare Metal & Virtualized` 标签页下载 ISO。

## 编写 FCC

FCC 是 Fedora CoreOS Configuration （Fedora CoreOS 配置）的简称。

```yaml
# example.fcc
variant: fcos
version: 1.0.0
passwd:
  users:
    - name: core
      ssh_authorized_keys:
        - ssh-rsa AAAA...
```

将 `ssh-rsa AAAA...` 替换为自己的 SSH 公钥（位于 `~/.ssh/id_rsa.pub`）。

## 转换 FCC 为 Ignition

```bash
$ docker run -i --rm quay.io/coreos/fcct:v0.5.0 --pretty --strict < example.fcc > example.ign
```

## 挂载 ISO 启动虚拟机并安装

> 虚拟机需要分配 3GB 以上内存，否则会无法启动。

在虚拟机终端执行以下命令安装：

```bash
$ sudo coreos-installer install /dev/sda --ignition-file example.ign
```

安装之后重新启动即可使用。

## 使用

```bash
$ ssh core@虚拟机IP

$ docker --version
```

## 参考链接

* [官方文档](https://docs.fedoraproject.org/en-US/fedora-coreos/bare-metal/)
