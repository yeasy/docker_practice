##Docker Hub
目前Docker官方维护了一个公共仓库--[Docker Hub](https://hub.docker.com/)，其中已经包括了超过15,000的镜像。大部分用户的需求，都可以通过在Docker Hub中直接下载镜像来实现。

### 登录
可以通过执行`docker login`命令来输入用户名、密码和邮箱来完成注册和登录。
注册成功后，本地用户目录的`.dockercfg`中将保存用户的认证信息。

### 基本操作
用户无需登录即可通过`docker search`命令来查找官方仓库中的镜像，并利用`docker pull`命令来将它下载到本地。

例如以centos为关键词进行搜索：
```
$ sudo docker search centos
NAME                                            DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
centos                                          The official build of CentOS.                   465       [OK]
tianon/centos                                   CentOS 5 and 6, created using rinse instea...   28
blalor/centos                                   Bare-bones base CentOS 6.5 image                6                    [OK]
saltstack/centos-6-minimal                                                                      6                    [OK]
tutum/centos-6.4                                DEPRECATED. Use tutum/centos:6.4 instead. ...   5                    [OK]
...
```
可以看到返回了很多包含关键字的镜像，其中包括镜像名字、描述、星级（表示该镜像的受欢迎程度）、是否官方创建、是否自动创建。
官方的镜像说明是官方项目组创建和维护的，automated 资源允许用户验证镜像的来源和内容。

根据是否是官方提供，可将镜像资源分为两类。
一种是类似centos这样的基础镜像，被称为基础或根镜像。这些基础镜像是由Docker公司创建、验证、支持、提供。这样的镜像往往使用单个单词作为名字。
还有一种类型，比如`tianon/centos`镜像，它是由Docker的用户创建并维护的，往往带有用户名称前缀。可以通过前缀`user_name/`来指定使用某个用户提供的镜像，比如tianon用户。

另外，在查找的时候通过`-s n`参数可以指定仅显示评价为`n`星以上的镜像。

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
