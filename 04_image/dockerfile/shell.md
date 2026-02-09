## SHELL 指令

### 基本语法

```docker
SHELL ["executable", "parameters"]
```

`SHELL` 指令允许覆盖 Docker 默认的 shell。
- **Linux 默认**：`["/bin/sh", "-c"]`
- **Windows 默认**：`["cmd", "/S", "/C"]`

该指令会影响后续的 `RUN`, `CMD`, `ENTRYPOINT` 指令（当它们使用 shell 格式时）。

---

### 为什么要用 SHELL 指令

#### 1. 使用 bash 特性

默认的 `/bin/sh`（通常是 dash 或 alpine 的 ash）功能有限。如果你需要使用 bash 的特有功能（如数组、`{}` 扩展、`pipefail` 等），可以切换 shell。

```docker
FROM ubuntu:24.04

## 切换到 bash
SHELL ["/bin/bash", "-c"]

## 现在可以使用 bash 特性了
RUN echo {a..z}
```

#### 2. 增强错误处理 (pipefail)

默认情况下，管道命令 `cmd1 | cmd2` 只要 `cmd2` 成功，整个指令就视为成功。这可能掩盖构建错误。

```docker
## ❌ 这里的 wget 失败了，但构建继续（因为 tar 成功了）
RUN wget -O - https://invalid-url | tar xz
```

使用 `SHELL` 启用 `pipefail`：

```docker
## ✅ 启用 pipefail
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

## 如果 wget 失败，整个 RUN 就会失败
RUN wget -O - https://invalid-url | tar xz
```

#### 3. Windows 环境

在 Windows 容器中，经常需要在 `cmd` 和 `powershell` 之间切换。

```docker
FROM mcr.microsoft.com/windows/servercore:ltsc2022

## 默认是 cmd
RUN echo Default shell is cmd

## 切换到 powershell
SHELL ["powershell", "-command"]
RUN Write-Host "Hello from PowerShell"

## 切回 cmd
SHELL ["cmd", "/S", "/C"]
```

---

### 作用范围

`SHELL` 指令可以出现多次，每次只影响其后的指令：

```docker
FROM ubuntu:24.04

## 使用默认 sh
RUN echo "Using sh"

SHELL ["/bin/bash", "-c"]
## 使用 bash
RUN echo "Using bash"

SHELL ["/bin/sh", "-c"]
## 回到 sh
RUN echo "Using sh again"
```

---

### 对其他指令的影响

`SHELL` 影响的是所有使用 **shell 格式** 的指令：

| 指令格式 | 是否受 SHELL 影响 |
|---------|-------------------|
| `RUN command` | ✅ 是 |
| `RUN ["exec", "param"]` | ❌ 否 |
| `CMD command` | ✅ 是 |
| `CMD ["exec", "param"]` | ❌ 否 |
| `ENTRYPOINT command` | ✅ 是 |
| `ENTRYPOINT ["exec", "param"]` | ❌ 否 |

---

### 最佳实践

#### 1. 推荐开启 pipefail

对于使用 bash 的镜像，强烈建议开启 `pipefail`，以确保构建过程中的错误能被及时捕获。

```docker
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
```

#### 2. 明确意图

如果由于脚本需求必须更改 shell，最好在 Dockerfile 中显式声明，而不是依赖默认行为。

#### 3. 尽量保持一致

避免在 Dockerfile 中频繁切换 SHELL，这会使构建过程难以理解和调试。尽量在头部定义一次即可。

---

### 本章小结

| 要点 | 说明 |
|------|------|
| **作用** | 更改 RUN/CMD/ENTRYPOINT 的默认 shell |
| **Linux 默认** | `["/bin/sh", "-c"]` |
| **Windows 默认** | `["cmd", "/S", "/C"]` |
| **推荐用法** | `SHELL ["/bin/bash", "-o", "pipefail", "-c"]` |
| **影响范围** | 后续所有使用 shell 格式的指令 |

### 延伸阅读

- [RUN 指令](../../04_image/4.5_build.md)：执行命令
- [Dockerfile 最佳实践](../../15_appendix/15.1_best_practices.md)：错误处理与调试
