## 私有仓库高级配置

上一节我们搭建了一个具有基础功能的私有仓库，本小节我们来使用 `Docker Compose` 搭建一个拥有权限认证、TLS 的私有仓库。

新建一个文件夹，以下步骤均在该文件夹中进行。

### 准备站点证书

如果你拥有一个域名，国内各大云服务商均提供免费的站点证书。你也可以使用 `openssl` 自行签发证书。

这里假设我们将要搭建的私有仓库地址为 `docker.domain.com`，下面我们介绍使用 `openssl` 自行签发 `docker.domain.com` 的站点 SSL 证书。

第一步创建 `CA` 私钥。

```bash
$ openssl genrsa -out "root-ca.key" 4096
```

第二步利用私钥创建 `CA` 根证书请求文件。

```bash
$ openssl req \
          -new -key "root-ca.key" \
          -out "root-ca.csr" -sha256 \
          -subj '/C=CN/ST=Shanxi/L=Datong/O=Your Company Name/CN=Your Company Name Docker Registry CA'
```

>以上命令中 `-subj` 参数里的 `/C` 表示国家，如 `CN`；`/ST` 表示省；`/L` 表示城市或者地区；`/O` 表示组织名；`/CN` 通用名称。

第三步配置 `CA` 根证书，新建 `root-ca.cnf`。

```bash
[root_ca]
basicConstraints = critical,CA:TRUE,pathlen:1
keyUsage = critical, nonRepudiation, cRLSign, keyCertSign
subjectKeyIdentifier=hash
```

第四步签发根证书。

```bash
$ openssl x509 -req  -days 3650  -in "root-ca.csr" \
               -signkey "root-ca.key" -sha256 -out "root-ca.crt" \
               -extfile "root-ca.cnf" -extensions \
               root_ca
```

第五步生成站点 `SSL` 私钥。

```bash
$ openssl genrsa -out "docker.domain.com.key" 4096
```

第六步使用私钥生成证书请求文件。

```bash
$ openssl req -new -key "docker.domain.com.key" -out "site.csr" -sha256 \
          -subj '/C=CN/ST=Shanxi/L=Datong/O=Your Company Name/CN=docker.domain.com'
```

第七步配置证书，新建 `site.cnf` 文件。

```bash
[server]
authorityKeyIdentifier=keyid,issuer
basicConstraints = critical,CA:FALSE
extendedKeyUsage=serverAuth
keyUsage = critical, digitalSignature, keyEncipherment
subjectAltName = DNS:docker.domain.com, IP:127.0.0.1
subjectKeyIdentifier=hash
```

第八步签署站点 `SSL` 证书。

```bash
$ openssl x509 -req -days 750 -in "site.csr" -sha256 \
    -CA "root-ca.crt" -CAkey "root-ca.key"  -CAcreateserial \
    -out "docker.domain.com.crt" -extfile "site.cnf" -extensions server
```

这样已经拥有了 `docker.domain.com` 的网站 SSL 私钥 `docker.domain.com.key` 和 SSL 证书 `docker.domain.com.crt`。

新建 `ssl` 文件夹并将 `docker.domain.com.key` `docker.domain.com.crt` 这两个文件移入，删除其他文件。

### 配置私有仓库

私有仓库默认的配置文件位于 `/etc/docker/registry/config.yml`，我们先在本地编辑 `config.yml`，之后挂载到容器中。

```yaml
version: 0.1
log:
  accesslog:
    disabled: true
  level: debug
  formatter: text
  fields:
    service: registry
    environment: staging
storage:
  delete:
    enabled: true
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
auth:
  htpasswd:
    realm: basic-realm
    path: /etc/docker/registry/auth/nginx.htpasswd
http:
  addr: :443
  host: https://docker.domain.com
  headers:
    X-Content-Type-Options: [nosniff]
  http2:
    disabled: false
  tls:
    certificate: /etc/docker/registry/ssl/docker.domain.com.crt
    key: /etc/docker/registry/ssl/docker.domain.com.key
health:
  storagedriver:
    enabled: true
    interval: 10s
threshold: 3
```

### 生成 http 认证文件

```bash
$ mkdir auth

$ docker run --rm \
    --entrypoint htpasswd \
    registry \
    -Bbn username password > auth/nginx.htpasswd
```

> 将上面的 `username` `password` 替换为你自己的用户名和密码。

### 编辑 `docker-compose.yml`

```yaml
version: '3'

services:
  registry:
    image: registry
    ports:
      - "443:443"
    volumes:
      - ./:/etc/docker/registry
      - registry-data:/var/lib/registry

volumes:
  registry-data:
```

### 修改 hosts

编辑 `/etc/hosts`

```bash
127.0.0.1 docker.domain.com
```

### 启动

```bash
$ docker-compose up -d
```

这样我们就搭建好了一个具有权限认证、TLS 的私有仓库，接下来我们测试其功能是否正常。

### 测试私有仓库功能

登录到私有仓库。

```bash
$ docker login docker.domain.com
```

尝试推送、拉取镜像。

```bash
$ docker pull ubuntu:17.10

$ docker tag ubuntu:17.10 docker.domain.com/username/ubuntu:17.10

$ docker push docker.domain.com/username/ubuntu:17.10

$ docker image rm docker.domain.com/username/ubuntu:17.10

$ docker pull docker.domain.com/username/ubuntu:17.10
```

如果我们退出登录，尝试推送镜像。

```bash
$ docker logout docker.domain.com

$ docker push docker.domain.com/username/ubuntu:17.10

no basic auth credentials
```

发现会提示没有登录，不能将镜像推送到私有仓库中。

### 注意事项

如果你本机占用了 `443` 端口，你可以配置 [Nginx 代理](https://docs.docker.com/registry/recipes/nginx/)，这里不再赘述。
