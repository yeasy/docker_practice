# 21.4 Drone Demo

## 21.4.1 Demo 项目说明

这是一个基于 Go 语言编写的简单 Web 应用示例，用于演示 Drone CI 的持续集成流程。

## 21.4.2 目录结构

* `drone_demo.app.go`：简单的 Go Web 服务器代码。
* `drone_demo.drone.yml`：Drone CI 的配置文件，定义了构建和测试流程。

## 21.4.3 如何使用

1. 确保本地已安装 Docker 环境。
2. 将示例文件重命名为 Drone 期望的文件名：

   ```bash
   cp drone_demo.app.go app.go
   cp drone_demo.drone.yml .drone.yml
   ```

3. 将 `app.go` 与 `.drone.yml` 推送到你的 `drone-demo` 仓库，即可在 Drone 中看到构建结果。
