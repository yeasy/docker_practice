## Docker Image

As we all know, Operating System consists of kernel space and user space. For linux, it will mount `root` filesystem to support user space. For Docker Image, it is similar to a `root` filesystem in Linux. For example, the offical image `ubuntu:18:04` contains a micro `root` filesystem of complete opreating system.

Docker Image is a special filesystem. Apart from programs, libs, resources and config which support running container, Docker Image also includes config parameters like anonymous volumes, environment variables, users and others. Images don't have any dynamic data. Its content will not be changed after build.

## Advanced Multi-layered Unification Filesystem (AUFS)

Because the image contains the complete `root` file system of the operating system, its volume is often huge. So Docker made full use of [Union FS](https://en.wikipedia.org/wiki/Union_mount) and was designed as AUFS when it was designed. So strictly speaking, image is not a packaged file like an ISO image file. Image is just a virtual concept. It is not composed of a single file, but a group of file systems, or a combination of multi-layered filesystems.

When building an image, it builds layer by layer, and the former is the basis for the latter. Once each layer is built, it will not change later. Any change on the latter layer will only occur on its own level. For example, deleting the previous layer of files is not really deleting the files, but only marked as deleted in the current layer. When the final container runs, you won't see the file, but in fact the file will always follow the image. Therefore, take more care when building the image, and any redundant file should be cleared up in ahead of the layer's final construction.

The layered storage feature also makes it easier to reuse and customize images. You can even use a previously built image as the base layer, and then add a new layer to customize the content to meet your need to build a new image.

As for image building, further explanations will be given in subsequent relevant chapters.
