## [Nginx](https://registry.hub.docker.com/_/nginx/)

### 基本信息
[Nginx](https://en.wikipedia.org/wiki/Nginx)是开源的高效的Web服务器实现，支持HTTP、HTTPS、SMTP、POP3、IMAP等协议。
该仓库提供了Nginx从1.0到1.7各个版本的镜像。

### 使用方法
下面的命令将作为一个静态页面服务器启动。
```
$ sudo docker run --name some-nginx -v /some/content:/usr/share/nginx/html:ro -d nginx
```
用户也可以不使用这种映射方式，通过利用Dockerfile来直接将静态页面内容放到镜像中，内容为
```
FROM nginx
COPY static-html-directory /usr/share/nginx/html
```
之后生成新的镜像，并启动一个容器。
```
$ sudo docker build -t some-content-nginx .
$ sudo docker run --name some-nginx -d some-content-nginx
```
开放端口，并映射到本地的`8080`端口。
```
sudo docker run --name some-nginx -d -p 8080:80 some-content-nginx
```

Nginx的默认配置文件路径为`/etc/nginx/nginx.conf`，可以通过映射它来使用本地的配置文件，例如
```
docker run --name some-nginx -v /some/nginx.conf:/etc/nginx/nginx.conf:ro -d nginx
```
使用配置文件时，为了在容器中正常运行，需要保持`daemon off;`。

### Dockerfile
* [1到1.7版本](https://github.com/nginxinc/docker-nginx/blob/3713a0157083eb4776e71f5a5aef4b2a5bc03ab1/Dockerfile)
