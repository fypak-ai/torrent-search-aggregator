#!/usr/bin/env bash
# update.sh — Atualiza o app após novo commit no GitHub
# Uso: sudo bash /opt/torrent-search/deploy/update.sh
set -e

APP_DIR="/opt/torrent-search"

echo "==> Puxando atualizações..."
git -C $APP_DIR pull

echo "==> Atualizando dependências Python..."
cd $APP_DIR/backend
./venv/bin/pip install -r requirements.txt

echo "==> Rebuildando frontend..."
cd $APP_DIR/frontend
npm install
npm run build

echo "==> Reiniciando serviço..."
systemctl restart torrent-search
nginx -t && systemctl reload nginx

echo "==> Atualização concluída!"
systemctl status torrent-search --no-pager
