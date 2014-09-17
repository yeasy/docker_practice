##创建tomcat/weblogic集群
###安装tomcat镜像
准备好需要的jdk tomcat等软件放到home目录下面，启动一个虚拟机
```
docker run -t -i -v /home:/opt/data  --name mk_tomcat ubuntu /bin/bash
```
这条命令挂载本地home目录到虚拟机的/opt/data目录，虚拟机内目录若不存在，则会自动创建。接下来就是tomcat的基本配置，jdk环境变量设置好之后，将tomcat程序放到/opt/apache-tomcat下面
编辑/etc/supervisor/conf.d/supervisor.conf文件，添加tomcat项
```
[supervisord]
nodaemon=true

[program:tomcat]
command=/opt/apache-tomcat/bin/startup.sh

[program:sshd]
command=/usr/sbin/sshd -D
docker commit  ac6474aeb31d  tomcat
```

新建tomcat文件夹，新建Dockerfile
```
FROM tomcat
EXPOSE  22 8080
CMD ["/usr/bin/supervisord"]
```
根据dockerfile 创建image
```
docker build tomcat tomcat 
```
###安装weblogic镜像

步骤和tomcat基本一致，这里贴一下配置文件
```
supervisor.conf
[supervisord]
nodaemon=true


[program:weblogic]
command=/opt/Middleware/user_projects/domains/base_domain/bin/startWebLogic.sh

[program:sshd]
command=/usr/sbin/sshd -D
dockerfile
FROM weblogic
EXPOSE  22 7001
CMD ["/usr/bin/supervisord"]
```

###tomcat/weblogic 镜像的使用
1)存储的使用
在启用docker run 的时候，使用 -v参数

    -v, --volume=[]            Bind mount a volume (e.g. from the host: -v /host:/container, from docker: -v /container)
    
将本地磁盘映射到虚拟机内部，它在主机和虚拟机容器之间是实时变化的，所以我们更新程序、上传代码只需要更新物理主机的目录就可以了，数据存储的详细介绍请参见本文第七小节
2)tomcat和weblogic集群的实现
tomcat只要开启多个容器即可
```
docker run -d -v -p 204:22 -p 7003:8080 -v /home/data:/opt/data --name tm1 tomcat /usr/bin/supervisord
docker run -d -v -p 205:22 -p 7004:8080 -v /home/data:/opt/data --name tm2 tomcat /usr/bin/supervisord
docker run -d -v -p 206:22 -p 7005:8080 -v /home/data:/opt/data --name tm3 tomcat /usr/bin/supervisord
```

这里说一下weblogic的配置，大家知道weblogic有一个域的概念。如果要使用常规的administrator +node的方式部署，就需要在supervisord中分别写出administartor server和node server的启动脚本，这样做的优点是：
* 可以使用weblogic的集群，同步等概念
* 部署一个集群应用程序，只需要安装一次应用到集群上即可
缺点是：
* docker配置复杂了
* 没办法自动扩展集群的计算容量，如需添加节点，需要在administrator上先创建节点，然后再配置心的容器supervisor启动脚本，然后再启动容器
另外种方法是将所有的程序都安装在adminiserver上面，需要扩展的时候，启动多个节点即可，它的优点和缺点和上一中方法恰恰相反。（目前我使用这种方式来部署开发和测试环境）
```
docker run -d -v -p 204:22 -p 7001:7001 -v /home/data:/opt/data --name node1 weblogic /usr/bin/supervisord
docker run -d -v -p 205:22 -p 7002:7001 -v /home/data:/opt/data --name node2 weblogic /usr/bin/supervisord
docker run -d -v -p 206:22 -p 7003:7001 -v /home/data:/opt/data --name node3 weblogic /usr/bin/supervisord
```

这样在前端使用nginx 来做负载均衡就可以完成配置了
