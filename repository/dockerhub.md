## Docker Hub
目前 Docker 官方維護了一個公共倉庫 [Docker Hub](https://hub.docker.com/)，其中已經包括了超過 15,000 的映像檔。大部分需求，都可以透過在 Docker Hub 中直接下載映像檔來實作。

### 登錄
可以透過執行 `docker login` 命令來輸入使用者名稱、密碼和電子信箱來完成註冊和登錄。
註冊成功後，本地使用者目錄的 `.dockercfg` 中將保存使用者的認證訊息。

### 基本操作
使用者無需登錄即可透過 `docker search` 命令來查詢官方倉庫中的映像檔，並利用 `docker pull` 命令來將它下載到本地。

例如以 centos 為關鍵字進行搜索：
```
$ sudo docker search centos
NAME                                            DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
centos                                          The official build of CentOS.                   465       [OK]
tianon/centos                                   CentOS 5 and 6, created using rinse instea...   28
blalor/centos                                   Bare-bones base CentOS 6.5 image                6                    [OK]
saltstack/centos-6-minimal                                                                      6                    [OK]
tutum/centos-6.4                                DEPRECATED. Use tutum/centos:6.4 instead. ...   5                    [OK]
...
```
可以看到顯示了很多包含關鍵字的映像檔，其中包括映像檔名字、描述、星級（表示該映像檔的受歡迎程度）、是否官方建立、是否自動建立。
官方的映像檔說明是官方項目組建立和維護的，automated 資源允許使用者驗證映像檔的來源和內容。

根據是否是官方提供，可將映像檔資源分為兩類。
一種是類似 centos 這樣的基礎映像檔，被稱為基礎或根映像檔。這些基礎映像檔是由 Docker 公司建立、驗證、支持、提供。這樣的映像檔往往使用單個單詞作為名字。
還有一種類型，比如 `tianon/centos` 映像檔，它是由 Docker 的使用者建立並維護的，往往帶有使用者名稱前綴。可以透過前綴 `user_name/` 來指定使用某個使用者提供的映像檔，比如 tianon 使用者。

另外，在查詢的時候透過 `-s N` 參數可以指定僅顯示評價為 `N` 星以上的映像檔。

下載官方 centos 映像檔到本地。
```
$ sudo docker pull centos
Pulling repository centos
0b443ba03958: Download complete
539c0211cd76: Download complete
511136ea3c5a: Download complete
7064731afe90: Download complete
```
使用者也可以在登錄後透過 `docker push` 命令來將映像檔推送到 Docker Hub。

### 自動建立
自動建立（Automated Builds）功能對於需要經常升級映像檔內程式來說，十分方便。
有時候，使用者建立了映像檔，安裝了某個軟體，如果軟體發布新版本則需要手動更新映像檔。。

而自動建立允許使用者透過 Docker Hub 指定跟蹤一個目標網站（目前支持 [GitHub](github.org) 或 [BitBucket](bitbucket.org)）上的項目，一旦項目發生新的提交，則自動執行建立。

要設定自動建立，包括以下的步驟：
* 建立並登陸 Docker Hub，以及目標網站；
* 在目標網站中連接帳戶到 Docker Hub；
* 在 Docker Hub 中 [設定一個自動建立](https://registry.hub.docker.com/builds/add/)；
* 選取一個目標網站中的項目（需要含 Dockerfile）和分支；
* 指定 Dockerfile 的位置，並提交建立。

之後，可以 在Docker Hub 的 [自動建立頁面](https://registry.hub.docker.com/builds/) 中跟蹤每次建立的狀態。
