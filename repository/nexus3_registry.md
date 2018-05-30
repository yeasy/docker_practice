# Nexus3.x 的私有仓库

使用 Docker 官网自带的 Registry 创建的仓库面临一些维护问题。比如某些不用的镜像删除以后空间默认是不会回收的，需要一些命令去回收空间然后重启 Registry 程序。在企业中把内部的一些工具包放入 Nexus 中是比较常见的做法，最新版本 Nexus3.x 全面支持 Docker 的私有镜像。所以使用一个软件来管理 Docker , Maven , Yum , PyPI 等是一个明智的选择。[`Nexus3.x`](https://www.sonatype.com/download-oss-sonatype/) 下载地址

## 安装 JDK
由于 Nexus 是 Java 开发的，所以需要安装 JRE 或 JDK 支持的版本在 1.8 以上。 具体安装方法请去网上搜索。
本例假设安装的目录在 `/opt/jdk1.8.0_172/` 中

## 安装 Nexus 程序
下载好软件包以后放在某个目录中

```bash
   mkdir /opt/nexus
   cd /opt/nexus
   wget https://sonatype-download.global.ssl.fastly.net/repository/repositoryManager/3/nexus-3.12.0-01-unix.tar.gz
   tar -zxf nexus-3.12.0-01-unix.tar.gz
```
编辑 Nexus 的启动文件指定 Java 版本，如果您的主机只安装了一个 JDK 的版本那么您可以使用如下命令进行设置

```bash
   echo 'export JAVA_HOME="/opt/jdk1.8.0_172/"' >> /etc/profile
   echo 'export PATH="$PATH:$JAVA_HOME/bin"' >> /etc/profile
   source /etc/profile
```
如果您的主机有多个 JDK 版本请修改 `/opt/nexus/nexus-3.12.0-01/bin/nexus` 文件修改 `INSTALL4J_JAVA_HOME_OVERRIDE="/opt/jdk1.8.0_172/"`

```bash
   cd /opt/nexus/nexus-3.12.0-01/
   ./bin/nexus start
```
其它启动参数，可以直接运行 `/bin/nexus` 命令查看。或者打开这个文件进行查看。
在 `/opt/nexus/` 目录中还有一个文件夹 `sonatype-work` 这是保存 Nexus 设置和上传的仓库数据。这个文件中的内容不丢，数据就不会丢失。后期对 Nexus 升级时这个文件不动，只需要把程序停止后覆盖掉低版本的目录就行。注意： Nexus2.x 版本不能直接升级到 Nexus3.x。如果您的情况是这样，请自行网上搜索升级方法。

上面如果启动命令没有问题，那么你可以打开浏览器访问 Nexus 了。 `http://YourIP:8080` 端口的定义请自行修改程序目录下的 `etc/nexus-default.properties` 文件第一次启动 Nexus 的默认帐号是 admin 密码是 admin123 登录以后点击页面上方的齿轮按钮进行设置。

## 创建仓库

创建一个私有仓库的方法： `Repository->Repositories` 点击右边菜单 `Create repository` 选择 docker (hosted)
页面上的一些参数解释。
Name: 仓库的名称
HTTP: 仓库单独的访问端口
Enable Docker V1 API: 如果需要同时支持 V1 版本请勾选此项。
Hosted
  Deployment pollcy: 请选择 Allow redeploy 否则无法上传。

其它的仓库创建方法请各位自己摸索，还可以创建一个 docker (proxy) 类型的仓库链接到 DockerHub 上。再创建一个 docker (group) 类型的仓库把刚才的 hosted 与 proxy 添加在一起。主机在访问的时候默认下载私有仓库中的镜像，如果没有将链接到 DockerHub 中下载并缓存到 Nexus 中。

## 添加访问权限

菜单 `Security->Realms` 把 Docker Bearer Token Realm 移到右边的框中保存。

添加用户规则：菜单 `Security->Roles` 点击 `Create role`  在 Privlleges 选项搜索 docker 把相应的规则移动到右边的框中然后保存。

添加用户：菜单 `Security->Users` 点击 `Create local user` 在 Roles 选项中选中刚才创建的规则移动到右边的窗口保存。

关于其他的使用方法，请参见 Nexus 的官网或者自行网上搜索。

## Nginx 加密代理

Nginx 的安装方法请自行网上查找答案，这里只讲配置方法。

证书的生成请参见 [`私有仓库高级配置`](https://yeasy.gitbooks.io/docker_practice/content/repository/registry_auth.html) 里面证书生成一节。

安装完以后编辑 Nginx 配置文件
```bash
upstream register
{
server "YourHostName OR IP":5001; #端口为上面添加的私有镜像仓库是设置的 HTTP 选项的端口号
check interval=3000 rise=2 fall=10 timeout=1000 type=http;
check_http_send "HEAD / HTTP/1.0\r\n\r\n";
check_http_expect_alive http_4xx;
}
server {
    server_name YourDomainName;#如果没有 DNS 服务器做解析，请删除此选项使用本机 IP 地址访问
    listen       443 ssl;
    ssl_certificate key/example.crt; #生成的证书放入到 Nginx 配置文件conf目录中，key 目录自行创建。
    ssl_certificate_key key/example.key;
    ssl_session_timeout  5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers  HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers   on;
    large_client_header_buffers 4 32k;
    client_max_body_size 300m;
    client_body_buffer_size 512k;
    proxy_connect_timeout 600;
    proxy_read_timeout   600;
    proxy_send_timeout   600;
    proxy_buffer_size    128k;
    proxy_buffers       4 64k;
    proxy_busy_buffers_size 128k;
    proxy_temp_file_write_size 512k;

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Port $server_port;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://register;
        proxy_read_timeout 900s;

    }
    error_page   500 502 503 504  /50x.html;
}
```
## Docker 主机访问镜像仓库

如果不启用 SSL 加密可以通过前面章节的方法添加信任地址到 Docker 的配置文件中重启程序
使用 SSL 加密以后程序需要访问就不能采用修改配置的访问了。具体方法如下：
```bash
openssl s_client -showcerts -connect YourDomainName OR HostIP:443 </dev/null 2>/dev/null|openssl x509 -outform PEM >ca.crt
cat ca.crt | sudo tee -a /etc/ssl/certs/ca-certificates.crt
systemctl restart docker
```
使用 `docker login YourDomainName OR HostIP` 进行测试，用户名密码填写上面 Nexus 中生成的。
