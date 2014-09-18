## Union文件系统
Union文件系统（[UionFS](http://en.wikipedia.org/wiki/UnionFS)）是一种特殊的文件系统，它支持对文件系统的修改作为一次提交来一层层的叠加，同时可以将不同目录挂载到同一个虚拟文件系统下(unite several directories into a single virtual filesystem)。

这样，不同Docker容器就可以共享一些基础的文件系统层，同时再加上自己独有的改动层，大大提高了存储的效率。

Docker中使用的AUFS (AnotherUnionFS) 就是一种 Union FS。 AUFS支持为每一个成员目录(类似Git的分支)设定只读（readonly）、读写（readwrite）和写出（whiteout-able）权限, 同时 AUFS 里有一个类似分层的概念, 对只读权限的分支可以逻辑上进行增量地修改(不影响只读部分的)。

Docker目前支持的Union文件系统种类包括AUFS, btrfs, vfs, 和DeviceMapper。
