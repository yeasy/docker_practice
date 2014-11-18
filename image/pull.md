## 獲取鏡像

可以使用 `docker pull` 命令來從倉庫獲取所需要的鏡像。

下面的例子將從 Docker Hub 倉庫下載一個 Ubuntu 12.04 操作系統的鏡像。
```
$ sudo docker pull ubuntu:12.04
Pulling repository ubuntu
ab8e2728644c: Pulling dependent layers
511136ea3c5a: Download complete
5f0ffaa9455e: Download complete
a300658979be: Download complete
904483ae0c30: Download complete
ffdaafd1ca50: Download complete
d047ae21eeaf: Download complete
```
下載過程中，會輸出獲取鏡像的每一層信息。

該命令實際上相當於 `$ sudo docker pull registry.hub.docker.com/ubuntu:12.04` 命令，即從註冊服務器 `registry.hub.docker.com` 中的 `ubuntu` 倉庫來下載標記為 `12.04` 的鏡像。

有時候官方倉庫註冊服務器下載較慢，可以從其他倉庫下載。
從其它倉庫下載時需要指定完整的倉庫註冊服務器地址。例如
```
$ sudo docker pull dl.dockerpool.com:5000/ubuntu:12.04
Pulling dl.dockerpool.com:5000/ubuntu
ab8e2728644c: Pulling dependent layers
511136ea3c5a: Download complete
5f0ffaa9455e: Download complete
a300658979be: Download complete
904483ae0c30: Download complete
ffdaafd1ca50: Download complete
d047ae21eeaf: Download complete
```

完成後，即可隨時使用該鏡像了，例如創建一個容器，讓其中運行 bash 應用。
```
$ sudo docker run -t -i ubuntu:12.04 /bin/bash
root@fe7fc4bd8fc9:/#
```
