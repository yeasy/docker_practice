##啟動容器
啟動容器有兩種方式，一種是將映像檔新建一個容器並啟動，另外一個是將終止狀態（stopped）的容器重新啟動。

因為 Docker 的容器實在太輕量級了，使用者可以隨時刪除和新建立容器。

###新建並啟動
所需要的命令主要為 `docker run`。

例如，下面的命令輸出一個 “Hello World”，之後終止容器。
```
$ sudo docker run ubuntu:14.04 /bin/echo 'Hello world'
Hello world
```
這跟在本地直接執行 `/bin/echo 'hello world'` 相同， 幾乎感覺不出任何區別。

下面的命令則啟動一個 bash 終端，允許使用者進行交互。
```
$ sudo docker run -t -i ubuntu:14.04 /bin/bash
root@af8bae53bdd3:/#
```
其中，`-t` 選項讓Docker分配一個虛擬終端（pseudo-tty）並綁定到容器的標準輸入上， `-i` 則讓容器的標準輸入保持打開。

在交互模式下，使用者可以透過所建立的終端來輸入命令，例如
```
root@af8bae53bdd3:/# pwd
/
root@af8bae53bdd3:/# ls
bin boot dev etc home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var
```

當利用 `docker run` 來建立容器時，Docker 在後臺執行的標準操作包括：

* 檢查本地是否存在指定的映像檔，不存在就從公有倉庫下載
* 利用映像檔建立並啟動一個容器
* 分配一個文件系統，並在唯讀的映像檔層外面掛載一層可讀寫層
* 從宿主主機配置的網路橋接口中橋接一個虛擬埠到容器中去
* 從地址堆中配置一個 ip 地址給容器
* 執行使用者指定的應用程序
* 執行完畢後容器被終止

###啟動已終止容器
可以利用 `docker start` 命令，直接將一個已經終止的容器啟動執行。

容器的核心為所執行的應用程序，所需要的資源都是應用程序執行所必需的。除此之外，並沒有其它的資源。可以在偽終端中利用 `ps` 或 `top` 來查看程序信息。
```
root@ba267838cc1b:/# ps
  PID TTY          TIME CMD
    1 ?        00:00:00 bash
   11 ?        00:00:00 ps
```
可見，容器中僅執行了指定的 bash 應用。這種特點使得 Docker 對資源的使用率極高，是貨真價實的輕量級虛擬化。
