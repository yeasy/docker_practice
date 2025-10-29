## Chinese Version :

# Docker — 从入门到实践

[![](https://img.shields.io/github/stars/yeasy/docker_practice.svg?style=social&label=Stars)](https://github.com/yeasy/docker_practice) [![](https://img.shields.io/github/release/yeasy/docker_practice/all.svg)](https://github.com/yeasy/docker_practice/releases) [![](https://img.shields.io/badge/Based-Docker%20CE%20v20.10-blue.svg)](https://github.com/docker/docker-ce) [![](https://img.shields.io/badge/Docker%20%E6%8A%80%E6%9C%AF%E5%85%A5%E9%97%A8%E4%B8%8E%E5%AE%9E%E6%88%98-jd.com-red.svg)][1]

**v1.3.0**

| 语言           | - |
| :------------- | :--- |
| [简体中文](https://github.com/yeasy/docker_practice)              | [阅读](https://vuepress.mirror.docker-practice.com/) |

[Docker](https://www.docker.com) 是个划时代的开源项目，它彻底释放了计算虚拟化的威力，极大提高了应用的维护效率，降低了云计算应用开发的成本！使用 Docker，可以让应用的部署、测试和分发都变得前所未有的高效和轻松！

无论是应用开发者、运维人员、还是其他信息技术从业人员，都有必要认识和掌握 Docker，节约有限的生命。

本书既适用于具备基础 Linux 知识的 Docker 初学者，也希望可供理解原理和实现的高级用户参考。同时，书中给出的实践案例，可供在进行实际部署时借鉴。前六章为基础内容，供用户理解 Docker 的基本概念和操作；7 ~ 9 章介绍包括数据管理、网络等高级操作；第 10 ~ 12 章介绍了容器生态中的几个核心项目；13、14 章讨论了关于 Docker 安全和实现技术等高级话题。后续章节则分别介绍包括 Etcd、Fedora CoreOS、Kubernetes、容器云等相关热门开源项目。最后，还展示了使用容器技术的典型的应用场景和实践案例。

* 在线阅读：[docker-practice.com](https://vuepress.mirror.docker-practice.com/)，[GitBook](https://yeasy.gitbook.io/docker_practice/)，[Github](https://github.com/yeasy/docker_practice/blob/master/SUMMARY.md)
* 离线阅读：[`$ docker run -it --rm -p 4000:80 ccr.ccs.tencentyun.com/dockerpracticesig/docker_practice:vuepress`](https://github.com/yeasy/docker_practice/wiki/%E7%A6%BB%E7%BA%BF%E9%98%85%E8%AF%BB%E5%8A%9F%E8%83%BD%E8%AF%A6%E8%A7%A3)

Docker 自身仍在快速发展中，生态环境也在蓬勃成长。建议初学者使用最新稳定版本的 Docker 进行学习实践。欢迎 [参与项目维护](CONTRIBUTING.md)。

* [修订记录](CHANGELOG.md)
* [贡献者名单](https://github.com/yeasy/docker_practice/graphs/contributors)

## 微信小程序

<p align="center">
<img width="200" src="https://docker_practice.gitee.io/pic/dp-wechat-miniprogram.jpg">
</p>

<p align="center"><strong>微信扫码 随时随地阅读~</strong></p>

## 技术交流

<p align="center">
<img width="200" src="https://docker_practice.gitee.io/pic/dpsig-wechat.jpg">
</p>

<p align="center"><strong>微信扫码 加入群聊~ 或者微信添加 <code>dpsigs</code> 邀请入群</strong></p>

欢迎加入 Docker 技术交流 QQ 群，分享 Docker 资源，交流 Docker 技术。

* QQ 群 I   （已满）：341410255
* QQ 群 II  （已满）：419042067
* QQ 群 III （已满）：210028779
* QQ 群 IV  （已满）：483702734
* QQ 群 V   （已满）：460598761
* QQ 群 VI  （已满）：581983671
* QQ 群 VII （已满）：252403484
* QQ 群 VIII（已满）：544818750
* QQ 群 IX  （已满）：571502246
* QQ 群 X   （可加）：145983035

>如果有容器技术相关的疑问，请通过 [Issues](https://github.com/yeasy/docker_practice/issues/new/choose) 来提出。

## 进阶学习

[![](https://github.com/yeasy/docker_practice/raw/master/_images/docker_primer3.png)][1]

《[Docker 技术入门与实战][1]》第三版已经面世，介绍最新的容器技术栈，欢迎大家阅读使用并反馈建议。

* [京东图书][1]
* [China-Pub](http://product.china-pub.com/8052127)

## 鼓励项目

<p align="center">
<img width="200" src="https://github.com/yeasy/docker_practice/raw/master/_images/donate.jpeg">
</p>

<p align="center"><strong>欢迎鼓励项目一杯 coffee~</strong></p>

[1]: https://union-click.jd.com/jdc?e=&p=JF8AANADIgZlGF0VAxUDVBJdHDISBFAfWRcCGzcRRANLXSJeEF4aVwkMGQ1eD0kdSVJKSQVJHBIEUB9ZFwIbGAxeB0gyS34PbFlHVHNkI0MQEAoIcSxyBWFLRAtZK1olABYHXR9eHAoQN2UbXCVQfN_jrYOwsw7T_5SOnZUiBmUbXBYBFwBVG14UBBAAZRxbHDJJUjscCEEHEQ4FSA4VBhBQZStrFjIiN1UrWCVAfARQT1gQA0cFAEwOEAcRDlMTDEALQAFTEwwRUhMAUR1cJQATBlES


---------------------------------------------------------------------------------------------------------------------

## English Version :


# Docker — From Beginner to Practice

[![](https://img.shields.io/github/stars/yeasy/docker_practice.svg?style=social&label=Stars)](https://github.com/yeasy/docker_practice) [![](https://img.shields.io/github/release/yeasy/docker_practice/all.svg)](https://github.com/yeasy/docker_practice/releases) [![](https://img.shields.io/badge/Based-Docker%20CE%20v20.10-blue.svg)](https://github.com/docker/docker-ce) [![](https://img.shields.io/badge/Docker%20Technology%20Introduction%20and%20Practice-jd.com-red.svg)][1]

**v1.3.0**

| Language | - |
| :------------- | :--- |
| [Simplified Chinese](https://github.com/yeasy/docker_practice) | [Read Online](https://vuepress.mirror.docker-practice.com/) |

[Docker](https://www.docker.com) is a revolutionary open-source project that unleashes the full potential of computing virtualization. It greatly improves application maintenance efficiency and reduces the cost of developing cloud applications! With Docker, deploying, testing, and distributing applications has never been more efficient and effortless!

Whether you are an application developer, operations engineer, or IT professional, understanding and mastering Docker is essential to save valuable time and energy.

This book is suitable for both beginners with basic Linux knowledge and advanced users who want to understand Docker’s principles and implementation. The provided practical cases can also serve as a reference for real-world deployments. The first six chapters cover the fundamentals of Docker concepts and operations; chapters 7–9 discuss advanced operations such as data management and networking; chapters 10–12 introduce core projects in the container ecosystem; chapters 13–14 cover topics on Docker security and implementation techniques. Later chapters introduce popular open-source projects like Etcd, Fedora CoreOS, Kubernetes, and container clouds. Finally, it showcases typical application scenarios and case studies of container technologies.

* Online reading: [docker-practice.com](https://vuepress.mirror.docker-practice.com/), [GitBook](https://yeasy.gitbook.io/docker_practice/), [Github](https://github.com/yeasy/docker_practice/blob/master/SUMMARY.md)
* Offline reading: [`$ docker run -it --rm -p 4000:80 ccr.ccs.tencentyun.com/dockerpracticesig/docker_practice:vuepress`](https://github.com/yeasy/docker_practice/wiki/%E7%A6%BB%E7%BA%BF%E9%98%85%E8%AF%BB%E5%8A%9F%E8%83%BD%E8%AF%A6%E8%A7%A3)

Docker itself is still evolving rapidly, and its ecosystem continues to grow. Beginners are encouraged to use the latest stable version of Docker for learning and practice. You are welcome to [contribute to the project](CONTRIBUTING.md).

* [Changelog](CHANGELOG.md)
* [List of Contributors](https://github.com/yeasy/docker_practice/graphs/contributors)

## WeChat Mini Program

<p align="center">
<img width="200" src="https://docker_practice.gitee.io/pic/dp-wechat-miniprogram.jpg">
</p>

<p align="center"><strong>Scan with WeChat to read anytime, anywhere~</strong></p>

## Technical Communication

<p align="center">
<img width="200" src="https://docker_practice.gitee.io/pic/dpsig-wechat.jpg">
</p>

<p align="center"><strong>Scan the QR code to join the group chat, or add <code>dpsigs</code> on WeChat to be invited.</strong></p>

Join the Docker Technology Exchange QQ groups to share resources and discuss Docker technology.

* QQ Group I (Full): 341410255
* QQ Group II (Full): 419042067
* QQ Group III (Full): 210028779
* QQ Group IV (Full): 483702734
* QQ Group V (Full): 460598761
* QQ Group VI (Full): 581983671
* QQ Group VII (Full): 252403484
* QQ Group VIII (Full): 544818750
* QQ Group IX (Full): 571502246
* QQ Group X (Available): 145983035

>If you have any questions about container technologies, please raise them via [Issues](https://github.com/yeasy/docker_practice/issues/new/choose).

## Advanced Learning

[![](https://github.com/yeasy/docker_practice/raw/master/_images/docker_primer3.png)][1]

The third edition of “[Docker Technology Introduction and Practice][1]” is now available. It introduces the latest container technology stack — readers are welcome to read, use, and provide feedback.

* [JD Books][1]
* [China-Pub](http://product.china-pub.com/8052127)

## Support the Project

<p align="center">
<img width="200" src="https://github.com/yeasy/docker_practice/raw/master/_images/donate.jpeg">
</p>

<p align="center"><strong>Support the project with a cup of coffee~</strong></p>

[1]: https://union-click.jd.com/jdc?e=&p=JF8AANADIgZlGF0VAxUDVBJdHDISBFAfWRcCGzcRRANLXSJeEF4aVwkMGQ1eD0kdSVJKSQVJHBIEUB9ZFwIbGAxeB0gyS34PbFlHVHNkI0MQEAoIcSxyBWFLRAtZK1olABYHXR9eHAoQN2UbXCVQfN_jrYOwsw7T_5SOnZUiBmUbXBYBFwBVG14UBBAAZRxbHDJJUjscCEEHEQ4FSA4VBhBQZStrFjIiN1UrWCVAfARQT1gQA0cFAEwOEAcRDlMTDEALQAFTEwwRUhMAUR1cJQATBlES
