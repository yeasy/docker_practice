## 私有倉庫

有時候使用 Docker Hub 這樣的公共倉庫可能不方便，用戶可以創建一個本地倉庫供私人使用。

本節介紹如何使用本地倉庫。

`docker-registry` 是官方提供的工具，可以用於構建私有的鏡像倉庫。
### 安裝運行 docker-registry
#### 容器運行
在安裝了 Docker 後，可以通過獲取官方 registry 鏡像來運行。
```
$ sudo docker run -d -p 5000:5000 registry
```
這將使用官方的 registry 鏡像來啟動本地的私有倉庫。
用戶可以通過指定參數來配置私有倉庫位置，例如配置鏡像存儲到 Amazon S3 服務。
```
$ sudo docker run \
         -e SETTINGS_FLAVOR=s3 \
         -e AWS_BUCKET=acme-docker \
         -e STORAGE_PATH=/registry \
         -e AWS_KEY=AKIAHSHB43HS3J92MXZ \
         -e AWS_SECRET=xdDowwlK7TJajV1Y7EoOZrmuPEJlHYcNP2k4j49T \
         -e SEARCH_BACKEND=sqlalchemy \
         -p 5000:5000 \
         registry
````
此外，還可以指定本地路徑（如 `/home/user/registry-conf` ）下的配置文件。
```
$ sudo docker run -d -p 5000:5000 -v /home/user/registry-conf:/registry-conf -e DOCKER_REGISTRY_CONFIG=/registry-conf/config.yml registry
```
默認情況下，倉庫會被創建在容器的 `/tmp/registry` 下。可以通過 `-v` 參數來將鏡像文件存放在本地的指定路徑。
例如下面的例子將上傳的鏡像放到 `/opt/data/registry` 目錄。
```
$ sudo docker run -d -p 5000:5000 -v /opt/data/registry:/tmp/registry registry
```

#### 本地安裝
對於 Ubuntu 或 CentOS 等發行版，可以直接通過源安裝。
* Ubuntu
```
$ sudo apt-get install -y build-essential python-dev libevent-dev python-pip liblzma-dev
$ sudo pip install docker-registry
```
* CentOS
```
$ sudo yum install -y python-devel libevent-devel python-pip gcc xz-devel
$ sudo python-pip install docker-registry
```

也可以從 [docker-registry](https://github.com/docker/docker-registry) 項目下載源碼進行安裝。
```
$ sudo apt-get install build-essential python-dev libevent-dev python-pip libssl-dev liblzma-dev libffi-dev
$ git clone https://github.com/docker/docker-registry.git
$ cd docker-registry
$ sudo python setup.py install
```
然後修改配置文件，主要修改 dev 模板段的 `storage_path` 到本地的存儲倉庫的路徑。
```
$ cp config/config_sample.yml config/config.yml
```
之後啟動 Web 服務。
```
$ sudo gunicorn -c contrib/gunicorn.py docker_registry.wsgi:application
```
或者
```
$ sudo gunicorn --access-logfile - --error-logfile - -k gevent -b 0.0.0.0:5000 -w 4 --max-requests 100 docker_registry.wsgi:application
```
此時使用訪問本地的 5000 端口，看到輸出 docker-registry 的版本信息說明運行成功。

*註：`config/config_sample.yml` 文件是示例配置文件。

###在私有倉庫上傳、下載、搜索鏡像
創建好私有倉庫之後，就可以使用 `docker tag` 來標記一個鏡像，然後推送它到倉庫，別的機器上就可以下載下來了。例如私有倉庫地址為 `192.168.7.26:5000`。

先在本機查看已有的鏡像。
```
$ sudo docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu                            latest              ba5877dc9bec        6 weeks ago         192.7 MB
ubuntu                            14.04               ba5877dc9bec        6 weeks ago         192.7 MB
```

使用`docker tag` 將 `ba58` 這個鏡像標記為 `192.168.7.26:5000/test`（格式為 `docker tag IMAGE[:TAG] [REGISTRYHOST/][USERNAME/]NAME[:TAG]`）。
```
$ sudo docker tag ba58 192.168.7.26:5000/test
root ~ # docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu                            14.04               ba5877dc9bec        6 weeks ago         192.7 MB
ubuntu                            latest              ba5877dc9bec        6 weeks ago         192.7 MB
192.168.7.26:5000/test            latest              ba5877dc9bec        6 weeks ago         192.7 MB
```
使用 `docker push` 上傳標記的鏡像。
```
$ sudo docker push 192.168.7.26:5000/test
The push refers to a repository [192.168.7.26:5000/test] (len: 1)
Sending image list
Pushing repository 192.168.7.26:5000/test (1 tags)
Image 511136ea3c5a already pushed, skipping
Image 9bad880da3d2 already pushed, skipping
Image 25f11f5fb0cb already pushed, skipping
Image ebc34468f71d already pushed, skipping
Image 2318d26665ef already pushed, skipping
Image ba5877dc9bec already pushed, skipping
Pushing tag for rev [ba5877dc9bec] on {http://192.168.7.26:5000/v1/repositories/test/tags/latest}
```
用 curl 查看倉庫中的鏡像。
```
$ curl http://192.168.7.26:5000/v1/search
{"num_results": 7, "query": "", "results": [{"description": "", "name": "library/miaxis_j2ee"}, {"description": "", "name": "library/tomcat"}, {"description": "", "name": "library/ubuntu"}, {"description": "", "name": "library/ubuntu_office"}, {"description": "", "name": "library/desktop_ubu"}, {"description": "", "name": "dockerfile/ubuntu"}, {"description": "", "name": "library/test"}]}
```
這裏可以看到 `{"description": "", "name": "library/test"}`，表明鏡像已經被成功上傳了。

現在可以到另外一臺機器去下載這個鏡像。
```
$ sudo docker pull 192.168.7.26:5000/test
Pulling repository 192.168.7.26:5000/test
ba5877dc9bec: Download complete
511136ea3c5a: Download complete
9bad880da3d2: Download complete
25f11f5fb0cb: Download complete
ebc34468f71d: Download complete
2318d26665ef: Download complete
$ sudo docker images
REPOSITORY                         TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
192.168.7.26:5000/test             latest              ba5877dc9bec        6 weeks ago         192.7 MB
```

可以使用 [這個腳本](https://github.com/yeasy/docker_practice/raw/master/_local/push_images.sh) 批量上傳本地的鏡像到註冊服務器中，默認是本地註冊服務器 `127.0.0.1:5000`。例如：
```
$ wget https://github.com/yeasy/docker_practice/raw/master/_local/push_images.sh; sudo chmod a+x push_images.sh
$ ./push_images.sh ubuntu:latest centos:centos7
The registry server is 127.0.0.1
Uploading ubuntu:latest...
The push refers to a repository [127.0.0.1:5000/ubuntu] (len: 1)
Sending image list
Pushing repository 127.0.0.1:5000/ubuntu (1 tags)
Image 511136ea3c5a already pushed, skipping
Image bfb8b5a2ad34 already pushed, skipping
Image c1f3bdbd8355 already pushed, skipping
Image 897578f527ae already pushed, skipping
Image 9387bcc9826e already pushed, skipping
Image 809ed259f845 already pushed, skipping
Image 96864a7d2df3 already pushed, skipping
Pushing tag for rev [96864a7d2df3] on {http://127.0.0.1:5000/v1/repositories/ubuntu/tags/latest}
Untagged: 127.0.0.1:5000/ubuntu:latest
Done
Uploading centos:centos7...
The push refers to a repository [127.0.0.1:5000/centos] (len: 1)
Sending image list
Pushing repository 127.0.0.1:5000/centos (1 tags)
Image 511136ea3c5a already pushed, skipping
34e94e67e63a: Image successfully pushed
70214e5d0a90: Image successfully pushed
Pushing tag for rev [70214e5d0a90] on {http://127.0.0.1:5000/v1/repositories/centos/tags/centos7}
Untagged: 127.0.0.1:5000/centos:centos7
Done
```
