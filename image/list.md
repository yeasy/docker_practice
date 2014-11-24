## 列出本地鏡像
使用 `docker images` 顯示本地已有的鏡像。
```
$ sudo docker images
REPOSITORY       TAG      IMAGE ID      CREATED      VIRTUAL SIZE
ubuntu           12.04    74fe38d11401  4 weeks ago  209.6 MB
ubuntu           precise  74fe38d11401  4 weeks ago  209.6 MB
ubuntu           14.04    99ec81b80c55  4 weeks ago  266 MB
ubuntu           latest   99ec81b80c55  4 weeks ago  266 MB
ubuntu           trusty   99ec81b80c55  4 weeks ago  266 MB
...
```

在列出訊息中，可以看到幾段文字訊息

* 來自於哪個倉庫，比如 ubuntu
* 鏡像的標記，比如 14.04
* 它的 `ID` 號（唯一）
* 建立時間
* 鏡像大小

其中鏡像的 `ID` 唯一標識了鏡像，注意到 `ubuntu:14.04` 和 `ubuntu:trusty` 具有相同的鏡像 `ID`，說明它們實際上是同一鏡像。

`TAG` 訊息用來標記來自同一個倉庫的不同鏡像。例如 `ubuntu` 倉庫中有多個鏡像，透過 `TAG` 訊息來區分發行版本，例如 `10.04`、`12.04`、`12.10`、`13.04`、`14.04` 等。例以下面的命令指定使用鏡像 `ubuntu:14.04` 來啟動一個容器。
```
$ sudo docker run -t -i ubuntu:14.04 /bin/bash
```

如果不指定具體的標記，則預設使用 `latest` 
