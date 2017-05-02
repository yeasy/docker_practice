## Mesos 配置项解析

Mesos 支持在运行时通过命令行参数形式提供的配置项。如果是通过系统服务方式启动，也支持以配置文件或环境变量方式给出。当然，实际上最终是提取为命令行参数传递给启动命令。

Mesos 的配置项分为三种类型：通用项（master 和 slave 都支持），只有 master 支持的，以及只有 slave 支持的。

Mesos 配置项比较多，下面对一些重点配置进行描述。少数为必备项，意味着必须给出配置值；另外一些是可选配置，自己带有默认值。

### 通用项
通用项数量不多，主要涉及到服务绑定地址和日志信息等，包括：

* `--advertise_ip=VALUE` 可以通过该地址访问到服务，比如应用框架访问到 master 节点；
* `--advertise_port=VALUE` 可以通过该端口访问到服务；
* `--external_log_file=VALUE` 指定存储日志的外部文件，可通过 Web 界面查看；
* `--firewall_rules=VALUE` endpoint 防火墙规则，`VALUE` 可以是 JSON 格式或者存有 JSON 格式的文件路径；
* `--ip=VALUE` 服务绑定到的IP 地址，用来监听外面过来的请求；
* `--log_dir=VALUE` 日志文件路径，如果为空（默认值）则不存储日志到本地；
* `--logbufsecs=VALUE`  buffer 多少秒的日志，然后写入本地；
* `--logging_level=VALUE` 日志记录的最低级别；
* `--port=VALUE` 绑定监听的端口，master 默认是 5050，slave 默认是 5051。

### master 专属配置项
这些配置项是针对主节点上的 Mesos master 服务的，围绕高可用、注册信息、对应用框架的资源管理等。用户应该根据本地主节点资源情况来合理的配置这些选项。

用户可以通过 `mesos-master --help` 命令来获取所有支持的配置项信息。

必须指定的配置项有三个：

* `--quorum=VALUE` 必备项，使用基于 replicated-Log 的注册表（即利用 ZooKeeper 实现 HA）时，参与投票时的最少节点个数；
* `--work_dir=VALUE` 必备项，注册表持久化信息存储位置；
* `--zk=VALUE` 如果主节点为 HA 模式，此为必备项，指定 ZooKeepr 的服务地址，支持多个地址，之间用逗号隔离，例如 `zk://username:password@host1:port1,host2:port2,.../path`。还可以为存有路径信息的文件路径。


可选的配置项有：

* `--acls=VALUE` ACL 规则或所在文件；
* `--allocation_interval=VALUE` 执行 allocation 的间隔，默认为 1sec；
* `--allocator=VALUE` 分配机制，默认为 HierarchicalDRF；
* `--[no-]authenticate` 是否允许非认证过的 framework 注册；
* `--[no-]authenticate_slaves` 是否允许非认证过的 slaves 注册；
* `--authenticators=VALUE` 对 framework 或 salves 进行认证时的实现机制；
* `--cluster=VALUE` 集群别名，显示在 Web 界面上供用户识别的；
* `--credentials=VALUE` 存储加密后凭证的文件的路径；
* `--external_log_file=VALUE` 采用外部的日志文件；
* `--framework_sorter=VALUE` 给定 framework 之间的资源分配策略；
* `--hooks=VALUE` master 中安装的 hook 模块；
* `--hostname=VALUE` master 节点使用的主机名，不配置则从系统中获取；
* `--[no-]log_auto_initialize` 是否自动初始化注册表需要的 replicated 日志；
* `--modules=VALUE` 要加载的模块，支持文件路径或者 JSON；
* `--offer_timeout=VALUE` offer 撤销的超时；
* `--rate_limits=VALUE` framework 的速率限制，即 query per second (qps)；
* `--recovery_slave_removal_limit=VALUE` 限制注册表恢复后可以移除或停止的 slave 数目，超出后 master 会失败，默认是 100%；
* `--slave_removal_rate_limit=VALUE slave` 没有完成健康度检查时候被移除的速率上限，例如 1/10mins 代表每十分钟最多有一个；
* `--registry=VALUE` 注册表信息的持久化策略，默认为 `replicated_log` 存放本地，还可以为 `in_memory` 放在内存中；
* `--registry_fetch_timeout=VALUE` 访问注册表失败超时；
* `--registry_store_timeout=VALUE` 存储注册表失败超时；
* `--[no-]registry_strict` 是否按照注册表中持久化信息执行操作，默认为 false；
* `--roles=VALUE` 集群中 framework 可以所属的分配角色；
* `--[no-]root_submissions` root 是否可以提交 framework，默认为 true；
* `--slave_reregister_timeout=VALUE` 新的 lead master 节点选举出来后，多久之内所有的 slave 需要注册，超时的 salve 将被移除并关闭，默认为 10mins；
* `--user_sorter=VALUE` 在用户之间分配资源的策略，默认为 drf；
* `--webui_dir=VALUE` webui 实现的文件目录所在，默认为 `/usr/local/share/mesos/webui`；
* `--weights=VALUE` 各个角色的权重；
* `--whitelist=VALUE` 文件路径，包括发送 offer 的 slave 名单，默认为 None；
* `--zk_session_timeout=VALUE` session 超时，默认为 10secs；
* `--max_executors_per_slave=VALUE` 配置了 `--with-network-isolator` 时可用，限制每个 slave 同时执行任务个数。

