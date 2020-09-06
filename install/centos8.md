# CentOS8 安装 Docker CE

当前官方版本的 Docker CE [尚未支持][docker-docker] CentOS8，我们可以使用 Moby 项目维护者 AkihiroSuda 所构建的包，具体请参考 https://github.com/AkihiroSuda/moby-snapshot。

[docker-docker]:https://download.docker.com/linux/centos/

## 设置

由于 CentOS8 防火墙使用了 `nftables`，我们可以使用如下设置使用 `iptables`

更改 `/etc/firewalld/firewalld.conf`

```bash
# FirewallBackend=nftables
FirewallBackend=iptables
```

或者执行如下命令：

```bash
$ firewall-cmd --permanent --zone=trusted --add-interface=docker0

$ firewall-cmd --reload
```

## 参考链接

* https://firewalld.org/2018/07/nftables-backend
* https://github.com/moby/libnetwork/issues/2496
