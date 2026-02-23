## 9.8 本章小结

本章介绍了 Docker 网络配置的各个方面：

| 概念 | 要点 |
|------|------|
| **DNS 配置** | 自定义网络支持嵌入式 DNS，可通过容器名解析 |
| **网络类型** | bridge (默认)、host、none、overlay、macvlan |
| **自定义网络** | 推荐使用，支持容器名 DNS 解析和更好的隔离 |
| **容器互联** | 同一自定义网络内容器可直接通过容器名通信 |
| **端口映射** | `-p 宿主机端口:容器端口` 暴露服务到外部 |
| **网络隔离** | 不同网络默认隔离，增强安全性 |
| **--link** | 已废弃，使用自定义网络替代 |

### 9.8.1 延伸阅读

- [配置 DNS](9.1_dns.md)：自定义 DNS 设置
- [网络类型](9.2_network_types.md)：Bridge、Host、None 等网络模式
- [自定义网络](9.3_custom_network.md)：创建和管理自定义网络
- [容器互联](9.4_container_linking.md)：容器间通信方式
- [端口映射](9.5_port_mapping.md)：高级端口配置
- [网络隔离](9.6_network_isolation.md)：网络安全与隔离策略
- [EXPOSE 指令](../07_dockerfile/7.9_expose.md)：在 Dockerfile 中声明端口
- [Compose 网络](../11_compose/11.5_compose_file.md)：Compose 中的网络配置
