##終止容器
可以使用 `docker stop` 來終止一個運行中的容器。

此外，當Docker容器中指定的應用終結時，容器也自動終止。
例如對於上一章節中只啟動了一個終端的容器，用戶通過 `exit` 命令或 `Ctrl+d` 來退出終端時，所創建的容器立刻終止。

終止狀態的容器可以用 `docker ps -a` 命令看到。例如
```
sudo docker ps -a
CONTAINER ID        IMAGE                    COMMAND                CREATED             STATUS                          PORTS               NAMES
ba267838cc1b        ubuntu:14.04             "/bin/bash"            30 minutes ago      Exited (0) About a minute ago                       trusting_newton
98e5efa7d997        training/webapp:latest   "python app.py"        About an hour ago   Exited (0) 34 minutes ago                           backstabbing_pike
```

處於終止狀態的容器，可以通過 `docker start` 命令來重新啟動。

此外，`docker restart` 命令會將一個運行態的容器終止，然後再重新啟動它。
