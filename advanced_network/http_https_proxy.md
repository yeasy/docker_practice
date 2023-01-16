# 配置 HTTP/HTTPS 网络代理

使用Docker的过程中，因为网络原因，通常需要使用 HTTP/HTTPS 代理来加速镜像拉取、构建和使用。下面是常见的三种场景。

## 为 dockerd 设置网络代理

"docker pull" 命令是由 dockerd 守护进程执行。而 dockerd 守护进程是由 systemd 管理。因此，如果需要在执行 "docker pull" 命令时使用 HTTP/HTTPS 代理，需要通过 systemd 配置。

- 为 dockerd 创建配置文件夹。
```
sudo mkdir -p /etc/systemd/system/docker.service.d
```

- 为 dockerd 创建 HTTP/HTTPS 网络代理的配置文件，文件路径是 /etc/systemd/system/docker.service.d/http-proxy.conf 。并在该文件中添加相关环境变量。
```
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080/"
Environment="HTTPS_PROXY=http://proxy.example.com:8080/"
Environment="NO_PROXY=localhost,127.0.0.1,.example.com"
```

- 刷新配置并重启 docker 服务。
```
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 为 docker 容器设置网络代理

在容器运行阶段，如果需要使用 HTTP/HTTPS 代理，可以通过更改 docker 客户端配置，或者指定环境变量的方式。

- 更改 docker 客户端配置：创建或更改 ~/.docker/config.json，并在该文件中添加相关配置。
```
{
 "proxies":
 {
   "default":
   {
     "httpProxy": "http://proxy.example.com:8080/",
     "httpsProxy": "http://proxy.example.com:8080/",
     "noProxy": "localhost,127.0.0.1,.example.com"
   }
 }
}
```

- 指定环境变量：运行 "docker run" 命令时，指定相关环境变量。

| 环境变量 |  docker run 示例 |
| -------- | ---------------- |
| HTTP_PROXY | --env HTTP_PROXY="http://proxy.example.com:8080/" |
| HTTPS_PROXY | --env HTTPS_PROXY="http://proxy.example.com:8080/" |
| NO_PROXY | --env NO_PROXY="localhost,127.0.0.1,.example.com" |

## 为 docker build 过程设置网络代理

在容器构建阶段，如果需要使用 HTTP/HTTPS 代理，可以通过指定 "docker build" 的环境变量，或者在 Dockerfile 中指定环境变量的方式。

- 使用 "--build-arg" 指定 "docker build" 的相关环境变量
```
docker build \
    --build-arg "HTTP_PROXY=http://proxy.example.com:8080/" \
    --build-arg "HTTPS_PROXY=http://proxy.example.com:8080/" \
    --build-arg "NO_PROXY=localhost,127.0.0.1,.example.com" .
```

- 在 Dockerfile 中指定相关环境变量

| 环境变量 | Dockerfile 示例 |
| -------- | ---------------- |
| HTTP_PROXY | ENV HTTP_PROXY="http://proxy.example.com:8080/" |
| HTTPS_PROXY | ENV HTTPS_PROXY="http://proxy.example.com:8080/" |
| NO_PROXY | ENV NO_PROXY="localhost,127.0.0.1,.example.com" |

