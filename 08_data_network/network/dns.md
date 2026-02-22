## 配置 DNS

本节涵盖了相关内容与详细描述，主要探讨以下几个方面：

### 容器的 DNS 机制

Docker 容器的 DNS 配置有两种情况：

1. **默认 Bridge 网络**：继承宿主机的 DNS 配置 (`/etc/resolv.conf`)。
2. **自定义网络** (推荐)：使用 Docker 嵌入式 DNS 服务器 (Embedded DNS)，支持通过 **容器名** 进行服务发现。

---

### 嵌入式 DNS

这是 Docker 网络最强大的功能之一。在自定义网络中，容器可以通过 “名字” 找到彼此，而不需要知道对方的 IP (因为 IP 可能会变)。

```bash
## 1. 创建自定义网络

$ docker network create mynet

## 2. 启动容器 web 并加入网络

$ docker run -d --name web --network mynet nginx

## 3. 启动容器 client 并尝试 ping web

$ docker run -it --rm --network mynet alpine ping web
PING web (172.18.0.2): 56 data bytes
64 bytes from 172.18.0.2: seq=0 ttl=64 time=0.074 ms
```

**原理**：
Docker 守护进程在 `127.0.0.11` 运行了一个 DNS 服务器。容器内的 DNS 请求会被转发到这里。如果是容器名，解析为容器 IP；如果是外部域名 (如 google.com)，转发给上游 DNS。

---

### 配置 DNS 参数

如果你需要手动配置容器的 DNS (例如使用内网 DNS 服务器)，可以在 `docker run` 中使用以下参数：

#### 1. --dns

指定 DNS 服务器 IP。

```bash
$ docker run -it --dns=114.114.114.114 ubuntu cat /etc/resolv.conf
nameserver 114.114.114.114
```

#### 2. --dns-search

指定 DNS 搜索域。例如设置为 `example.com`，则 `ping host` 会尝试解析 `host.example.com`。

```bash
$ docker run --dns-search=example.com myapp
```

#### 3. --hostname (-h)

设置容器的主机名。

```bash
$ docker run -h myweb nginx
```

---

### 全局 DNS 配置

如果希望所有容器都使用特定的 DNS 服务器 (而不是继承宿主机)，可以修改 `/etc/docker/daemon.json`：

```json
{
  "dns": [
    "114.114.114.114",
    "8.8.8.8"
  ]
}
```

修改后需要重启 Docker 服务：`systemctl restart docker`。

---

### 常见问题

本节涵盖了相关内容与详细描述，主要探讨以下几个方面：

#### Q：容器无法解析域名

**现象**：`ping www.baidu.com` 失败，但 `ping 8.8.8.8` 成功。**解决**：

1. 宿主机的 `/etc/resolv.conf` 可能有问题 (例如使用了本地回环地址 127.0.0.53，特别是 Ubuntu 系统)。Docker 可能会尝试修复，但有时会失败。
2. 尝试手动指定 DNS：`docker run --dns 8.8.8.8 ...`
3. 检查防火墙是否拦截了 UDP 53 端口。

#### Q：无法通过容器名通信

**现象**：`ping db` 提示 `bad address 'db'`。**原因**：

- 你可能在使用 **默认的 bridge 网络**。默认 bridge 网络 **不支持** 通过容器名进行 DNS 解析 (这是一个历史遗留设计)。
- **解决**：使用自定义网络 (`docker network create ...`)。

---
