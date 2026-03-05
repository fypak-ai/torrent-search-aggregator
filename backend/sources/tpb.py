import urllib.parse
from .base import TorrentSource

TRACKERS = [
    "udp://tracker.opentrackr.org:1337/announce",
    "udp://open.demonii.com:1337/announce",
    "udp://tracker.openbittorrent.com:80/announce",
    "udp://tracker.coppersurfer.tk:6969/announce",
    "udp://tracker.leechers-paradise.org:6969/announce",
]


class TPBSource(TorrentSource):
    id = "tpb"
    name = "The Pirate Bay"
    categories = ["all", "movies", "tv", "music", "games", "software", "anime"]
    # apibay.org is the official TPB JSON API
    APIS = [
        "https://apibay.org",
        "https://apibay.nocensor.space",
    ]
    CAT_MAP = {
        "movies": 200, "tv": 205, "music": 100,
        "games": 400, "software": 300, "anime": 205, "all": 0
    }

    async def search(self, session, query, category, limit):
        cat = self.CAT_MAP.get(category, 0)
        for api in self.APIS:
            try:
                params = {"q": query, "cat": cat}
                async with session.get(
                    f"{api}/q.php", params=params, timeout=15
                ) as r:
                    if r.status != 200:
                        print(f"[TPB] {api} status {r.status}")
                        continue
                    data = await r.json(content_type=None)
                if not data or (len(data) == 1 and data[0].get("name") == "No results returned"):
                    return []
                results = []
                for t in data[:limit]:
                    info_hash = t.get("info_hash", "")
                    if not info_hash or info_hash == "0" * 40:
                        continue
                    magnet = self._magnet(info_hash, t.get("name", ""))
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
                print(f"[TPB] {api} error: {e}")
        return []

    def _magnet(self, hash_, name):
        dn = urllib.parse.quote(name)
        tr = "&tr=".join(urllib.parse.quote(t) for t in TRACKERS)
        return f"magnet:?xt=urn:btih:{hash_}&dn={dn}&tr={tr}"
