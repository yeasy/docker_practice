##使用 Wordpress 入门 Fig
Fig 让 Wordpress 运行在一个独立的环境中很简易。
[安装](install.md) Fig ，然后下载 Wordpress 到当前目录：

```
wordpress.org/latest.tar.gz | tar -xvzf -
```
这将会创建一个叫 wordpress 目录，你也可以重命名成你想要的名字。在目录里面，创建一个 `Dockerfile` 文件，定义应用的运行环境：

```
FROM orchardup/php5
ADD . /code
```
以上内容告诉 Docker 创建一个包含 PHP 和 Wordpress 的镜像。更多关于如何编写 Dockerfile 文件的信息可以查看 [镜像创建](../image/create.md#利用 Dockerfile 来创建镜像) 和 [Dockerfile 使用](../dockerfile/README.md)。


下一步，`fig.yml` 文件将开启一个 web 服务和一个独立的 MySQL 实例：

```
web:
  build: .
  command: php -S 0.0.0.0:8000 -t /code
  ports:
    - "8000:8000"
  links:
    - db
  volumes:
    - .:/code
db:
  image: orchardup/mysql
  environment:
    MYSQL_DATABASE: wordpress
```
要让这个应用跑起来还需要两个文件。
第一个，`wp-config.php` ，它是一个标准的 Wordpress 配置文件，有一点需要修改的是把数据库的配置指向 `db` 容器。

```
<?php
define('DB_NAME', 'wordpress');
define('DB_USER', 'root');
define('DB_PASSWORD', '');
define('DB_HOST', "db:3306");
define('DB_CHARSET', 'utf8');
define('DB_COLLATE', '');

define('AUTH_KEY',         'put your unique phrase here');
define('SECURE_AUTH_KEY',  'put your unique phrase here');
define('LOGGED_IN_KEY',    'put your unique phrase here');
define('NONCE_KEY',        'put your unique phrase here');
define('AUTH_SALT',        'put your unique phrase here');
define('SECURE_AUTH_SALT', 'put your unique phrase here');
define('LOGGED_IN_SALT',   'put your unique phrase here');
define('NONCE_SALT',       'put your unique phrase here');

$table_prefix  = 'wp_';
define('WPLANG', '');
define('WP_DEBUG', false);

if ( !defined('ABSPATH') )
    define('ABSPATH', dirname(__FILE__) . '/');

require_once(ABSPATH . 'wp-settings.php');
```
第二个，`router.php` ，它告诉 PHP 内置的服务器怎么运行 Wordpress:

```
<?php

$root = $_SERVER['DOCUMENT_ROOT'];
chdir($root);
$path = '/'.ltrim(parse_url($_SERVER['REQUEST_URI'])['path'],'/');
set_include_path(get_include_path().':'.__DIR__);
if(file_exists($root.$path))
{
    if(is_dir($root.$path) && substr($path,strlen($path) - 1, 1) !== '/')
        $path = rtrim($path,'/').'/index.php';
    if(strpos($path,'.php') === false) return false;
    else {
        chdir(dirname($root.$path));
        require_once $root.$path;
    }
}else include_once 'index.php';
```

这些配置文件就绪后，在你的 Wordpress 目录里面执行 `fig up` 指令，Fig 就会拉取镜像再创建我们所需要的镜像，然后启动 web 和数据库容器。 接着访问 docker 守护进程监听的 8000 端口就能看你的 Wordpress 网站了。（如果你有使用 boot2docker ，执行 `boot2docker ip` ，就会看到它的地址）。

