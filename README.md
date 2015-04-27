Docker —— 从入门到实践
===============

v0.3.5

[Docker](docker.com) 是个伟大的项目，它彻底释放了虚拟化的威力，极大降低了云计算资源供应的成本，同时让应用的分发、测试、部署和分发都变得前所未有的高效和轻松！

本书既适用于具备基础 Linux 知识的 Docker 初学者，也希望可供理解原理和实现的高级用户参考。同时，书中给出的实践案例，可供在进行实际部署时借鉴。前六章为基础内容，供用户理解 Docker 的基本概念和操作；7 ~ 9 章介绍一些高级操作；第 10 章给出典型的应用场景和实践案例；11 ~ 13 章介绍关于 Docker 实现的相关技术。14 ~ 17章介绍相关的一些开源项目。

在线阅读：[GitBook](https://www.gitbook.io/book/gnu4cn/docker-io-abc)。



源码在 Github 上维护，欢迎参与：[https://github.com/gnu4cn/docker_practice](https://github.com/gnu4cn/docker_practice)。贡献者 [名单](https://github.com/yeasy/docker_practice/graphs/contributors)。

## 参加步骤
* 在 GitHub 上 `fork` 到自己的仓库，如 `docker_user/docker_practice`，然后 `clone` 到本地，并设置用户信息。
```
$ git clone git@github.com:docker_user/docker_practice.git
$ cd docker_practice
$ git config user.name "yourname"
$ git config user.email "your email"
```
* 修改代码后提交，并推送到自己的仓库。测试一下git.
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
