# Custom Bridge
In addition to the default docker0 bridge, users can also specify a bridge to connect containers.
When starting the Docker service, use -b BRIDGE or --bridge=BRIDGE to specify the bridge to use.
If the service is already running, you need to stop the service and delete the old bridge.


$ sudo systemctl stop docker
$ sudo ip link set dev docker0 down
$ sudo brctl delbr docker0
Then create a bridge bridge0.


$ sudo brctl addbr bridge0
$ sudo ip addr add 192.168.5.1/24 dev bridge0
$ sudo ip link set dev bridge0 up
Check that the bridge has been created and started.


$ ip addr show bridge0
4: bridge0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state UP group default
 link/ether 66:38:d0:0d:76:18 brd ff:ff:ff:ff:ff:ff
 inet 192.168.5.1/24 scope global bridge0
 valid_lft forever preferred_lft forever
Add the following content to the Docker configuration file /etc/docker/daemon.json to bridge Docker to the created bridge by default.


{
 "bridge": "bridge0",
}
Start the Docker service.
Create a new container and you can see that it is already bridged to bridge0.
You can continue to use the brctl show command to view bridging information. In addition, you can use the ip addr and ip route commands in the container to view IP address configuration and routing information.