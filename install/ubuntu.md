## Install Docker CE on Ubuntu

> warning: Don't install Docker CE directly using apt without configuring Docker APT source.

### Preparation

#### System requirements

Docker CE supported [Ubuntu](https://www.ubuntu.com/server) versions:

* Disco 19.04
* Cosmic 18.10
* Bionic 18.04 (LTS)
* Xenial 16.04 (LTS)

Docker CE can be installed on x86 platform or ARM. In Ubuntu distributions, LTS (Long-Term-Support) will get 5 years updating support, distributions like this will be stable. Therefore, LTS version is recommended in production environment.

#### Uninstall old version

Old version of Docker is called `docker` or `docker-engine`. Use the following command to uninstall the old version:

```bash
$ sudo apt-get remove docker \
               docker-engine \
               docker.io
```

### Use APT to install

Because the `apt` source uses HTTPS to ensure that software downloads are not tampered with. Therefore, we need to add software packages and CA certificates that are transmitted using HTTPS first.

```bash
$ sudo apt-get update

$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
```

If you are in China, it is strongly recommended to use Chinese sources. The official sources are in the comments.

In order to confirm the validity of the downloaded package, we need to add the `GPG` key of the software source.

```bash
$ curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg | sudo apt-key add -


# official
# $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

Then, we need to add Docker software source to `source.list`

```bash
$ sudo add-apt-repository \
    "deb [arch=amd64] https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu \
    $(lsb_release -cs) \
    stable"


# official
# $ sudo add-apt-repository \
#    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
#    $(lsb_release -cs) \
#    stable"
```

> The above commands will add stable Docker CE APT source. If you need the `test` or `nightly` version of Docker, you can change `stable` to `test` or `nightly`.

#### Install Docker CE

Update apt cache and install `docker-ce`:

```bash
$ sudo apt-get update

$ sudo apt-get install docker-ce
```

### Auto install by script

Docker Offical has provided a set of convenient installation scripts which can be installed on Ubuntu for test or dev environments.

```bash
$ curl -fsSL get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh --mirror Aliyun
```

The script will have everything prepared and install the stable version of Docker CE for the system after execution.

### Launcher Docker CE

```bash
$ sudo systemctl enable docker
$ sudo systemctl start docker
```

### Add docker user group

Command `docker` uses [Unix socket](https://en.wikipedia.org/wiki/Unix_domain_socket) to communicate with Docker engine default. Only users of `root` and `docker` groups can communicate with Unix socket of Docker engine.`root` user is not directly used on Linux systems in general for security. Therefore, it is better to add users who need to use `docker` to the `docker` user group.

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

If you pull docker images very slowly, then you can configurate [Registry Mirror](mirror.md).

### References

* [Offical Docker Docs](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
