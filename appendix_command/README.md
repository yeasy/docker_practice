# Docker命令查詢

##基本語法
    docker [OPTIONS] COMMAND [arg...]
一般來說，Docker 命令可以用來管理 daemon，或者通過 CLI 命令管理鏡像和容器。可以通過 `man docker` 來查看這些命令。


##選項
    -D=true|false
        使用 debug 模式。默認為 false。

    -H, --host=[unix:///var/run/docker.sock]: tcp://[host:port]來綁定或者 unix://[/path/to/socket] 來使用。
        在 daemon 模式下綁定的 socket，通過一個或多個 tcp://host:port, unix:///path/to/socket, fd://* or fd://socketfd 來指定。

    --api-enable-cors=true|false
        在遠端 API 中啟用 CORS 頭。缺省為 false。

    -b=""
        將容器掛載到一個已存在的網橋上。指定為 'none' 時則禁用容器的網絡。

    --bip=""
        讓動態創建的 docker0 采用給定的 CIDR 地址; 與 -b 選項互斥。

    -d=true|false
        使用 daemon 模式。缺省為 false。

    --dns=""
        讓 Docker 使用給定的 DNS 服務器。

    -g=""
        指定 Docker 執行時的 root 路徑。缺省為 /var/lib/docker。

    --icc=true|false
        啟用容器間通信。默認為 true。

    --ip=""
        綁定端口時候的默認 IP 地址。缺省為 0.0.0.0。

    --iptables=true|false
        禁止 Docker 添加 iptables 規則。缺省為 true。

    --mtu=VALUE
        指定容器網絡的 mtu。缺省為 1500。

    -p=""
        指定 daemon 的 PID 文件路徑。缺省為 /var/run/docker.pid。

    -s=""
        強制 Docker 執行時使用給定的存儲驅動。

    -v=true|false
        輸出版本信息並退出。缺省值為 false。

    --selinux-enabled=true|false
        啟用 SELinux 支持。缺省值為 false。SELinux 目前不支持 BTRFS 存儲驅動。


##命令
Docker 的命令可以采用 `docker-CMD` 或者 `docker CMD` 的方式執行。兩者一致。

    docker-attach(1)
        依附到一個正在執行的容器中。

    docker-build(1)
        從一個 Dockerfile 創建一個鏡像

    docker-commit(1)
        從一個容器的修改中創建一個新的鏡像

    docker-cp(1)
        從容器中復制文件到宿主系統中

    docker-diff(1)
        檢查一個容器文件系統的修改

    docker-events(1)
        從服務端獲取實時的事件

    docker-export(1)
        導出容器內容為一個 tar 包

    docker-history(1)
        顯示一個鏡像的歷史

    docker-images(1)
        列出存在的鏡像

    docker-import(1)
        導入一個文件（典型為 tar 包）路徑或目錄來創建一個鏡像

    docker-info(1)
        顯示一些相關的系統信息

    docker-inspect(1)
        顯示一個容器的底層具體信息。

    docker-kill(1)
        關閉一個執行中的容器 (包括程序和所有資源)

    docker-load(1)
        從一個 tar 包中加載一個鏡像

    docker-login(1)
        註冊或登錄到一個 Docker 的倉庫服務器

    docker-logout(1)
        從 Docker 的倉庫服務器登出

    docker-logs(1)
        獲取容器的 log 信息

    docker-pause(1)
        暫停一個容器中的所有程序

    docker-port(1)
        查找一個 nat 到一個私有網口的公共口

    docker-ps(1)
        列出容器

    docker-pull(1)
        從一個Docker的倉庫服務器下拉一個鏡像或倉庫

    docker-push(1)
        將一個鏡像或者倉庫推送到一個 Docker 的註冊服務器

    docker-restart(1)
        重啟一個執行中的容器

    docker-rm(1)
        刪除給定的若幹個容器

    docker-rmi(1)
        刪除給定的若幹個鏡像

    docker-run(1)
        創建一個新容器，並在其中執行給定命令

    docker-save(1)
        保存一個鏡像為 tar 包文件

    docker-search(1)
        在 Docker index 中搜索一個鏡像

    docker-start(1)
        啟動一個容器

    docker-stop(1)
        終止一個執行中的容器

    docker-tag(1)
        為一個鏡像打標簽

    docker-top(1)
        查看一個容器中的正在執行的程序信息

    docker-unpause(1)
        將一個容器內所有的程序從暫停狀態中恢復

    docker-version(1)
        輸出 Docker 的版本信息

    docker-wait(1)
        阻塞直到一個容器終止，然後輸出它的退出符

##一張圖總結 Docker 的命令

![命令周期](../_images/cmd_logic.png)
