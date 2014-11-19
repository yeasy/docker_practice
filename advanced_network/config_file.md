## 編輯網絡配置文件

Docker 1.2.0 開始支持在運行中的容器裏編輯 `/etc/hosts`, `/etc/hostname` 和 `/etc/resolve.conf` 文件。

但是這些修改是臨時的，只在運行的容器中保留，容器終止或重啟後並不會被保存下來。也不會被 `docker commit` 提交。
