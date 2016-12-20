# Docker — 从入门到实践

0.7.6

[Docker](http://www.docker.com) 是个划时代的开源项目，它彻底释放了虚拟化的威力，极大提高了应用的运行效率，降低了云计算资源供应的成本，同时让应用的部署、测试和分发都变得前所未有的高效和轻松！

无论是应用开发者，运维人员，还是云计算从业人员，都有必要认识和掌握 Docker，以在有限的时间内做更多有意义的事。

本书既适用于具备基础 Linux 知识的 Docker 初学者，也希望可供理解原理和实现的高级用户参考。同时，书中给出的实践案例，可供在进行实际部署时借鉴。前六章为基础内容，供用户理解 Docker 的基本概念和操作；7 ~ 9 章介绍一些高级操作；第 10 章给出典型的应用场景和实践案例；11 ~ 13 章介绍关于 Docker 实现的相关细节技术。后续章节则分别介绍一些相关的热门开源项目。

在线阅读：[GitBook](https://www.gitbook.io/book/yeasy/docker_practice) 或 [Github](https://github.com/yeasy/docker_practice/blob/master/SUMMARY.md)。

* pdf 版本 [下载](https://www.gitbook.com/download/pdf/book/yeasy/docker_practice)
* epub 版本 [下载](https://www.gitbook.com/download/epub/book/yeasy/docker_practice)

欢迎关注 DockerPool 社区微博 [@dockerpool](http://weibo.com/u/5345404432)，或加入 Docker 技术交流 QQ 群或微信组，分享 Docker 资源，交流 Docker 技术。

* QQ 群 I   （已满）：341410255
* QQ 群 II  （已满）：419042067
* QQ 群 III （已满）：210028779
* QQ 群 IV  （已满）：483702734
* QQ 群 V   （已满）：460598761
* QQ 群 VI  （已满）：581983671
* QQ 群 VII （已满）：252403484
* QQ 群 VIII（已满）：544818750
* QQ 群 IX  （已满）：571502246
* QQ 群 X   （可加）：366203473

![Docker 技术入门与实战](docker_primer.png)

《[Docker 技术入门与实战](http://item.jd.com/11598400.html)》一书已经正式出版，包含大量第一手实战案例和更为深入的技术剖析，欢迎大家阅读使用并反馈建议。

* [China-Pub](http://product.china-pub.com/3770833)
* [京东图书](http://item.jd.com/11598400.html)
* [当当图书](http://product.dangdang.com/23620853.html)
* [亚马逊图书](http://www.amazon.cn/%E5%9B%BE%E4%B9%A6/dp/B00R5MYI7C/ref=lh_ni_t?ie=UTF8&psc=1&smid=A1AJ19PSB66TGU)

## 主要版本历史

* 0.8.0: 2016-MM-DD

  * 修正文字内容
  * 根据最新版本修订安装使用
  * 补充附录章节

* 0.7.0: 2016-06-12

  * 根据最新版本进行命令调整
  * 修正若干文字描述

* 0.6.0: 2015-12-24

  * 补充 Machine 项目
  * 修正若干 bug

* 0.5.0: 2015-06-29

  * 添加 Compose 项目
  * 添加 Machine 项目
  * 添加 Swarm 项目
  * 完善 Kubernetes 项目内容
  * 添加 Mesos 项目内容

* 0.4.0: 2015-05-08

  * 添加 Etcd 项目
  * 添加 Fig 项目
  * 添加 CoreOS 项目
  * 添加 Kubernetes 项目

* 0.3.0: 2014-11-25

  * 完成仓库章节；
  * 重写安全章节；
  * 修正底层实现章节的架构、命名空间、控制组、文件系统、容器格式等内容；
  * 添加对常见仓库和镜像的介绍；
  * 添加 Dockerfile 的介绍；
  * 重新校订中英文混排格式。
  * 修订文字表达。
  * 发布繁体版本分支：zh-Hant。

* 0.2.0: 2014-09-18

  * 对照官方文档重写介绍、基本概念、安装、镜像、容器、仓库、数据管理、网络等章节；
  * 添加底层实现章节；
  * 添加命令查询和资源链接章节；
  * 其它修正。

* 0.1.0: 2014-09-05

  * 添加基本内容;
  * 修正错别字和表达不通顺的地方。

Docker 自身仍在快速发展中，生态环境也在蓬勃成长。源码开源托管在 Github 上，欢迎参与维护：[https:\/\/github.com\/yeasy\/docker\_practice](https://github.com/yeasy/docker_practice)。贡献者 [名单](https://github.com/yeasy/docker_practice/graphs/contributors)。

## 参加步骤

* 在 GitHub 上 `fork` 到自己的仓库，如 `docker_user/docker_practice`，然后 `clone` 到本地，并设置用户信息。

  ```
  $ git clone git@github.com:docker_user/docker_practice.git
  $ cd docker_practice
  $ git config user.name "yourname"
  $ git config user.email "your email"
  ```

* 修改代码后提交，并推送到自己的仓库。

  ```
  $ #do some change on the content
  $ git commit -am "Fix issue #1: change helo to hello"
  $ git push
  ```

* 在 GitHub 网站上提交 pull request。

* 定期使用项目仓库内容更新自己仓库内容。
  ```
  $ git remote add upstream https://github.com/yeasy/docker_practice
  $ git fetch upstream
  $ git checkout master
  $ git rebase upstream/master
  $ git push -f origin master
  ```



