# Container Access Control
Container access control is mainly managed and implemented through the iptables firewall on Linux. iptables is the default firewall software on Linux and comes with most distributions.
Container Access to External Networks
For containers to access external networks, local system forwarding support is required. In Linux systems, check if forwarding is turned on.


$sysctl net.ipv4.ip_forward
net.ipv4.ip_forward = 1
If it is 0, it means that forwarding is not turned on and needs to be turned on manually.


$sysctl -w net.ipv4.ip_forward=1
If you set --ip-forward=true when starting the Docker service, Docker will automatically set the system's ip_forward parameter to 1.
Container-to-Container Access
Container-to-container access requires two levels of support.
 - Whether the container's network topology is interconnected. By default, all containers are connected to the docker0 bridge.
 - Whether the local system's firewall software -- iptables allows passage.

Access to All Ports
When starting the Docker service (i.e., dockerd), a forwarding policy is added to the local host iptables FORWARD chain by default. Whether the policy is passed (ACCEPT) or prohibited (DROP) depends on whether it is configured with --icc=true (default value) or --icc=false. Of course, if you manually specify --iptables=false, no iptables rules will be added.
As you can see, by default, different containers are allowed to communicate with each other over the network. For security reasons, you can configure {"icc": false} in the /etc/docker/daemon.json file to disable it.
Access to Specified Ports
After closing network access with -icc=false, you can also use the --link=CONTAINER_NAME:ALIAS option to access open ports of the container.
For example, when starting the Docker service, you can use both icc=false --iptables=true parameters to close network access that allows mutual access and allow Docker to modify system iptables rules.
At this point, the system's iptables rules may be similar


$ sudo iptables -nL
...
Chain FORWARD (policy ACCEPT)
target prot opt source destination
DROP all -- 0.0.0.0/0 0.0.0.0/0
...
Afterwards, use the --link=CONTAINER_NAME:ALIAS option when starting a container (docker run). Docker will add an ACCEPT rule for both containers in iptable, allowing mutual access to open ports (depending on the EXPOSE directive in the Dockerfile).
After adding the --link=CONTAINER_NAME:ALIAS option and adding an iptables rule.


$ sudo iptables -nL
...
Chain FORWARD (policy ACCEPT)
target prot opt source destination
ACCEPT tcp -- 172.17.0.2 172.17.0.3 tcp spt:80
ACCEPT tcp -- 172.17.0.3 172.17.0.2 tcp dpt:80
DROP all -- 0.0.0.0/0 0.0.0.0/0
Note: The CONTAINER_NAME in --link=CONTAINER_NAME:ALIAS must currently be a name assigned by Docker or a name specified using the --name parameter. Hostnames are not recognized."
