##工作原理

docker image是怎么实现增量的修改和维护的？
每个docker都有很多层次构成，docker使用 [Union FS](http://en.wikipedia.org/wiki/UnionFS) 将这些不同的层结合到一个image中去。
Union FS是一种特殊的文件系统，它支持将不同目录挂载到同一个虚拟文件系统下(unite several directories into a single virtual filesystem),

AUFS (AnotherUnionFS) 就是一种 Union FS, AUFS支持为每一个成员目录(类似Git Branch)设定readonly、readwrite 和 whiteout-able 权限, 同时 AUFS 里有一个类似分层的概念, 对 readonly 权限的 branch 可以逻辑上进行修改(增量地, 不影响 readonly 部分的)。

通常 Union FS 有两个用途, 一方面可以实现不借助 LVM、RAID 将多个disk挂到同一个目录下, 另一个更常用的就是将一个 readonly 的 branch 和一个 writeable 的 branch 联合在一起，Live CD正是基于此方法可以允许在 OS image 不变的基础上允许用户在其上进行一些写操作。
Docker 在 AUFS 上构建的 container image 也正是如此。
