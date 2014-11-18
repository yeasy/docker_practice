## Union 文件系統
Union文件系統（[UnionFS](http://en.wikipedia.org/wiki/UnionFS)）是一種分層、輕量級並且高性能的文件系統，它支持對文件系統的修改作為一次提交來一層層的疊加，同時可以將不同目錄掛載到同一個虛擬文件系統下(unite several directories into a single virtual filesystem)。

Union 文件系統是 Docker 鏡像的基礎。鏡像可以通過分層來進行繼承，基於基礎鏡像（沒有父鏡像），可以制作各種具體的應用鏡像。

另外，不同 Docker 容器就可以共享一些基礎的文件系統層，同時再加上自己獨有的改動層，大大提高了存儲的效率。

Docker 中使用的 AUFS（AnotherUnionFS）就是一種 Union FS。 AUFS 支持為每一個成員目錄（類似 Git 的分支）設定只讀（readonly）、讀寫（readwrite）和寫出（whiteout-able）權限, 同時 AUFS 裏有一個類似分層的概念, 對只讀權限的分支可以邏輯上進行增量地修改(不影響只讀部分的)。

Docker 目前支持的 Union 文件系統種類包括 AUFS, btrfs, vfs 和 DeviceMapper。
