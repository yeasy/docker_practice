## Install Docker CE on CentOS

> WARNING: DO NOT install Docker with yum directly without configuring yum source.

### Prerequisites

#### OS Requirement
Docker CE supports 64-bit version of CentOS 7, and it requires the kernel version to be no older than 3.10. CentOS 7 satisfies the minimum kernel version requirement. But due to the comparatively old kernel, some of the functionalities like `overlay2` are unable to be used, and some other features may be unstable.

#### Uninstall the Old Versions

The old versions of Docker are called `docker` or `docker-engine`, you can have them uninstalled with the following command:

```bash
$ sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
```

### Install with yum

Use the following commands to install the dependencies:

```bash
$ sudo yum install -y yum-utils \
           device-mapper-persistent-data \
           lvm2
```

Due to the network issues in China mainland, it is highly recommended for Chinese users to use Chinese sources. Please refer to the official sources in the comments(they are replaced by a Chinese source).

Use the following command to add `dnf` source.
```bash
$ sudo yum-config-manager \
    --add-repo \
    https://mirrors.ustc.edu.cn/docker-ce/linux/centos/docker-ce.repo


# Official source
# $ sudo yum-config-manager \
#     --add-repo \
#     https://download.docker.com/linux/centos/docker-ce.repo
```

If you want to use the `test` version of Docker CE, use the following command:

```bash
$ sudo yum-config-manager --enable docker-ce-test
```

As for `nightly` version:

```bash
$ sudo yum-config-manager --enable docker-ce-nightly
```

#### Install Docker CE

Update `yum` source cache，and then install `docker-ce`.

```bash
$ sudo yum makecache fast
$ sudo yum install docker-ce
```

### Install with Automatic Scripts

To simplify the installation process during test or development, Docker official provides a convenient installation script, you can install docker on Fedora with the following script:

```bash
$ curl -fsSL get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh --mirror Aliyun
```

After execution, the script will have everything prepared, and have installed the stable version on your OS.

### Start Docker CE

```bash
$ sudo systemctl enable docker
$ sudo systemctl start docker
```

### Add Docker Usergroups

Command `docker` uses [Unix socket](https://en.wikipedia.org/wiki/Unix_domain_socket) to communicate with Docker engine by default. Only users of `root` and `docker` groups can communicate with Unix socket of the Docker engine.`root` user is not directly used on Linux systems in general for security. Therefore, it is better to add users who need to use `docker` to the `docker` user group.

create `docker` group:

```bash
$ sudo groupadd docker
```

add current user to `docker` group:

```bash
$ sudo usermod -aG docker $USER
```

Exit current terminal and relogin to test.

### Verify the Installation

```bash
$ docker run hello-world

Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
d1725b59e92d: Pull complete
Digest: sha256:0add3ace90ecb4adbf7777e9aacf18357296e799f81cabc9fde470971e499788
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

If it shows the above message, it means your installation is successful.

### Registry Mirror(In China)

If you pull docker images very slowly, then you can configure [Registry Mirror](mirror.md).

### Add kernel Parameters

If you see the following warnings when using Docker CE,

```bash
WARNING: bridge-nf-call-iptables is disabled
WARNING: bridge-nf-call-ip6tables is disabled
```

Please add the kernel parameters to enable these features.

```bash
$ sudo tee -a /etc/sysctl.conf <<-EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
```

Then reload the `sysctl.confg`

```bash
$ sudo sysctl -p
```

### References

* [Docker Official Installation Documents for Fedora](https://docs.docker.com/install/linux/docker-ce/centos/)
