## Pull Docker Images

As we have mentioned, there are many high quality docker images on [Docker Hub](https://hub.docker.com/explore/). In this section, we will introduce how to `pull` these images.

The command to fetch image from docker registry is `docker pull`. The command format is:

```bash
docker pull [OPTIONS] [Docker Registry ADDRESS[:PORT]/]NAME[:TAG]
```

More options can be found by `docker pull --help` command. Now let us see the format for image names.

* Docker Repository Address: the address format is typically `<domain/IP>[:PORT]`. The default address is Docker Hub.

* Repository: as mentioned before, the repository name consists of 2 parts, i.e., `username/software-name`(separated by the slash). For docker Hub, if the username is not specified, the default is `library`, where all the official images are in.

For example,

```bash
$ docker pull ubuntu:18.04
18.04: Pulling from library/ubuntu
bf5d46315322: Pull complete
9f13e0ac480c: Pull complete
e8988b5b3097: Pull complete
40af181810e7: Pull complete
e6f7c7e5c03e: Pull complete
Digest: sha256:147913621d9cdea08853f6ba9116c2e27a3ceffecf3b492983ae97c3d643fbbe
Status: Downloaded newer image for ubuntu:18.04
```

The Docker image repository is not given, so it will pull the image from Docker Hub. Since the image name is `ubuntu:18.04`, so it will get the official image with tag `18.04` from `library/ubuntu`.

From the download log, we can see the layered storage concept - images are composed of multiple layers of storage. And we download images layer by layer instead of a single file. During the download process, the first 12 hexadecimal bits of each layer are shown. And after the download, the `sha256` summary is given, to verify the integrity of downloaded files.

When using the above command, you may find that the layer ID and `sha256` you see are different from what they are here, because the official layer is maintained and updated frequently. In case there is any new bug or new edition, the image will be rebuilt and published with the original tag. This makes sure that all the users use safer and more stable images.

*If it is slow to download images from Docker Hub, you can refer to [Image Accelerators](/install/mirror.md) to configure accelerator.*

### Run
With the image, we can run a container based on the image. Taking the above `ubuntu:18.04` as an example, if we want to start the `bash` inside it for interactive operations, we can execute the following commands.


```bash
$ docker run -it --rm \
    ubuntu:18.04 \
    bash

root@e7009c6ce357:/# cat /etc/os-release
NAME="Ubuntu"
VERSION="18.04.1 LTS (Bionic Beaver)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 18.04.1 LTS"
VERSION_ID="18.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=bionic
UBUNTU_CODENAME=bionic
```

`docker run` is the command for running the container, the detailed format will be explained in the [container](../container) chapter. Here we only illustrate the parameters used above.

* `-it`: There are 2 parameters here, the first is `-i`, for interactive operations, another is `-t`, which is for terminal. What we intend to do is to enter the `bash` terminal of docker, then execute some commands and see the output. That's why we need the interactive terminal.

* `--rm`: Remove the docker after stop it. In default, for troubleshooting, the docker is not removed immediately after quitting, unless manually remove it using `docker rm`. But in our case, we only test the commands and to see the resutls, we don't care much about the results, so we use `--rm` to avoid wasting space.

* `ubuntu:18.04`: use `ubuntu:18:04` as the base image to start the container.

* `bash`: What we have after the image name is **command**, since we want an interactive shell, so we use `bash` as the command here.

After entering the comainer, we can execute any command we want. Here, we executed `cat etc/os-release`, which is the commonly-used command to view the version of the current OS. We can see from the result that the container is based on `Ubuntu 18.04.1 LTS`.

In the end, we quit the container with `exit`.
