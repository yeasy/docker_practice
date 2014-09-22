##部署本地仓库
有时候使用Docker Hub这样的公共仓库可能不方便，用户可以创建一个本地仓库供私人使用。

本节介绍如何创建部署本地仓库。

###创建一个镜像
创建镜像有很多方法，用户可以从Docker Hub获取一个，也可以利用本地文件系统创建一个。

要从本地文件系统导入一个镜像，可以使用openvz（容器虚拟化的先锋技术）的模板来创建：
openvz的模板下载地址为http://openvz.org/Download/templates/precreated。

比如：先下载了一个ubuntu14.04的镜像，之后使用以下命令导入：
```
sudo cat ubuntu-14.04-x86_64-minimal.tar.gz  |docker import - ubuntu:14.04
```
然后查看新导入的镜像。
```
docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu              14.04               05ac7c0b9383        17 seconds ago      215.5 MB
```


###创建私有仓库
创建私有仓库可以使用`docker-registry`工具。
#### 系统自带
在安装了Docker后，系统中就自带了`docker-registry`工具，可以运行
```
docker run -p 5000:5000 registry
```
这将使用官方的registry镜像来启动本地的私有仓库。可以通过指定参数来配置私有仓库位置，例如配置镜像存储到Amazon的S3服务。
```
docker run \
         -e SETTINGS_FLAVOR=s3 \
         -e AWS_BUCKET=acme-docker \
         -e STORAGE_PATH=/registry \
         -e AWS_KEY=AKIAHSHB43HS3J92MXZ \
         -e AWS_SECRET=xdDowwlK7TJajV1Y7EoOZrmuPEJlHYcNP2k4j49T \
         -e SEARCH_BACKEND=sqlalchemy \
         -p 5000:5000 \
         registry
````

#### 源码安装
从[docker-registry](https://github.com/docker/docker-registry)项目下载源码并安装。
```
$ sudo apt-get install build-essential python-dev libevent-dev python-pip libssl-dev liblzma-dev libffi-dev
$ sudo pip install .
```
`config/config_sample.yml`文件是配置文件。

###在私有仓库上传、下载、搜索镜像
创建好私有仓库之后，就可以使用`docker tag`来标记一个镜像，然后推送它到仓库，别的机器上就可以下载下来了。例如私有仓库地址为`192.168.7.26:5000`。

先在本机查看已有的镜像。
```
$ sudo docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu                            latest              ba5877dc9bec        6 weeks ago         192.7 MB
ubuntu                            14.04               ba5877dc9bec        6 weeks ago         192.7 MB
```

使用`docker tag`将ba58这个镜像标记为`192.168.7.26:5000/test`（格式为`[REGISTRYHOST/][USERNAME/]NAME[:TAG]`）。
```
$ sudo docker tag ba58 192.168.7.26:5000/test
root ~ # docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu                            14.04               ba5877dc9bec        6 weeks ago         192.7 MB
ubuntu                            latest              ba5877dc9bec        6 weeks ago         192.7 MB
192.168.7.26:5000/test            latest              ba5877dc9bec        6 weeks ago         192.7 MB
```
使用`docker push`上传标记的镜像。
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
用curl查看仓库中的镜像。
```
$ curl http://192.168.7.26:5000/v1/search
{"num_results": 7, "query": "", "results": [{"description": "", "name": "library/miaxis_j2ee"}, {"description": "", "name": "library/tomcat"}, {"description": "", "name": "library/ubuntu"}, {"description": "", "name": "library/ubuntu_office"}, {"description": "", "name": "library/desktop_ubu"}, {"description": "", "name": "dockerfile/ubuntu"}, {"description": "", "name": "library/test"}]}
```
这里可以看到`{"description": "", "name": "library/test"}`，表明镜像已经被成功上传了。

现在可以到另外一台机器去下载这个镜像
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
