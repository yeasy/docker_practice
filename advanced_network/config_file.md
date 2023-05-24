# Editing Network Configuration Files

Starting with Docker 1.2.0, you can edit the /etc/hosts, /etc/hostname, and /etc/resolv.conf files in a running container.

However, these changes are temporary and are only retained in the running container. They are not saved after the container terminates or restarts and are not committed by docker commit.