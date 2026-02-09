## ELK/EFK 堆栈

ELK (Elasticsearch, Logstash, Kibana) 是目前业界最流行的开源日志解决方案。而在容器领域，由于 Fluentd 更加轻量级且对容器支持更好，EFK (Elasticsearch, Fluentd, Kibana) 组合也变得非常流行。

### 方案架构

我们将采用以下架构：

1. **Docker Container**: 容器将日志输出到标准输出 (stdout/stderr)。
2. **Fluentd**: 作为 Docker 的 Logging Driver 或运行为守护容器，收集容器日志。
3. **Elasticsearch**: 存储从 Fluentd 接收到的日志数据。
4. **Kibana**: 从 Elasticsearch 读取数据并进行可视化展示。

### 部署流程

#### 1. 编写 docker-compose.yml

```yaml
version: '3'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
    container_name: elasticsearch
    environment:
      - "discovery.type=single-node"
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    networks:
      - logging

  kibana:
    image: docker.elastic.co/kibana/kibana:7.17.0
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    links:
      - elasticsearch
    networks:
      - logging

  fluentd:
    image: fluent/fluentd-kubernetes-daemonset:v1.14.3-debian-elasticsearch7-1.0
    container_name: fluentd
    environment:
      - "FLUENT_ELASTICSEARCH_HOST=elasticsearch"
      - "FLUENT_ELASTICSEARCH_PORT=9200"
      - "FLUENT_ELASTICSEARCH_SCHEME=http"
      - "FLUENT_UID=0"
    ports:
      - "24224:24224"
      - "24224:24224/udp"
    links:
      - elasticsearch
    volumes:
      - ./fluentd/conf:/fluentd/etc
    networks:
      - logging

volumes:
  es_data:

networks:
  logging:
```

#### 2. 配置 Fluentd

创建 `fluentd/conf/fluent.conf`:

```conf
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<match *.**>
  @type copy
  <store>
    @type elasticsearch
    host elasticsearch
    port 9200
    logstash_format true
    logstash_prefix docker
    logstash_dateformat %Y%m%d
    include_tag_key true
    type_name access_log
    tag_key @log_name
    flush_interval 1s
  </store>
  <store>
    @type stdout
  </store>
</match>
```

#### 3. 配置应用容器使用 fluentd 驱动

启动一个测试容器，指定日志驱动为 `fluentd`:

```bash
docker run -d \
  --log-driver=fluentd \
  --log-opt fluentd-address=localhost:24224 \
  --log-opt tag=nginx-test \
  --name nginx-test \
  nginx
```

**注意**: 确保 `fluentd` 容器已经启动并监听在 `localhost:24224`。在生产环境中，如果你是在不同机器上，需要将 `localhost` 替换为运行 fluentd 的主机 IP。

#### 4. 在 Kibana 中查看日志

1. 访问 `http://localhost:5601`。
2. 进入 **Management** -> **Kibana** -> **Index Patterns**。
3. 创建新的 Index Pattern，输入 `docker-*` (我们在 fluent.conf 中配置的前缀)。
4. 选择 `@timestamp` 作为时间字段。
5. 去 **Discover** 页面，你就能看到 Nginx 容器的日志了。

### 总结

通过 Docker 的日志驱动机制，结合 ELK/EFK 强大的收集和分析能力，我们可以轻松构建一个能够处理海量日志的监控平台，这对于排查生产问题至关重要。
