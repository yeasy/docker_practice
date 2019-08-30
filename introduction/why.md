## Why use Docker ?
As a new virtualization solution, Docker has many advantager over
other traditional virtualization solutions.

### Use System Resources more efficiently

Docker has high utilization rate of system resources, because container does not need additional overhead such as hardware virtualization and running the whole system. It's more efficient than traditional virtual machine technology in application executing speed, memory expend and file storage speed. Therefore, a host with the same configuration can often run more applications than virtual machine technology.

### Faster startup time

The traditional virtual machine technology needs minutes to startup application service, but Docker can do it in seconds or milliseconds due to running on the kernel of host machine and not running the whole system. It saves a considerable amount of time for developing, testing, deploying.

### Consistent operating environment

The consensus problem of environment is a common problem in developing. It causes some bugs which weren't found at developing due to different environments of developing, testing, production. Docker's image provides a complete runtime environment without kernel, which ensures consistency of the application runtime environment so that problmes like * This piece of code is okey on my machine * do not recur.


### CI/CD

For development and operation（[DevOps](https://zh.wikipedia.org/wiki/DevOps)）people, desirable thing is to create or configure at once and run normally anywhere.

CI/CD can be achieved by customizing application mirrors with Docker. Developers can build images with [Dockerfile](../image/dockerfile/) and use [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration) for integration testing. Operators can deply product environment quickly with this images, even use [Continuous Delivery/Deployment](https://en.wikipedia.org/wiki/Continuous_delivery) for automatic deployment.

And `Dockerfile` makes mirror construction transparent.Not only does the developmentteam understand the application runtime environment, but it also facilitates the operation team to understande the requirements of the application and better deployment in production environments.

### Easier migration

Because Docker ensures consistency in the execution environment, application migration is easier. Docker can run on many platforms, whether physical, virtual, public/private clouds, or even laptops, and the results are consistent.Therefore, users can easily migrate applications from one platform to another whitout worrying about the situation that different environment makes applications not running properly.

### Easier maintenance and extension

Docker uses layered storage and mirror technology, so it is easier to reuse the repetitive parts of the application and simpler to expand the image based on the basic mirror.In addition, the Docker team maintain a lot of high-quality [official images](https://hub.docker.com/search/?type=image&image_filter=official) together with various open source project team. It can be used directly in the production environment and customed which greatly reducing the cost of image production of application services.

### Contrast traditional virtual machines

|   Feature      |   Container        |   Virtual Machine   |
| :--------      | :--------          | :----------         |
| Boot           | seconds            | minutes             |
| Disk Usage     | MB                 | GB                  |
| Performance    | close to native    | weaker              |
| System Support | thousandes         | dozens in general   |