下面给出一个由三个节点组成的 master 集群典型配置，工作目录指定为 `/tmp/mesos`，集群名称为 `mesos_cluster`。

```sh
mesos-master \
--zk=zk://10.0.0.2:2181,10.0.0.3:2181,10.0.0.4:2181/mesos \
--quorum=2 \
--work_dir=/tmp/mesos \
--cluster=mesos_cluster
```


### slave 专属配置项
slave 节点支持的配置项是最多的，因为它所完成的事情也最复杂。这些配置项既包括跟主节点打交道的一些参数，也包括对本地资源的配置，包括隔离机制、本地任务的资源限制等。

用户可以通过 `mesos-slave --help` 命令来获取所有支持的配置项信息。

必备项就一个：

* `--master=VALUE` 必备项，master 所在地址，或对应 ZooKeeper 服务地址，或文件路径，可以是列表。

以下为可选配置项：

* `--attributes=VALUE` 机器属性；
* `--authenticatee=VALUE` 跟 master 进行认证时候的认证机制；
* `--[no-]cgroups_enable_cfs` 采用 CFS 进行带宽限制时候对 CPU 资源进行限制，默认为 false；
* `--cgroups_hierarchy=VALUE` cgroups 的目录根位置，默认为 `/sys/fs/cgroup`；
* `--[no-]cgroups_limit_swap` 限制内存和 swap，默认为 false，只限制内存；
* `--cgroups_root=VALUE` 根 cgroups 的名称，默认为 mesos；
* `--container_disk_watch_interval=VALUE` 为容器进行硬盘配额查询的时间间隔；
* `--containerizer_path=VALUE` 采用外部隔离机制（`--isolation=external`）时候，外部容器机制执行文件路径；
* `--containerizers=VALUE` 可用的容器实现机制，包括 mesos、external、docker；
* `--credential=VALUE` 加密后凭证，或者所在文件路径；
* `--default_container_image=VALUE` 采用外部容器机制时，任务缺省使用的镜像；
* `--default_container_info=VALUE` 容器信息的缺省值；
* `--default_role=VALUE` 资源缺省分配的角色；
* `--disk_watch_interval=VALUE` 硬盘使用情况的周期性检查间隔，默认为 1mins；
* `--docker=VALUE` docker 执行文件的路径；
* `--docker_remove_delay=VALUE` 删除容器之前的等待时间，默认为 6hrs；
* `--[no-]docker_kill_orphans` 清除孤儿容器，默认为 true；
* `--docker_sock=VALUE` docker sock 地址，默认为 `/var/run/docker.sock`；
* `--docker_mesos_image=VALUE` 运行 slave 的 docker 镜像，如果被配置，docker 会假定 slave 运行在一个 docker 容器里；
* `--docker_sandbox_directory=VALUE` sandbox 映射到容器里的哪个路径；
* `--docker_stop_timeout=VALUE` 停止实例后等待多久执行 kill 操作，默认为 0secs；
* `--[no-]enforce_container_disk_quota` 是否启用容器配额限制，默认为 false；
* `--executor_registration_timeout=VALUE` 执行应用最多可以等多久再注册到 slave，否则停止它，默认为 1mins；
* `--executor_shutdown_grace_period=VALUE` 执行应用停止后，等待多久，默认为 5secs；
* `--external_log_file=VALUE` 外部日志文件；
* `--fetcher_cache_size=VALUE` fetcher 的 cache 大小，默认为 2 GB；
* `--fetcher_cache_dir=VALUE` fetcher cache 文件存放目录，默认为 /tmp/mesos/fetch；
* `--frameworks_home=VALUE` 执行应用前添加的相对路径，默认为空；
* `--gc_delay=VALUE` 多久清理一次执行应用目录，默认为 1weeks；
* `--gc_disk_headroom=VALUE` 调整计算最大执行应用目录年龄的硬盘留空量，默认为 0.1；
* `--hadoop_home=VALUE` hadoop 安装目录，默认为空，会自动查找 HADOOP_HOME 或者从系统路径中查找；
* `--hooks=VALUE` 安装在 master 中的 hook 模块列表；
* `--hostname=VALUE` slave 节点使用的主机名；
* `--isolation=VALUE` 隔离机制，例如 `posix/cpu,posix/mem`（默认）或者 `cgroups/cpu,cgroups/mem`、`external` 等；
* `--launcher_dir=VALUE` mesos 可执行文件的路径，默认为 `/usr/local/lib/mesos`；
* `--image_providers=VALUE` 支持的容器镜像机制，例如 'APPC,DOCKER'；
* `--oversubscribed_resources_interval=VALUE` slave 节点定期汇报超配资源状态的周期；
* `--modules=VALUE` 要加载的模块，支持文件路径或者 JSON；
* `--perf_duration=VALUE` perf 采样时长，必须小于 perf_interval，默认为 10secs；
* `--perf_events=VALUE` perf 采样的事件；
* `--perf_interval=VALUE` perf 采样的时间间隔；
* `--qos_controller=VALUE` 超配机制中保障 QoS 的控制器名；
* `--qos_correction_interval_min=VALUE` Qos 控制器纠正超配资源的最小间隔，默认为 0secs；
* `--recover=VALUE` 回复后是否重连旧的执行应用，reconnect（默认值）是重连，cleanup 清除旧的执行器并退出；
* `--recovery_timeout=VALUE` slave 恢复时的超时，太久则所有相关的执行应用将自行退出，默认为 15mins；
* `--registration_backoff_factor=VALUE` 跟 master 进行注册时候的重试时间间隔算法的因子，默认为 1secs，采用随机指数算法，最长 1mins；
* `--resource_monitoring_interval=VALUE` 周期性监测执行应用资源使用情况的间隔，默认为 1secs；
* `--resources=VALUE` 每个 slave 可用的资源，比如主机端口默认为 [31000, 32000]；
* `--[no-]revocable_cpu_low_priority` 运行在可撤销 CPU 上容器将拥有较低优先级，默认为 true。
* `--slave_subsystems=VALUE` slave 运行在哪些 cgroup 子系统中，包括 memory，cpuacct 等，缺省为空；
* `--[no-]strict` 是否认为所有错误都不可忽略，默认为 true；
* `--[no-]switch_user` 用提交任务的用户身份来运行，默认为 true；
* `--work_dir=VALUE` framework 的工作目录，默认为 /tmp/mesos。

