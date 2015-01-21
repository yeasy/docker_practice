##环境变量参考

*注意: 现在已经不推荐使用环境变量链接服务。替代方案是使用链接名称（默认就是被连接的服务名字）作为主机名来链接。详情查看 [fig.yml章节](./yml_ref.md)。

Fig 使用 Docker 链接来暴露一个服务的容器给其它容器。每一个链接的容器会注入一组以容器名称的大写字母开头得环境变量。

查看一个服务有那些有效的环境变量可以执行 `fig run SERVICE env`。

`name_PORT`

完整URL，例如： `DB_PORT=tcp://172.17.0.5:5432`

`name_PORT_num_protocol`

完整URL，例如： `DB_PORT_5432_TCP=tcp://172.17.0.5:5432`

`name_PORT_num_protocol_ADDR`

容器的IP地址，例如： `DB_PORT_5432_TCP_ADDR=172.17.0.5`

`name_PORT_num_protocol_PORT`

暴露端口号，例如： `DB_PORT_5432_TCP_PORT=5432`

`name_PORT_num_protocol_PROTO`

协议（tcp 或 udp），例如： `DB_PORT_5432_TCP_PROTO=tcp`

`name_NAME`

完整合格的容器名称，例如： `DB_1_NAME=/myapp_web_1/myapp_db_1`