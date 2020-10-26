## Install Docker Desktop CE on maxOS

### OS Requirement

The minimum OS version requirement [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/) is macOS El Capitan 10.11.

### Installation

#### Install with Homebrew

The [Cask](https://caskroom.github.io/) of [Homebrew](https://brew.sh/) has already supported Docker Desktop for Mac, so we can instrall it with Homebrew Cask easily.

```bash
$ brew cask install docker
```

#### Download and Install Manually

If you need to download `Docker Desktop for Mac` manually, please click the [Stable](https://download.docker.com/mac/stable/Docker.dmg) or [Edge](https://download.docker.com/mac/edge/Docker.dmg) link to downlaod it.

Just as other softwares on macOS, the installation of Docker Desktop for macOS is easy. You only need to double click the `.dmg` file, and then drag the whale([Moby](https://blog.docker.com/2013/10/call-me-moby-dock/)) icon to the `Applications` folder. During the process, you will be prompted to enter your password for your mac.

![](_images/install-mac-dmg.png)

### Run

Find the Docker icon from your applications, and double click the icon to run Docker Desktop.

![](_images/install-mac-apps.png)

After running, there should be a whale icon on the top right bar of your mac desktop. This icon indicates the running status of Docker.

![](_images/install-mac-menubar.png)

For the first time clicking on the icon, you may see the successful installation window. Clicking on "Got it!" will close the window.

![](_images/install-mac-success.png)

Clicking on the whale icon each time afterwards will show you the operation menu.

![](_images/install-mac-menu.png)

After opening the terminal, you can check the newly-installed Docker version with commands.

```bash
$ docker --version
Docker version 19.03.1, build 74b1e89
$ docker-compose --version
docker-compose version 1.24.1, build 4667896b
$ docker-machine --version
docker-machine version 0.16.1, build cce350d7
```

If `docker version` and `docker info` shows no error nor warning, you can try to run an [Nginx Server](https://hub.docker.com/_/nginx/).


```bash
$ docker run -d -p 80:80 --name webserver nginx
```

When the sever is up and running, you can visit <http://localhost>, if you see "Welcome to nginx!", it means the installation of Docker Desktop for macOS is successful.

![](_images/install-mac-example-nginx.png)

To stop the Nginx server and delete it, you can execute the following commands:

```bash
$ docker stop webserver
$ docker rm webserver
```

### Registry Mirror(In China)

If you pull docker images very slowly, then you can configure [Registry Mirror](mirror.md).

### References

* [Official Document](https://docs.docker.com/docker-for-mac/install/)
