## 什么是Docker
Docker是一个开源项目，诞生于2013年初，最初是dotCloud公司内部的一个业余项目。它基于Google公司推出的Go语言实现。
项目后来加入了Linux基金会，遵从了Apache 2.0协议，项目代码在[GitHub](https://github.com/docker/docker)上进行维护。

Docker自开源后受到广泛的关注和讨论，以至于dotCloud公司后来都改名为Docker Inc。Redhat已经在其RHEL6.5中集中支持Docker；Google也在其PaaS产品中广泛应用。

Docker项目的目标是实现轻量级的操作系统虚拟化解决方案。
Docker的基础是Linux的容器（LXC）等技术。

在LXC的基础上Docker进行了进一步的封装，让用户不需要去关心容器的管理，使得操作更为简便。用户操作Docker的容器就像操作一个快速轻量级的虚拟机一样简单。

下面的图片比较了Docker和传统虚拟化方式的不同之处，可见容器是在操作系统层面上实现虚拟化，直接复用本地主机的操作系统，而传统方式则是在硬件层面实现。

![传统虚拟化](../_images/virtualization.png)

![Docker](../_images/docker.png)
