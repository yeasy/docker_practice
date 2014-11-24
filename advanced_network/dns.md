## 設定 DNS
Docker 沒有為每個容器專門定制鏡像，那麽怎麽自定義設定容器的主機名和 DNS 設定呢？
秘訣就是它利用虛擬文件來掛載到來容器的 3 個相關設定文件。

在容器中使用 mount 命令可以看到掛載訊息：
```
$ mount
...
/dev/disk/by-uuid/1fec...ebdf on /etc/hostname type ext4 ...
/dev/disk/by-uuid/1fec...ebdf on /etc/hosts type ext4 ...
tmpfs on /etc/resolv.conf type tmpfs ...
...
```
這種機制可以讓宿主主機 DNS 訊息發生更新後，所有 Docker 容器的 dns 設定透過 `/etc/resolv.conf` 文件立刻得到更新。

如果使用者想要手動指定容器的設定，可以利用下面的選項。

`-h HOSTNAME or --hostname=HOSTNAME`
設定容器的主機名，它會被寫到容器內的 `/etc/hostname` 和 `/etc/hosts`。但它在容器外部看不到，既不會在 `docker ps` 中顯示，也不會在其他的容器的 `/etc/hosts` 看到。

`--link=CONTAINER_NAME:ALIAS`
選項會在建立容器的時候，新增一個其他容器的主機名到 `/etc/hosts` 文件中，讓新容器的程式可以使用主機名 ALIAS 就可以連接它。

`--dns=IP_ADDRESS`
新增 DNS 伺服器到容器的 `/etc/resolv.conf` 中，讓容器用這個伺服器來解析所有不在 `/etc/hosts` 中的主機名。

`--dns-search=DOMAIN`
設定容器的搜索域，當設定搜索域為 `.example.com` 時，在搜索一個名為 host 的主機時，DNS 不僅搜索host，還會搜索 `host.example.com`。
註意：如果沒有上述最後 2 個選項，Docker 會默認用主機上的 `/etc/resolv.conf` 來設定容器。
