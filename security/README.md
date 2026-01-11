# 安全

容器安全是生产环境部署的核心考量。评估 Docker 的安全性时，主要考虑以下几个方面：

## 核心安全机制

* **内核命名空间（Namespace）**：提供进程、网络、文件系统等资源的隔离
* **控制组（Cgroups）**：限制容器的 CPU、内存、I/O 等资源使用
* **Docker 守护进程安全**：服务端的访问控制和防护
* **内核能力机制（Capabilities）**：细粒度的权限控制

## 现代安全实践

### 镜像安全扫描

使用工具扫描镜像中的已知漏洞：

* **Docker Scout**：Docker 官方集成的安全扫描工具，提供 SBOM 分析
* **Trivy**：开源的全面漏洞扫描器
* **Snyk**：商业级安全平台

```bash
# 使用 Docker Scout 扫描镜像
$ docker scout cves myimage:latest

# 使用 Trivy 扫描
$ trivy image myimage:latest
```

### 非 root 用户运行

避免以 root 用户运行容器，降低权限逃逸风险：

```dockerfile
FROM node:20-alpine
RUN addgroup -g 1001 appgroup && adduser -u 1001 -G appgroup -D appuser
USER appuser
```

### 只读文件系统

使用只读根文件系统增强安全性：

```bash
$ docker run --read-only --tmpfs /tmp myimage
```

### Docker Content Trust（DCT）

启用镜像签名验证，确保镜像来源可信：

```bash
$ export DOCKER_CONTENT_TRUST=1
$ docker pull myregistry/myimage:latest
```

## 本章内容

本章将详细介绍各安全机制的原理和配置方法。
