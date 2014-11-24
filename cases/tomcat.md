## 建立 tomcat/weblogic 集群
### 安裝 tomcat 鏡像
準備好需要的 jdk、tomcat 等軟件放到 home 目錄下面，啟動一個容器
```
docker run -t -i -v /home:/opt/data  --name mk_tomcat ubuntu /bin/bash
```
這條命令掛載本地 home 目錄到容器的 /opt/data 目錄，容器內目錄若不存在，則會自動建立。接下來就是 tomcat 的基本設定，jdk 環境變量設置好之後，將 tomcat 程式放到 /opt/apache-tomcat 下面
編輯 /etc/supervisor/conf.d/supervisor.conf 文件，新增 tomcat 項
```
[supervisord]
nodaemon=true

[program:tomcat]
command=/opt/apache-tomcat/bin/startup.sh

[program:sshd]
command=/usr/sbin/sshd -D
docker commit  ac6474aeb31d  tomcat
```

新建 tomcat 文件夾，新建 Dockerfile。
```
FROM mk_tomcat
EXPOSE  22 8080
CMD ["/usr/bin/supervisord"]
```
根據 Dockerfile 建立鏡像。
```
docker build tomcat tomcat
```
### 安裝 weblogic 鏡像

步驟和 tomcat 基本一致，這裡貼一下設定文件
```
supervisor.conf
[supervisord]
nodaemon=true


[program:weblogic]
command=/opt/Middleware/user_projects/domains/base_domain/bin/startWebLogic.sh

[program:sshd]
command=/usr/sbin/sshd -D
dockerfile
FROM weblogic
EXPOSE  22 7001
CMD ["/usr/bin/supervisord"]
```

### tomcat/weblogic 鏡像的使用
#### 存儲的使用
在啟動的時候，使用 `-v` 參數

    -v, --volume=[]            Bind mount a volume (e.g. from the host: -v /host:/container, from docker: -v /container)

將本地磁盤映射到容器內部，它在主機和容器之間是實時變化的，所以我們更新程式、上傳代碼只需要更新物理主機的目錄就可以了

#### tomcat 和 weblogic 集群的實做
tomcat 只要開啟多個容器即可
```
docker run -d -v -p 204:22 -p 7003:8080 -v /home/data:/opt/data --name tm1 tomcat /usr/bin/supervisord
docker run -d -v -p 205:22 -p 7004:8080 -v /home/data:/opt/data --name tm2 tomcat /usr/bin/supervisord
docker run -d -v -p 206:22 -p 7005:8080 -v /home/data:/opt/data --name tm3 tomcat /usr/bin/supervisord
```

這裡說一下 weblogic 的設定，大家知道 weblogic 有一個域的概念。如果要使用常規的 administrator +node 的方式部署，就需要在 supervisord 中分別寫出 administartor server 和 node server 的啟動腳本，這樣做的優點是：
* 可以使用 weblogic 的集群，同步等概念
* 部署一個集群應用程式，只需要安裝一次應用到集群上即可

缺點是：
* Docker 設定復雜了
* 沒辦法自動擴展集群的計算容量，如需新增節點，需要在 administrator 上先建立節點，然後再設定新的容器 supervisor 啟動腳本，然後再啟動容器
另外種方法是將所有的程式都安裝在 adminiserver 上面，需要擴展的時候，啟動多個節點即可，它的優點和缺點和上一種方法恰恰相反。（建議使用這種方式來部署開發和測試環境）
```
docker run -d -v -p 204:22 -p 7001:7001 -v /home/data:/opt/data --name node1 weblogic /usr/bin/supervisord
docker run -d -v -p 205:22 -p 7002:7001 -v /home/data:/opt/data --name node2 weblogic /usr/bin/supervisord
docker run -d -v -p 206:22 -p 7003:7001 -v /home/data:/opt/data --name node3 weblogic /usr/bin/supervisord
```

這樣在前端使用 nginx 來做負載均衡就可以完成設定了
