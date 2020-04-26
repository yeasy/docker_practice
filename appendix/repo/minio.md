# minio
[TOC]
MinIO 是一个基于Apache License v2.0开源协议的对象存储服务。它兼容亚马逊S3云存储服务接口，非常适合于存储大容量非结构化的数据，例如图片、视频、日志文件、备份数据和容器/虚拟机镜像等，而一个对象文件可以是任意大小，从几kb到最大5T不等。

MinIO是一个非常轻量的服务,可以很简单的和其他应用的结合，类似 NodeJS, Redis 或者 MySQL。

[官方文档](https://docs.min.io/)

## 简单使用

测试、开发环境下不考虑数据存储的情况下可以使用下面的命令快速开启服务。

```bash
docker pull minio/minio
docker run -p 9000:9000 minio/minio server /data
```



## 离线部署

许多生产环境是一般是没有公网资源的，这就需要从有公网资源的服务器上把镜像导出，然后导入到需要运行镜像的内网服务器。

### 导出镜像

在有公网资源的服务器上下载好`minio/minio`镜像

```bash
docker save -o minio.tar minio/minio:latest
```

<!--使用docker save 的时候，也可以使用image id 来导出，但是那样导出的时候，就会丢失原来的镜像名称，推荐，还是使用镜像名字+tag来导出镜像-->

### 导入镜像

把压缩文件复制到内网服务器上，使用下面的命令导入镜像

```bash
docker load minio.tar 
```

### 运行 minio

- 把/mnt/data 改成要替换的数据目录
- 替换 MINIO_ACCESS_KEY
- 替换 MINIO_SECRET_KEY
- 替换 name,minio1(可选)
- 如果9000端口冲突,替换端口前面的如:9009:9000

```bash
sudo docker run -d -p 9000:9000 --name minio1 \
  -e "MINIO_ACCESS_KEY=改成自己需要的" \
  -e "MINIO_SECRET_KEY=改成自己需要的" \
  -v /mnt/data:/data \
  --restart=always \
  minio/minio server /data
```

### 访问 web 管理页面

http://x.x.x.x:9000/minio/

