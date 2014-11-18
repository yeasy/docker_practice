## 數據卷容器
如果你有一些持續更新的數據需要在容器之間共享，最好創建數據卷容器。

數據卷容器，其實就是一個正常的容器，專門用來提供數據卷供其它容器掛載的。

首先，創建一個命名的數據卷容器 dbdata：
```
$ sudo docker run -d -v /dbdata --name dbdata training/postgres echo Data-only container for postgres
```
然後，在其他容器中使用 `--volumes-from` 來掛載 dbdata 容器中的數據卷。
```
$ sudo docker run -d --volumes-from dbdata --name db1 training/postgres
$ sudo docker run -d --volumes-from dbdata --name db2 training/postgres
```
還可以使用多個 `--volumes-from` 參數來從多個容器掛載多個數據卷。
也可以從其他已經掛載了容器卷的容器來掛載數據卷。
```
$ sudo docker run -d --name db3 --volumes-from db1 training/postgres
```
*註意：使用 `--volumes-from` 參數所掛載數據卷的容器自己並不需要保持在運行狀態。

如果刪除了掛載的容器（包括 dbdata、db1 和 db2），數據卷並不會被自動刪除。如果要刪除一個數據卷，必須在刪除最後一個還掛載著它的容器時使用 `docker rm -v` 命令來指定同時刪除關聯的容器。
這可以讓用戶在容器之間升級和移動數據卷。具體的操作將在下一節中進行講解。
