## 倉庫配置文件
Docker 的 Registry 利用配置文件提供了一些倉庫的模組（flavor），用戶可以直接使用它們來進行開發或生產部署。

### 模組
在 `config_sample.yml` 文件中，可以看到一些現成的模組段：
* `common`：基礎配置
* `local`：儲存數據到本地文件系統
* `s3`：儲存數據到 AWS S3 中
* `dev`：使用 `local` 模組的基本配置
* `test`：單元測試使用
* `prod`：生產環境配置（基本上跟s3配置類似）
* `gcs`：儲存數據到 Google 的雲端
* `swift`：儲存數據到 OpenStack Swift 服務
* `glance`：儲存數據到 OpenStack Glance 服務，本地文件系統為後備
* `glance-swift`：儲存數據到 OpenStack Glance 服務，Swift 為後備
* `elliptics`：儲存數據到 Elliptics key/value 存儲

用戶也可以添加自定義的模版段。

默認情況下使用的模組是 `dev`，要使用某個模組作為默認值，可以添加 `SETTINGS_FLAVOR` 到環境變數中，例如
```
export SETTINGS_FLAVOR=dev
```

另外，配置文件中支持從環境變數中加載值，語法格式為 `_env:VARIABLENAME[:DEFAULT]`。

### 範例配置
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

### 選項
