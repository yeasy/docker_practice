#简介

##什么是Docker
Docker是一个开源项目，诞生于2013年初，最初是dotCloud公司内部的一个业余项目。它基于Google公司推出的Go语言实现。
项目后来加入了Linux基金会，遵从了Apache 2.0协议，项目代码在[GitHub](https://github.com/docker/docker)上进行维护。

Docker自开源后受到广泛的关注和讨论，以至于dotCloud公司后来都改名为Docker Inc。Redhat已经在其RHEL6.5中集中支持Docker；Google也在其PaaS产品中广泛应用。

Docker项目的目标是实现轻量级的操作系统虚拟化解决方案。
Docker的基础是Linux的容器（LXC）等技术。

在容器的基础上Docker进行了进一步的封装，让用户不需要去关心容器的管理，使得操作更为简便。用户操作Docker的容器就像操作一个快速轻量级的虚拟机一样简单。

下面的图片比较了Docker和传统虚拟化方式的不同之处，可见容器是在操作系统层面上实现虚拟化，直接复用本地主机的操作系统，而传统方式则是在硬件层面实现。

![传统虚拟化](../_images/virtualization.png)

![Docker](../_images/docker.png)


##为什么要使用docker？
作为一种新兴的虚拟化方式，Docker跟传统的虚拟化方式相比具有众多的优势。

首先，Docker容器的启动可以在秒级实现，这相比传统的虚拟机方式要快得多。
其次，Docker对系统资源的利用率很高，一台主机上可以同时运行数千个Docker容器。

而且容器除了运行其中应用外，基本不消耗额外的系统资源，使得应用的性能很高，同时系统的开销尽量小。传统虚拟机方式运行10个不同的应用就要起10个虚拟机，而Docker只需要启动10个隔离的应用即可。


