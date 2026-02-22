## 常见错误速查表

相关信息如下表：

| 错误信息 / 现象 | 可能原因 | 解决方案 |
| :--- | :--- | :--- |
| `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?` | Docker 服务未启动 | Linux: `sudo systemctl start docker`<br>Mac/Win: 启动 Docker Desktop |
| `permission denied while trying to connect to the Docker daemon socket` | 当前用户不在 `docker` 用户组 | `sudo usermod -aG docker $USER` (需重新登录) |
| `manifest for ... not found: manifest unknown` | 镜像 tag 不存在 | 检查 Docker Hub 该镜像是否存在该 tag，或拼写是否正确 |
| `connection refused` (pull image) | 网络不通或镜像源无法访问 | 检查网络，配置[镜像加速器](../../03_install/3.9_mirror.md) |
| `Bind for 0.0.0.0:8080 failed: port is already allocated` | 端口被占用 | 检查占用端口的进程 (`lsof -i:8080`) 并杀掉，或换个端口映射 (`-p 8081:80`) |
| `exec user process caused "exec format error"` | 架构不匹配 (如在 x86 上跑 ARM 镜像) | 使用 `docker buildx` 构建多架构镜像，或拉取对应架构的镜像 |
| `standard_init_linux.go:211: exec user process caused "no such file or directory"` | 找不到解释器或依赖库 | 检查 `ENTRYPOINT`/`CMD` 脚本开头的 shebang (`#!/bin/sh` vs `#!/bin/bash`)，或确认二进制文件是否依赖缺失 (Alpine 常见缺少 glibc) |
| `iptables: No chain/target/match by that name` | 防火墙规则缺失或冲突 | 重启 Docker 服务重置 iptables 链: `sudo systemctl restart docker` |
| 容器内无法访问外网 | DNS 配置或转发问题 | 检查 `/etc/docker/daemon.json` 中的 DNS 配置 |
