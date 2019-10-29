## 实战多阶段构建 Laravel 镜像

> 本节适用于 PHP 开发者阅读。

### 准备

新建一个 `Laravel` 项目或在已有的 `Laravel` 项目根目录下新建 `Dockerfile` `.dockerignore` `laravel.conf` 文件。

在 `.dockerignore` 文件中写入以下内容。

```bash
.idea/
.git/
vendor/
node_modules/
public/js/
public/css/
yarn-error.log

bootstrap/cache/*
storage/

# 自行添加其他需要排除的文件，例如 .env.* 文件
```

在 `laravel.conf` 文件中写入 nginx 配置。

```nginx
server {
  listen 80 default_server;
  root /app/laravel/public;
  index index.php index.html;

  location / {
      try_files $uri $uri/ /index.php?$query_string;
  }

  location ~ .*\.php(\/.*)*$ {
    fastcgi_pass   laravel:9000;
    include        fastcgi.conf;

    # fastcgi_connect_timeout 300;
    # fastcgi_send_timeout 300;
    # fastcgi_read_timeout 300;
  }
}
```

### 前端构建

第一阶段进行前端构建。

```docker
FROM node:alpine as frontend

COPY package.json /app/

RUN cd /app \
      && npm install --registry=https://registry.npm.taobao.org

COPY webpack.mix.js /app/
COPY resources/assets/ /app/resources/assets/

RUN cd /app \
      && npm run production
```

### 安装 Composer 依赖

第二阶段安装 Composer 依赖。

```docker
FROM composer as composer

COPY database/ /app/database/
COPY composer.json composer.lock /app/

RUN cd /app \
      && composer config -g repo.packagist composer https://mirrors.aliyun.com/composer/ \
      && composer install \
           --ignore-platform-reqs \
           --no-interaction \
           --no-plugins \
           --no-scripts \
           --prefer-dist
```

### 整合以上阶段所生成的文件

第三阶段对以上阶段生成的文件进行整合。

```docker
FROM php:7.2-fpm-alpine as laravel

ARG LARAVEL_PATH=/app/laravel

COPY --from=composer /app/vendor/ ${LARAVEL_PATH}/vendor/
COPY . ${LARAVEL_PATH}
COPY --from=frontend /app/public/js/ ${LARAVEL_PATH}/public/js/
COPY --from=frontend /app/public/css/ ${LARAVEL_PATH}/public/css/
COPY --from=frontend /app/mix-manifest.json ${LARAVEL_PATH}/mix-manifest.json

RUN cd ${LARAVEL_PATH} \
      && php artisan package:discover \
      && mkdir -p storage \
      && mkdir -p storage/framework/cache \
      && mkdir -p storage/framework/sessions \
      && mkdir -p storage/framework/testing \
      && mkdir -p storage/framework/views \
      && mkdir -p storage/logs \
      && chmod -R 777 storage
```

### 最后一个阶段构建 NGINX 镜像

```docker
FROM nginx:alpine as nginx

ARG LARAVEL_PATH=/app/laravel

COPY laravel.conf /etc/nginx/conf.d/
COPY --from=laravel ${LARAVEL_PATH}/public ${LARAVEL_PATH}/public
```

### 构建 Laravel 及 Nginx 镜像

使用 `docker build` 命令构建镜像。

```bash
$ docker build -t my/laravel --target=laravel .

$ docker build -t my/nginx --target=nginx .
```

### 启动容器并测试

新建 Docker 网络

```bash
$ docker network create laravel
```

启动 laravel 容器， `--name=laravel` 参数设定的名字必须与 `nginx` 配置文件中的 `fastcgi_pass   laravel:9000;` 一致

```bash
$ docker run -it --rm --name=laravel --network=laravel my/laravel
```

启动 nginx 容器

```bash
$ docker run -it --rm --network=laravel -p 8080:80 my/nginx
```

浏览器访问 `127.0.0.1:8080` 可以看到 Laravel 项目首页。

> 也许 Laravel 项目依赖其他外部服务，例如 redis、MySQL，请自行启动这些服务之后再进行测试，本小节不再赘述。

### 生产环境优化

本小节内容为了方便测试，将配置文件直接放到了镜像中，实际在使用时 **建议** 将配置文件作为 `config` 或 `secret` 挂载到容器中，请读者自行学习 `Swarm mode` 或 `Kubernetes` 的相关内容。

### 附录

完整的 `Dockerfile` 文件如下。

```docker
FROM node:alpine as frontend

COPY package.json /app/

RUN cd /app \
      && npm install --registry=https://registry.npm.taobao.org

COPY webpack.mix.js /app/
COPY resources/assets/ /app/resources/assets/

RUN cd /app \
      && npm run production

FROM composer as composer

COPY database/ /app/database/
COPY composer.json /app/

RUN cd /app \
      && composer config -g repo.packagist composer https://mirrors.aliyun.com/composer/ \
      && composer install \
           --ignore-platform-reqs \
           --no-interaction \
           --no-plugins \
           --no-scripts \
           --prefer-dist

FROM php:7.2-fpm-alpine as laravel

ARG LARAVEL_PATH=/app/laravel

COPY --from=composer /app/vendor/ ${LARAVEL_PATH}/vendor/
COPY . ${LARAVEL_PATH}
COPY --from=frontend /app/public/js/ ${LARAVEL_PATH}/public/js/
COPY --from=frontend /app/public/css/ ${LARAVEL_PATH}/public/css/
COPY --from=frontend /app/mix-manifest.json ${LARAVEL_PATH}/mix-manifest.json

RUN cd ${LARAVEL_PATH} \
      && php artisan package:discover \
      && mkdir -p storage \
      && mkdir -p storage/framework/cache \
      && mkdir -p storage/framework/sessions \
      && mkdir -p storage/framework/testing \
      && mkdir -p storage/framework/views \
      && mkdir -p storage/logs \
      && chmod -R 777 storage

FROM nginx:alpine as nginx

ARG LARAVEL_PATH=/app/laravel

COPY laravel.conf /etc/nginx/conf.d/
COPY --from=laravel ${LARAVEL_PATH}/public ${LARAVEL_PATH}/public
```
