## Docker Container

The relationship between `Image` and `Container` is just as `Class` and `Instance` in [OOP](https://en.wikipedia.org/wiki/Object-oriented_programming). `Image` is the static definition of `container`, while `containers` are the `images` in running state. `Containers` can be created, started, halted, deleted or stopped.

The essence of `container` is `process`, but different from that in the host OS, the container processes run in their individual [`namespaces`](https://en.wikipedia.org/wiki/Linux_namespaces). With the namespace, a container can have its own `root` filesystem, network configurations, process space and even an ID sapce for users. The processes in a container run in an isolated environment, thus can be used as if it were an individual OS independent of the host OS. This feature makes docker-encapsulated applications safer than those running directly on the host. And that's also an important factor that confuses the novices to tell it from virtual machines.

As we've discussed, `multi-layered filesystem` is applied to images, and so as the containers. When a container is running, it is based on its image, with a writable layer created on top of it. We call this layer prepared for R/W at runtime [**`Container Layer`**](https://docs.docker.com/storage/storagedriver/#images-and-layers).

The lifecyle of the container layer is the same as contaier. The container layer dies as soon as the container dies. Therefore, anything stored at the container layer will be discarded when the container is deleted.

As recommended by the [Docker Development Best Practices](https://docs.docker.com/develop/dev-best-practices/#where-and-how-to-persist-application-data), we should not write any data to the container layer to make it stateless. All file write operations should adhere to [`Volume`](../data_management/volume.md) or bind mounts. Writing to volume or bind mounts skips the container layer and R/W to host storage(or network storage) directly, which achieves better performance and stability.

The lifecyle of volume is independent of the container, and will not vanish when the container is deleted. In light of it, the data persists when a container is deleted or restarted.
