##镜像的工作原理

Docker镜像是怎么实现增量的修改和维护的？
每个docker都有很多层次构成，docker使用 [Union FS](http://en.wikipedia.org/wiki/UnionFS) 将这些不同的层结合到一个镜像中去。

通常 Union FS 有两个用途, 一方面可以实现不借助 LVM、RAID 将多个disk挂到同一个目录下, 另一个更常用的就是将一个只读的分支和一个可写的 分支联合在一起，Live CD正是基于此方法可以允许在 OS 镜像不变的基础上允许用户在其上进行一些写操作。
Docker 在 AUFS 上构建的容器也正是如此。
