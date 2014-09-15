##删除容器
可以使用`docker rm`来删除一个处于终止状态的容器。
例如
```
$sudo docker rm  trusting_newton
trusting_newton
```
如果要删除一个运行中的容器，可以添加`-f`参数。Docker会发送SIGKILL信号给容器。

