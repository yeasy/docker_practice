Docker —— 从入门到实践
===============

v0.2.3

[Docker](docker.com)是个伟大的项目，它彻底释放了虚拟化的威力，让应用的分发、部署和管理都变得前所未有的高效和轻松！

本书既适用于具备基础Linux知识的Docker初学者，也可供希望理解原理和实现的高级用户参考。同时，书中给出的实践案例，可供在进行实际部署时借鉴。

本书源于[WaitFish](github.com/qcpm1983)的《[Docker学习手册v1.0](https://github.com/yeasy/docker_practice/blob/master/_local/docker_manual_waitfish.pdf)》内容。后来，[yeasy](github.com/yeasy)
根据最新Docker版本对内容进行了修订和重写，并增加了部分内容；与WaitFish协商，将所有内容开源，采用互联网合作的方式进行创作和维护。

在线阅读：[https://www.gitbook.io/book/yeasy/docker_practice](https://www.gitbook.io/book/yeasy/docker_practice)。

维护本书的Github项目： [https://github.com/yeasy/docker_practice](https://github.com/yeasy/docker_practice)。
欢迎参与。

另外，欢迎加入Docker QQ群（341410255）一起交流学习，共同提高。

本书发布时，Docker的最新版本为1.20。

## 主要版本历史
* 0.3: 2014-09-TODO
        完成仓库章节；
        重写安全章节；
        修正底层实现章节的架构、名字空间、控制组、文件系统、容器格式等内容。
* 0.2: 2014-09-18
        对照官方文档重写介绍、基本概念、安装、镜像、容器、仓库、数据管理、网络等章节；
        添加底层实现章节；
        添加命令查询和资源链接章节；
        其它修正。
* 0.1: 2014-09-05
        添加pdf文件内容;
        修正错别字和表达不通顺的地方。


## 参加步骤
* 在GitHub上fork到自己的仓库，如docker_user/docker_practice，然后clone到本地，并设置用户信息。
```
$ git clone git@github.com:docker_user/docker_practice.git
$ cd docker_practice
$ git config user.name "Docker User"
$ git config user.email docker_user@dockcer.com
```
* 修改代码后提交，并推送到自己的仓库。
```
$ #do some change on the content
$ git commit -am "Fix issue #1: change helo to hello"
$ git push
```
* 在GitHub网站上提交pull request。
* 定期使用项目仓库内容更新自己仓库内容。
```
$ git remote add upstream github.com/yeasy/docker_practice
$ git fetch upstream
$ git checkout master
$ git rebase upstream/master
$ git push -f origin master
```


