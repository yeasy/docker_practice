# 开启实验特性

一些 docker 命令或功能仅当 **实验特性** 开启时才能使用，请按照以下方法进行设置。

## Docker CLI 的实验特性

从 `v20.10` 版本开始，Docker CLI 所有实验特性的命令均默认开启，无需再进行配置或设置系统环境变量。

## 开启 dockerd 的实验特性

编辑 `/etc/docker/daemon.json`，新增如下条目

```json
{
  "experimental": true
}
```
