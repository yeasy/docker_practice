# Busybox

## 简介

![Busybox - Linux 瑞士军刀](_images/busybox-logo.png)

`BusyBox` 是一个集成了一百多个最常用 Linux 命令和工具（如 `cat`、`echo`、`grep`、`mount`、`telnet` 等）的精简工具箱，它只需要几 MB 的大小，很方便进行各种快速验证，被誉为“Linux 系统的瑞士军刀”。

`BusyBox` 可运行于多款 `POSIX` 环境的操作系统中，如 `Linux`（包括 `Android`）、`Hurd`、`FreeBSD` 等。

## 获取官方镜像

在 `Docker Hub` 中搜索 `busybox` 相关的镜像。

```bash
$ docker search busybox
NAME                            DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
busybox                         Busybox base image.                             755       [OK]
progrium/busybox                                                                63                   [OK]
radial/busyboxplus              Full-chain, Internet enabled, busybox made...   11                   [OK]
odise/busybox-python                                                            3                    [OK]
multiarch/busybox               multiarch ports of ubuntu-debootstrap           2                    [OK]
azukiapp/busybox                This image is meant to be used as the base...   2                    [OK]
...
```

读者可以看到最受欢迎的镜像同时带有 `OFFICIAL` 标记，说明它是官方镜像。用户使用 `docker pull` 指令下载 `busybox:latest` 镜像：

```bash
$ docker pull busybox:latest
busybox:latest: The image you are pulling has been verified
e433a6c5b276: Pull complete
e72ac664f4f0: Pull complete
511136ea3c5a: Pull complete
df7546f9f060: Pull complete
Status: Downloaded newer image for busybox:latest
```

下载后，可以看到 `busybox` 镜像只有 **2.433 MB**：

```bash
$ docker image ls
REPOSITORY                   TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
busybox                   latest              e72ac664f4f0        6 weeks ago         2.433 MB
```

## 运行 busybox

启动一个 `busybox` 容器，并在容器中执行 `grep` 命令。

```bash
$ docker run -it busybox
/ # grep
BusyBox v1.22.1 (2014-05-22 23:22:11 UTC) multi-call binary.

Usage: grep [-HhnlLoqvsriwFE] [-m N] [-A/B/C N] PATTERN/-e PATTERN.../-f FILE [FILE]...

Search for PATTERN in FILEs (or stdin)

        -H      Add 'filename:' prefix
        -h      Do not add 'filename:' prefix
        -n      Add 'line_no:' prefix
        -l      Show only names of files that match
        -L      Show only names of files that don't match
        -c      Show only count of matching lines
        -o      Show only the matching part of line
        -q      Quiet. Return 0 if PATTERN is found, 1 otherwise
        -v      Select non-matching lines
        -s      Suppress open and read errors
        -r      Recurse
        -i      Ignore case
        -w      Match whole words only
        -x      Match whole lines only
        -F      PATTERN is a literal (not regexp)
        -E      PATTERN is an extended regexp
        -m N    Match up to N times per file
        -A N    Print N lines of trailing context
        -B N    Print N lines of leading context
        -C N    Same as '-A N -B N'
        -e PTRN Pattern to match
        -f FILE Read pattern from file
```

查看容器内的挂载信息。

```bash
/ # mount
rootfs on / type rootfs (rw)
none on / type aufs (rw,relatime,si=b455817946f8505c)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
tmpfs on /dev type tmpfs (rw,nosuid,mode=755)
shm on /dev/shm type tmpfs (rw,nosuid,nodev,noexec,relatime,size=65536k)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=666)
sysfs on /sys type sysfs (ro,nosuid,nodev,noexec,relatime)
/dev/disk/by-uuid/b1f2dba7-d91b-4165-a377-bf1a8bed3f61 on /etc/resolv.conf type ext4 (rw,relatime,errors=remount-ro,data=ordered)
/dev/disk/by-uuid/b1f2dba7-d91b-4165-a377-bf1a8bed3f61 on /etc/hostname type ext4 (rw,relatime,errors=remount-ro,data=ordered)
/dev/disk/by-uuid/b1f2dba7-d91b-4165-a377-bf1a8bed3f61 on /etc/hosts type ext4 (rw,relatime,errors=remount-ro,data=ordered)
devpts on /dev/console type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
proc on /proc/sys type proc (ro,nosuid,nodev,noexec,relatime)
proc on /proc/sysrq-trigger type proc (ro,nosuid,nodev,noexec,relatime)
proc on /proc/irq type proc (ro,nosuid,nodev,noexec,relatime)
proc on /proc/bus type proc (ro,nosuid,nodev,noexec,relatime)
tmpfs on /proc/kcore type tmpfs (rw,nosuid,mode=755)
```

`busybox` 镜像虽然小巧，但包括了大量常见的 `Linux` 命令，读者可以用它快速熟悉 `Linux` 命令。

## 相关资源

* `Busybox` 官网：https://busybox.net/
* `Busybox` 官方仓库：https://git.busybox.net/busybox/
* `Busybox` 官方镜像：https://hub.docker.com/_/busybox/
* `Busybox` 官方仓库：https://github.com/docker-library/busybox
