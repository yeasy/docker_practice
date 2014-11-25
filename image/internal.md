## 映像檔的實現原理

Docker 映像檔是怎麽實現增量的修改和維護的？
每個映像檔都由很多層次構成，Docker 使用 [Union FS](http://en.wikipedia.org/wiki/UnionFS) 將這些不同的層結合到一個映像檔中。

通常 Union FS 有兩個用途, 一方面可以實現不經由 LVM、RAID 將多個 disk 掛到同一個目錄下,另一個更常用的就是將一個唯讀的分支和一個可寫的分支結合在一起，Live CD 正是基於此方法，可以允許在映像檔不變的基礎上允許用戶在其上進行一些寫入操作。
Docker 在 AUFS 上構建的容器也是利用了類似的原理。