下面这些选项需要配置 `--with-network-isolator` 一起使用（编译时需要启用 ` --with-network-isolator` 参数）。

* `--ephemeral_ports_per_container=VALUE` 分配给一个容器的临时端口的最大数目，需要为 2 的整数幂（默认为 1024）；
* `--eth0_name=VALUE` public 网络的接口名称，如果不指定，根据主机路由进行猜测；
* `--lo_name=VALUE` loopback 网卡名称；
* `--egress_rate_limit_per_container=VALUE` 每个容器的输出流量限制速率限制（采用 fq_codel 算法来限速），单位是字节每秒；
* `--[no-]-egress_unique_flow_per_container` 是否把不同容器的流量当作彼此不同的流，避免彼此影响（默认为 false）；
* `--[no-]network_enable_socket_statistics` 是否采集每个容器的 socket 统计信息，默认为 false。

下面给出一个典型的 slave 配置，容器为 Docker，监听在 `10.0.0.10` 地址；节点上限制 16 个 CPU、64 GB 内存，容器的非临时端口范围指定为 [31000-32000]，临时端口范围指定为 [32768-57344]；每个容器临时端口最多为 512 个，并且外出流量限速为 50 MB/s。

```sh
mesos-slave \
--master=zk://10.0.0.2:2181,10.0.0.3:2181,10.0.0.4:2181/mesos \
--containerizers=docker \
--ip=10.0.0.10 \
--isolation=cgroups/cpu,cgroups/mem,network/port_mapping \
--resources=cpus:16;mem:64000;ports:[31000-32000];ephemeral_ports:[32768-57344] \
--ephemeral_ports_per_container=512 \
--egress_rate_limit_per_container=50000KB \
--egress_unique_flow_per_container
```

为了避免主机分配的临时端口跟我们指定的临时端口范围冲突，需要在主机节点上进行配置。
```sh
$ echo "57345 61000" > /proc/sys/net/ipv4/ip_local_port_range
```

*注：非临时端口是 Mesos 分配给框架，绑定到任务使用的，端口号往往有明确意义；临时端口是系统分配的，往往不太关心具体端口号。*
