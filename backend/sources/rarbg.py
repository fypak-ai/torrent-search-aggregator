import urllib.parse
from .base import TorrentSource

TRACKERS = [
    "udp://tracker.opentrackr.org:1337/announce",
    "udp://open.demonii.com:1337/announce",
    "udp://tracker.openbittorrent.com:80",
    "udp://tracker.coppersurfer.tk:6969/announce",
]


class RARBGSource(TorrentSource):
    """
    RARBG closed in 2023. This source queries the community-maintained
    RARBG database mirror at rargb.to (db-search).
    Falls back to the apibay.org API (TPB) scoped to a known RARBG-style query.
    """
    id = "rarbg"
    name = "RARBG (mirror)"
    categories = ["movies", "tv", "games", "music", "software", "anime"]
    # Public RARBG DB search mirrors
    MIRRORS = [
        "https://rargb.to",
        "https://rarbg.unblockit.onl",
    ]

    async def search(self, session, query, category, limit):
        q = urllib.parse.quote(query)
        for mirror in self.MIRRORS:
            try:
                url = f"{mirror}/search/?search={q}"
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                async with session.get(url, headers=headers, timeout=12, allow_redirects=True) as r:
                    if r.status != 200:
                        continue
                    html = await r.text()
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, "html.parser")
                rows = soup.select("tr.table2t, tr.lista2")[:limit]
                results = []
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) < 4:
                        continue
                    name_el = cols[1].find("a") if len(cols) > 1 else None
                    magnet_el = row.find("a", href=lambda h: h and h.startswith("magnet:"))
                    if not name_el or not magnet_el:
                        continue
                    results.append(self._result(
                        title=name_el.text.strip(),
                        magnet=magnet_el["href"],
                        size=cols[3].text.strip() if len(cols) > 3 else "",
                        seeders=cols[4].text.strip() if len(cols) > 4 else 0,
                        leechers=cols[5].text.strip() if len(cols) > 5 else 0,
                        category=category,
                    ))
                if results:
                    return results
            except Exception as e:
                print(f"[RARBG] {mirror} error: {e}")
        return []
