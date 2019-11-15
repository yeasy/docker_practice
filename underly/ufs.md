# 联合文件系统

联合文件系统（[UnionFS](https://en.wikipedia.org/wiki/UnionFS)）是一种分层、轻量级并且高性能的文件系统，它支持对文件系统的修改作为一次提交来一层层的叠加，同时可以将不同目录挂载到同一个虚拟文件系统下(unite several directories into a single virtual filesystem)。

联合文件系统是 Docker 镜像的基础。镜像可以通过分层来进行继承，基于基础镜像（没有父镜像），可以制作各种具体的应用镜像。

另外，不同 Docker 容器就可以共享一些基础的文件系统层，同时再加上自己独有的改动层，大大提高了存储的效率。

Docker 中使用的 AUFS（AnotherUnionFS）就是一种联合文件系统。 `AUFS` 支持为每一个成员目录（类似 Git 的分支）设定只读（readonly）、读写（readwrite）和写出（whiteout-able）权限, 同时 `AUFS` 里有一个类似分层的概念, 对只读权限的分支可以逻辑上进行增量地修改(不影响只读部分的)。

Docker 目前支持的联合文件系统包括 `OverlayFS`, `AUFS`, `Btrfs`, `VFS`, `ZFS` 和 `Device Mapper`。

各 Linux 发行版 Docker 推荐使用的存储驱动如下表。

|Linux 发行版 |	Docker 推荐使用的存储驱动 |
| :--        | :--                     |
|Docker CE on Ubuntu |	`overlay2` (16.04 +) |
|Docker CE on Debian |	`overlay2` (Debian Stretch), `aufs`, `devicemapper` |
|Docker CE on CentOS |	`overlay2`  |
|Docker CE on Fedora |	`overlay2`  |

在可能的情况下，[推荐](https://docs.docker.com/storage/storagedriver/select-storage-driver/) 使用 `overlay2` 存储驱动，`overlay2` 是目前 Docker 默认的存储驱动，以前则是 `aufs`。你可以通过配置来使用以上提到的其他类型的存储驱动。
