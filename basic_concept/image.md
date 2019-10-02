## Docker Image

As we all know, Operating System constitutes kernel and user space. For linux, it will mount `root` file system to support user space. For Docker Image, it almost likes a `root` file system. For example, the offical image `ubuntu:18:04` contains a micro `root` file system of complete opreating system.

Docker Image is a special file system. Except for programes, libs, resources and config witch support running container, Docker Image also includes config parameters like anonymous volumes, environment variables, users and others. Images don't have any dynamic data. Its content will not be changed after build.

## Advanced Multi-layered Unification Filesystem (AUFS)

Because the image contains the complete `root` file system of the operating system, its volume is often huge. So Docker made full use of [Union FS](https://en.wikipedia.org/wiki/Union_mount) and was designed as AUFS when it was designed. So strictly speaking, image is not a packaged file like an ISO. Image is just a virtual concept. It is not composed of a single file, but a group of file systems, or a combination of multi-layers file systems.

When build an image, it builds layer by layer, and the former is the base of the latter. Once each layer is built, it will not change later. Any change on the latter layer will only occur on its own level. For example,  deleting the previous layer of files is not really deleting the files, but only marked as deleted in the current layter. When the final conatiner runs, you won't see the file, but in fact the file will always follow the image. Therefore, take more care when  building the image, and any additional things should be cleared up before the end of the layer's construction.

Layered storage features also make it easier to reuse and customize image. You can even use the previously built image as the base layer, and then add a new layer to customize the content you need to build a new image.

As for image building, further explanations will be given in subsequent relevant chapters.
