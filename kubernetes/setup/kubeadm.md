# 使用 kubeadm 部署 kubernetes(CRI 使用 containerd)

`kubeadm` 提供了 `kubeadm init` 以及 `kubeadm join` 这两个命令作为快速创建 `kubernetes` 集群的最佳实践。

## 安装 containerd

参考 [安装 Docker](../../install) 一节添加 apt/yum 源，之后执行如下命令。

```bash
# debian 系
$ sudo apt install containerd.io

# rhel 系
$ sudo yum install containerd.io
```

## 配置 containerd

新建 `/etc/systemd/system/cri-containerd.service` 文件

```
[Unit]
Description=containerd container runtime for kubernetes
Documentation=https://containerd.io
After=network.target local-fs.target

[Service]
ExecStartPre=-/sbin/modprobe overlay
ExecStart=/usr/bin/containerd --config //etc/cri-containerd/config.toml

Type=notify
Delegate=yes
KillMode=process
Restart=always
RestartSec=5
# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNPROC=infinity
LimitCORE=infinity
LimitNOFILE=infinity
# Comment TasksMax if your systemd version does not supports it.
# Only systemd 226 and above support this version.
TasksMax=infinity
OOMScoreAdjust=-999

[Install]
WantedBy=multi-user.target
```

新建 `/etc/cri-containerd/config.toml` containerd 配置文件

```toml
version = 2
# persistent data location
root = "/var/lib/cri-containerd"
# runtime state information
state = "/run/cri-containerd"
plugin_dir = ""
disabled_plugins = []
required_plugins = []
# set containerd's OOM score
oom_score = 0

[grpc]
  address = "/run/cri-containerd/cri-containerd.sock"
  tcp_address = ""
  tcp_tls_cert = ""
  tcp_tls_key = ""
  # socket uid
  uid = 0
  # socket gid
  gid = 0
  max_recv_message_size = 16777216
  max_send_message_size = 16777216

[debug]
  address = ""
  format = "json"
  uid = 0
  gid = 0
  level = ""

[metrics]
  address = "127.0.0.1:1338"
  grpc_histogram = false

[cgroup]
  path = ""

[timeouts]
  "io.containerd.timeout.shim.cleanup" = "5s"
  "io.containerd.timeout.shim.load" = "5s"
  "io.containerd.timeout.shim.shutdown" = "3s"
  "io.containerd.timeout.task.state" = "2s"

[plugins]
  [plugins."io.containerd.gc.v1.scheduler"]
    pause_threshold = 0.02
    deletion_threshold = 0
    mutation_threshold = 100
    schedule_delay = "0s"
    startup_delay = "100ms"
  [plugins."io.containerd.grpc.v1.cri"]
    disable_tcp_service = true
    stream_server_address = "127.0.0.1"
    stream_server_port = "0"
    stream_idle_timeout = "4h0m0s"
    enable_selinux = false
    selinux_category_range = 1024
    sandbox_image = "registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.5"
    stats_collect_period = 10
    # systemd_cgroup = false
    enable_tls_streaming = false
    max_container_log_line_size = 16384
    disable_cgroup = false
    disable_apparmor = false
    restrict_oom_score_adj = false
    max_concurrent_downloads = 3
    disable_proc_mount = false
    unset_seccomp_profile = ""
    tolerate_missing_hugetlb_controller = true
    disable_hugetlb_controller = true
    ignore_image_defined_volumes = false
    [plugins."io.containerd.grpc.v1.cri".containerd]
      snapshotter = "overlayfs"
      default_runtime_name = "runc"
      no_pivot = false
      disable_snapshot_annotations = false
      discard_unpacked_layers = false
      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
          runtime_type = "io.containerd.runc.v2"
          pod_annotations = []
          container_annotations = []
          privileged_without_host_devices = false
          base_runtime_spec = ""
          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
            # SystemdCgroup enables systemd cgroups.
            SystemdCgroup = true
            # BinaryName is the binary name of the runc binary.
            # BinaryName = "runc"
            # BinaryName = "crun"
            # NoPivotRoot disables pivot root when creating a container.
            # NoPivotRoot = false

            # NoNewKeyring disables new keyring for the container.
            # NoNewKeyring = false

            # ShimCgroup places the shim in a cgroup.
            # ShimCgroup = ""

            # IoUid sets the I/O's pipes uid.
            # IoUid = 0

            # IoGid sets the I/O's pipes gid.
            # IoGid = 0

            # Root is the runc root directory.
            Root = ""

            # CriuPath is the criu binary path.
            # CriuPath = ""

            # CriuImagePath is the criu image path
            # CriuImagePath = ""

            # CriuWorkPath is the criu work path.
            # CriuWorkPath = ""
    [plugins."io.containerd.grpc.v1.cri".cni]
      bin_dir = "/opt/cni/bin"
      conf_dir = "/etc/cni/net.d"
      max_conf_num = 1
      conf_template = ""
    [plugins."io.containerd.grpc.v1.cri".registry]
      config_path = "/etc/cri-containerd/certs.d"
      [plugins."io.containerd.grpc.v1.cri".registry.headers]
        # Foo = ["bar"]
    [plugins."io.containerd.grpc.v1.cri".image_decryption]
      key_model = ""
    [plugins."io.containerd.grpc.v1.cri".x509_key_pair_streaming]
      tls_cert_file = ""
      tls_key_file = ""
  [plugins."io.containerd.internal.v1.opt"]
    path = "/opt/cri-containerd"
  [plugins."io.containerd.internal.v1.restart"]
    interval = "10s"
  [plugins."io.containerd.metadata.v1.bolt"]
    content_sharing_policy = "shared"
  [plugins."io.containerd.monitor.v1.cgroups"]
    no_prometheus = false
  [plugins."io.containerd.runtime.v2.task"]
    platforms = ["linux/amd64"]
  [plugins."io.containerd.service.v1.diff-service"]
    default = ["walking"]
  [plugins."io.containerd.snapshotter.v1.devmapper"]
    root_path = ""
    pool_name = ""
    base_image_size = ""
    async_remove = false
```

