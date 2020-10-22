## Why use Docker ?
As a new virtualization technology, Docker has many advantages over
other traditional virtualization solutions.

### Use System Resources more Efficiently

Docker has high utilization rate of system resources, because container does not need additional overhead such as hardware virtualization or running the whole system. It's more efficient than traditional virtual machine technology in terms of execution speed, memory expense and file storage speed. Therefore, a host with the same configuration can often run more applications than virtual machine technology.

### Faster Startup Time

The traditional virtual machine technology needs minutes to startup application service, but Docker can do it in seconds or milliseconds due to running on the kernel of host machine and not running the whole system. It saves a considerable amount of time for development, testing and deployment.

### Consistent Operating Environment

Environment setup consistency is a common problem in DevOps. Inconsistent configuration can cause some bugs not found at development time but revealed at production due to the subtle differences between the development, testing and production environments. The docker image can provide a complete runtime environment without kernel, which ensures consistency of the application environment throughout its lifecycle, eliminating issues like * This piece of code is okey on my machine *.


### CI/CD

For development and operation（[DevOps](https://zh.wikipedia.org/wiki/DevOps)）engineers, the desirable thing is to create and configure once to run anywhere.

CI/CD can be achieved by customizing application mirrors with Docker. Developers can build images with [Dockerfile](../image/dockerfile/) and use [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration) for integration testing. Operation teams can deploy production environments quickly with the images, and even make automatic deployments possible by using [Continuous Delivery/Deployment](https://en.wikipedia.org/wiki/Continuous_delivery) techniques.

And `Dockerfile` makes mirror construction transparent. Not only does the development team understand the application runtime environment, but it also facilitates the operation team to understand the requirements of the application and better deployment in production environments.

### Easier migration

Because Docker ensures consistency in the execution environment, application migration is easier. Docker can run on multiple platforms, including physical, virtual machines or public/private clouds, with consistent results. Therefore, users can easily migrate applications from one platform to another whitout worrying about the cross-platform difficulties.

### Easier maintenance and extension

Docker uses layered storage and mirror technology, so it is easier to reuse the repetitive parts of the application and simpler to expand the image based on the basic mirror. In addition, the Docker team maintains a lot of high-quality [official images](https://hub.docker.com/search/?type=image&image_filter=official) together with various open-source project teams. It can be used directly in the production environment with customization, greatly reducing the cost of image production of various application services.

### Contrast traditional virtual machines

|   Feature      |   Container        |   Virtual Machine   |
| :--------      | :--------          | :----------         |
| Boot           | seconds            | minutes             |
| Disk Usage     | MB                 | GB                  |
| Performance    | close to native    | weaker              |
| System Support | thousands          | dozens in general   |
