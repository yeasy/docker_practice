## 本章小结

Docker 的安全性依赖于多层隔离机制的协同工作，同时需要用户遵循最佳实践。本章涵盖的核心安全维度包括：

| 维度 | 关键措施 |
|------|---------|
| **内核隔离** | Namespace 隔离进程/网络/文件系统，Cgroups 限制资源使用 |
| **权限控制** | 非 root 运行、`--cap-drop ALL` 最小能力集、`--read-only` 只读根文件系统 |
| **镜像安全** | 使用可信基础镜像、定期扫描漏洞（Trivy / Snyk）、启用 Sigstore / Notation / Registry 原生签名验证；DCT 仅作为遗留迁移对象 |
| **运行时防护** | Seccomp 系统调用过滤、AppArmor / SELinux 强制访问控制 |
| **网络隔离** | 自定义 bridge 网络隔离容器通信、限制容器对宿主机网络的访问 |

总体来看，Docker 容器还是十分安全的，特别是在容器内不使用 root 权限来运行进程的话。

另外，用户可以使用现有工具，比如 [Apparmor](https://docs.docker.com/engine/security/apparmor/)，[Seccomp](https://docs.docker.com/engine/security/seccomp/)，SELinux，GRSEC 来增强安全性；甚至自己在内核中实现更复杂的安全机制。
---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/docker_practice/issues) 或 [PR](https://github.com/yeasy/docker_practice/pulls)。
