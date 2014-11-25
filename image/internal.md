## 鏡像的實作原理

Docker 鏡像是怎麽實作增量的修改和維護的？
每個鏡像都由很多層次構成，Docker 使用 [Union FS](http://en.wikipedia.org/wiki/UnionFS) 將這些不同的層結合到一個鏡像中去。

通常 Union FS 有兩個用途, 一方面可以實作不借助 LVM、RAID 將多個 disk 掛到同一個目錄下,另一個更常用的就是將一個唯讀的分支和一個可寫的分支聯合在一起，Live CD 正是基於此方法可以允許在鏡像不變的基礎上允許使用者在其上進行一些寫操作。
Docker 在 AUFS 上建立的容器也是利用了類似的原理。
