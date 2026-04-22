## 附录八：Docker 学习路线图与知识体系

本附录为学习者提供清晰的学习路线、知识点依赖关系、认证指南和常见面试题，帮助快速成长为 Docker 和 DevOps 专家。

### 学习阶段划分

Docker 学习可分为四个递进阶段，每个阶段都有明确的学习目标和时间投入。

#### 第一阶段：基础入门（0-2 周）

**学习目标：**
- 理解容器化的基本概念
- 能够运行、管理基本的容器
- 了解镜像和仓库的基本操作

**核心内容：**
```text
Docker 简介
├── 为什么需要 Docker
├── 容器 vs 虚拟机 vs 云计算
└── Docker 的三大核心概念
    ├── 镜像（Image）
    ├── 容器（Container）
    └── 仓库（Repository）

基础命令
├── docker run / create / start / stop / rm
├── docker ps / logs / exec / inspect
├── docker pull / push / tag
└── docker build -t

Docker 安装配置
├── Linux 平台安装
├── macOS 和 Windows 安装
├── 镜像加速器配置
└── 权限和用户配置
```
**学习资源：**
- [官方教程](https://docs.docker.com/get-started/)
- 本书第 1-3 章：入门篇基础概念
- [Docker CLI 参考](https://docs.docker.com/engine/reference/commandline/)

**时间投入：**
- 理论学习：3-4 小时
- 实操练习：8-10 小时
- 总计：2 周

**验证学习成果：**
```bash
# 完成以下任务说明基础入门完成
1. 运行官方 nginx 镜像，访问 http://localhost
2. 使用 docker exec 进入容器修改首页
3. 提交修改为新镜像
4. 推送镜像到 Docker Hub（需创建账户）
```

#### 第二阶段：核心开发（2-6 周）

**学习目标：**
- 掌握 Dockerfile 编写
- 能够构建自己的应用镜像
- 理解数据管理和网络配置
- 熟悉 Docker Compose 编排

**核心内容：**
```text
Dockerfile 指令详解
├── FROM / RUN / COPY / ADD
├── WORKDIR / ENV / ARG
├── EXPOSE / CMD / ENTRYPOINT
├── VOLUME / USER / HEALTHCHECK
└── 最佳实践和性能优化
    ├── 分层缓存机制
    ├── 减少镜像体积
    ├── 多阶段构建
    └── 安全最佳实践

容器数据管理
├── 数据卷（Volume）
│   ├── 命名卷
│   ├── 匿名卷
│   └── 卷挂载最佳实践
├── 绑定挂载（Bind Mount）
│   ├── 宿主机路径映射
│   └── 权限和隔离
└── tmpfs 挂载
    └── 临时文件系统

容器网络
├── 网络类型
│   ├── bridge（默认）
│   ├── host
│   ├── overlay
│   └── macvlan
├── 端口映射
├── 容器互联
├── DNS 配置
└── 自定义网络

Docker Compose
├── compose.yml/docker-compose.yml 编写
├── services 定义
├── volumes 配置
├── networks 配置
├── 依赖关系
├── 环境变量
└── 命令操作
    ├── up / down / ps / logs
    ├── exec / run
    └── build / push
```
**学习资源：**
- 本书第 4-11 章：进阶篇
- [Docker 官方最佳实践](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile 参考](https://docs.docker.com/engine/reference/builder/)

**时间投入：**
- 理论学习：8-10 小时
- 实操练习：30-40 小时（多个实战项目）
- 总计：4-6 周

**项目实战：**
```text
项目 1: Python Web 应用（Flask/Django）
- 编写多阶段 Dockerfile
- 使用 Compose 配置数据库
- 实现热重载开发环境

项目 2: Node.js 微服务
- 优化镜像大小
- 配置 Compose 多个服务
- 设置网络和环保境变量

项目 3: 数据库容器化
- PostgreSQL/MySQL 配置
- 数据持久化
- 备份恢复策略
```

#### 第三阶段：生产优化（6-12 周）

**学习目标：**
- 掌握容器安全最佳实践
- 理解性能监控和优化
- 学会容器编排（Kubernetes 基础）
- 熟悉 CI/CD 集成

**核心内容：**
```text
容器安全
├── 镜像安全
│   ├── 漏洞扫描（Trivy/Grype/Snyk）
│   ├── 镜像签名和验证（Cosign）
│   ├── SBOM 生成和管理
│   └── 供应链安全
├── 运行时安全
│   ├── 用户和权限
│   ├── Linux 能力机制
│   ├── AppArmor 和 SELinux
│   ├── Rootless 容器
│   └── 安全的 Docker socket 访问
└── 宿主机安全
    ├── API 访问控制
    ├── TLS 认证
    └── 审计日志

性能监控和优化
├── 监控指标体系
│   ├── CPU / 内存 / 网络 / I/O
│   └── 应用级指标
├── 监控工具
│   ├── docker stats
│   ├── cAdvisor
│   ├── Prometheus
│   └── Grafana
├── 性能优化
│   ├── 镜像大小优化
│   ├── 内存和 CPU 限制
│   ├── OOM 诊断和处理
│   └── 网络性能优化
└── 日志管理
    ├── 日志驱动配置
    ├── ELK Stack
    └── 日志聚合

容器编排基础
├── Kubernetes 核心概念
│   ├── Pod / Deployment / Service
│   ├── ConfigMap / Secret
│   └── 健康检查和自动恢复
├── 容器执行环境
│   ├── containerd
│   ├── CRI-O
│   └── Docker
├── 网络插件
│   ├── CNI 标准
│   ├── Calico / Flannel / Cilium
│   └── 网络策略
└── 存储和有状态应用
    ├── PV / PVC
    ├── StorageClass
    └── StatefulSet

CI/CD 集成
├── GitHub Actions
│   ├── 镜像构建和推送
│   ├── 安全扫描
│   └── 自动化测试
├── GitLab CI
├── Jenkins Docker 集成
└── Drone

生态工具
├── Buildx（多架构构建）
├── Skopeo（镜像管理）
├── Podman（替代方案）
├── Buildah（镜像构建）
└── Kollabot
```
**学习资源：**
- 本书第 12-21 章：深入篇和实战篇
- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [CNCF 学习路线](https://landscape.cncf.io/)

**时间投入：**
- 理论学习：15-20 小时
- 实操练习：60-80 小时（多个生产级项目）
- 总计：6-12 周

**项目实战：**
```text
项目 1: 安全镜像构建流程
- 集成 Trivy 扫描
- 镜像签名和验证
- 生成 SBOM 文档

项目 2: 完整监控栈
- 搭建 Prometheus + Grafana
- 配置告警规则
- 性能数据采集和分析

项目 3: CI/CD 流程
- GitHub Actions 或 GitLab CI 配置
- 自动化镜像构建
- 安全扫描和合规检查
- 自动化部署到 Kubernetes

项目 4: Kubernetes 集群部署
- 本地 K3s/Kind 集群
- 部署有状态应用
- 配置持久化存储
```

#### 第四阶段：专家深造（12+ 周）

**学习目标：**
- 掌握 Kubernetes 高级特性
- 理解容器运行时底层实现
- 能够设计和优化大规模容器平台
- 贡献开源社区

**核心内容：**
```text
Kubernetes 高级特性
├── 集群管理
│   ├── 节点管理和驱逐
│   ├── 集群自动扩缩容
│   └── 节点亲和性和污点容忍
├── 存储编排
│   ├── 动态存储配置
│   ├── 有状态应用管理（StatefulSet）
│   └── 备份和灾难恢复
├── 服务网格（Service Mesh）
│   ├── Istio / Linkerd / Cilium
│   ├── 流量管理
│   └── 可观测性增强
├── 安全和多租户
│   ├── RBAC（角色访问控制）
│   ├── Network Policy 深入
│   ├── Pod Security Policy
│   └── 准入控制器（Admission Controller）
└── 性能和扩展性
    ├── 大规模集群优化
    ├── 自定义 Operator
    └── 集群联邦

容器运行时底层
├── Linux 内核机制
│   ├── Namespace 详解
│   ├── Cgroup v1 和 v2
│   ├── OverlayFS 和 UnionFS
│   └── SELinux 和 AppArmor
├── 容器运行时
│   ├── containerd 源码阅读
│   ├── runc 实现
│   ├── gVisor 和 Kata
│   └── Firecracker
└── OCI 标准
    ├── Image Spec
    └── Runtime Spec

DevOps 工程化
├── 大规模集群管理
│   ├── Helm / Kustomize
│   ├── GitOps（Flux / ArgoCD）
│   └── 配置管理
├── 灾难恢复和高可用
│   ├── 多集群部署
│   ├── 故障转移
│   └── 备份策略
├── 成本优化
│   ├── 资源申请和限制
│   ├── 自动扩缩容
│   └── 成本监控
└── 团队协作
    ├── GitFlow 工作流
    ├── 代码审查
    └── 文档和最佳实践传播
```
**贡献机会：**
- [Kubernetes](https://github.com/kubernetes/kubernetes)
- [Cilium](https://github.com/cilium/cilium)
- [Prometheus](https://github.com/prometheus/prometheus)
- [Docker/Moby](https://github.com/moby/moby)

### 知识点依赖关系

```text
基础概念 (Week 0-2)
├── 容器 vs 虚拟机
├── Docker 三大概念
└── 基础命令
    ↓
Dockerfile 和镜像构建 (Week 2-4)
├── Dockerfile 指令
├── 多阶段构建
└── 镜像优化
    ↓ ↓ ↓
数据管理 ← 网络配置 ← Docker Compose (Week 4-6)
├── Volume    ├── Bridge    ├── YAML 编写
├── Bind Mount├── Overlay   ├── 多容器编排
└── tmpfs     └── 自定义网络└── 开发工作流
    ↓            ↓            ↓
    └─────────────────────────┘
          实战项目开发 (Week 6-10)
          ├── Web 应用容器化
          ├── 数据库容器化
          ├── 微服务架构
          └── 本地开发环境
              ↓
容器安全 ← 性能优化 ← 监控和日志 (Week 10-14)
├── 镜像扫描  ├── 大小优化  ├── Prometheus
├── 漏洞管理  ├── 内存优化  ├── Grafana
├── 镜像签名  ├── CPU 优化  └── ELK Stack
└── SBOM    └── 诊断工具
    ↓          ↓          ↓
    └─────────────────────┘
          安全生产环境 (Week 14-18)
          ├── CI/CD 流程
          ├── 镜像仓库
          ├── 日志集中
          └── 告警系统
              ↓
Kubernetes 基础 (Week 18-24)
├── Pod / Service / Deployment
├── 资源管理
├── 存储管理
└── 网络策略
    ↓
Kubernetes 进阶 (Week 24-36)
├── StatefulSet / DaemonSet
├── Operator 开发
├── 集群管理
└── 服务网格
    ↓
企业级平台设计 (Week 36+)
├── 多集群管理
├── GitOps 工作流
├── 成本优化
└── 开源贡献
```

### 推荐学习资源

#### 官方文档

| 资源 | URL | 推荐程度 |
|------|-----|--------|
| Docker 官方文档 | [docs.docker.com](https://docs.docker.com) | ⭐⭐⭐⭐⭐ |
| Docker Hub | [hub.docker.com](https://hub.docker.com) | ⭐⭐⭐⭐⭐ |
| Kubernetes 官方 | [kubernetes.io/docs](https://kubernetes.io/docs) | ⭐⭐⭐⭐⭐ |
| CNCF 景观 | [landscape.cncf.io](https://landscape.cncf.io) | ⭐⭐⭐⭐ |

#### 在线课程

- **Udemy**：Docker 和 Kubernetes 完整课程（70-100 小时）
- **Linux Academy**：Linux 和容器管理
- **A Cloud Guru**：AWS/Azure 容器服务
- **Pluralsight**：Docker 和容器生态系统

#### 书籍推荐

- 《Docker 深入浅出》- 本书的原版
- 《Kubernetes 权威指南》- 深入 Kubernetes 的必读书
- 《容器技术核心技术与应用》- 理解底层实现
- 《SRE Google 运维之道》- 生产环境最佳实践

#### 博客和社区

- [Docker 官方博客](https://www.docker.com/blog/)
- [Kubernetes 官方博客](https://kubernetes.io/blog/)
- [CNCF 博客](https://www.cncf.io/blog/)
- [DZone](https://dzone.com/containers-cloud)

### 认证指南

#### Docker 认证

**Docker Certified Associate (DCA)**

考试信息：
- 题目数：55 道
- 时间限制：90 分钟
- 及格分数：73%（约 41 道题）
- 费用：$165 USD
- 有效期：3 年

考试内容比例：
```text
镜像和仓库（20%）
- 镜像构建和管理
- 镜像层和缓存
- 私有仓库配置

容器运行（15%）
- 容器生命周期
- 资源限制
- 容器隔离

网络（15%）
- 网络驱动
- 容器通信
- 端口映射

存储（10%）
- Volume 管理
- 数据持久化
- 绑定挂载

编排（20%）
- Docker Compose
- Docker Swarm 基础

安全（15%）
- 用户和权限
- 密钥管理
- 镜像安全
- 守护进程安全

和日志（5%）
- Logging drivers
- 事件处理
```
准备建议：
```bash
# 1. 学习本书第 1-11 章（基础到中级）
# 2. 完成 20+ 个实战项目
# 3. 参考官方学习指南
curl https://docker.training.kodekloud.com/dca-guide

# 4. 模拟考试
- Linux Academy DCA 练习题
- Whizlabs DCA 模拟考试

# 5. 重点掌握的命令
docker build / push / pull / tag
docker run / exec / logs / inspect / ps
docker volume / network / service
docker compose up / down / logs / ps
docker stats / events / inspect
```

#### Kubernetes 认证

**认证路径：**
1. **CKA - Certified Kubernetes Administrator**
   - 难度：高
   - 时间：3 小时（实操）
   - 费用：$395
   - 内容：集群安装、管理、故障排查

2. **CKAD - Certified Kubernetes Application Developer**
   - 难度：中
   - 时间：2 小时（实操）
   - 费用：$395
   - 内容：应用开发和部署

3. **CKS - Certified Kubernetes Security Specialist**
   - 难度：很高
   - 时间：2 小时（实操）
   - 费用：$395
   - 内容：安全最佳实践

### 常见面试题与答案要点

#### 基础概念面试题

**Q1: Docker 容器和虚拟机有什么区别？**

A（要点）：
```text
虚拟机：
- 完整的操作系统环境（GB 级）
- 启动时间：分钟级
- 隔离级别：完全硬件隔离
- 性能开销：高（5-20%）

容器：
- 共享内核，包含应用和依赖（MB 级）
- 启动时间：秒级
- 隔离级别：进程级隔离（Namespace/Cgroup）
- 性能开销：低（1-5%）

总结：容器更轻量、更快、密度更高
```
**Q2: 什么是 Docker 镜像？它如何存储的？**

A（要点）：
```text
镜像本质：
- 只读的文件系统快照
- 分层存储结构
- 每一层是前一层的增量

存储方式：
- Union FS：多个只读层 + 一个可写层
- 每个 RUN/COPY/ADD 指令创建一层
- 层之间通过 diff 增量存储，节省空间

优点：
- 共享基础层减少存储
- 层级缓存加快构建
- 支持高效分发
```
**Q3: 容器如何实现隔离？**

A（要点）：
```text
技术手段：
1. Namespace（资源隔离）：
   - PID Namespace：进程隔离
   - Network Namespace：网络隔离
   - Mount Namespace：文件系统隔离
   - UTS Namespace：主机名隔离
   - IPC Namespace：进程间通信隔离

2. Cgroup（资源限制）：
   - 限制 CPU 使用
   - 限制内存使用
   - 限制磁盘 I/O
   - 限制网络带宽

3. Linux 能力机制（权限控制）：
   - 削减不必要的 root 权限
   - 限制容器能力

4. SELinux / AppArmor（强制访问控制）
```

#### Dockerfile 面试题

**Q4: 如何优化 Docker 镜像大小？**

A（要点）：
```text
1. 选择合适的基础镜像：
   scratch < alpine:3.17 < python:3.14-slim < python:3.14

2. 多阶段构建：
   - 构建阶段只保留编译工具
   - 运行阶段只包含最终二进制
   - 典型场景：Go、Node.js、Java

3. 清理包管理器缓存：
   apt-get clean && rm -rf /var/lib/apt/lists/*
   yum clean all && rm -rf /var/cache/yum
   pip install --no-cache-dir

4. 合并 RUN 指令：
   减少镜像层数

5. 使用 .dockerignore：
   排除不必要的构建上下文

6. 去除调试符号：
   Go: -ldflags="-w -s"
   C/C++: strip binary

7. 压缩资源：
   gzip 静态文件，压缩图片
```
**Q5: CMD 和 ENTRYPOINT 有什么区别？**

A（要点）：
```text
CMD：
- 定义容器默认命令
- 容器运行时可被覆盖：docker run image_name custom_cmd
- 可以有多个 CMD，只有最后一个生效

ENTRYPOINT：
- 定义容器的可执行程序
- 容器运行时参数追加而非覆盖
- 与 CMD 配合使用

推荐用法：
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8000"]

# 运行 docker run image --debug 会执行：
# python app.py --debug
```

#### 网络和存储面试题

**Q6: Docker 网络驱动的区别？**

A（要点）：
```text
Bridge（默认）：
- 虚拟网桥，容器间通过网桥通信
- 支持端口映射
- 隔离性好，性能适中

Host：
- 使用宿主机网络栈
- 性能最优，隔离性最差
- 容器端口直接映射到宿主机

Overlay：
- 跨主机通信，基于 VXLAN
- Swarm 和 Kubernetes 标准
- 性能略低，支持分布式

macvlan：
- 容器获得 MAC 地址
- 表现为物理机，性能好
- 用于物理网络集成

None：
- 无网络，完全隔离
```
**Q7: Volume 和 Bind Mount 有什么区别？**

A（要点）：
```text
Volume：
- Docker 管理，存储位置：/var/lib/docker/volumes/
- 跨平台兼容，隔离性好
- 支持驱动，可扩展
- 推荐在生产环境使用

Bind Mount：
- 宿主机管理，任意位置
- 跨平台兼容性一般
- 性能好，用于开发环境
- 权限管理复杂

tmpfs：
- 内存文件系统，不持久化
- 用于临时文件、敏感数据
- 性能最好，重启丢失
```

#### 安全和生产面试题

**Q8: 如何提高 Docker 安全性？**

A（要点）：
```text
镜像安全：
- 使用官方镜像或可信镜像源
- 定期扫描漏洞（Trivy/Grype）
- 镜像签名验证（Cosign）
- 生成和管理 SBOM

容器运行：
- 以非 root 用户运行
- 使用 read-only 文件系统
- 限制 Linux 能力
- 使用 AppArmor 或 SELinux

宿主机安全：
- 启用 TLS 认证 API
- 不暴露 /var/run/docker.sock
- 使用 Rootless 容器
- 定期更新 Docker

网络安全：
- 使用自定义网络隔离
- 配置网络策略
- 限制出入站流量
```
**Q9: 容器被 OOM 杀死，如何诊断和解决？**

A（要点）：
```text
诊断：
1. 检查容器是否被 OOM 杀死：
   docker inspect <container> | grep OOMKilled

2. 查看宿主机日志：
   dmesg | grep -i oom
   journalctl -u docker | grep -i oom

3. 监控内存使用：
   docker stats <container>
   docker exec <container> ps aux --sort=-%mem

解决：
1. 增加内存限制：
   docker update -m 2g <container>

2. 检查内存泄漏：
   使用内存分析工具（heapdump、pprof）

3. 优化应用：
   - 增加垃圾回收频率
   - 减少缓存大小
   - 使用对象池模式

4. 使用内存交换（最后手段）：
   docker run -m 512m --memory-swap 1g
```
**Q10: 如何在 CI/CD 中集成 Docker？**

A（要点）：
```text
构建阶段：
- 触发器：Push / PR 事件
- 构建镜像：docker build
- 标记：git sha、版本号
- 扫描：Trivy 漏洞扫描
- 签名：Cosign 镜像签名

存储阶段：
- 推送到镜像仓库：docker push
- 记录 SBOM 和扫描报告

部署阶段：
- 验证镜像签名
- 获取镜像摘要
- 更新部署配置
- 触发 GitOps 工作流

监控阶段：
- 收集应用日志
- 监控性能指标
- 告警异常情况

示例工作流：
1. GitHub Actions / GitLab CI 监听 push
2. 运行单元测试
3. 构建 Docker 镜像
4. 推送到 Docker Hub / ECR
5. 触发 ArgoCD / Flux 自动部署
6. 监控部署状态
```

### 学习进度跟踪模板

```markdown
# Docker 学习进度跟踪

## 第一阶段：基础入门（目标：2 周）
- [ ] 学完第 1-3 章（6 小时）
- [ ] 完成基础命令练习（10 小时）
- [ ] 运行官方镜像
- [ ] 创建和推送第一个镜像到 Docker Hub
- [ ] 完成度：___%

## 第二阶段：核心开发（目标：4-6 周）
- [ ] 学完第 4-11 章（15 小时）
- [ ] 完成 3 个 Dockerfile 最佳实践项目
- [ ] 掌握 Docker Compose（5 个项目）
- [ ] 学习数据管理和网络（8 小时）
- [ ] 完成度：___%

## 第三阶段：生产优化（目标：6-12 周）
- [ ] 学完第 12-21 章（25 小时）
- [ ] 镜像安全扫描和签名
- [ ] 搭建完整监控栈
- [ ] 配置 CI/CD 流程
- [ ] Kubernetes 基础（30 小时）
- [ ] 完成度：___%

## 第四阶段：专家深造（目标：12+ 周）
- [ ] Kubernetes 高级特性
- [ ] 服务网格学习
- [ ] 底层实现研究
- [ ] 贡献开源项目
- [ ] 完成度：___%

## 证书目标
- [ ] Docker DCA 认证
- [ ] CKA 认证
- [ ] CKAD 认证

## 实战项目清单
- [ ] Python Web 应用容器化
- [ ] Node.js 微服务
- [ ] 数据库容器化
- [ ] 完整微服务架构
- [ ] 监控和日志系统
- [ ] CI/CD 流程实现
```

### 快速参考速查表

**常用命令速查：**

```bash
# 镜像管理
docker build -t image:tag .              # 构建镜像
docker images                             # 列出镜像
docker rmi image:tag                      # 删除镜像
docker tag source:tag target:tag          # 标记镜像
docker push registry/image:tag            # 推送镜像
docker pull image:tag                     # 拉取镜像
docker history image:tag                  # 查看镜像历史
docker inspect image:tag                  # 查看镜像详情

# 容器管理
docker run [OPTIONS] image                # 运行容器
docker ps [-a]                            # 列出容器
docker stop/start/restart container       # 容器生命周期
docker rm container                       # 删除容器
docker logs [-f] container                # 查看日志
docker exec -it container cmd             # 进入容器
docker inspect container                  # 查看容器详情
docker stats [container]                  # 查看资源使用

# 网络管理
docker network ls                         # 列出网络
docker network create name                # 创建网络
docker network connect/disconnect         # 连接/断开网络
docker network inspect name               # 查看网络详情

# 卷管理
docker volume ls                          # 列出卷
docker volume create name                 # 创建卷
docker volume rm name                     # 删除卷
docker volume inspect name                # 查看卷详情

# Docker Compose
docker compose up [-d]                    # 启动服务
docker compose down                       # 停止服务
docker compose ps                         # 列出服务
docker compose logs [-f] [service]        # 查看日志
docker compose exec service cmd           # 在服务中执行命令
docker compose build                      # 构建服务镜像
```
