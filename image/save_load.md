## 存出和載入鏡像

### 存出鏡像
如果要導出鏡像到本地文件，可以使用 `docker save` 命令。
```
$ sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu              14.04               c4ff7513909d        5 weeks ago         225.4 MB
...
$sudo docker save -o ubuntu_14.04.tar ubuntu:14.04
```

### 載入鏡像
可以使用 `docker load` 從導出的本地文件中再導入到本地鏡像庫，例如
```
$ sudo docker load --input ubuntu_14.04.tar
```
或
```
$ sudo docker load < ubuntu_14.04.tar
```
這將導入鏡像以及其相關的元數據信息（包括標簽等）。
