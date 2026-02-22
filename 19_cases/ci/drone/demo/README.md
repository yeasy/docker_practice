# Drone CI Demo 项目

这是一个基于 Go 语言编写的简单 Web 应用示例，用于演示 Drone CI 的持续集成流程。

## 目录结构

*   `app.go`：简单的 Go Web 服务器代码。
*   `.drone.yml`：Drone CI 的配置文件，定义了构建和测试流程。
*   `Dockerfile`：定义了如何将该应用构建为 Docker 镜像。

## 如何运行

1.  确保本地已安装 Docker 环境。
2.  进入本目录构建镜像：
    ```bash
    docker build -t drone-demo-app .
    ```

3.  运行容器：
    ```bash
    docker run -p 8080:8080 drone-demo-app
    ```

4.  访问 `http://localhost:8080` 查看效果。
