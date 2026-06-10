# WordPress Compose 示例

本示例使用 Docker Compose secrets 管理数据库密码，启动前需要先创建密钥文件（参见书中 11.8 节）：

```bash
mkdir -p secrets
printf '%s\n' 'somestrongrootpassword' > secrets/db_root_password.txt
printf '%s\n' 'somestronguserpassword' > secrets/db_password.txt
chmod 600 secrets/*.txt
```

然后启动：

```bash
docker compose up -d
```

注意：`secrets/` 目录不要提交到版本库；生产环境应改用平台的密钥管理能力。
