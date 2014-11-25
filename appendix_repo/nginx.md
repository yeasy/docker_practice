## [Nginx](https://registry.hub.docker.com/_/nginx/)

### 基本訊息
[Nginx](https://en.wikipedia.org/wiki/Nginx) 是開源的有效率的 Web 伺服器實作，支持 HTTP、HTTPS、SMTP、POP3、IMAP 等協議。
該倉庫提供了 Nginx 1.0 ~ 1.7 各個版本的鏡像。

### 使用方法
下面的命令將作為一個靜態頁面伺服器啟動。
```
$ sudo docker run --name some-nginx -v /some/content:/usr/share/nginx/html:ro -d nginx
```
使用者也可以不使用這種映射方式，透過利用 Dockerfile 來直接將靜態頁面內容放到鏡像中，內容為
```
FROM nginx
COPY static-html-directory /usr/share/nginx/html
```
之後生成新的鏡像，並啟動一個容器。
```
$ sudo docker build -t some-content-nginx .
$ sudo docker run --name some-nginx -d some-content-nginx
```
開放端口，並映射到本地的 `8080` 端口。
```
sudo docker run --name some-nginx -d -p 8080:80 some-content-nginx
```

Nginx的默認設定文件路徑為 `/etc/nginx/nginx.conf`，可以透過映射它來使用本地的設定文件，例如
```
docker run --name some-nginx -v /some/nginx.conf:/etc/nginx/nginx.conf:ro -d nginx
```
使用設定文件時，為了在容器中正常執行，需要保持 `daemon off;`。

### Dockerfile
* [1 ~ 1.7 版本](https://github.com/nginxinc/docker-nginx/blob/3713a0157083eb4776e71f5a5aef4b2a5bc03ab1/Dockerfile)
