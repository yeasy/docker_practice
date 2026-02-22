## Prometheus + Grafana

Prometheus 和 Grafana 是目前最流行的开源监控组合，前者负责数据采集与存储，后者负责数据可视化。

[Prometheus](https://prometheus.io/) 是一个开源的系统监控和报警工具包。它受 Google Borgmon 的启发，由 SoundCloud 在 2012 年创建。

### 架构简介

Prometheus 的主要组件包括：

* **Prometheus Server**：核心组件，负责收集和存储时间序列数据。
* **Exporters**：负责向 Prometheus 暴露监控数据 (如 Node Exporter，cAdvisor)。
* **Alertmanager**：处理报警发送。
* **Pushgateway**：用于支持短生命周期的 Job 推送数据。

### 快速部署

我们可以使用 Docker Compose 快速部署一套 Prometheus + Grafana 监控环境。

#### 1。准备配置文件

创建 `prometheus.yml`：

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```

#### 2。编写 Docker Compose 文件

创建 `compose.yaml` (或 `docker-compose.yml`)：

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    networks:
      - monitoring
    depends_on:
      - prometheus

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    networks:
      - monitoring

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    networks:
      - monitoring

networks:
  monitoring:
```

#### 3。启动服务

运行以下命令：

```bash
$ docker compose up -d
```

启动后，访问以下地址：

* Prometheus: `http://localhost:9090`
* Grafana：`http://localhost:3000` (默认账号密码：admin/admin)

### 配置 Grafana 面板

1. 在 Grafana 中添加 Prometheus 数据源，URL 填写 `http://prometheus:9090`。
2. 导入现成的 Dashboard 模板，例如 [Node Exporter Full](https://grafana.com/grafana/dashboards/1860) (ID：1860) 和 [Docker Container](https://grafana.com/grafana/dashboards/193) (ID：193)。

这样，你就拥有了一个直观的容器监控大屏。
