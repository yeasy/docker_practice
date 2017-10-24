# Docker 数据管理
这一章介绍如何在 Docker 内部以及容器之间管理数据，在容器中管理数据主要有两种方式：
* 数据卷（Data volumes）
* 数据卷容器（Data volume containers）

Docker 在 1.13 版本引进了新的管理命令（management commands），在 Docker 1.13+ 推荐使用 `docker volume` 子命令来管理 Docker 数据卷。
