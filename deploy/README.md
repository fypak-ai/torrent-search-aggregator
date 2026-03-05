# Deploy em VM (Ubuntu/Debian)

## Instalação inicial

```bash
# Na VM, como root:
curl -fsSL https://raw.githubusercontent.com/fypak-ai/torrent-search-aggregator/main/deploy/install.sh | sudo bash
```

Ou manualmente:

```bash
git clone https://github.com/fypak-ai/torrent-search-aggregator /opt/torrent-search
sudo bash /opt/torrent-search/deploy/install.sh
```

## Atualizar após novo commit

```bash
sudo bash /opt/torrent-search/deploy/update.sh
```

## Comandos úteis

```bash
# Ver status do backend
systemctl status torrent-search

# Ver logs em tempo real
journalctl -u torrent-search -f

# Reiniciar backend
systemctl restart torrent-search

# Ver logs do nginx
tail -f /var/log/nginx/error.log
```

## Estrutura pós-deploy

```
/opt/torrent-search/     # código do app
├── backend/
│   ├── venv/            # virtualenv Python
│   └── .env             # variáveis de ambiente
└── frontend/
    └── dist/            # build estático servido pelo Nginx

/etc/systemd/system/torrent-search.service
/etc/nginx/sites-enabled/torrent-search
```

## Portas

- **80** — Nginx (frontend + proxy para API)
- **5000** — Flask (interno, não exposto)

## SSL (opcional)

```bash
apt-get install -y certbot python3-certbot-nginx
certbot --nginx -d seu-dominio.com
```
