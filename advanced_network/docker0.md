# Configuring the docker0 Bridge
The Docker service will create a docker0 bridge by default (with an internal docker0 interface on it), which connects other physical or virtual network cards at the kernel layer, putting all containers and the local host on the same physical network.
Docker specifies the IP address and subnet mask of the docker0 interface by default, allowing communication between the host and containers through the bridge. It also specifies the MTU (maximum transmission unit allowed by the interface), which is usually 1500 Bytes or the default value supported by the host network routing. These values can be configured when starting the service.
 - --bip=CIDR IP address plus mask format, such as 192.168.1.5/24
 - --mtu=BYTES Override the default Docker mtu configuration

You can also configure DOCKER_OPTS in the configuration file and then restart the service.
Since Docker's bridge is currently a Linux bridge, users can use brctl show to view bridge and port connection information.

$ sudo brctl show
bridge name bridge id STP enabled interfaces
docker0 8000.3a1d7362b4ee no veth65f9
 vethdda6
*Note: The brctl command can be installed on Debian and Ubuntu using sudo apt-get install bridge-utils.
Each time a new container is created, Docker selects an available IP address from the available address range and assigns it to the container's eth0 port. Use the IP of the docker0 interface on the local host as the default gateway for all containers.

$ sudo docker run -i -t --rm base /bin/bash
$ ip addr show eth0
24: eth0: <BROADCAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
 link/ether 32:6f:e0:35:57:91 brd ff:ff:ff:ff:ff:ff
 inet 172.17.0.3/16 scope global eth0
 valid_lft forever preferred_lft forever
 inet6 fe80::306f:e0ff:fe35:5791/64 scope link
 valid_lft forever preferred_lft forever

$ ip route
default via 172.17.42.1 dev eth0
172.17.0.0/16 dev eth0 proto kernel scope link src 172.17.0.3
