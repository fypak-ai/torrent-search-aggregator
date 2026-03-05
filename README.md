# 🔍 Torrent Search Aggregator

Super buscador de torrents que agrega múltiplos sites e retorna magnet links unificados.

## Fontes suportadas

| Fonte             | Método   | Categorias         |
|-------------------|----------|--------------------|
| YTS               | API      | Filmes             |
| Nyaa              | API      | Anime, Manga       |
| 1337x             | Scraping | Geral              |
| The Pirate Bay    | Scraping | Geral              |
| EZTV              | API      | Séries             |
| RARBG mirror      | Scraping | Geral              |

## Stack

- **Backend**: Flask (Python) — deploy Railway
- **Frontend**: React + TanStack Start + Tailwind CSS

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Deploy

- **Backend**: Railway (aponta para `/backend`, usa `railway.json`)
- **Frontend**: Vercel ou Railway (aponta para `/frontend`)

Lembre de definir `VITE_API_URL` no frontend com a URL do backend deployado.
