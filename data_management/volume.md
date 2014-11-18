## 數據卷
數據卷是一個可供一個或多個容器使用的特殊目錄，它繞過 UFS，可以提供很多有用的特性：
* 數據卷可以在容器之間共享和重用
* 對數據卷的修改會立馬生效
* 對數據卷的更新，不會影響鏡像
* 卷會一直存在，直到沒有容器使用

*數據卷的使用，類似於 Linux 下對目錄或文件進行 mount。


### 創建一個數據卷
在用 `docker run` 命令的時候，使用 `-v` 標記來創建一個數據卷並掛載到容器裏。在一次 run 中多次使用可以掛載多個數據卷。

下面創建一個 web 容器，並加載一個數據卷到容器的 `/webapp` 目錄。
```
$ sudo docker run -d -P --name web -v /webapp training/webapp python app.py
```
*註意：也可以在 Dockerfile 中使用 `VOLUME` 來添加一個或者多個新的卷到由該鏡像創建的任意容器。

### 掛載一個主機目錄作為數據卷
使用 `-v` 標記也可以指定掛載一個本地主機的目錄到容器中去。
```
$ sudo docker run -d -P --name web -v /src/webapp:/opt/webapp training/webapp python app.py
```
上面的命令加載主機的 `/src/webapp` 目錄到容器的 `/opt/webapp`
目錄。這個功能在進行測試的時候十分方便，比如用戶可以放置一些程序到本地目錄中，來查看容器是否正常工作。本地目錄的路徑必須是絕對路徑，如果目錄不存在 Docker 會自動為你創建它。

*註意：Dockerfile 中不支持這種用法，這是因為 Dockerfile 是為了移植和分享用的。然而，不同操作系統的路徑格式不一樣，所以目前還不能支持。

Docker 掛載數據卷的默認權限是讀寫，用戶也可以通過 `:ro` 指定為只讀。
```
$ sudo docker run -d -P --name web -v /src/webapp:/opt/webapp:ro
training/webapp python app.py
```
加了 `:ro` 之後，就掛載為只讀了。

### 掛載一個本地主機文件作為數據卷
`-v` 標記也可以從主機掛載單個文件到容器中
```
$ sudo docker run --rm -it -v ~/.bash_history:/.bash_history ubuntu /bin/bash
```
這樣就可以記錄在容器輸入過的命令了。

*註意：如果直接掛載一個文件，很多文件編輯工具，包括 `vi` 或者 `sed --in-place`，可能會造成文件 inode 的改變，從 Docker 1.1
.0起，這會導致報錯誤信息。所以最簡單的辦法就直接掛載文件的父目錄。
