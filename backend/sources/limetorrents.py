import urllib.parse
from bs4 import BeautifulSoup
from .base import TorrentSource


class LimeTorrentsSource(TorrentSource):
    id = "lime"
    name = "Lime Torrents"
    categories = ["movies", "tv", "music", "games", "software", "anime"]
    MIRRORS = ["https://www.limetorrents.lol", "https://www.limetorrents.info"]
    CAT_MAP = {
        "movies": "movies", "tv": "tv", "music": "music",
        "games": "games", "software": "applications", "anime": "anime",
    }

    async def search(self, session, query, category, limit):
        cat = self.CAT_MAP.get(category, "all")
        q = urllib.parse.quote(query)
        for mirror in self.MIRRORS:
            try:
                url = f"{mirror}/search/{cat}/{q}/seeds/1/"
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                async with session.get(url, headers=headers, timeout=12) as r:
                    if r.status != 200:
                        continue
                    html = await r.text()
                results = self._parse(html, limit)
                if results:
                    return results
            except Exception as e:
                print(f"[LIME] {mirror} error: {e}")
        return []

    def _parse(self, html, limit):
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select("table.table2 tbody tr")[:limit]
        results = []
        for row in rows:
            try:
                cols = row.find_all("td")
                if len(cols) < 5:
                    continue
                name_tag = cols[0].find("a", href=lambda h: h and "/torrent/" in h)
                magnet_tag = row.find("a", href=lambda h: h and h.startswith("magnet:"))
                if not name_tag:
                    continue
                # Lime Torrents detail page needed for magnet — skip if no direct magnet
                if not magnet_tag:
                    continue
                results.append(self._result(
                    title=name_tag.get_text(strip=True),
                    magnet=magnet_tag["href"],
                    size=cols[2].get_text(strip=True),
                    seeders=cols[3].get_text(strip=True),
                    leechers=cols[4].get_text(strip=True),
                    category="general",
                ))
            except Exception:
                continue
        return results
