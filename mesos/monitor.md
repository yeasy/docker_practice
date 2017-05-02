## 日志与监控

Mesos 自身提供了强大的日志和监控功能，某些应用框架也提供了针对框架中任务的监控能力。通过这些接口，用户可以实时获知集群的各种状态。

### 日志配置
日志文件默认在 `/var/log/mesos` 目录下，根据日志等级带有不同后缀。

用户可以通过日志来调试使用中碰到的问题。

一般的，推荐使用 `--log_dir` 选项来指定日志存放路径，并通过日志分析引擎来进行监控。


### 监控

Mesos 提供了方便的监控接口，供用户查看集群中各个节点的状态。

#### 主节点
通过 `http://MASTER_NODE:5050/metrics/snapshot` 地址可以获取到 Mesos 主节点的各种状态统计信息，包括资源（CPU、硬盘、内存）使用、系统状态、从节点、应用框架、任务状态等。

例如查看主节点 `10.0.0.2` 的状态信息，并用 jq 来解析返回的 json 对象。

```sh
$ curl -s http://10.0.0.2:5050/metrics/snapshot |jq .
{
  "system/mem_total_bytes": 4144713728,
  "system/mem_free_bytes": 153071616,
  "system/load_5min": 0.37,
  "system/load_1min": 0.6,
  "system/load_15min": 0.29,
  "system/cpus_total": 4,
  "registrar/state_store_ms/p9999": 45.4096616192,
  "registrar/state_store_ms/p999": 45.399272192,
  "registrar/state_store_ms/p99": 45.29537792,
  "registrar/state_store_ms/p95": 44.8336256,
  "registrar/state_store_ms/p90": 44.2564352,
  "registrar/state_store_ms/p50": 34.362368,
  ...
  "master/recovery_slave_removals": 1,
  "master/slave_registrations": 0,
  "master/slave_removals": 0,
  "master/slave_removals/reason_registered": 0,
  "master/slave_removals/reason_unhealthy": 0,
  "master/slave_removals/reason_unregistered": 0,
  "master/slave_reregistrations": 2,
  "master/slave_shutdowns_canceled": 0,
  "master/slave_shutdowns_completed": 1,
  "master/slave_shutdowns_scheduled": 1
}
```

#### 从节点

通过 `http://SLAVE_NODE:5051/metrics/snapshot` 地址可以获取到 Mesos 从节点的各种状态统计信息，包括资源、系统状态、各种消息状态等。

例如查看从节点 `10.0.0.10` 的状态信息。

```sh
$ curl -s http://10.0.0.10:5051/metrics/snapshot |jq .
{
  "system/mem_total_bytes": 16827785216,
  "system/mem_free_bytes": 3377315840,
  "system/load_5min": 0.11,
  "system/load_1min": 0.16,
  "system/load_15min": 0.13,
  "system/cpus_total": 8,
  "slave/valid_status_updates": 11,
  "slave/valid_framework_messages": 0,
  "slave/uptime_secs": 954125.458927872,
  "slave/tasks_starting": 0,
  "slave/tasks_staging": 0,
  "slave/tasks_running": 1,
  "slave/tasks_lost": 0,
  "slave/tasks_killed": 2,
  "slave/tasks_finished": 0,
  "slave/executors_preempted": 0,
  "slave/executor_directory_max_allowed_age_secs": 403050.709525191,
  "slave/disk_used": 0,
  "slave/disk_total": 88929,
  "slave/disk_revocable_used": 0,
  "slave/disk_revocable_total": 0,
  "slave/disk_revocable_percent": 0,
  "slave/disk_percent": 0,
  "containerizer/mesos/container_destroy_errors": 0,
  "slave/container_launch_errors": 6,
  "slave/cpus_percent": 0.025,
  "slave/cpus_revocable_percent": 0,
  "slave/cpus_revocable_total": 0,
  "slave/cpus_revocable_used": 0,
  "slave/cpus_total": 8,
  "slave/cpus_used": 0.2,
  "slave/executors_registering": 0,
  "slave/executors_running": 1,
  "slave/executors_terminated": 8,
  "slave/executors_terminating": 0,
  "slave/frameworks_active": 1,
  "slave/invalid_framework_messages": 0,
  "slave/invalid_status_updates": 0,
  "slave/mem_percent": 0.00279552715654952,
  "slave/mem_revocable_percent": 0,
  "slave/mem_revocable_total": 0,
  "slave/mem_revocable_used": 0,
  "slave/mem_total": 15024,
  "slave/mem_used": 42,
  "slave/recovery_errors": 0,
  "slave/registered": 1,
  "slave/tasks_failed": 6
}
```

另外，通过 `http://MASTER_NODE:5050/monitor/statistics.json` 地址可以看到该从节点上容器网络相关的统计数据，包括进出流量、丢包数、队列情况等。获取方法同上，在此不再演示。