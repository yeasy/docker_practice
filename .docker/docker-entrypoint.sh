#!/usr/bin/env sh
set -euo pipefail

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-4000}"

echo
echo
echo "Please open your browser: ${HOST}:${PORT}"
echo
echo "欢迎加入 QQ 群：【 145983035 】 分享 Docker 资源，交流 Docker 技术"
echo
echo

exec nginx -g "daemon off;"
