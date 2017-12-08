## LinuxKit

`LinuxKit` 这个工具可以将多个 Docker 镜像组成一个最小化、可自由定制的 Linux 系统，最后的生成的系统只有几十 M 大小，可以很方便的在云端进行部署。

下面我们在 macOS 上通过实例，来编译并运行一个全部由 Docker 镜像组成的包含 nginx 服务的 Linux 系统。

### 安装 Linuxkit

```bash
$ brew tap linuxkit/linuxkit

$ brew install --HEAD linuxkit
```

### 克隆源代码

```bash
$ git clone -b master --depth=1 https://github.com/linuxkit/linuxkit.git

$ cd linuxkit
```

### 编译 Linux 系统

LinuxKit 通过 `yaml` 文件配置。

我们来查看 `linuxkit.yml` 文件，了解各个字段的作用。

`kernel` 字段定义了内核版本。

`init` 字段中配置系统启动时的初始化顺序。

`onboot` 字段配置系统级的服务。

`services` 字段配置镜像启动后运行的服务。

`files` 字段配置制作镜像时打包入镜像中的文件。

```bash
$ linuxkit build linuxkit.yml
```

### 启动 Linux 系统

编译成功后，接下来启动这个 Linux 系统。

```bash
$ linuxkit run -publish 8080:80/tcp linuxkit
```

接下来在浏览器中打开 `127.0.0.1:8080` 即可看到 nginx 默认页面。
