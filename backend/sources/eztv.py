from .base import TorrentSource


class EZTVSource(TorrentSource):
    id = "eztv"
    name = "EZTV"
    categories = ["tv", "shows"]
    BASE_URL = "https://eztv.re/api"

    async def search(self, session, query, category, limit):
        if category not in ("all", "tv", "shows"):
            return []
        try:
            params = {"query": query, "limit": min(limit, 100), "page": 1}
            async with session.get(f"{self.BASE_URL}/get-torrents", params=params, timeout=10) as r:
                data = await r.json()
            torrents = data.get("torrents") or []
            results = []
            for t in torrents[:limit]:
                if query.lower() not in t.get("title", "").lower():
                    continue
                results.append(self._result(
                    title=t.get("title", ""),
                    magnet=t.get("magnet_url", ""),
                    size=str(t.get("size_bytes", "")),
                    seeders=t.get("seeds", 0),
                    leechers=t.get("peers", 0),
                    category="tv",
                    date=str(t.get("date_released_unix", "")),
                    extra={"imdb": t.get("imdb_id", "")}
                ))
            return results
        except Exception as e:
            print(f"[EZTV] error: {e}")
            return []
