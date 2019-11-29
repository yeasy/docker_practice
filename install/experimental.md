# 开启实验特性

一些 docker 命令或功能仅当 **实验特性** 开启时才能使用，请按照以下方法进行设置。

## 开启 Docker CLI 的实验特性

编辑 `~/.docker/config.json` 文件，新增如下条目

```json
{
  "experimental": "enabled"
}
```

或者通过设置环境变量的方式：

**Linux/macOS**

```bash
$ export DOCKER_CLI_EXPERIMENTAL=enabled
```

**Windows**

```powershell
# 临时生效
$ set $env:DOCKER_CLI_EXPERIMENTAL="enabled"

# 永久生效
$ [environment]::SetEnvironmentvariable("DOCKER_CLI_EXPERIMENTAL","enabled","User")
```

## 开启 Dockerd 的实验特性

编辑 `/etc/docker/daemon.json`，新增如下条目

```json
{
  "experimental": true
}
```
