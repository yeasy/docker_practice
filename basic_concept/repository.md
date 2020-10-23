## Docker Registry

After the construction of an image, we can easily run it on a host. However, if we want to use the image on other servers, we need a centralized image storage and distribution service. The [Docker Registry](../repository/registry.md) we will introduce is such a service.

A **Docker Registry** can contain several `Repositories`, where each  repository can contain several tags and each tag corresponds to an image.

Typically, a repository contains images for different versions of the same software, where each tags corresponds to different versions of the software. We can uniquely identify an image of the same software with `repository:tag`. In case not explicitly specified, `latest` is taken as default tag. 

Taking the [Ubuntu Image](https://hub.docker.com/_/ubuntu) as an example. `ubuntu` is the name for repository, and inside it are tags for different versions, for instance, `16.04`, `18.04`. We can use `ubuntu:16.04` or `ubuntu:18.04` to specify the particular image we want. If the tag is omitted, for example, `ubuntu`, then it will be considered as `ubuntu:latest`.

Repository name is typically seperated by a forward slash(/), for example, `jwilder/nginx-proxy`, the former is to identify a particular user in a multi-user Docker Registry, while the latter corresponds to the software name. But it is not always the case. It also depends on the Docker Registry software or service you are using.

### Docker Registry Public Services

`Docker Registry Public Services` are registry services open to users, allowing users to manage their images. Typically, those public services offer user free image uploads and downloads, and possibly provide charged service for privately managed images.

The most commonly used registry public service is the official [Docker Hub](https://hub.docker.com/), which is the default registry with thousands of high quality official images. Besides, the images for [Quay.io](https://quay.io/repository/) and CoreOS of [CoreOS](https://coreos.com/) are stored there. Google's [Google Container Registry](https://cloud.google.com/container-registry/) and [Kubernetes](https://kubernetes.io/) also use this service.

Due to some reasons knwon to all, accessing those services from China mainland is slow. There are some cloud service providers in China providing `Registry Mirror` for Docker Hub, those mirror services are called `accelerators`. The well-known ones are [Ali Cloud Image Accelerator](https://cr.console.aliyun.com/#/accelerator) and [DaoCloud Accelerator](https://www.daocloud.io/mirror#accelerator-doc). In China, downloading from these services are much faster than from Docker Hub. The detailed image source configuration tutorial is in the [Docker Installation](../install/mirror.md) section.

There are also some cloud service providers that provide public services similar to Docker Hub in China. For example, [Tenxcloud Mirror Registry](https://hub.tenxcloud.com/), [NetEase Mirror Registry](https://c.163.com/hub#/m/library/), [DaoCloud Mirror Market](https://hub.daocloud.io/), [Ali Cloud Mirror Registry](https://cr.console.aliyun.com), etc.

### Private Docker Registry

Apart from using public service, a user can set up private Docker Registry. Docker offical offers the [Docker Registry](https://hub.docker.com/_/registry/) docker image, which can be deployed for private registry service. We will explain how to set it up in detail in the [Private Registry](../repository/registry.md) section.

The open source Docker Registry image only provides the backend of  [Docker Registry API](https://docs.docker.com/registry/spec/api/), which supports the `docker` commands and is enough for personal use, although the advanced functionalities like GUI(Graphical User Interface), Image Maintenance and Access Control are not supported. However, they are provided in the commercial version - [Docker Trusted Registry](https://docs.docker.com/datacenter/dtr/2.0/).

Except for the official Docker Registry, there are third-party softwares that implement Docker Registry API, even with some advanced features like user interface. For example, [Harbor](https://github.com/goharbor/harbor) and [Sonatype Nexus](../repository/nexus3_registry.md).