## 安装 **kubelet** **kubeadm** **kubectl** **cri-tools** **kubernetes-cni**

### Ubuntu/Debian

```bash
$ apt-get update && apt-get install -y apt-transport-https
$ curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add -

$ cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF

$ apt-get update
$ apt-get install -y kubelet kubeadm kubectl
```

### CentOS/Fedora

```bash
$ cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

$ sudo yum install -y kubelet kubeadm kubectl
```

## 修改内核的运行参数

```bash
$ cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

# 应用配置
$ sysctl --system
```

## 配置 kubelet

### 修改 `kubelet.service`

`/etc/systemd/system/kubelet.service.d/10-proxy-ipvs.conf` 写入以下内容

```bash
# 启用 ipvs 相关内核模块
[Service]
ExecStartPre=-/sbin/modprobe ip_vs
ExecStartPre=-/sbin/modprobe ip_vs_rr
ExecStartPre=-/sbin/modprobe ip_vs_wrr
ExecStartPre=-/sbin/modprobe ip_vs_sh
```

执行以下命令应用配置。

```bash
$ sudo systemctl daemon-reload
```

## 部署

### master

```bash
$ systemctl enable cri-containerd

$ systemctl start cri-containerd

$ sudo kubeadm init \
      --image-repository registry.cn-hangzhou.aliyuncs.com/google_containers \
      --pod-network-cidr 10.244.0.0/16 \
      --cri-socket /run/cri-containerd/cri-containerd.sock \
      --v 5 \
      --ignore-preflight-errors=all
```

* `--pod-network-cidr 10.244.0.0/16` 参数与后续 CNI 插件有关，这里以 `flannel` 为例，若后续部署其他类型的网络插件请更改此参数。

> 执行可能出现错误，例如缺少依赖包，根据提示安装即可。

执行成功会输出

```bash
...
[addons] Applied essential addon: CoreDNS
I1116 12:35:13.270407   86677 request.go:538] Throttling request took 181.409184ms, request: POST:https://192.168.199.100:6443/api/v1/namespaces/kube-system/serviceaccounts
I1116 12:35:13.470292   86677 request.go:538] Throttling request took 186.088112ms, request: POST:https://192.168.199.100:6443/api/v1/namespaces/kube-system/configmaps
[addons] Applied essential addon: kube-proxy

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 192.168.199.100:6443 --token cz81zt.orsy9gm9v649e5lf \
    --discovery-token-ca-cert-hash sha256:5edb316fd0d8ea2792cba15cdf1c899a366f147aa03cba52d4e5c5884ad836fe
```

### node 工作节点

在 **另一主机** 重复 **部署** 小节以前的步骤，安装配置好 kubelet。根据提示，加入到集群。

```bash
$ systemctl enable cri-containerd

$ systemctl start cri-containerd

$ kubeadm join 192.168.199.100:6443 \
    --token cz81zt.orsy9gm9v649e5lf \
    --discovery-token-ca-cert-hash sha256:5edb316fd0d8ea2792cba15cdf1c899a366f147aa03cba52d4e5c5884ad836fe \
    --cri-socket /run/cri-containerd/cri-containerd.sock
```

## 查看服务

所有服务启动后，通过 `crictl` 查看本地实际运行的容器。这些服务大概分为三类：主节点服务、工作节点服务和其它服务。

```bash
CONTAINER_RUNTIME_ENDPOINT=/run/cri-containerd/cri-containerd.sock crictl ps -a
```

### 主节点服务

* `apiserver` 是整个系统的对外接口，提供 RESTful 方式供客户端和其它组件调用；

* `scheduler` 负责对资源进行调度，分配某个 pod 到某个节点上；

* `controller-manager` 负责管理控制器，包括 endpoint-controller（刷新服务和 pod 的关联信息）和 replication-controller（维护某个 pod 的复制为配置的数值）。

### 工作节点服务

* `proxy` 为 pod 上的服务提供访问的代理。

### 其它服务

* Etcd 是所有状态的存储数据库；

## 使用

将 `/etc/kubernetes/admin.conf` 复制到 `~/.kube/config`

执行 `$ kubectl get all -A` 查看启动的服务。

由于未部署 CNI 插件，CoreDNS 未正常启动。如何使用 Kubernetes，请参考后续章节。

## 部署 CNI

这里以 `flannel` 为例进行介绍。

### flannel

检查 podCIDR 设置

```bash
$ kubectl get node -o yaml | grep CIDR

# 输出
    podCIDR: 10.244.0.0/16
    podCIDRs:
```

```bash
$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/v0.11.0/Documentation/kube-flannel.yml
```

## master 节点默认不能运行 pod

如果用 `kubeadm` 部署一个单节点集群，默认情况下无法使用，请执行以下命令解除限制

```bash
$ kubectl taint nodes --all node-role.kubernetes.io/master-

# 恢复默认值
# $ kubectl taint nodes NODE_NAME node-role.kubernetes.io/master=true:NoSchedule
```

## 参考文档

* [官方文档](https://kubernetes.io/zh/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
* [Container runtimes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/#containerd)
