## 使用 Rail

我们现在将使用 Compose 配置并运行一个 Rails/PostgreSQL 应用。


在一切工作开始前，需要先设置好三个必要的文件。  
首先，因为应用将要运行在一个满足所有环境依赖的 Docker 容器里面，那么我们可以通过编辑 `Dockerfile` 文件来指定 Docker 容器要安装内容。内容如下：

```docker
FROM ruby
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev
RUN mkdir /myapp
WORKDIR /myapp
ADD Gemfile /myapp/Gemfile
RUN bundle install
ADD . /myapp
```
以上内容指定应用将使用安装了 Ruby、Bundler 以及其依赖件的镜像。更多关于如何编写 Dockerfile 文件的信息可以查看 [镜像创建](../image/create.md#利用 Dockerfile 来创建镜像) 和 [Dockerfile 使用](../dockerfile/README.md)。
下一步，我们需要一个引导加载 Rails 的文件 `Gemfile` 。 等一会儿它还会被 `rails new` 命令覆盖重写。

```bash
source 'https://rubygems.org'
gem 'rails', '4.0.2'
```
最后，`docker-compose.yml` 文件才是最神奇的地方。 `docker-compose.yml` 文件将把所有的东西关联起来。它描述了应用的构成（一个 web 服务和一个数据库）、每个镜像的来源（数据库运行在使用预定义的 PostgreSQL 镜像，web 应用侧将从本地目录创建）、镜像之间的连接，以及服务开放的端口。

```yaml
version: "3"
services:

  db:
    image: postgres
    ports:
      - "5432"
  web:
    build: .
    command: bundle exec rackup -p 3000
    volumes:
      - .:/myapp
    ports:
      - "3000:3000"
    links:
      - db
```
所有文件就绪后，我们就可以通过使用 `docker-compose run` 命令生成应用的骨架了。

```bash
$ docker-compose run web rails new . --force --database=postgresql --skip-bundle
```
Compose 会先使用 `Dockerfile` 为 web 服务创建一个镜像，接着使用这个镜像在容器里运行 `rails new ` 和它之后的命令。一旦这个命令运行完后，应该就可以看一个崭新的应用已经生成了。

```bash
$ ls
Dockerfile   app          docker-compose.yml      tmp
Gemfile      bin          lib          vendor
Gemfile.lock condocker-compose       log
README.rdoc  condocker-compose.ru    public
Rakefile     db           test
```
在新的 `Gemfile` 文件去掉加载 `therubyracer` 的行的注释，这样我们便可以使用 Javascript 运行环境：

```bash
gem 'therubyracer', platforms: :ruby
```
现在我们已经有一个新的 `Gemfile` 文件，需要再重新创建镜像。（这个会步骤会改变 Dockerfile 文件本身，仅仅需要重建一次）。

```bash
$ docker-compose build
```
应用现在就可以启动了，但配置还未完成。Rails 默认读取的数据库目标是 `localhost` ，我们需要手动指定容器的 `db` 。同样的，还需要把用户名修改成和 postgres 镜像预定的一致。
打开最新生成的 `database.yml` 文件。用以下内容替换：

```bash
development: &default
  adapter: postgresql
  encoding: unicode
  database: postgres
  pool: 5
  username: postgres
  password:
  host: db

test:
  <<: *default
  database: myapp_test
```
现在就可以启动应用了。

```bash
$ docker-compose up
```
如果一切正常，你应该可以看到 PostgreSQL 的输出，几秒后可以看到这样的重复信息：

```bash
myapp_web_1 | [2014-01-17 17:16:29] INFO  WEBrick 1.3.1
myapp_web_1 | [2014-01-17 17:16:29] INFO  ruby 2.0.0 (2013-11-22) [x86_64-linux-gnu]
myapp_web_1 | [2014-01-17 17:16:29] INFO  WEBrick::HTTPServer#start: pid=1 port=3000
```
最后， 我们需要做的是创建数据库，打开另一个终端，运行：

```bash
$ docker-compose run web rake db:create
```
这个 web 应用已经开始在你的 docker 守护进程里面监听着 3000 端口了。

![](../_images/docker-compose-rails-screenshot.png)
