# kubectl 使用
[kubectl](https://github.com/GoogleCloudPlatform/kubernetes) 是 Kubernetes 自带的客户端，可以用它来直接操作 Kubernetes。

使用格式有两种：
```sh
kubectl [flags]
kubectl [command]
```

## get
Display one or many resources
## describe
Show details of a specific resource
## create
Create a resource by filename or stdin
## update
Update a resource by filename or stdin.
## delete
Delete a resource by filename, stdin, resource and ID, or by resources and label selector.
## namespace
SUPERCEDED: Set and view the current Kubernetes namespace
## log
Print the logs for a container in a pod.
## rolling-update
Perform a rolling update of the given ReplicationController.
## resize
Set a new size for a Replication Controller.
## exec
Execute a command in a container.
## port-forward
Forward one or more local ports to a pod.
## proxy
Run a proxy to the Kubernetes API server
## run-container
Run a particular image on the cluster.
## stop
Gracefully shut down a resource by id or filename.
## expose
Take a replicated application and expose it as Kubernetes Service
## label
Update the labels on a resource
## config
config modifies kubeconfig files
## cluster-info
Display cluster info
## api-versions
Print available API versions.
## version
Print the client and server version information.
## help
Help about any command
