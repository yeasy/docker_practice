##建立鏡像

建立鏡像有很多方法，使用者可以從 Docker Hub 取得已有鏡像並更新，也可以利用本地文件系統建立一個。

### 修改已有鏡像
先使用下載的鏡像啟動容器。
```
$ sudo docker run -t -i training/sinatra /bin/bash
root@0b2616b0e5a8:/#
```
註意：記住容器的 ID，稍後還會用到。

在容器中新增 json 和 gem 兩個應用。
```
root@0b2616b0e5a8:/# gem install json
```
當結束後，我們使用 exit 來退出，現在我們的容器已經被我們改變了，使用 `docker commit` 命令來提交更新後的副本。
```
$ sudo docker commit -m "Added json gem" -a "Docker Newbee" 0b2616b0e5a8 ouruser/sinatra:v2
4f177bd27a9ff0f6dc2a830403925b5360bfe0b93d476f7fc3231110e7f71b1c
```
其中，`-m` 來指定提交的說明訊息，跟我們使用的版本控制工具一樣；`-a` 可以指定更新的使用者訊息；之後是用來建立鏡像的容器的 ID；最後指定目標鏡像的倉庫名和 tag 訊息。建立成功後會返回這個鏡像的 ID 訊息。


使用 `docker images` 來查看新建立的鏡像。
```
$ sudo docker images
REPOSITORY          TAG     IMAGE ID       CREATED       VIRTUAL SIZE
training/sinatra    latest  5bc342fa0b91   10 hours ago  446.7 MB
ouruser/sinatra     v2      3c59e02ddd1a   10 hours ago  446.7 MB
ouruser/sinatra     latest  5db5f8471261   10 hours ago  446.7 MB
```
之後，可以使用新的鏡像來啟動容器
```
$ sudo docker run -t -i ouruser/sinatra:v2 /bin/bash
root@78e82f680994:/#
```

###利用 Dockerfile 來建立鏡像
使用 `docker commit` 來擴展一個鏡像比較簡單，但是不方便在一個團隊中分享。我們可以使用 `docker build` 來建立一個新的鏡像。為此，首先需要建立一個 Dockerfile，包含一些如何建立鏡像的指令。

新建一個目錄和一個 Dockerfile
```
$ mkdir sinatra
$ cd sinatra
$ touch Dockerfile
```
Dockerfile 中每一條指令都建立鏡像的一層，例如：
```
# This is a comment
FROM ubuntu:14.04
MAINTAINER Docker Newbee <newbee@docker.com>
RUN apt-get -qq update
RUN apt-get -qqy install ruby ruby-dev
RUN gem install sinatra
```
Dockerfile 基本的語法是
* 使用`#`來註解
* `FROM` 指令告訴 Docker 使用哪個鏡像作為基礎
* 接著是維護者的訊息
* `RUN`開頭的指令會在建立中執行，比如安裝一個軟件包，在這裡使用 apt-get 來安裝了一些軟件

編寫完成 Dockerfile 後可以使用 `docker build` 來生成鏡像。

```
$ sudo docker build -t="ouruser/sinatra:v2" .
Uploading context  2.56 kB
Uploading context
Step 0 : FROM ubuntu:14.04
 ---> 99ec81b80c55
Step 1 : MAINTAINER Kate Smith <ksmith@example.com>
 ---> Running in 7c5664a8a0c1
 ---> 2fa8ca4e2a13
Removing intermediate container 7c5664a8a0c1
Step 2 : RUN apt-get -qq update
 ---> Running in b07cc3fb4256
 ---> 50d21070ec0c
Removing intermediate container b07cc3fb4256
Step 3 : RUN apt-get -qqy install ruby ruby-dev
 ---> Running in a5b038dd127e
Selecting previously unselected package libasan0:amd64.
(Reading database ... 11518 files and directories currently installed.)
Preparing to unpack .../libasan0_4.8.2-19ubuntu1_amd64.deb ...
Setting up ruby (1:1.9.3.4) ...
Setting up ruby1.9.1 (1.9.3.484-2ubuntu1) ...
Processing triggers for libc-bin (2.19-0ubuntu6) ...
 ---> 2acb20f17878
Removing intermediate container a5b038dd127e
Step 4 : RUN gem install sinatra
 ---> Running in 5e9d0065c1f7
. . .
Successfully installed rack-protection-1.5.3
Successfully installed sinatra-1.4.5
4 gems installed
 ---> 324104cde6ad
Removing intermediate container 5e9d0065c1f7
Successfully built 324104cde6ad
```
其中 `-t` 標記來新增 tag，指定新的鏡像的使用者訊息。
“.” 是 Dockerfile 所在的路徑（當前目錄），也可以替換為一個具體的 Dockerfile 的路徑。

可以看到 build 程式在執行操作。它要做的第一件事情就是上傳這個 Dockerfile 內容，因為所有的操作都要依據 Dockerfile 來進行。
然後，Dockfile 中的指令被一條一條的執行。每一步都建立了一個新的容器，在容器中執行指令並提交修改（就跟之前介紹過的 `docker commit` 一樣）。當所有的指令都執行完畢之後，返回了最終的鏡像 id。所有的中間步驟所產生的容器都被刪除和清理了。

*註意一個鏡像不能超過 127 層

此外，還可以利用 `ADD` 命令復制本地文件到鏡像；用 `EXPOSE` 命令來向外部開放端口；用 `CMD` 命令來描述容器啟動後執行的程式等。例如
```
# put my local web site in myApp folder to /var/www
ADD myApp /var/www
# expose httpd port
EXPOSE 80
# the command to run
CMD ["/usr/sbin/apachectl", "-D", "FOREGROUND"]
```

現在可以利用新建立的鏡像來啟動一個容器。
```
$ sudo docker run -t -i ouruser/sinatra:v2 /bin/bash
root@8196968dac35:/#
```
還可以用 `docker tag` 命令來修改鏡像的標簽。
```
$ sudo docker tag 5db5f8471261 ouruser/sinatra:devel
$ sudo docker images ouruser/sinatra
REPOSITORY          TAG     IMAGE ID      CREATED        VIRTUAL SIZE
ouruser/sinatra     latest  5db5f8471261  11 hours ago   446.7 MB
ouruser/sinatra     devel   5db5f8471261  11 hours ago   446.7 MB
ouruser/sinatra     v2      5db5f8471261  11 hours ago   446.7 MB
```

*註：更多用法，請參考 [Dockerfile](../dockerfile/README.md) 章節。

### 從本地文件系統導入
要從本地文件系統導入一個鏡像，可以使用 openvz（容器虛擬化的先鋒技術）的模板來建立：
openvz 的模板下載地址為 http://openvz.org/Download/templates/precreated。

比如，先下載了一個 ubuntu-14.04 的鏡像，之後使用以下命令導入：
```
sudo cat ubuntu-14.04-x86_64-minimal.tar.gz  |docker import - ubuntu:14.04
```
然後查看新導入的鏡像。
```
docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu              14.04               05ac7c0b9383        17 seconds ago      215.5 MB
```

###上傳鏡像
使用者可以透過 `docker push` 命令，把自己建立的鏡像上傳到倉庫中來共享。例如，使用者在 Docker Hub 上完成註冊後，可以推送自己的鏡像到倉庫中。
```
$ sudo docker push ouruser/sinatra
The push refers to a repository [ouruser/sinatra] (len: 1)
Sending image list
Pushing repository ouruser/sinatra (3 tags)
```
