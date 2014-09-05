##配置DNS
docker没有定制为每一个容器定制image，是怎么提供容器的主机名和dns配置呢？秘诀就是它用主机上的3个配置文件来覆盖容器的这3个文件，在容器中使用mount命令可以看到：
```
$ mount
...
/dev/disk/by-uuid/1fec...ebdf on /etc/hostname type ext4 ...
/dev/disk/by-uuid/1fec...ebdf on /etc/hosts type ext4 ...
tmpfs on /etc/resolv.conf type tmpfs ...
...
```
这种机制可以让宿主主机从dhcp更新dns信息后，马上更新所有docker容器的dns配置。如果要保持docker中这些文件固定不变，你可以不覆盖容器中的这些配置文件，然后使用下面的选项来配置它们。
配置容器dns服务的方法

-h HOSTNAME or --hostname=HOSTNAME  
设定容器的主机名，它会被写到/etc/hostname，/etc/hosts中的ip地址自动写成分配的ip地址，在/bin/bash中显示该主机名。但它不会在docker ps中显示，也不会在其他的容器的/etc/hosts中显示。

--link=CONTAINER_NAME:ALIAS
这选项会在创建容器的时候添加一个其他容器CONTAINE_NAME的主机名到/etc/hosts文件中，让新容器的进程可以使用主机名ALIAS就可以连接它。--link=会在容器之间的通信中更详细的介绍

--dns=IP_ADDRESS
添加dns服务器到容器的/etc/resolv,conf中，让容器用这ip地址来解析所有不在/etc/hosts中的主机名。

--dns-search=DOMAIN
设定容器的搜索域，当设定搜索域为.example.com时，会在搜索一个host主机名时，dns不仅搜索host，还会搜索host.example.com
注意：如果没有上述最后2个选项，docker会用主机上的/etc/resolv.conf来配置容器，它是默认配置。