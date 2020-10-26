## Install Docker CE on Debian
> WARNING: DO NOT install Docker with apt directly without configuring apt source.

### Prerequisites

#### OS Requirement

Docker CE supports the following [Debian](https://www.debian.org/intro/about) versions.

* Buster 10
* Stretch 9

#### Uninstall the Old Versions

The old versions of Docker are called `docker` or `docker-engine`, you can have them uninstalled with the following command:

```bash
$ sudo apt-get remove docker \
               docker-engine \
               docker.io
```

### Install with apt

Since the apt source uses HTTPS to make sure that the software is not modified maliciously during download, we have to add the apt source via HTTPS as well as the CA certificate.

```bash
$ sudo apt-get update

$ sudo apt-get install \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg2 \
     lsb-release \
     software-properties-common
```

Due to the network issues in China mainland, it is highly recommended for Chinese users to use Chinese sources. Please refer to the official sources in the comments(they are replaced by a Chinese source).

To verify the validity of the package downloaded, we have to add the GPG key for the package source.

```bash
$ curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/debian/gpg | sudo apt-key add -


# Official source
# $ curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
```

After that, we need to add the Docker CE source to `source.list`: 

```bash
$ sudo add-apt-repository \
   "deb [arch=amd64] https://mirrors.ustc.edu.cn/docker-ce/linux/debian \
   $(lsb_release -cs) \
   stable"

# Official source
# $ sudo add-apt-repository \
#    "deb [arch=amd64] https://download.docker.com/linux/debian \
#    $(lsb_release -cs) \
#    stable"
```

> The above commands will add the APT source for the stable version of Docker CE. If you need the `test` or `nightly` source, please replace with them to meet your own needs.

#### Install Docker CE

Update apt cache and install `docker-ce`

```bash
$ sudo apt-get update

$ sudo apt-get install docker-ce
```

### Install with Automatic Scripts

To simplify the installation process during test or development, Docker official provides a convenient installation script, you can install docker on Debian with the following script:

```bash
$ curl -fsSL get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh --mirror Aliyun
```

After execution, the script will have everything prepared, and install the stable version on your OS.

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

### Test whether Docker is installed correctly

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

If it shows above message, it means your installation is successful.

### Registry Mirror(In China)

If you pull docker images very slowly, then you can configure [Registry Mirror](mirror.md).

### References

* [Docker Oficial Debian Installation Documents](https://docs.docker.com/install/linux/docker-ce/debian/)
