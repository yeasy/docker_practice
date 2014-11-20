## 進入容器
在使用 `-d` 參數時，容器啟動後會進入後臺。
某些時候需要進入容器進行操作，有很多種方法，包括使用 `docker attach` 命令或 `nsenter` 工具等。
### attach 命令
`docker attach` 是Docker自帶的命令。下面示例如何使用該命令。
```
$ sudo docker run -idt ubuntu
243c32535da7d142fb0e6df616a3c3ada0b8ab417937c853a9e1c251f499f550
$ sudo docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
243c32535da7        ubuntu:latest       "/bin/bash"         18 seconds ago      Up 17 seconds                           nostalgic_hypatia
$sudo docker attach nostalgic_hypatia
root@243c32535da7:/#
```
但是使用 `attach` 命令有時候並不方便。當多個窗口同時 attach 到同一個容器的時候，所有窗口都會同步顯示。當某個窗口因命令阻塞時,其他窗口也無法執行操作了。

### nsenter 命令
#### 安裝
`nsenter` 工具在 util-linux 包2.23版本後包含。
如果系統中 util-linux 包沒有該命令，可以按照下面的方法從源碼安裝。
```
$ cd /tmp; curl https://www.kernel.org/pub/linux/utils/util-linux/v2.24/util-linux-2.24.tar.gz | tar -zxf-; cd util-linux-2.24;
$ ./configure --without-ncurses
$ make nsenter && sudo cp nsenter /usr/local/bin
```

#### 使用
`nsenter` 可以訪問另一個程序的名字空間。nsenter 要正常工作需要有 root 權限。
很不幸，Ubuntu 14.4 仍然使用的是 util-linux 2.20。安裝最新版本的 util-linux（2.24）版，請按照以下步驟：
```
$ wget https://www.kernel.org/pub/linux/utils/util-linux/v2.24/util-linux-2.24.tar.gz; tar xzvf util-linux-2.24.tar.gz
$ cd util-linux-2.24
$ ./configure --without-ncurses && make nsenter
$ sudo cp nsenter /usr/local/bin
```
為了連接到容器，你還需要找到容器的第一個程序的 PID，可以通過下面的命令獲取。
```
PID=$(docker inspect --format "{{ .State.Pid }}" <container>)
```
通過這個 PID，就可以連接到這個容器：
```
$ nsenter --target $PID --mount --uts --ipc --net --pid
```
下面給出一個完整的例子。
```
$ sudo docker run -idt ubuntu
243c32535da7d142fb0e6df616a3c3ada0b8ab417937c853a9e1c251f499f550
$ sudo docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
243c32535da7        ubuntu:latest       "/bin/bash"         18 seconds ago      Up 17 seconds                           nostalgic_hypatia
$ PID=$(docker-pid 243c32535da7)
10981
$ sudo nsenter --target 10981 --mount --uts --ipc --net --pid
root@243c32535da7:/#
```
更簡單的，建議大家下載
[.bashrc_docker](https://github.com/yeasy/docker_practice/raw/master/_local/.bashrc_docker)，並將內容放到 .bashrc 中。
```
$ wget -P ~ https://github.com/yeasy/docker_practice/raw/master/_local/.bashrc_docker;
$ echo "[ -f ~/.bashrc_docker ] && . ~/.bashrc_docker" >> ~/.bashrc; source ~/.bashrc
```
這個文件中定義了很多方便使用 Docker 的命令，例如 `docker-pid` 可以獲取某個容器的 PID；而 `docker-enter` 可以進入容器或直接在容器內執行命令。
```
$ echo $(docker-pid <container>)
$ docker-enter <container> ls
```
