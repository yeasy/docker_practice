## 快速配置指南

下面是一個跟 Docker 網路相關的命令列表。

其中有些命令選項只有在 Docker 服務啟動的時候才能配置，而且不能馬上生效。
* `-b BRIDGE or --bridge=BRIDGE` --指定容器掛載的網橋
* `--bip=CIDR` --定制 docker0 的掩碼
* `-H SOCKET... or --host=SOCKET...` --Docker 服務端接收命令的通道
* `--icc=true|false` --是否支持容器之間進行通信
* `--ip-forward=true|false` --請看下文容器之間的通信
* `--iptables=true|false` --禁止 Docker 新增 iptables 規則
* `--mtu=BYTES` --容器網路中的 MTU

下面2個命令選項既可以在啟動服務時指定，也可以 Docker 容器啟動（`docker run`）時候指定。在 Docker 服務啟動的時候指定則會成為默認值，後面執行 `docker run` 時可以覆蓋設置的默認值。
* `--dns=IP_ADDRESS...` --使用指定的DNS服務器
* `--dns-search=DOMAIN...` --指定DNS搜索域

最後這些選項只有在 `docker run` 執行時使用，因為它是針對容器的特性內容。
* `-h HOSTNAME or --hostname=HOSTNAME` --配置容器主機名
* `--link=CONTAINER_NAME:ALIAS` --新增到另一個容器的連接
* `--net=bridge|none|container:NAME_or_ID|host` --配置容器的橋接模式
* `-p SPEC or --publish=SPEC` --映射容器端口到宿主主機
* `-P or --publish-all=true|false` --映射容器所有端口到宿主主機
