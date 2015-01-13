##从 Fig 结合 Rail 开玩

我们现在将使用 Fig 配置并运行一个 Rails/PostgreSQL 应用。在开始之前，先确保 Fig 已经 [安装](install.md)。

先设置好三个必要的文件。首先，我们的应用将要运行在一个安装好所有依赖环境的 Docker 容器里面。我们可以通过指定 `Dockerfile` 文件的内容从而决定 Docker 容器安装什么内容。内容如下： 

```
FROM ruby
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev
RUN mkdir /myapp
WORKDIR /myapp
ADD Gemfile /myapp/Gemfile
RUN bundle install
ADD . /myapp
```
这些内容指定了的应用使用一个 Ruby 镜像，并安装插件和其它依赖。关于 Dockerfile 的更多信息可以查看 [镜像创建](../image/create.md#利用 Dockerfile 来创建镜像) 和 [Dockerfile 使用](../dockerfile/README.md)
下一步，我们需要一个引导加载 Rails 的文件 `Gemfile` 。 它将通过 `rails new` 短暂的覆盖  。

```
source 'https://rubygems.org'
gem 'rails', '4.0.2'
```
最后，`fig.yml` 文件才是最神奇的地方。 