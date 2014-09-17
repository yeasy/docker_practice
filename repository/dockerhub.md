##Docker Hub
目前Docker官方维护了一个公共仓库--[Docker Hub](https://hub.docker.com/)，其中已经包括了超过15,000的镜像。大部分用户的需求，都可以通过在Docker Hub中直接下载镜像来实现。

###登录
可以通过执行`docker login`命令来输入用户名、密码和邮箱来完成注册和登录。
注册成功后，本地用户目录的`.dockercfg`中将保存用户的认证信息。

###操作
用户可以无需登录通过`docker search`命令来查找官方仓库中的镜像，并利用`docker pull`命令来将它下载到本地。

例如以centos为关键词进行搜索：
```
$ sudo docker search centos
NAME           DESCRIPTION                                     STARS     OFFICIAL   TRUSTED
centos         Official CentOS 6 Image as of 12 April 2014     88
tianon/centos  CentOS 5 and 6, created using rinse instea...   21
...
```
下载官方centos镜像到本地。
```
$ sudo docker pull centos
Pulling repository centos
0b443ba03958: Download complete
539c0211cd76: Download complete
511136ea3c5a: Download complete
7064731afe90: Download complete
```
用户也可以在登录后通过`docker push`命令来将镜像推送到Docker Hub中。

###自动创建
自动创建（Automated Builds）功能对于需要经常升级镜像内程序来说，十分方便。
有时候，用户创建了镜像，安装了某个软件，如果软件发布新版本则需要手动更新镜像。。

而自动创建允许用户通过Docker Hub指定跟踪一个目标网站（目前支持[GitHub](github.org)或[BitBucket](bitbucket.org)）上的项目，一旦项目发生新的提交，则自动执行创建。

要配置自动创建，包括如下的步骤：
* 创建并登陆Docker Hub，以及目标网站；
* 在目标网站中连接帐户到Docker Hub；
* 在Docker Hub中[配置一个自动创建](https://registry.hub.docker.com/builds/add/)；
* 选取一个目标网站中的项目（需要含Dockerfile）和分支；
* 指定Dockerfile的位置，并提交创建。

之后，可以在Docker Hub的[自动创建页面](https://registry.hub.docker.com/builds/)中跟踪每次创建的状态。
