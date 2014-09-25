## 仓库配置文件
Docker的Registry利用配置文件提供了一些仓库的模板（flavor），用户可以直接使用它们来进行开发或生产部署。

### 模板
在`config_sample.yml`文件中，可以看到一些现成的模板段：
* `common`：基础配置
* `local`：存储数据到本地文件系统
* `s3`：存储数据到AWS S3中
* `dev`：使用`local`模板的基本配置
* `test`：单元测试使用
* `prod`：生产环境配置（基本上跟s3配置类似）
* `gcs`：存储数据到Google的云存储
* `swift`：存储数据到OpenStack Swift服务
* `glance`：存储数据到OpenStack Glance服务，本地文件系统为后备
* `glance-swift`：存储数据到OpenStack Glance服务，Swift为后备
* `elliptics`：存储数据到Elliptics key/value存储

用户也可以添加自定义的模版段。

默认情况下使用的模板是`dev`，要使用某个模板作为默认值，可以添加`SETTINGS_FLAVOR`到环境变量中，例如
```
export SETTINGS_FLAVOR=dev
```

另外，配置文件中支持从环境变量中加载值，语法格式为`_env:VARIABLENAME[:DEFAULT]`。

### 示例配置
```
common:
    loglevel: info
    search_backend: "_env:SEARCH_BACKEND:"
    sqlalchemy_index_database:
        "_env:SQLALCHEMY_INDEX_DATABASE:sqlite:////tmp/docker-registry.db"

prod:
    loglevel: warn
    storage: s3
    s3_access_key: _env:AWS_S3_ACCESS_KEY
    s3_secret_key: _env:AWS_S3_SECRET_KEY
    s3_bucket: _env:AWS_S3_BUCKET
    boto_bucket: _env:AWS_S3_BUCKET
    storage_path: /srv/docker
    smtp_host: localhost
    from_addr: docker@myself.com
    to_addr: my@myself.com

dev:
    loglevel: debug
    storage: local
    storage_path: /home/myself/docker

test:
    storage: local
    storage_path: /tmp/tmpdockertmp
```

### 选项
