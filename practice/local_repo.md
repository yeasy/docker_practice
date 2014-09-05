##部署本地仓库
由于网络的关系，国内用户在使用docker hub的时候，很难pull一个基本的镜像下来。
本节介绍如何创建部署本地仓库。

###安装docker
参见本文第三小节
###从文件系统创建一个image镜像
创建镜像有很多方法，官方的推荐是pull一个，不过在墙内，想pull一个基本的ubuntu都没办法完成。
这里推荐一个办法就是从一个文件系统import一个镜像，个人推荐可以使用opvz的模板来创建：（openvz可以说是容器虚拟化的先锋吧）
openvz的模板下载地址如下：
http://openvz.org/Download/templates/precreated
下载完之后，比如：下载了一个ubuntu14.04的镜像
使用以下命令：
```
sudo cat ubuntu-14.04-x86_64-minimal.tar.gz  |docker import - ubuntu:14.04
```
然后用docker images看下：
```
docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu              14.04               05ac7c0b9383        17 seconds ago      215.5 MB
```
就多了一个我们的ubuntu镜像

###创建私有仓库
官方指南称最简单的办法是 docker run -p 5000:5000 registry，如果被墙了，也无法下载该images。感谢CSDN，我有一个1M的腾讯云服务器，上面搭建了一个私有仓库大家可以使用
docker pull 203.195.193.251:5000/registry
到我的服务器下载 速度虽然慢点，但有保证！	
另外的方法是使用刚才的创建的ubuntu来创建，官方有个docker仓库的源码地址  https://github.com/dotcloud/docker-registry 下载私有仓库的源码，可以根据上面的docker file来创建。

也可以参考：
http://www.vpsee.com/2013/11/build-your-own-docker-private-regsitry-service/
 
###在私有仓库上传、下载、搜索images
创建好自己的私有仓库之后，可以使用docker tag 一个镜像，然后push，然后在别的机器上pull下来就好了。这样我们的局域网私有docker仓库就搭建好了。
步骤如下：
使用 docker run -p 5000:5000 registry 在局域网的一台机器上开启一个容器之后，我的局域网私有仓库地址为192.168.7.26:5000
先在本机看下现有的images
```
root ~ # docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu                            latest              ba5877dc9bec        6 weeks ago         192.7 MB
ubuntu                            14.04               ba5877dc9bec        6 weeks ago         192.7 MB
使用 docker tag 将ba58这个image标记为192.168.7.26:5000/test
root ~ # docker tag ba58  -t 192.168.7.26:5000/test
root ~ # docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu                            14.04               ba5877dc9bec        6 weeks ago         192.7 MB
ubuntu                            latest              ba5877dc9bec        6 weeks ago         192.7 MB
192.168.7.26:5000/test            latest              ba5877dc9bec        6 weeks ago         192.7 MB
```
使用docker push 上传我们标记的新image，这里因为我的服务器上已经有这个images，所有在上传文件层的时候，都跳过了，但是标记还是不一样的。
```
root ~ # docker push 192.168.7.26:5000/test
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
root ~ # curl http://192.168.7.26:5000/v1/search
The program 'curl' is currently not installed. You can install it by typing:
apt-get install curl
```
现在的私有仓库只支持这样简陋的搜索方式，如果没有安装curl，可以先安装后再使用
```
root ~ # apt-get install curl
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following NEW packages will be installed:
  curl
0 upgraded, 1 newly installed, 0 to remove and 570 not upgraded.
Need to get 123 kB of archives.
After this operation, 313 kB of additional disk space will be used.
Get:1 http://192.168.7.26/ubuntu/ trusty/main curl amd64 7.35.0-1ubuntu2 [123 kB]
Fetched 123 kB in 0s (7457 kB/s)
Selecting previously unselected package curl.
(Reading database ... 184912 files and directories currently installed.)
Preparing to unpack .../curl_7.35.0-1ubuntu2_amd64.deb ...
Unpacking curl (7.35.0-1ubuntu2) ...
Processing triggers for man-db (2.6.7.1-1) ...
Setting up curl (7.35.0-1ubuntu2) ...
root ~ # curl http://192.168.7.26:5000/v1/search
{"num_results": 7, "query": "", "results": [{"description": "", "name": "library/miaxis_j2ee"}, {"description": "", "name": "library/tomcat"}, {"description": "", "name": "library/ubuntu"}, {"description": "", "name": "library/ubuntu_office"}, {"description": "", "name": "library/desktop_ubu"}, {"description": "", "name": "dockerfile/ubuntu"}, {"description": "", "name": "library/test"}]}
```
这里我们可以看到 {"description": "", "name": "library/test"} 表示我们的image已经被成功上传了。
现在我们到另外一台机器上下载这个images
```
[root@opnvz ~]# docker pull 192.168.7.26:5000/test
Pulling repository 192.168.7.26:5000/test
ba5877dc9bec: Download complete 
511136ea3c5a: Download complete 
9bad880da3d2: Download complete 
25f11f5fb0cb: Download complete 
ebc34468f71d: Download complete 
2318d26665ef: Download complete 
[root@opnvz ~]# docker images
REPOSITORY                         TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
192.168.7.26:5000/test             latest              ba5877dc9bec        6 weeks ago         192.7 MB
```

这样我们就可以在新的机器上使用这个images了！