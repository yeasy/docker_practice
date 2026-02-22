# 日志管理

在容器化环境中，日志管理比传统环境更为复杂。容器是短暂的，意味着容器内的日志文件可能会随着容器的销毁而丢失。因此，我们需要一种集中式的日志管理方案来收集、存储和分析容器日志。

## Docker 日志驱动

Docker 提供了多种日志驱动 (Log Driver) 机制，允许我们将容器日志转发到不同的后端。

常见的日志驱动包括：

* `json-file`：默认驱动，将日志以 JSON 格式写入本地文件。
* `syslog`：将日志转发到 syslog 服务器。
* `journald`：将日志写入 systemd journal。
* `fluentd`：将日志转发到 fluentd 收集器。
* `gelf`：支持 GELF 协议的日志后端 (如 Graylog)。
* `awslogs`：发送到 Amazon CloudWatch Logs。

## 日志管理方案

对于大规模的容器集群，我们通常会采用 EFK (Elasticsearch + Fluentd + Kibana) 或 ELK (Elasticsearch + Logstash + Kibana) 方案。

* **Elasticsearch**：负责日志的存储和全文检索。
* **Fluentd/Logstash**：负责日志的采集、过滤和转发。
* **Kibana**：负责日志的可视化展示。

本章将介绍如何使用 EFK 方案来处理 Docker 容器日志。
