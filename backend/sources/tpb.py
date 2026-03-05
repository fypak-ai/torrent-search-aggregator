from .base import TorrentSource

TRACKERS = [
    "udp://tracker.coppersurfer.tk:6969/announce",
    "udp://9.rarbg.to:2920/announce",
    "udp://tracker.opentrackr.org:1337",
    "udp://tracker.internetwarriors.net:1337/announce",
    "udp://tracker.leechers-paradise.org:6969/announce",
]


class TPBSource(TorrentSource):
    id = "tpb"
    name = "The Pirate Bay"
    categories = ["movies", "tv", "music", "games", "software", "anime"]
    BASE_URL = "https://apibay.org"
    CAT_MAP = {
        "movies": 200, "tv": 205, "music": 100,
        "games": 400, "software": 300, "anime": 205, "all": 0
    }

    async def search(self, session, query, category, limit):
        cat = self.CAT_MAP.get(category, 0)
        try:
            params = {"q": query, "cat": cat}
            async with session.get(f"{self.BASE_URL}/q.php", params=params, timeout=10) as r:
                data = await r.json()
            if not data or (len(data) == 1 and data[0].get("name") == "No results returned"):
                return []
            results = []
            for t in data[:limit]:
                magnet = self._magnet(t.get("info_hash", ""), t.get("name", ""))
                results.append(self._result(
                    title=t.get("name", ""),
                    magnet=magnet,
                    size=t.get("size", ""),
                    seeders=t.get("seeders", 0),
                    leechers=t.get("leechers", 0),
                    category=category,
                    date=str(t.get("added", "")),
                    extra={"imdb": t.get("imdb", "")}
                ))
            return results
        except Exception as e:
            print(f"[TPB] error: {e}")
            return []

    def _magnet(self, hash_, name):
        tr = "&tr=".join(TRACKERS)
        return f"magnet:?xt=urn:btih:{hash_}&dn={name.replace(' ', '+')}&tr={tr}"
