# Debian操作系统安装Docker
##支持的版本
- Debian testing stretch (64-bit)
- Debian 8.0 Jessie (64-bit)
- Debian 7.7 Wheezy (64-bit)
##预安装
Docker支持64位、内核高于3.10的Debian操作系统，内核低于3.10将导致数据丢失和系统不稳定等问题。
查看内核版本使用以下命令：
```
$ uname -r
```
###更新APT仓库
Docker的APT仓库包含了1.7.1及以上版本的Docker，安装前需要更新APT设置，来使用新的仓库：
1. 清理旧的仓库信息
```sh
 $ apt-get purge lxc-docker*
 $ apt-get purge docker.io*
```
2. 更新和安装软件包
```sh
 $ apt-get update
 $ apt-get install apt-transport-https ca-certificates
```
3. 添加GPG键
```
 $ apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
```
4. 添加APT源
  - 编辑文件 ```/etc/apt/sources.list.d/docker.list```,清理已存在的信息
5. 校验安装结果
##安装Docker
##为非root用户授权
##更新Docker
##卸载Docker

