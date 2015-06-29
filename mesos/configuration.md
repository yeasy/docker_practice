## Mesos 配置项解析

Mesos 的 [配置项](http://mesos.apache.org/documentation/latest/configuration/) 可以通过启动时候传递参数或者配置目录下文件的方式给出（推荐方式，一目了然）。

分为三种类型：通用项（master 和 slave 都支持），只有 master 支持的，以及只有 slave 支持的。


### 通用项
* `--ip=VALUE` 监听的 IP 地址
* `--firewall_rules=VALUE` endpoint 防火墙规则，`VALUE` 可以是 JSON 格式或者存有 JSON 格式的文件路径。
* `--log_dir=VALUE` 日志文件路径，默认不存储日志到本地
* `--logbufsecs=VALUE`  buffer 多少秒的日志，然后写入本地
* `--logging_level=VALUE` 日志记录的最低级别
* `--port=VALUE` 监听的端口，master 默认是 5050，slave 默认是 5051。

### master 专属配置项
* `--quorum=VALUE` 必备项，使用基于 replicated-Log 的注册表时，复制的个数
* `--work_dir=VALUE` 必备项，注册表持久化信息存储位置
* `--zk=VALUE` 必备项，zookeepr 的接口地址，支持多个地址，之间用逗号隔离，可以为文件路径
* `--acls=VALUE` ACL 规则或所在文件
* `--allocation_interval=VALUE` 执行 allocation 的间隔，默认为 1sec
* `--allocator=VALUE` 分配机制，默认为 HierarchicalDRF
* `--[no-]authenticate` 是否允许非认证过的 framework 注册
* `--[no-]authenticate_slaves` 是否允许非认证过的 slaves 注册
* `--authenticators=VALUE` 对 framework 或 salves 进行认证时的实现机制
* `--cluster=VALUE` 集群别名
* `--credentials=VALUE` 存储加密后凭证的文件的路径
* `--external_log_file=VALUE` 采用外部的日志文件
* `--framework_sorter=VALUE` 给定 framework 之间的资源分配策略
* `--hooks=VALUE` master 中安装的 hook 模块
* `--hostname=VALUE` master 节点使用的主机名，不配置则从系统中获取
* `--[no-]log_auto_initialize` 是否自动初始化注册表需要的 replicated 日志
* `--modules=VALUE` 要加载的模块，支持文件路径或者 JSON
* `--offer_timeout=VALUE` offer 撤销的超时
* `--rate_limits=VALUE` framework 的速率限制，比如 qps
* `--recovery_slave_removal_limit=VALUE` 限制注册表恢复后可以移除或停止的 slave 数目，超出后 master 会失败，默认是 100%
* `--slave_removal_rate_limit=VALUE slave` 没有完成健康度检查时候被移除的速率上限，例如 1/10mins 代表每十分钟最多有一个
* `--registry=VALUE` 注册表的持久化策略，默认为 `replicated_log`，还可以为 `in_memory`
* `--registry_fetch_timeout=VALUE` 访问注册表失败超时
* `--registry_store_timeout=VALUE` 存储注册表失败超时
* `--[no-]registry_strict` 是否按照注册表中持久化信息执行操作，默认为 false
* `--roles=VALUE` 集群中 framework 可以所属的分配角色
* `--[no-]root_submissions` root 是否可以提交 framework，默认为 true
* `--slave_reregister_timeout=VALUE` 新的 lead master 节点选举出来后，多久之内所有的 slave 需要注册，超时的 salve 将被移除并关闭，默认为 10mins
* `--user_sorter=VALUE` 在用户之间分配资源的策略，默认为 drf
* `--webui_dir=VALUE` webui 实现的文件目录所在，默认为 `/usr/local/share/mesos/webui`
* `--weights=VALUE` 各个角色的权重
* `--whitelist=VALUE` 文件路径，包括发送 offer 的 slave 名单，默认为 None
* `--zk_session_timeout=VALUE` session 超时，默认为 10secs
* `--max_executors_per_slave=VALUE` 配置了 `--with-network-isolator` 时可用，限制每个 slave 同时执行任务个数

### slave 专属配置项
* `--master=VALUE` 必备项，master 所在地址，或 zookeeper 地址，或文件路径，可以是列表
* `--attributes=VALUE` 机器属性
* `--authenticatee=VALUE` 跟 master 进行认证时候的认证机制
* `--[no-]cgroups_enable_cfs` 采用 CFS 进行带宽限制时候对 CPU 资源进行限制，默认为 false
* `--cgroups_hierarchy=VALUE` cgroups 的目录根位置，默认为 `/sys/fs/cgroup`
* `--[no-]cgroups_limit_swap` 限制内存和 swap，默认为 false，只限制内存
* `--cgroups_root=VALUE` 根 cgroups 的名称，默认为 mesos
* `--container_disk_watch_interval=VALUE` 为容器进行硬盘配额查询的时间间隔
* `--containerizer_path=VALUE` 采用外部隔离机制（`--isolation=external`）时候，外部容器机制执行文件路径
* `--containerizers=VALUE` 可用的容器实现机制，包括 mesos、external、docker
* `--credential=VALUE` 加密后凭证，或者所在文件路径
* `--default_container_image=VALUE` 采用外部容器机制时，任务缺省使用的镜像
* `--default_container_info=VALUE` 容器信息的缺省值
* `--default_role=VALUE` 资源缺省分配的角色
* `--disk_watch_interval=VALUE` 硬盘使用情况的周期性检查间隔，默认为 1mins
* `--docker=VALUE` docker 执行文件的路径
* `--docker_remove_delay=VALUE` 删除容器之前的等待时间，默认为 6hrs
* `--[no-]docker_kill_orphans` 清除孤儿容器，默认为 true
* `--docker_sock=VALUE` docker sock 地址，默认为 `/var/run/docker.sock`
* `--docker_mesos_image=VALUE` 运行 slave 的 docker 镜像，如果被配置，docker 会假定 slave 运行在一个 docker 容器里
* `--docker_sandbox_directory=VALUE` sandbox 映射到容器里的哪个路径
* `--docker_stop_timeout=VALUE` 停止实例后等待多久执行 kill 操作，默认为 0secs
* `--[no-]enforce_container_disk_quota` 是否启用容器配额限制，默认为 false
* `--executor_registration_timeout=VALUE` 执行应用最多可以等多久再注册到 slave，否则停止它，默认为 1mins
* `--executor_shutdown_grace_period=VALUE` 执行应用停止后，等待多久，默认为 5secs
* `--external_log_file=VALUE` 外部日志文件
* `--frameworks_home=VALUE` 执行应用前添加的相对路径，默认为空
* `--gc_delay=VALUE` 多久清理一次执行应用目录，默认为 1weeks
* `--gc_disk_headroom=VALUE` 调整计算最大执行应用目录年龄的硬盘留空量，默认为 0.1
* `--hadoop_home=VALUE` hadoop 安装目录，默认为空，会自动查找 HADOOP_HOME 或者从系统路径中查找
* `--hooks=VALUE` 安装在 master 中的 hook 模块列表
* `--hostname=VALUE` slave 节点使用的主机名
* `--isolation=VALUE` 隔离机制，例如 `posix/cpu,posix/mem`（默认）或者 `cgroups/cpu,cgroups/mem`
* `--launcher_dir=VALUE` mesos 可执行文件的路径，默认为 `/usr/local/lib/mesos`
* `--modules=VALUE` 要加载的模块，支持文件路径或者 JSON
* `--perf_duration=VALUE` perf 采样时长，必须小于 perf_interval，默认为 10secs
* `--perf_events=VALUE` perf 采样的事件
* `--perf_interval=VALUE` perf 采样的时间间隔
* `--recover=VALUE` 回复后是否重连上旧的执行应用
* `--recovery_timeout=VALUE` slave 恢复时的超时，太久则所有相关的执行应用将自行退出，默认为 15mins
* `--registration_backoff_factor=VALUE` 跟 master 进行注册时候的重试时间间隔算法的因子，默认为 1secs，采用随机指数算法，最长 1mins
* `--resource_monitoring_interval=VALUE` 周期性监测执行应用资源使用情况的间隔，默认为 1secs
* `--resources=VALUE` 每个 slave 可用的资源
* `--slave_subsystems=VALUE` slave 运行在哪些 cgroup 子系统中，包括 memory，cpuacct 等，缺省为空
* `--[no-]strict` 是否认为所有错误都不可忽略，默认为 true
* `--[no-]switch_user` 用提交任务的用户身份来运行，默认为 true
* `--fetcher_cache_size=VALUE` fetcher 的 cache 大小，默认为 2 GB
* `--fetcher_cache_dir=VALUE` fetcher cache 文件存放目录，默认为 /tmp/mesos/fetch
* `--work_dir=VALUE` framework 的工作目录，默认为 /tmp/mesos

下面的选项需要配置 `--with-network-isolator` 一起使用
* `--ephemeral_ports_per_container=VALUE` 分配给一个容器的临时端口，默认为 1024
* `--eth0_name=VALUE` public 网络的接口名称，如果不指定，根据主机路由进行猜测
* `--lo_name=VALUE` loopback 网卡名称
* `--egress_rate_limit_per_container=VALUE` 每个容器的 egress 流量限制速率
* `--[no-]network_enable_socket_statistics` 是否采集每个容器的 socket 统计信息，默认为 false
