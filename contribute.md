## 如何贡献项目

* 在 GitHub 上 `fork` 到自己的仓库，如 `docker_user/docker_practice`，然后 `clone` 到本地，并设置用户信息。

  ```sh
  $ git clone git@github.com:docker_user/docker_practice.git
  $ cd docker_practice
  $ git config user.name "yourname"
  $ git config user.email "your email"
  ```

* 修改代码后提交，并推送到自己的仓库。

  ```sh
  $ #do some change on the content
  $ git commit -am "Fix issue #1: change helo to hello"
  $ git push
  ```

* 在 GitHub 网站上提交 pull request。

* 定期使用项目仓库内容更新自己仓库内容。
  ```sh
  $ git remote add upstream https://github.com/yeasy/docker_practice
  $ git fetch upstream
  $ git checkout master
  $ git rebase upstream/master
  $ git push -f origin master
  ```

## 排版规范

本开源书籍遵循 [中文排版指南](https://github.com/mzlogin/chinese-copywriting-guidelines) 规范。
