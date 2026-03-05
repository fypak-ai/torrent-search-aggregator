#!/usr/bin/env bash
# install.sh — Configura o torrent-search-aggregator em uma VM Ubuntu/Debian limpa
# Uso: sudo bash install.sh
set -e

APP_DIR="/opt/torrent-search"
APP_USER="torrent"
DOMAIN="${DOMAIN:-localhost}"

echo "==> Atualizando sistema..."
apt-get update -y && apt-get upgrade -y

echo "==> Instalando dependências..."
apt-get install -y python3 python3-pip python3-venv nginx git curl

echo "==> Criando usuário de serviço..."
id -u $APP_USER &>/dev/null || useradd -r -s /bin/false -d $APP_DIR $APP_USER

echo "==> Clonando/atualizando repositório..."
if [ -d "$APP_DIR" ]; then
  git -C $APP_DIR pull
else
  git clone https://github.com/fypak-ai/torrent-search-aggregator $APP_DIR
fi

echo "==> Configurando backend Python..."
cd $APP_DIR/backend
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "PORT=5000" >> .env
fi

chown -R $APP_USER:$APP_USER $APP_DIR

echo "==> Instalando serviço systemd..."
cp /opt/torrent-search/deploy/torrent-search.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable torrent-search
systemctl restart torrent-search

echo "==> Buildando frontend..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
cd $APP_DIR/frontend
npm install
VITE_API_URL="http://$DOMAIN/api" npm run build

echo "==> Configurando Nginx..."
cat > /etc/nginx/sites-available/torrent-search << 'NGINX'
server {
    listen 80;
    server_name _;

    # Frontend estático
    root /opt/torrent-search/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy para o backend Flask
    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 60;
    }
}
NGINX

ln -sf /etc/nginx/sites-available/torrent-search /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

echo ""
echo "==> Deploy concluído!"
echo "    Acesse: http://$(curl -s ifconfig.me)"
echo "    Status backend: systemctl status torrent-search"
echo "    Logs: journalctl -u torrent-search -f"
