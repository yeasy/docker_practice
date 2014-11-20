## 建立映像檔
編輯完成 Dockerfile 之後，可以透過 `docker build` 命令建立映像檔。

基本的格式為 `docekr build [選項] 路徑`，該命令將讀取指定路徑下（包括子目錄）的 Dockerfile，並將該路徑下所有內容發送給 Docker 伺服端，由伺服端來創建鏡像。因此一般會建議放置 Dockerfile 的目錄為空目錄。也可以透過 `.dockerignore` 文件（每一行添加一條排除模式：exclusion patterns）來讓 Docker 忽略路徑下的目錄和文件。

要指定鏡像的標籤資訊，可以透過 `-t` 選項，例如
```
$ sudo docker build -t myrepo/myapp /tmp/test1/
```
