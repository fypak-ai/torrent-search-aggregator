import urllib.parse
from .base import TorrentSource

TRACKERS = [
    "udp://open.demonii.com:1337/announce",
    "udp://tracker.openbittorrent.com:80",
    "udp://tracker.coppersurfer.tk:6969",
    "udp://glotorrents.pw:6969/announce",
    "udp://tracker.opentrackr.org:1337/announce",
]


class YTSSource(TorrentSource):
    id = "yts"
    name = "YTS"
    categories = ["movies", "all"]
    BASE_URL = "https://yts.mx/api/v2"

    async def search(self, session, query, category, limit):
        if category not in ("all", "movies"):
            return []
        try:
            params = {"query_term": query, "limit": min(limit, 50), "sort_by": "seeds"}
            async with session.get(f"{self.BASE_URL}/list_movies.json", params=params, timeout=12) as r:
                data = await r.json(content_type=None)
            movies = data.get("data", {}).get("movies") or []
            results = []
            for m in movies:
                for t in m.get("torrents", []):
                    magnet = self._magnet(t.get("hash", ""), m.get("title_long", "Unknown"))
                    results.append(self._result(
                        title=f"{m.get('title_long', 'Unknown')} [{t.get('quality','?')}] [{t.get('type','?')}]",
                        magnet=magnet,
                        size=t.get("size", ""),
                        seeders=t.get("seeds", 0),
                        leechers=t.get("peers", 0),
                        category="movies",
                        date=t.get("date_uploaded", ""),
                        extra={"cover": m.get("medium_cover_image", ""), "rating": m.get("rating", "")}
                    ))
            return results
        except Exception as e:
            print(f"[YTS] error: {e}")
            return []

    def _magnet(self, hash_, title):
        tr = "&tr=".join(TRACKERS)
        return f"magnet:?xt=urn:btih:{hash_}&dn={urllib.parse.quote(title)}&tr={tr}"
