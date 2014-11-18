## 創建鏡像
編寫完成 Dockerfile 之後，可以通過 `docker build` 命令來創建鏡像。

基本的格式為 `docker build [選項] 路徑`，該命令將讀取指定路徑下（包括子目錄）的 Dockerfile，並將該路徑下所有內容發送給 Docker 服務端，由服務端來創建鏡像。因此一般建議放置 Dockerfile 的目錄為空目錄。也可以通過 `.dockerignore` 文件（每一行添加一條匹配模式）來讓 Docker 忽略路徑下的目錄和文件。

要指定鏡像的標簽信息，可以通過 `-t` 選項，例如
```
$ sudo docker build -t myrepo/myapp /tmp/test1/
```
