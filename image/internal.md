##镜像的工作原理

Docker镜像是怎么实现增量的修改和维护的？
每个docker都有很多层次构成，docker使用 [Union FS](http://en.wikipedia.org/wiki/UnionFS) 将这些不同的层结合到一个镜像中去。

Union FS是一种特殊的文件系统，它支持对文件系统的修改作为一次提交来一层层的叠加，同时可以将不同目录挂载到同一个虚拟文件系统下(unite several directories into a single virtual filesystem)。这样的话，不同容器可以共享一些文件系统层，同时再加上自己独有的改动层，提高了存储的效率。

AUFS (AnotherUnionFS) 就是一种 Union FS, AUFS支持为每一个成员目录(类似Git 分支)设定只读（readonly）、读写（readwrite）和写出（whiteout-able）权限, 同时 AUFS 里有一个类似分层的概念, 对只读权限的分支可以逻辑上进行修改(增量地, 不影响 只读部分的)。

通常 Union FS 有两个用途, 一方面可以实现不借助 LVM、RAID 将多个disk挂到同一个目录下, 另一个更常用的就是将一个只读的分支和一个可写的 分支联合在一起，Live CD正是基于此方法可以允许在 OS 镜像不变的基础上允许用户在其上进行一些写操作。
Docker 在 AUFS 上构建的容器也正是如此。
