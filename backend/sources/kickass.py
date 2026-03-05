import urllib.parse
from .base import TorrentSource

TRACKERS = [
    "udp://tracker.coppersurfer.tk:6969/announce",
    "udp://9.rarbg.to:2920/announce",
    "udp://tracker.opentrackr.org:1337",
    "udp://tracker.internetwarriors.net:1337/announce",
]


class KickassSource(TorrentSource):
    id = "kat"
    name = "Kickass Torrents"
    categories = ["movies", "tv", "music", "games", "software", "anime", "books"]
    # Uses katcr.co JSON API
    BASE_URL = "https://katcr.co/api/v2/search"

    async def search(self, session, query, category, limit):
        try:
            params = {
                "phraseSearch": query,
                "page": 1,
            }
            if category not in ("all", ""):
                params["category"] = category
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            async with session.get(self.BASE_URL, params=params, headers=headers, timeout=12) as r:
                if r.status != 200:
                    return []
                data = await r.json(content_type=None)
            items = data.get("results", []) or []
            results = []
            for t in items[:limit]:
                hash_ = t.get("hash", "")
                name = t.get("title", "Unknown")
                magnet = self._build_magnet(hash_, name) if hash_ else t.get("magnet", "")
                if not magnet:
                    continue
                results.append(self._result(
                    title=name,
                    magnet=magnet,
                    size=t.get("size", ""),
                    seeders=t.get("seeders", 0),
                    leechers=t.get("leechers", 0),
                    category=category,
                    date=t.get("added", ""),
                ))
            return results
        except Exception as e:
            print(f"[KAT] error: {e}")
            return []

    def _build_magnet(self, hash_, name):
        tr = "&tr=".join(TRACKERS)
        return f"magnet:?xt=urn:btih:{hash_}&dn={urllib.parse.quote(name)}&tr={tr}"
