#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${APP_DIR:-/opt/rebrewie-control-pi}"
SERVICE_NAME="rebrewie-control-pi"

if [[ $EUID -ne 0 ]]; then
  echo "Re-running with sudo..."
  exec sudo -E bash "$0" "$@"
fi

apt-get update
apt-get install -y python3 python3-venv python3-pip unzip
mkdir -p "$APP_DIR"
rsync -a --delete --exclude '.venv' ./ "$APP_DIR"/
cd "$APP_DIR"
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
if [[ ! -f .env ]]; then
  cp .env.example .env
fi
cp systemd/rebrewie-control-pi.service /etc/systemd/system/${SERVICE_NAME}.service
sed -i "s#WorkingDirectory=.*#WorkingDirectory=${APP_DIR}#" /etc/systemd/system/${SERVICE_NAME}.service
sed -i "s#ExecStart=.*#ExecStart=${APP_DIR}/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080#" /etc/systemd/system/${SERVICE_NAME}.service
systemctl daemon-reload
systemctl enable ${SERVICE_NAME}
systemctl restart ${SERVICE_NAME}
echo "Installed. Open http://$(hostname -I | awk '{print $1}'):8080"
