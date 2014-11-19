## 使用 Supervisor 來管理程序
Docker 容器在啟動的時候開啟單個程序，比如，一個 ssh 或者 apache 的 daemon 服務。但我們經常需要在一個機器上開啟多個服務，這可以有很多方法，最簡單的就是把多個啟動命令方到一個啟動腳本裏面，啟動的時候直接啟動這個腳本，另外就是安裝程序管理工具。

本小節將使用程序管理工具 supervisor 來管理容器中的多個程序。使用 Supervisor 可以更好的控制、管理、重啟我們希望執行的程序。在這裏我們演示一下如何同時使用 ssh 和 apache 服務。

### 配置
首先創建一個 Dockerfile，內容和各部分的解釋如下。
```
FROM ubuntu:13.04
MAINTAINER examples@docker.com
RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade -y
```

### 安裝 supervisor
安裝 ssh、apache 和 supervisor。
```
RUN apt-get install -y openssh-server apache2 supervisor
RUN mkdir -p /var/run/sshd
RUN mkdir -p /var/log/supervisor
```

這裏安裝 3 個軟件，還創建了 2 個 ssh 和 supervisor 服務正常執行所需要的目錄。
```
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
```
添加 supervisord 的配置文件，並復制配置文件到對應目錄下面。

```
EXPOSE 22 80
CMD ["/usr/bin/supervisord"]
```
這裏我們映射了 22 和 80 端口，使用 supervisord 的可執行路徑啟動服務。


### supervisor配置文件內容
```
[supervisord]
nodaemon=true
[program:sshd]
command=/usr/sbin/sshd -D

[program:apache2]
command=/bin/bash -c "source /etc/apache2/envvars && exec /usr/sbin/apache2 -DFOREGROUND"
```
配置文件包含目錄和程序，第一段 supervsord 配置軟件本身，使用 nodaemon 參數來執行。第二段包含要控制的 2 個服務。每一段包含一個服務的目錄和啟動這個服務的命令。

### 使用方法
創建鏡像。
```
$ sudo docker build -t test/supervisord .
```
啟動 supervisor 容器。
```
$ sudo docker run -p 22 -p 80 -t -i test/supervisords
2013-11-25 18:53:22,312 CRIT Supervisor running as root (no user in config file)
2013-11-25 18:53:22,312 WARN Included extra file "/etc/supervisor/conf.d/supervisord.conf" during parsing
2013-11-25 18:53:22,342 INFO supervisord started with pid 1
2013-11-25 18:53:23,346 INFO spawned: 'sshd' with pid 6
2013-11-25 18:53:23,349 INFO spawned: 'apache2' with pid 7
```
使用 `docker run` 來啟動我們創建的容器。使用多個 `-p` 來映射多個端口，這樣我們就能同時訪問 ssh 和 apache 服務了。

可以使用這個方法創建一個只有 ssh 服務的基礎鏡像，之後創建鏡像可以使用這個鏡像為基礎來創建
