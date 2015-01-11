## 私有仓库

有时候使用 Docker Hub 这样的公共仓库可能不方便，用户可以创建一个本地仓库供私人使用。

本节介绍如何使用本地仓库。

`docker-registry` 是官方提供的工具，可以用于构建私有的镜像仓库。
### 安装运行 docker-registry
#### 容器运行
在安装了 Docker 后，可以通过获取官方 registry 镜像来运行。
```
$ sudo docker run -d -p 5000:5000 registry
```
这将使用官方的 registry 镜像来启动本地的私有仓库。
用户可以通过指定参数来配置私有仓库位置，例如配置镜像存储到 Amazon S3 服务。
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
此外，还可以指定本地路径（如 `/home/user/registry-conf` ）下的配置文件。
```
$ sudo docker run -d -p 5000:5000 -v /home/user/registry-conf:/registry-conf -e DOCKER_REGISTRY_CONFIG=/registry-conf/config.yml registry
```
默认情况下，仓库会被创建在容器的 `/tmp/registry` 下。可以通过 `-v` 参数来将镜像文件存放在本地的指定路径。
例如下面的例子将上传的镜像放到 `/opt/data/registry` 目录。
```
$ sudo docker run -d -p 5000:5000 -v /opt/data/registry:/tmp/registry registry
```

#### 本地安装
对于 Ubuntu 或 CentOS 等发行版，可以直接通过源安装。
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

也可以从 [docker-registry](https://github.com/docker/docker-registry) 项目下载源码进行安装。
```
$ sudo apt-get install build-essential python-dev libevent-dev python-pip libssl-dev liblzma-dev libffi-dev
$ git clone https://github.com/docker/docker-registry.git
$ cd docker-registry
$ sudo python setup.py install
```
然后修改配置文件，主要修改 dev 模板段的 `storage_path` 到本地的存储仓库的路径。
```
$ cp config/config_sample.yml config/config.yml
```
之后启动 Web 服务。
```
$ sudo gunicorn -c contrib/gunicorn.py docker_registry.wsgi:application
```
或者
```
$ sudo gunicorn --access-logfile - --error-logfile - -k gevent -b 0.0.0.0:5000 -w 4 --max-requests 100 docker_registry.wsgi:application
```
此时使用curl访问本地的 5000 端口，看到输出 docker-registry 的版本信息说明运行成功。

*注：`config/config_sample.yml` 文件是示例配置文件。

###在私有仓库上传、下载、搜索镜像
创建好私有仓库之后，就可以使用 `docker tag` 来标记一个镜像，然后推送它到仓库，别的机器上就可以下载下来了。例如私有仓库地址为 `192.168.7.26:5000`。

先在本机查看已有的镜像。
```
$ sudo docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu                            latest              ba5877dc9bec        6 weeks ago         192.7 MB
ubuntu                            14.04               ba5877dc9bec        6 weeks ago         192.7 MB
```

使用`docker tag` 将 `ba58` 这个镜像标记为 `192.168.7.26:5000/test`（格式为 `docker tag IMAGE[:TAG] [REGISTRYHOST/][USERNAME/]NAME[:TAG]`）。
```
$ sudo docker tag ba58 192.168.7.26:5000/test
root ~ # docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu                            14.04               ba5877dc9bec        6 weeks ago         192.7 MB
ubuntu                            latest              ba5877dc9bec        6 weeks ago         192.7 MB
192.168.7.26:5000/test            latest              ba5877dc9bec        6 weeks ago         192.7 MB
```
使用 `docker push` 上传标记的镜像。
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
用 curl 查看仓库中的镜像。
```
$ curl http://192.168.7.26:5000/v1/search
{"num_results": 7, "query": "", "results": [{"description": "", "name": "library/miaxis_j2ee"}, {"description": "", "name": "library/tomcat"}, {"description": "", "name": "library/ubuntu"}, {"description": "", "name": "library/ubuntu_office"}, {"description": "", "name": "library/desktop_ubu"}, {"description": "", "name": "dockerfile/ubuntu"}, {"description": "", "name": "library/test"}]}
```
这里可以看到 `{"description": "", "name": "library/test"}`，表明镜像已经被成功上传了。

现在可以到另外一台机器去下载这个镜像。
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

可以使用 [这个脚本](https://github.com/yeasy/docker_practice/raw/master/_local/push_images.sh) 批量上传本地的镜像到注册服务器中，默认是本地注册服务器 `127.0.0.1:5000`。例如：
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
